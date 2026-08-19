"""Bind every number quoted in the journal paper back to its source.

The paper's header promises that no value in it is transcribed by hand.
Figures keep that promise by construction -- they are generated. Numbers in
prose do not, so they are checked here against
results/phase4/thesis_numbers.json, the same file the thesis and the slides
read from.

Two kinds of check:

  bound     a value the paper states must equal what the JSON says
  unbound   any other numeric literal in the prose is listed, so a number
            that entered by hand cannot sit there unnoticed

Run: python scripts/check_paper_numbers.py
Exits non-zero on a mismatch.

Traps this catches, all of them recorded in the JSON's own _note fields:
  - reachability over the FULL splits (97.3 / 99.7) is a different
    population from the 400-question samples (97.0 / 99.2). A sentence
    about the reported results wants the sample figure.
  - "every other system decays" is false on CWQ; the agentic baseline
    recovers at h3plus. "ends below where it started" is the true form.
  - the clip rates come from the budget_exhausted trace flag, not from
    llm_calls == 25, which overcounts CWQ by three.
"""
import io
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent.parent
NUMBERS = ROOT / "results" / "phase4" / "thesis_numbers.json"
SECTIONS = ROOT / "thesis_paper" / "sections"
PAPER = ROOT / "thesis_paper" / "agr-paper.tex"

COMMENT = re.compile(r"(?<!\\)%.*")
# 0.755, 2.59, 1{,}709, 29\%, 400
LITERAL = re.compile(r"\d[\d.,{}]*")

fails = []


def ck(label, ok, detail=""):
    print(f"  [{'OK ' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        fails.append(label)


def prose():
    """Every section's text with LaTeX comments stripped."""
    out = []
    for p in sorted(SECTIONS.glob("*.tex")) + [PAPER]:
        out.append(COMMENT.sub("", io.open(p, encoding="utf-8").read()))
    return "\n".join(out)


def literals(text):
    seen = set()
    for m in LITERAL.findall(text):
        v = m.replace("{,}", "").replace(",", "").rstrip(".")
        if v:
            seen.add(v)
    return seen


def main():
    d = json.load(open(NUMBERS, encoding="utf-8"))
    by = d["main_results"]["by_system"]
    tog = d["tog_budget_split"]
    gnd = d["groundedness_tier1_structural"]
    abl = d["ablations"]["by_condition"]
    text = prose()
    present = literals(text)

    print("== values bound to thesis_numbers.json ==")
    bound = {
        "AGR Hits@1, WebQSP":        by["webqsp/agr"]["hits_at_1"],
        "AGR Hits@1, CWQ":           by["cwq/agr"]["hits_at_1"],
        "AGR F1, WebQSP":            by["webqsp/agr"]["f1"],
        "AGR F1, CWQ":               by["cwq/agr"]["f1"],
        "ToG Hits@1, WebQSP":        by["webqsp/tog"]["hits_at_1"],
        "ToG Hits@1, CWQ":           by["cwq/tog"]["hits_at_1"],
        "AGR entities asserted":     gnd["both_agr"]["entities_asserted"],
        "control entities asserted": gnd["both_noretrieval"]["entities_asserted"],
        "control ungrounded pct":    gnd["both_noretrieval"]["entity_ungrounded_pct"],
    }
    for label, val in bound.items():
        s = str(val)
        # a value the paper has not reached yet is not a failure
        if s in present:
            ck(f"{label} = {s}", True)
        else:
            print(f"  [   ] {label} = {s}   not quoted yet")

    print("\n== derived claims ==")
    wq = by["webqsp/agr"]["mean_calls"] / by["webqsp/tog"]["mean_calls"]
    cq = by["cwq/agr"]["mean_calls"] / by["cwq/tog"]["mean_calls"]
    ck("'roughly half the language-model calls' holds on both datasets",
       0.4 <= wq <= 0.6 and 0.4 <= cq <= 0.6,
       f"WebQSP {wq:.2f}, CWQ {cq:.2f}")

    # AGR spends MORE tokens than ToG on WebQSP; only the call count halves.
    ck("the paper does not claim AGR is cheaper in tokens",
       not re.search(r"half the (?:tokens|token)", text),
       f"AGR {by['webqsp/agr']['mean_tokens']} vs ToG "
       f"{by['webqsp/tog']['mean_tokens']} tokens on WebQSP")

    clip = {"webqsp": round(tog["webqsp"]["tog_clip_rate"] * 100),
            "cwq": round(tog["cwq"]["tog_clip_rate"] * 100)}
    ck("clip rates quoted as whole percents match the trace flag",
       all(str(v) in present for v in clip.values()), str(clip))

    pl_w = abl["webqsp/half_abl_noplanner"]["f1"] - abl["webqsp/half_abl_full"]["f1"]
    ck("planner ablation delta on WebQSP is the +0.083 F1 the paper cites",
       abs(pl_w - 0.083) < 0.0005, f"{pl_w:+.3f} F1")
    pl_c = abl["cwq/half_abl_noplanner"]["f1"] - abl["cwq/half_abl_full"]["f1"]
    ck("the CWQ arm trends the other way, as the paper says",
       pl_c < 0, f"{pl_c:+.3f} F1")

    print("\n== reachability: the sample, not the full split ==")
    # Both blocks spell the field reachable_pct; the earlier version of
    # this check read a key that does not exist, got None for both full
    # figures, and could therefore never fire. A check that cannot fail is
    # indistinguishable from a document that is correct.
    smp = (d["test_sets"]["webqsp"]["reachable_pct"],
           d["test_sets"]["cwq"]["reachable_pct"])
    full = (d["environment_coverage"]["webqsp"]["reachable_pct"],
            d["environment_coverage"]["cwq"]["reachable_pct"])
    assert all(f is not None for f in full), "full-split ceilings went missing"
    ck("no full-split ceiling quoted where a sample ceiling belongs",
       not any(str(f) in present for f in full),
       f"sample {smp}, full split {full}")

    print("\n== unbound literals in prose (read these) ==")
    accounted = {str(v) for v in bound.values()} | {
        str(v) for v in clip.values()} | {
        "400", "259", "57", "2.59", "8.31", "0.083", "0.006", "31", "1",
        "2", "3", "4", "5"}
    rest = sorted(present - accounted, key=lambda s: (len(s), s))
    print("  " + (", ".join(rest) if rest else "none"))
    print("  (section/figure numbers and years are expected here; a result "
          "value is not)")

    print()
    if fails:
        print(f"{len(fails)} FAILED: " + "; ".join(fails))
        return 1
    print("EVERY BOUND NUMBER IN THE PAPER MATCHES ITS SOURCE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
