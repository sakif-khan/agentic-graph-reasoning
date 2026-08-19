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
from decimal import Decimal, ROUND_HALF_UP

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
        # 1{,}709 -> 1709; then drop any brace the match dragged in from
        # surrounding LaTeX, which was reporting "1}" as a distinct literal.
        v = m.replace("{,}", "").replace(",", "")
        v = v.replace("{", "").replace("}", "").rstrip(".")
        if v:
            seen.add(v)
    return seen


def numbers(strings):
    """The same literals as floats.

    String matching made 0.66 and 0.660 different values, so the table cell
    quoting ToG's WebQSP Hits@1 correctly was reported "not quoted yet".
    Comparing numerically is what the check actually meant to do, and it
    also lets a value be written 8.20 or 8.2 as the sentence prefers.
    """
    out = set()
    for s in strings:
        try:
            out.add(float(s))
        except ValueError:
            pass
    return out


def quoted(nums, val, tol=1e-9):
    return any(abs(n - float(val)) <= tol for n in nums)


def rnd(val, places=3):
    """Round the way a person writing the number would.

    Not round(): the IEEE double nearest 0.6295 is 0.62949999999999994849,
    which is below the tie, so round(0.6295, 3) gives 0.629 while both
    half-up and half-even on the true decimal give 0.630. That discrepancy
    reported the budget-split table as mistranscribed when the table was
    right and this check was wrong. Going through Decimal(str(...)) rounds
    the decimal the JSON actually carries.
    """
    q = Decimal(1).scaleb(-places)
    return float(Decimal(str(val)).quantize(q, rounding=ROUND_HALF_UP))


def main():
    d = json.load(open(NUMBERS, encoding="utf-8"))
    by = d["main_results"]["by_system"]
    tog = d["tog_budget_split"]
    gnd = d["groundedness_tier1_structural"]
    abl = d["ablations"]["by_condition"]
    text = prose()
    present = literals(text)
    nums = numbers(present)

    print("== main results table, every cell bound ==")
    # The whole of tab:main is transcribed by hand into the .tex, which is
    # exactly what the paper's header says does not happen anywhere. Binding
    # every cell is what makes that promise true of the table too. A cell
    # mistyped to a value appearing nowhere else in the paper fails here.
    SYSTEMS = ("noretrieval", "vectorrag", "graphrag", "tog", "agr")
    for ds in ("webqsp", "cwq"):
        for sysname in SYSTEMS:
            row = by[f"{ds}/{sysname}"]
            for field in ("hits_at_1", "f1", "hedge_pct", "mean_calls"):
                val = row[field]
                ck(f"{ds}/{sysname} {field} = {val}", quoted(nums, val))

    print("\n== budget-split table bound ==")
    for ds in ("webqsp", "cwq"):
        for subset in ("tog_finished", "tog_clipped"):
            blk = tog[ds][subset]
            ck(f"{ds} {subset} n = {blk['n']}", quoted(nums, blk["n"]))
            for who in ("tog_hits_at_1", "agr_hits_at_1"):
                v = rnd(blk[who])
                ck(f"{ds} {subset} {who} = {v}", quoted(nums, v))

    print("\n== ablation table bound ==")
    for ds in ("webqsp", "cwq"):
        ref = abl[f"{ds}/half_abl_full"]
        for cond in ("noplanner", "nobacktrack", "noverifier", "embonly"):
            cur = abl[f"{ds}/half_abl_{cond}"]
            delta = rnd(cur["f1"] - ref["f1"])
            ck(f"{ds} {cond} dF1 = {delta:+.3f}", quoted(nums, abs(delta)))
            pct = rnd(100 * (cur["mean_tokens"] - ref["mean_tokens"])
                      / ref["mean_tokens"], 0)
            ck(f"{ds} {cond} token change = {pct}%", quoted(nums, abs(pct)))
    for row in d["ablations"]["mcnemar_vs_full"]:
        p = rnd(row["p"])
        cond = row["system_b"].replace("half_abl_", "")
        ck(f"{row['dataset']} {cond} p = {p}", quoted(nums, p))

    print("\n== groundedness bound ==")
    bound = {
        "AGR entities asserted":     gnd["both_agr"]["entities_asserted"],
        "control entities asserted": gnd["both_noretrieval"]["entities_asserted"],
        "control ungrounded pct":    gnd["both_noretrieval"]["entity_ungrounded_pct"],
        "ToG entities asserted":     gnd["both_tog"]["entities_asserted"],
    }
    for label, val in bound.items():
        ck(f"{label} = {val}", quoted(nums, val))

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
