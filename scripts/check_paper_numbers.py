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
import math
import pathlib
import re
import sys
import unicodedata
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


def _pmf(k, n, p):
    return math.comb(n, k) * p**k * (1 - p)**(n - k)


def exact_p(b, n):
    """McNemar exact two-sided p for b of n discordant, doubling the tail."""
    lo = sum(_pmf(k, n, 0.5) for k in range(0, min(b, n - b) + 1))
    return min(1.0, 2 * lo)


def reject_set(n, alpha=0.05):
    return {b for b in range(n + 1) if exact_p(b, n) < alpha}


def mcnemar_power(n, ratio):
    p = ratio / (1 + ratio)
    return sum(_pmf(b, n, p) for b in reject_set(n))


def min_detectable_gap(n):
    """Smallest |b-(n-b)| the exact test can call significant; None if never."""
    R = reject_set(n)
    if not R:
        return None
    return min(abs(2 * b - n) for b in R)


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

    print("\n== power arithmetic bound ==")
    # These are DERIVED claims, computed here rather than read from the JSON,
    # and the paper's first version got every component of them wrong: it
    # asserted 80% power at a 2:1 ratio from "about 30 discordant pairs split
    # 20 to 10", a split whose exact p is 0.0987 and which does not reject at
    # all. True power there is 0.43; 80% at 2:1 needs ~72 pairs. Those numbers
    # were sitting in the unbound-literal list at the bottom of this report,
    # which is where a value goes to not be read. Recomputing them makes a
    # wrong one fail the build instead.
    N_HALF = {"webqsp": 200, "cwq": 198}
    disc, gaps = {}, {}
    for row in d["ablations"]["mcnemar_vs_full"]:
        cond = row["system_b"].replace("half_abl_", "")
        key = (row["dataset"], cond)
        disc[key] = row["a_only_correct"] + row["b_only_correct"]
        gaps[key] = min_detectable_gap(disc[key])

    def says(pattern, label, expect):
        """Bind a tuple of numbers to the ONE sentence that states them.

        Presence-matching is not enough here. Corrupting "conditions produced
        $21$" to $22$ still passed, because 21 also appears in the sentence
        listing the pair counts and the check only asked whether the value
        was somewhere in the paper. In a document full of small integers, it
        always is. These patterns pin each number to its own sentence.
        """
        m = re.search(pattern.replace(" ", r"\s+"), text)
        got = tuple(int(g) for g in m.groups()) if m else None
        ck(label, got == expect, f"paper {got or 'NO MATCH'}, computed {expect}")

    says(r"Backtracking produced \$(\d+)\$ and \$(\d+)\$ discordant pairs, "
         r"and model scoring \$(\d+)\$ and \$(\d+)\$",
         "the discordant-pair sentence states the real counts",
         (disc[("webqsp", "nobacktrack")], disc[("cwq", "nobacktrack")],
          disc[("webqsp", "embonly")], disc[("cwq", "embonly")]))

    says(r"called significant is \$(\d+)\$ and \$(\d+)\$ questions for backtracking",
         "backtracking's minimum detectable gap is stated correctly",
         (gaps[("webqsp", "nobacktrack")], gaps[("cwq", "nobacktrack")]))

    says(r"and \$(\d+)\$ and \$(\d+)\$ for model scoring",
         "model scoring's minimum detectable gap is stated correctly",
         (gaps[("webqsp", "embonly")], gaps[("cwq", "embonly")]))

    # Both verifier arms have a single discordant pair, where no split can
    # reach alpha at all. That is a stronger statement than a failed test and
    # the paper has to make it, not soften it into "underpowered".
    ck("the verifier arms are reported as untestable, not merely underpowered",
       all(gaps[(ds, "noverifier")] is None for ds in ("webqsp", "cwq"))
       and "no split whatsoever" in text,
       f"discordant pairs: {disc[('webqsp','noverifier')]} and "
       f"{disc[('cwq','noverifier')]}")

    # The ablations run on HALF-splits. The first draft reported the verifier
    # null "across 400 questions per dataset" and as "399 of 400" agreeing --
    # the full test-set size, which is the denominator two sections away, not
    # this one. Both sentences are bound to the half-split sizes here so the
    # ablation section cannot quote a test-set denominator again.
    says(r"the half-splits --- \$(\d+)\$ questions on WebQSP and \$(\d+)\$ on",
         "the verification-null sentence uses the half-split denominators",
         (N_HALF["webqsp"], N_HALF["cwq"]))

    paired = N_HALF["webqsp"] + N_HALF["cwq"]
    agree = paired - disc[("webqsp", "noverifier")] - disc[("cwq", "noverifier")]
    says(r"agreeing on \$(\d+)\$ of the \$(\d+)\$ paired questions",
         "the agreement count is over the paired half-splits, not the test sets",
         (agree, paired))

    pcts = sorted(rnd(100 * gaps[k] / N_HALF[k[0]], 1)
                  for k in gaps if gaps[k] is not None and k[1] != "noplanner")
    m = re.search(r"between\s+\$([\d.]+)\$\s+and\s+\$([\d.]+)\$\s+points of accuracy",
                  text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the MDE range endpoints match the computed range",
       got == (min(pcts), max(pcts)),
       f"paper {got or 'NO MATCH'}, computed {(min(pcts), max(pcts))}")

    n80 = next(n for n in range(4, 200) if mcnemar_power(n, 2) >= 0.80)
    ck(f"discordant pairs for 80% power at 2:1 = {n80}", quoted(nums, n80))

    biggest = max(v for k, v in disc.items() if k[1] != "noplanner")
    says(r"the largest of these conditions produced \$(\d+)\$",
         "the largest-condition sentence states the real count", (biggest,))
    ratio = 1.0
    while mcnemar_power(biggest, ratio) < 0.80 and ratio < 20:
        ratio += 0.01
    # Read the ratio out of the sentence that states it, rather than asking
    # whether the rounded value appears anywhere. Presence-matching passed
    # this when the paper said 3:1 and the truth was 4.23:1, because "4.0"
    # was already in the text as an MDE endpoint and round(4.23) == 4 met
    # it by coincidence. A small integer will always find a match somewhere
    # in a paper full of small integers.
    m = re.search(r"detectable at\s*\$?80\\%\$?\s*power is nearer \$(\d+)\{:\}1\$",
                  text)
    ck("the detectable-ratio sentence states the computed ratio",
       m is not None and int(m.group(1)) == round(ratio),
       f"paper says {m.group(1) if m else 'NO MATCH'}:1, computed {ratio:.2f}:1")

    ck("a 2:1 effect's power at that pair count is quoted as about a quarter",
       "a quarter" in text,
       f"power({biggest}, 2:1) = {mcnemar_power(biggest, 2):.3f}")

    ck("the paper does not claim 80% power at 2:1 from ~30 pairs",
       not re.search(r"2\{:\}1[^.]{0,80}80\\%\s*power", text)
       and "$20$ to $10$" not in text)

    print("\n== the static baseline's claim boundary ==")
    # The thesis draws a hard line here (sec:baseline-graphrag, sec:findings):
    # GraphRAG's per-stratum decay is confounded by its ONE-hop radius and is
    # "not offered as evidence", because "the alternative is to read an
    # implementation limit as a result". The paper's first draft crossed that
    # line -- it called the baseline "actively worse than parametric memory"
    # and invented a context-flooding mechanism. The thesis's actual finding
    # is the opposite: the raw-hits comparison misleads, and GraphRAG is the
    # MORE precise system once abstention is accounted for.
    caps = d["candidate_caps"]["expanded_entity_degree"]
    for sysname, label in (("graphrag", "GraphRAG"), ("noretrieval", "control")):
        ans = gnd[f"test_webqsp_{sysname}"]["questions_answered"]
        hits = round(by[f"webqsp/{sysname}"]["hits_at_1"] * 400)
        ck(f"{label} asserts on {ans}, wrong on {ans - hits}",
           quoted(nums, ans) and quoted(nums, ans - hits))
        ck(f"{label} assertion precision = {rnd(100 * hits / ans, 1)}%",
           quoted(nums, rnd(100 * hits / ans, 1)))

    ck("the paper does not call the static baseline worse than parametric memory",
       not re.search(r"actively worse than parametric", text))
    ck("the paper does not attribute its score to context flooding",
       not re.search(r"floods the context", text))
    ck("the radius confound is disclosed where the strata are discussed",
       "radius confounds it" in text or "radius confounds" in text)
    ck("the fanout cap's question-level reach is stated",
       quoted(nums, caps["questions_any_topic_over_100_pct"]),
       f"{caps['questions_any_topic_over_100_pct']}% of questions "
       "have >=1 topic entity truncated")

    print("\n== gold-defect exclusions: recomputed, not asserted ==")
    # The paper claimed exclusion "raises every system's accuracy by roughly
    # the defect rate", which is wrong by up to 20x -- the true range is
    # +0.001 to +0.020 against defect rates of 5.5% and 4.8%, because a
    # broken label hands out hits as well as denying them. The thesis
    # declines to rescore at all. This block recomputes the sensitivity from
    # the run records so the paper's range and its ordering claim are
    # measured rather than asserted.
    P4 = NUMBERS.parent
    excl = json.load(open(P4 / "census_exclusions.json", encoding="utf-8"))
    SYSTEMS_ALL = ("noretrieval", "vectorrag", "graphrag", "tog", "agr")

    def _n(s):
        return unicodedata.normalize("NFKC", s).strip().lower()

    def _hit(rec):
        return bool({_n(g) for g in rec["gold"]}
                    & {_n(a) for a in rec.get("answer_entities", [])})

    deltas, order_ok, repro_ok = [], True, True
    for ds in ("webqsp", "cwq"):
        drop = set(excl[ds])
        acc = {}
        for s in SYSTEMS_ALL:
            recs = [json.loads(l) for l in
                    open(P4 / f"test_{ds}_{s}.jsonl", encoding="utf-8")]
            full = sum(_hit(r) for r in recs) / len(recs)
            kept = [r for r in recs if r["qid"] not in drop]
            acc[s] = (full, sum(_hit(r) for r in kept) / len(kept))
            # The recomputation must reproduce the published cell first --
            # to within a last-place rounding, not exactly. The two
            # conventions genuinely disagree on one cell: CWQ no-retrieval is
            # 123/400 = 0.3075, whose double is 0.30749999999999999556, so
            # Python's round() gives the published 0.307 while rnd()'s
            # Decimal half-up gives 0.308. That is the 0.6295 hazard again,
            # pointing the other way. Neither convention is wrong; comparing
            # exactly against either one is.
            repro_ok &= abs(full - by[f"{ds}/{s}"]["hits_at_1"]) < 0.001
            deltas.append(acc[s][1] - acc[s][0])
        order_ok &= (sorted(SYSTEMS_ALL, key=lambda s: -acc[s][0])
                     == sorted(SYSTEMS_ALL, key=lambda s: -acc[s][1]))

    ck("the rescoring recomputation reproduces the published table", repro_ok)
    lo, hi = rnd(min(deltas)), rnd(max(deltas))
    m = re.search(r"between\s+\$\+([\d.]+)\$\s+and\s+\$\+([\d.]+)\$\s+Hits@1", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the exclusion-sensitivity range is the measured one",
       got == (lo, hi), f"paper {got or 'NO MATCH'}, computed {(lo, hi)}")
    ck("the ordering claim matches the recomputation", order_ok)
    ck("the paper no longer equates the shift with the defect rate",
       not re.search(r"roughly the defect rate", text))
    ck("the paper does not claim a defect floor bounding achievable accuracy",
       not re.search(r"label-defect floor", text))

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
