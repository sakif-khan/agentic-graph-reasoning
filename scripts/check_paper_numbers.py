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
SECTIONS = ROOT / "journal" / "sections"
PAPER = ROOT / "journal" / "journal_0421052099.tex"

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


def section_body(label):
    """The text under the section carrying `label`, whitespace collapsed.

    Collapsing matters: the .tex is hard-wrapped, so a phrase as short as
    "relations per entity" straddles a newline and a naive substring search
    misses it. That reported sec:cost as failing to deliver text sitting
    right inside it.
    """
    for p in sorted(SECTIONS.glob("*.tex")):
        raw = COMMENT.sub("", io.open(p, encoding="utf-8").read())
        m = re.search(r"\\(?:sub)*section\{[^}]*\}\s*\\label\{"
                      + re.escape(label) + r"\}", raw)
        if not m:
            continue
        rest = raw[m.end():]
        nxt = re.search(r"\n\\(?:sub)*section\{", rest)
        return re.sub(r"\s+", " ", rest[:nxt.start()] if nxt else rest)
    return None


def rnd(val, places=3):
    """Round the way a person writing the number would.

    Not round(): the IEEE double nearest a decimal tie can sit below it,
    so round() can go either way. Going through Decimal(str(...)) rounds
    the decimal the JSON actually carries. Beware of using this on a value
    the JSON has ALREADY rounded: 141/224 = 0.62946 is stored as 0.6295,
    and half-up on that gives 0.630 when the true rate rounds to 0.629.
    Where a count and an n are available, round the exact fraction once
    instead (see the budget-split block).
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
    # The JSON carries these rates to four decimals, which is itself a
    # rounding: CWQ tog_finished is 141/224 = 0.62946, stored as 0.6295,
    # and rounding THAT half-up gives 0.630 while the true rate rounds to
    # 0.629 (which is what the thesis's generated table prints). So the
    # hit count is recovered from n and the rate, and the exact fraction is
    # rounded once.
    for ds in ("webqsp", "cwq"):
        for subset in ("tog_finished", "tog_clipped"):
            blk = tog[ds][subset]
            ck(f"{ds} {subset} n = {blk['n']}", quoted(nums, blk["n"]))
            for who in ("tog_hits_at_1", "agr_hits_at_1"):
                hits = round(blk[who] * blk["n"])
                v = float((Decimal(hits) / Decimal(blk["n"])).quantize(
                    Decimal("0.001"), rounding=ROUND_HALF_UP))
                ck(f"{ds} {subset} {who} = {v} ({hits}/{blk['n']})",
                   quoted(nums, v))

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
        got = tuple(float(g) if "." in g else int(g)
                    for g in m.groups()) if m else None
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
    # Whitespace-tolerant, like the kappa and candidate-width blocks below:
    # the .tex hard-wraps at 72 columns, and the September 2026 shortening
    # moved the break into "no split / whatsoever", which reported the
    # sentence missing while it sat there in full.
    ck("the verifier arms are reported as untestable, not merely underpowered",
       all(gaps[(ds, "noverifier")] is None for ds in ("webqsp", "cwq"))
       and re.search(r"no\s+split\s+whatsoever", text) is not None,
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
    m = re.search(r"between\s+\$([\d.]+)\$\s+and\s+\$([\d.]+)\$\s+points\s+of\s+accuracy",
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
    m = re.search(r"detectable\s+at\s*\$?80\\%\$?\s*power\s+is\s+nearer\s+\$(\d+)\{:\}1\$",
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
    counts = {}
    for sysname in ("graphrag", "noretrieval"):
        ans = gnd[f"test_webqsp_{sysname}"]["questions_answered"]
        hits = round(by[f"webqsp/{sysname}"]["hits_at_1"] * 400)
        counts[sysname] = (ans, ans - hits, rnd(100 * hits / ans, 1))

    # Pinned to their own sentences. These were presence checks until adding
    # "All $41$ were removed" to the error analysis gave GraphRAG's
    # wrong-answer count a second home in the paper -- after which
    # corrupting it here still passed. Any small integer will eventually
    # acquire one; the sentence is the only stable anchor.
    says(r"The control asserts on \$(\d+)\$ of \$400\$ questions and is "
         r"wrong on \$(\d+)\$ of them",
         "the control's assert/wrong counts are stated in their sentence",
         counts["noretrieval"][:2])
    says(r"GraphRAG asserts on \$(\d+)\$ and is wrong on \$(\d+)\$",
         "GraphRAG's assert/wrong counts are stated in their sentence",
         counts["graphrag"][:2])
    for sysname, label in (("graphrag", "GraphRAG"), ("noretrieval", "control")):
        ck(f"{label} assertion precision = {counts[sysname][2]}%",
           quoted(nums, counts[sysname][2]))

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

    print("\n== semantic tier: every cell, no selection ==")
    # The draft quoted AGR's 66.7/48.3 against Think-on-Graph and the
    # parametric control only, omitting Vector-RAG's 50.0 -- the highest
    # cell on CWQ, above AGR. Quoting the comparators a system beats and
    # dropping the one it loses to is the failure mode this block exists
    # for, so every cell must appear and the second-place fact must be said.
    t2 = d["groundedness_tier2_judge"]
    # Parse the TABLE ROWS, not the document. A presence check passed when
    # Vector-RAG's leading CWQ cell was corrupted in the table, because the
    # same value also appears in the prose sentence beside it. Every cell
    # has to be right where a reader reads it off.
    MACRO = {"noretrieval": r"\\noret", "vectorrag": r"\\vecrag",
             "graphrag": r"\\graphrag", "tog": r"\\tog", "agr": r"\\agr"}
    NUM = r"(?:\\textbf\{)?([\d.]+)\\%\}?"
    for s in SYSTEMS:
        m = re.search(MACRO[s] + r"\s*&\s*" + NUM + r"\s*&\s*" + NUM + r"\s*\\\\",
                      text)
        got = tuple(float(g) for g in m.groups()) if m else None
        want = (t2[f"test_webqsp_{s}"]["supported_pct"],
                t2[f"test_cwq_{s}"]["supported_pct"])
        ck(f"tier-2 table row for {s} = {want}",
           got == want, f"table says {got or 'NO ROW'}")

    cwq = {s: t2[f"test_cwq_{s}"]["supported_pct"] for s in SYSTEMS}
    wq = {s: t2[f"test_webqsp_{s}"]["supported_pct"] for s in SYSTEMS}
    best_cwq = max(cwq, key=cwq.get)
    ck("AGR is not the top system on CWQ's semantic tier",
       best_cwq != "agr", f"{best_cwq} leads at {cwq[best_cwq]}%")
    ck("the paper says AGR is second there",
       "it is second" in text.lower(),
       f"AGR {cwq['agr']}% vs {best_cwq} {cwq[best_cwq]}%")
    ck("the paper scopes the clean sweep to WebQSP",
       "WebQSP result only" in text,
       f"AGR leads WebQSP at {wq['agr']}% but not CWQ")
    band = (min(list(wq.values()) + list(cwq.values())),
            max(list(wq.values()) + list(cwq.values())))
    m = re.search(r"lands?\s+in\s+a\s+\$([\d.]+)\$--\$([\d.]+)\\%\$\s+band", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the stated band is the measured one",
       got == band, f"paper {got or 'NO MATCH'}, computed {band}")

    print("\n== the judge's kappa is reported short, never rounded ==")
    # The judge that produces the semantic tier above missed its own
    # pre-specified bar. The draft wrote "Cohen's $\kappa = 0.70$", which is
    # precisely the rendering the thesis singles out: "Rounded to three
    # decimals this value reads 0.700 and appears to clear; it does not."
    # Four ways to lose that, all of which passed before this block existed:
    # rounding to 0.70, rounding to 0.700, keeping 0.6995 but cutting the
    # miss, and dropping the sentence from setup.tex entirely -- the last
    # one silent because discussion.tex also says 0.6995, so a
    # document-wide presence test stayed green.
    jv = d["judge_validation"]
    kappa, bar = jv["cohens_kappa"], jv["preregistered_threshold"]
    setup = section_body("sec:protocol")
    ck("setup states the judge's kappa exactly, not rounded",
       re.search(r"\\kappa\s*=\s*" + re.escape(str(kappa)) + r"\b", setup or ""),
       f"expected \\kappa = {kappa} in sec:protocol")
    ck("setup states that it MISSES the bar it was set",
       bool(setup) and re.search(r"misses\}? the \$0\.70?\$", setup, re.I),
       "the number without the miss reads as a pass")
    shortfall = float(Decimal(str(bar)) - Decimal(str(kappa)))
    ck(f"the stated shortfall is {shortfall}",
       bool(setup) and f"{shortfall}" in setup,
       f"{bar} - {kappa} = {shortfall}")
    says(r"on \$(\d+)\$ items, reaching \$(\d+)\\%\$", "judge validated on n items at agreement",
         (jv["n"], int(round(jv["observed_agreement"] * 100))))
    # No occurrence of \kappa anywhere in the paper may assign it a rounded
    # value. Whitespace-tolerant: the .tex hard-wraps, and "\kappa =\n0.70"
    # slipped past a literal-space guard. Mentions of the THRESHOLD as
    # "$0.70$" are untouched -- this fires only on \kappa being *set* to it.
    rounded = re.findall(r"\\kappa\$?\s*=\s*\$?(0\.7|0\.70|0\.700)\b", text)
    ck("kappa is never assigned a rounded value anywhere in the paper",
       not rounded, f"found \\kappa = {', '.join(rounded)}")

    print("\n== the limitations list is complete ==")
    # discussion.tex claims every limitation a reviewer could raise appears
    # there. An earlier draft made that claim while carrying six of the
    # thesis's eleven threats. A claim of completeness that is not complete
    # is worse than no claim, so the roster is enforced rather than trusted.
    # Each entry: a phrase that must appear in the discussion section.
    # The whole file, not section_body("sec:discussion"): that stops at the
    # first \subsection and returned only the two-line preamble, which
    # reported all sixteen limitations missing when none were.
    disc = re.sub(r"\s+", " ", COMMENT.sub(
        "", io.open(SECTIONS / "discussion.tex", encoding="utf-8").read()))
    LIMITS = {
        # Phrases must avoid LaTeX math delimiters: "400 questions per
        # dataset" is written "$400$ questions per dataset" and does not
        # match as a plain substring.
        "sample size": "questions per dataset",
        "one backbone": "one backbone",
        "nondeterminism": "trajectory stability",
        "environment ceiling": "reachability",
        "ablation power": "no effect detected",
        "scope": "English factoid",
        "wrongful acceptance": "Wrongful acceptance is unmeasured",
        "output contract unauditable": "cannot be audited",
        "candidate widths": "identical access",
        "static baseline radius": "radius-bounded",
        "entity linking assumed": "given, not linked",
        "homonym merging": "homonyms merge",
        "extraction-bug floor": "unmeasured floor",
        "judge missed its bar": "0.6995",
        "single-annotator adjudication": "single-annotator",
        "post-hoc relabelling": "after its outcome was known",
    }
    missing = [k for k, v in LIMITS.items() if v.lower() not in disc.lower()]
    ck(f"all {len(LIMITS)} limitations are present in the discussion",
       not missing, f"missing: {', '.join(missing)}" if missing else "")

    # The three that bound claims this paper actually makes must be stated
    # at full strength, not merely mentioned.
    ck("wrongful acceptance is called the most serious gap",
       "most serious gap" in disc)
    ck("the output-contract gap names what the log actually keeps",
       "count" in disc and "discards the list" in disc)
    # The rounding guard itself lives in the kappa block above, which is
    # whitespace-tolerant and covers every section. This one only asserts
    # that the discussion states the shortfall as a limitation; the literal
    # regex that used to sit here missed a hard-wrapped "\kappa =\n0.70".
    ck("the discussion carries the judge shortfall as a limitation",
       "0.6995" in disc and "missed its own bar" in disc,
       "the discussion must name the miss, not just the number")

    print("\n== forward promises land somewhere that delivers ==")
    # LaTeX verifies that a \Cref target EXISTS; nothing verifies that the
    # target says what the sentence promised. setup.tex pointed at Sec 5.2
    # for "the measurement that bounds" the candidate-width confound, Sec 5.2
    # resolved fine, and contained nothing about widths. A dangling promise
    # of this kind is invisible to the build and to a reading that follows
    # the reference forward expecting to find the topic already introduced.
    # sec:margin was split out of sec:cost in September 2026; the
    # candidate-width measurement and the equal-width caveat moved with it.
    PROMISES = [
        ("sec:margin", ("relations per entity",),
         "setup names the candidate-width confound and points here"),
        ("sec:power", ("detectable",),
         "discussion points here for the minimum detectable effect"),
        ("sec:removal", ("flag",),
         "the framework lead-in promises that each component is one flag"),
        ("sec:outlook", ("cap",),
         "sec:margin promises that the cap sweep is the first experiment named"),
        ("sec:defects", ("no-retrieval control",),
         "sec:echo promises that the defect pass measures which systems converge"),
        ("sec:groundedness", ("ungrounded",),
         "the introduction points here for the groundedness result"),
        ("sec:verification", ("claim",),
         "the introduction points here for the verification layer"),
        ("sec:echo", ("echo attractor",),
         "the introduction names the echo attractor and points here"),
    ]
    for label, keywords, why in PROMISES:
        body = section_body(label)
        ck(f"{label} delivers what is promised of it",
           body is not None and any(k.lower() in body.lower() for k in keywords),
           why if body is not None else f"NO SECTION LABELLED {label}")

    print("\n== the candidate-width confound is measured, not just named ==")
    # setup.tex names this confound and promised "Sec 5.2 reports the
    # measurement that bounds it". Sec 5.2 reported nothing of the kind --
    # it discusses the call cap only. The binding rates and the lower-bound
    # reading they force are stated in the thesis four times and appeared
    # nowhere in the paper.
    cc = d["candidate_caps"]
    says(r"the first \$(\d+)\$ relations per entity and the first \$(\d+)\$ "
         r"neighbours per relation",
         "the baseline's candidate widths are stated",
         (cc["tog"]["relation_cap"], cc["tog"]["neighbor_cap"]))
    says(r"against AGR's \$(\d+)\$ and \$(\d+)\$",
         "AGR's candidate widths are stated",
         (cc["agr"]["relation_cap"], cc["agr"]["neighbor_cap"]))
    # Whitespace-tolerant throughout: the .tex hard-wraps, and a break
    # between "binds" and "on" reported the measured rates as missing.
    m = re.search(r"binds\s+on\s+\$([\d.]+)\\%\$\s+of\s+the\s+\$1\{,\}(\d+)\$"
                  r"\s+entities[\s\S]{0,80}?on\s+\$([\d.]+)\\%\$\s+of\s+its\s+"
                  r"\$7\{,\}(\d+)\$\s+neighbour\s+calls", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = (cc["tog"]["entities_at_relation_cap_pct"],
            float(str(cc["tog"]["entities_expanded"])[1:]),
            cc["tog"]["neighbor_calls_at_cap_pct"],
            float(str(cc["tog"]["get_neighbors_calls"])[1:]))
    ck("the baseline's binding rates are the measured ones",
       got == want, f"paper {got or 'NO MATCH'}, computed {want}")
    ck("AGR's own binding rates are stated for contrast",
       quoted(nums, cc["agr"]["entities_at_relation_cap"])
       and quoted(nums, cc["agr"]["entities_expanded"])
       and quoted(nums, cc["agr"]["neighbor_calls_at_cap_pct"]))
    ck("the unclipped figures are called a lower bound",
       re.search(r"lower bound", text) is not None
       and "equal-width" in text)
    # Proposing the equal-width re-run without its confound reads as a
    # clean single-variable experiment, which it is not: the thesis's
    # future-work section notes that wider candidate sets make each
    # pruning call dearer, so equalising widths ALSO raises the baseline's
    # clip rate and moves the boundary of the very split the comparison is
    # read from. The paper proposed the re-run and dropped the caveat.
    cost = section_body("sec:margin") or ""
    ck("the equal-width re-run carries its clip-rate confound",
       "clip rate" in cost and "read apart" in cost,
       "equalising widths also moves the split it would be measured on")
    ck("and says to report the split rather than an aggregate",
       re.search(r"rather than an aggregate", cost) is not None,
       "the two effects cancel or compound invisibly in a pooled number")

    print("\n== populations are not mixed, and ratios are per dataset ==")
    # Three ways a number can be right and still be wrong in place.
    #
    # 1. Right value, wrong population. The backtracking paragraph paired
    #    "38 and 108 backtracks across the half-splits" with a 6.2% refusal
    #    rate -- but 6.2% is 50/800 over the MAIN runs (budget_binding is
    #    sourced from test_{ds}_agr.jsonl and says n_questions: 800). Over
    #    the 398 paired questions the figure is 7.0%. Recomputed here from
    #    the ablation records with the same unit build_thesis_numbers uses
    #    -- the meter DENIED a request -- rather than read from the JSON,
    #    which does not carry a half-split budget block at all.
    cap = d["budget_binding"]["_caps"]["backtracks"]
    ref = n_ab = bts = 0
    for ds in ("webqsp", "cwq"):
        rows = [json.loads(l) for l in io.open(
            ROOT / "results" / "phase4" / "ablations" /
            f"test_{ds}_half_abl_full.jsonl", encoding="utf-8") if l.strip()]
        ref += sum(1 for r in rows
                   if "backtrack" in (r["budget"].get("exhausted") or []))
        bts += sum(r["budget"].get("backtracks", 0) for r in rows)
        n_ab += len(rows)
    m = re.search(r"\$(\d+)\$\s+and\s+\$(\d+)\$\s+backtracks\s+over\s+the\s+"
                  r"\$(\d+)\$\s+paired\s+questions[\s\S]{0,90}?refuses\s+a\s+"
                  r"further\s+attempt\s+on\s+\$(\d+)\$\s+of\s+them,\s+"
                  r"\$([\d.]+)\\%\$", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    reasons = d["ablations"]["backtrack_reasons"]
    want = (float(reasons["webqsp/full"]["total"]),
            float(reasons["cwq/full"]["total"]),
            float(n_ab), float(ref), rnd(100 * ref / n_ab, 1))
    ck("backtracking's rarity is stated over the half-splits throughout",
       got == want, f"paper {got or 'NO MATCH'}, computed {want}")
    main_pct = d["budget_binding"]["both"]["backtracks"]["refused_pct"]
    nulls = section_body("sec:nulls") or ""
    ck("the ablation paragraph does not quote the main-run refusal rate",
       f"${main_pct}\\%$" not in nulls,
       f"{main_pct}% is the 800-question figure, a different population")
    ck("the recomputed backtrack total matches the reasons table",
       bts == (d["ablations"]["backtrack_reasons"]["webqsp/full"]["total"]
               + d["ablations"]["backtrack_reasons"]["cwq/full"]["total"]),
       f"records {bts}")

    # 2. Right counts, wrong fraction named. "Roughly half of what the
    #    consensus pass flagged was not a bad label" -- 105 flagged, 41
    #    confirmed, so it is roughly three-fifths. The word is checked
    #    against the arithmetic, not spot-read: if the counts move, the
    #    nearest simple fraction moves and this fails.
    ga = d["gold_adjudication"]
    flagged = ga["webqsp"]["flagged_questions"] + ga["cwq"]["flagged_questions"]
    confirmed = d["benchmark_defects"]["excluded_before_census"]
    says(r"flagged \$(\d+)\$ questions and adjudication confirmed \$(\d+)\$",
         "the flagged and confirmed counts are both stated", (flagged, confirmed))
    NAMED = {"half": 0.5, "three-fifths": 0.6, "two-thirds": 2 / 3,
             "three-quarters": 0.75, "two-fifths": 0.4, "a third": 1 / 3}
    not_defect = 1 - confirmed / flagged
    nearest = min(NAMED, key=lambda k: abs(NAMED[k] - not_defect))
    ck(f"the fraction is named {nearest} ({not_defect:.3f} of {flagged})",
       re.search(r"roughly\s+" + nearest + r"\s+of\s+what", text),
       f"{flagged} flagged - {confirmed} confirmed = {flagged - confirmed}")

    # 3. One ratio quoted for two datasets that do not share it. 6.2/12.8
    #    is 0.48, but 8.9/18.2 is 0.49; "a ratio of 0.48 on both" was true
    #    of one of them.
    ratios = tuple(rnd(by[f"{ds}/agr"]["mean_calls"]
                       / by[f"{ds}/tog"]["mean_calls"], 2)
                   for ds in ("webqsp", "cwq"))
    m = re.search(r"ratios\s+of\s+\$([\d.]+)\$\s+and\s+\$([\d.]+)\$", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the call ratios are stated per dataset, not merged",
       got == ratios, f"paper {got or 'NO MATCH'}, computed {ratios}")

    print("\n== the 57 must be reachable from the numbers printed ==")
    # 57 is 41 + 17 - 1, not 22 + 19 reconciled. The paper presented it as
    # the latter, which is arithmetically impossible (22 + 19 = 41) and
    # hides the 17 census-found defects entirely; it also described the
    # duplicate as spanning the two datasets when it spans the exclusion set
    # and the census. Every term is bound here so the total has to add up in
    # the text a reader can see.
    bd = d["benchmark_defects"]
    ce = d["census_exclusions"]
    hist = d["failure_histogram"]
    excl_total = ce["webqsp"] + ce["cwq"]
    ck("the per-dataset exclusion counts are stated",
       quoted(nums, ce["webqsp"]) and quoted(nums, ce["cwq"]))
    # Pinned, not merely present: 41 also appears as GraphRAG's wrong-answer
    # count, so a presence check passed this when the total was corrupted.
    says(r"All \$(\d+)\$ were removed",
         "the exclusion total is stated in its own sentence", (excl_total,))
    ck("the exclusion total matches the JSON's own",
       excl_total == bd["excluded_before_census"],
       f"{ce['webqsp']} + {ce['cwq']} = {excl_total}")

    per_ds = {ds: sum(hist[ds][k].get(c, 0)
                      for k in ("wrong", "hedge")
                      for c in ("gold_noise", "ambiguous_question"))
              for ds in ("webqsp", "cwq")}
    census_defects = sum(per_ds.values())
    # Also pinned: 17 appears as the CWQ gold_wrong count two sentences up,
    # so dropping this term entirely still left 17 "present" in the paper.
    # That is the term whose omission made 57 unreachable in the first place.
    says(r"found \$(\d+)\$ more that the pre-pass had missed --- "
         r"\$(\d+)\$ on WebQSP and \$(\d+)\$ on",
         "the census-found defects and their split are stated in one sentence",
         (census_defects, per_ds["webqsp"], per_ds["cwq"]))
    ck("the census-defect count matches the JSON's own",
       census_defects == bd["census_rows_in_defect_categories"])

    dup = len(bd["counted_in_both"])
    ck(f"57 = {excl_total} + {census_defects} - {dup} adds up",
       excl_total + census_defects - dup == bd["distinct_questions"])
    ck(f"the paper quotes the distinct total {bd['distinct_questions']}",
       quoted(nums, bd["distinct_questions"]))
    # Target the retired wording, not the phrase "both datasets", which is
    # ordinary English used correctly four times elsewhere in the paper.
    ck("the duplicate is not described as spanning the two datasets",
       not re.search(r"appearing in both counts", text)
       and not re.search(r"both datasets'? counts", text),
       "it spans the exclusion set and the census")

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

    print("\n== figures carried over from the thesis in September 2026 ==")
    # Each of these entered the paper when it was re-synchronised with the
    # thesis chapters. Every one is bound to its own sentence, for the reason
    # the power block gives: in a paper full of small numbers, presence is
    # not evidence.

    # CWQ assertion precision: commitments, hits, wrongs and the rate, for
    # AGR and the agentic baseline. Hits come from the main table; the
    # commitments from the structural-groundedness log, which counts
    # answered questions.
    ap = {}
    for s in ("agr", "tog"):
        ans = gnd[f"test_cwq_{s}"]["questions_answered"]
        hits = round(by[f"cwq/{s}"]["hits_at_1"] * 400)
        ap[s] = (ans, hits, ans - hits, rnd(100 * hits / ans, 1))
    says(r"on \$(\d+)\$ and \$(\d+)\$ of \$400\$ questions",
         "the two systems' CWQ commitment counts are stated",
         (ap["agr"][0], ap["tog"][0]))
    says(r"AGR is right \$(\d+)\$ times and wrong \$(\d+)\$, against \$(\d+)\$ "
         r"and \$(\d+)\$ for Think-on-Graph",
         "the CWQ hit and wrong counts are stated for both systems",
         (ap["agr"][1], ap["agr"][2], ap["tog"][1], ap["tog"][2]))
    m = re.search(r"\$([\d.]+)\\%\$\s+assertion\s+precision\s+against\s+"
                  r"\$([\d.]+)\\%\$", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the CWQ assertion precisions are the computed ones",
       got == (ap["agr"][3], ap["tog"][3]),
       f"paper {got or 'NO MATCH'}, computed {(ap['agr'][3], ap['tog'][3])}")
    says(r"finds \$(\d+)\$ more answers and asserts \$(\d+)\$ fewer falsehoods",
         "the hit and falsehood margins add up",
         (ap["agr"][1] - ap["tog"][1], ap["tog"][2] - ap["agr"][2]))

    # AGR against the agentic baseline, paired: discordant counts and the
    # exact McNemar p, recomputed from the run records.
    def _hits(ds, s):
        return {json.loads(l)["qid"]: _hit(json.loads(l)) for l in
                open(P4 / f"test_{ds}_{s}.jsonl", encoding="utf-8")}
    disc_tog = {}
    for ds in ("webqsp", "cwq"):
        a, t = _hits(ds, "agr"), _hits(ds, "tog")
        a_only = sum(1 for q in a if a[q] and not t[q])
        t_only = sum(1 for q in a if t[q] and not a[q])
        disc_tog[ds] = (a_only, t_only, exact_p(t_only, a_only + t_only))
    says(r"rest on \$(\d+)\$ questions AGR alone answers against \$(\d+)\$ "
         r"the other way on WebQSP",
         "the WebQSP discordant counts against the baseline are stated",
         disc_tog["webqsp"][:2])
    says(r"and \$(\d+)\$ against \$(\d+)\$ on ComplexWebQuestions",
         "the CWQ discordant counts against the baseline are stated",
         disc_tog["cwq"][:2])
    for ds, name in (("webqsp", "WebQSP"), ("cwq", "ComplexWebQuestions")):
        mant, expo = f"{disc_tog[ds][2]:.1e}".split("e")
        pat = (r"on " + name + r"\s+\(\$p = ([\d.]+) \\times 10\^\{(-?\d+)\}\$\)")
        m = re.search(pat.replace(" ", r"\s+"), text)
        got = (float(m.group(1)), int(m.group(2))) if m else None
        ck(f"the {name} McNemar p against the baseline is stated correctly",
           got == (float(mant), int(expo)),
           f"paper {got or 'NO MATCH'}, computed {mant}e{expo}")

    # Breadth check: entities per answered question and entity precision
    # over the answered subset, both systems, both datasets.
    bw = tog["webqsp"]
    bc = tog["cwq"]
    m = re.search(r"AGR names \$([\d.]+)\$ entities against Think-on-Graph's "
                  r"\$([\d.]+)\$, and its entity precision over those same "
                  r"answered questions is \$([\d.]+)\$ against \$([\d.]+)\$"
                  .replace(" ", r"\s+"), text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = (bw["agr_answered"]["entities_per_answer"],
            bw["tog_answered"]["entities_per_answer"],
            rnd(bw["agr_answered"]["precision"]),
            rnd(bw["tog_answered"]["precision"]))
    ck("the WebQSP breadth check quotes the measured figures",
       got == want, f"paper {got or 'NO MATCH'}, computed {want}")
    m = re.search(r"the figures are \$([\d.]+)\$ against \$([\d.]+)\$ entities "
                  r"and \$([\d.]+)\$ against \$([\d.]+)\$ precision"
                  .replace(" ", r"\s+"), text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = (bc["agr_answered"]["entities_per_answer"],
            bc["tog_answered"]["entities_per_answer"],
            rnd(bc["agr_answered"]["precision"]),
            rnd(bc["tog_answered"]["precision"]))
    ck("the CWQ breadth check quotes the measured figures",
       got == want, f"paper {got or 'NO MATCH'}, computed {want}")

    # AGR's own binding budget: the depth cap, over both test sets.
    says(r"refuses a deeper expansion on \$([\d.]+)\\%\$ of test questions",
         "the depth-cap refusal rate is the measured one",
         (d["budget_binding"]["both"]["depth"]["refused_pct"],))

    # The planner's per-stratum effect, recomputed from the half-split
    # records and the committed test-set strata.
    def _strata(ds):
        ts = json.load(open(P4 / f"test_{ds}.json", encoding="utf-8"))
        qs = ts["questions"] if isinstance(ts, dict) and "questions" in ts else ts
        return {q.get("qid") or q.get("id"):
                q.get("stratum") or q.get("hop_stratum") for q in qs}
    strat_eff = {}
    for ds in ("webqsp", "cwq"):
        st = _strata(ds)
        full = {json.loads(l)["qid"]: _hit(json.loads(l)) for l in open(
            P4 / "ablations" / f"test_{ds}_half_abl_full.jsonl", encoding="utf-8")}
        nop = {json.loads(l)["qid"]: _hit(json.loads(l)) for l in open(
            P4 / "ablations" / f"test_{ds}_half_abl_noplanner.jsonl", encoding="utf-8")}
        for s in ("h1", "h2", "h3plus"):
            qs = [q for q in full if st.get(q) == s]
            # unrounded on purpose; see _near below
            strat_eff[(ds, s)] = (sum(full[q] for q in qs) / len(qs),
                                  sum(nop[q] for q in qs) / len(qs))
    # Within half a unit in the last place of the UNROUNDED fraction, not
    # equal to a rounded one: CWQ's three-hop reference is 15/24 = 0.625,
    # an exact tie that the thesis rounds to 0.62 (round-half-even) and
    # rnd() to 0.63. Both are the same number; a transcription error is
    # not, and is still caught.
    def _near(got, want):
        return got is not None and len(got) == len(want) and all(
            abs(g - w) <= 0.005 + 1e-9 for g, w in zip(got, want))
    m = re.search(r"raises one-hop Hits@1 from \$([\d.]+)\$ to \$([\d.]+)\$ and "
                  r"two-hop Hits@1 from \$([\d.]+)\$ to \$([\d.]+)\$"
                  .replace(" ", r"\s+"), text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = strat_eff[("webqsp", "h1")] + strat_eff[("webqsp", "h2")]
    ck("the WebQSP per-stratum planner effect is the recomputed one",
       _near(got, want), f"paper {got or 'NO MATCH'}, computed {want}")
    m = re.search(r"from \$([\d.]+)\$ to \$([\d.]+)\$, two-hop collapses from "
                  r"\$([\d.]+)\$ to \$([\d.]+)\$, and three-hop-plus moves from "
                  r"\$([\d.]+)\$ to \$([\d.]+)\$".replace(" ", r"\s+"), text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = (strat_eff[("cwq", "h1")] + strat_eff[("cwq", "h2")]
            + strat_eff[("cwq", "h3plus")])
    ck("the CWQ per-stratum planner effect is the recomputed one",
       _near(got, want), f"paper {got or 'NO MATCH'}, computed {want}")

    # The RoG comparison: AGR's intervals and its own row of tab:rog. RoG's
    # published row is external and is not bound here.
    ci = {ds: tuple(rnd(100 * v, 1) for v in by[f"{ds}/agr"]["hits_at_1_ci95"])
          for ds in ("webqsp", "cwq")}
    m = re.search(r"\$\[([\d.]+), ([\d.]+)\]\$ on WebQSP and \$\[([\d.]+), "
                  r"([\d.]+)\]\$ on ComplexWebQuestions".replace(" ", r"\s+"),
                  text)
    got = tuple(float(g) for g in m.groups()) if m else None
    ck("the RoG comparison quotes AGR's bootstrap intervals",
       got == ci["webqsp"] + ci["cwq"],
       f"paper {got or 'NO MATCH'}, computed {ci['webqsp'] + ci['cwq']}")
    m = re.search(r"\\agr\{\}\s+\(this work\)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*&"
                  r"\s*([\d.]+)\s*&\s*([\d.]+)\s*\\\\", text)
    got = tuple(float(g) for g in m.groups()) if m else None
    want = tuple(rnd(100 * by[f"{ds}/agr"][k], 1)
                 for ds in ("webqsp", "cwq") for k in ("hits_at_1", "f1"))
    ck("AGR's row of the RoG table is the main table in points",
       got == want, f"table {got or 'NO ROW'}, computed {want}")

    # Gold-set shape, from the committed test samples.
    ts = d["test_sets"]
    says(r"its mean is \$([\d.]+)\$ gold entities per question and its largest "
         r"question lists \$(\d+)\$",
         "the WebQSP gold-set shape is the committed one",
         (ts["webqsp"]["gold_mean"], ts["webqsp"]["gold_max"]))
    ck("exactly half the WebQSP sample carries one gold answer",
       ts["webqsp"]["questions_with_one_gold"] * 2 == ts["webqsp"]["n_questions"]
       and re.search(r"Exactly\s+half\s+of\s+the\s+WebQSP\s+sample", text) is not None)
    says(r"ComplexWebQuestions averages \$([\d.]+)\$ with a median of \$(\d+)\$",
         "the CWQ gold mean and median are the committed ones",
         (ts["cwq"]["gold_mean"], int(ts["cwq"]["gold_median"])))

    # Surface-form near-misses among AGR's wrong answers, from the
    # committed pre-pass artifacts.
    nm = {}
    for ds in ("webqsp", "cwq"):
        w = json.load(open(P4 / f"prepass_wrongs_{ds}.json", encoding="utf-8"))
        nm[ds] = (sum(1 for r in w if r["near_miss"]), len(w))
    says(r"\$(\d+)\$ of \$(\d+)\$ on WebQSP and \$(\d+)\$ of \$(\d+)\$ on "
         r"ComplexWebQuestions are surface-form near-misses",
         "the near-miss counts and wrong-answer denominators are the measured ones",
         nm["webqsp"] + nm["cwq"])

    # The ban-list misalignment that bounds the backtracking null.
    bs = d["backtrack_ban_scope"]["total"]
    says(r"\$(\d+)\$ explorer passes re-expanded",
         "the repeat-expansion count is the traced one",
         (bs["repeat_expansion_passes"],))
    says(r"at least \$(\d+)\$ of the \$(\d+)\$ backtracks restored a depth",
         "the below-stack-top count and backtrack total are the traced ones",
         (bs["pops_below_stack_top"], bs["backtracks"]))

    # RoG's training-split sizes are counted from the distribution itself
    # when it is checked out beside the repository; otherwise reported as
    # unverified rather than passed silently.
    rog = ROOT.parent
    try:
        import glob as _glob
        import pyarrow.parquet as _pq
        counts = tuple(sum(_pq.ParquetFile(f).metadata.num_rows for f in
                           _glob.glob(str(rog / f"RoG-{ds}" / "data" / "train-*.parquet")))
                       for ds in ("webqsp", "cwq"))
        if all(counts):
            says(r"which hold \$(\d+)\{,\}(\d+)\$ and \$(\d+)\{,\}(\d+)\$ questions",
                 "RoG's training-split sizes are the distribution's own",
                 (counts[0] // 1000, counts[0] % 1000, counts[1] // 1000, counts[1] % 1000))
        else:
            print("  [SKIP] RoG parquet files not found beside the repository; "
                  "training-split sizes unverified")
    except ImportError:
        print("  [SKIP] pyarrow not installed; RoG training-split sizes unverified")

    print("\n== figures added in the September 2026 reframe ==")
    # Each is recomputed from the committed records or read from the
    # JSON, and pinned to the sentence or table cell that states it.
    import csv as _csv

    # -- the sample's strata, as the setup section lists them --
    for ds, name in (("webqsp", "WebQSP"), ("cwq", "ComplexWebQuestions")):
        st = ts[ds]["strata"]
        if ds == "webqsp":
            says(r"\$(\d+)\$, \$(\d+)\$, and \$(\d+)\$ questions at one, two, and "
                 r"three or more hops on WebQSP, with \$(\d+)\$ whose",
                 "the WebQSP strata are the committed sample's",
                 (st["h1"], st["h2"], st["h3plus"], st["unreachable"]))
        else:
            says(r"and \$(\d+)\$, \$(\d+)\$, and \$(\d+)\$ on ComplexWebQuestions, "
                 r"with \$(\d+)\$ unreachable",
                 "the CWQ strata are the committed sample's",
                 (st["h1"], st["h2"], st["h3plus"], st["unreachable"]))

    # -- the agentic baseline's call structure under the cap --
    from agr.baselines.tog import WIDTH as _W, DEPTH as _D
    ck("a full ToG depth at width 3 costs up to thirteen calls",
       _W + _W * _W + 1 == 13 and _D == 3
       and re.search(r"up\s+to\s+thirteen\s+calls", text) is not None,
       f"width {_W}, depth {_D}: {_W} + {_W * _W} + 1")
    third = {}
    for ds in ("webqsp", "cwq"):
        recs = [json.loads(l) for l in
                open(P4 / f"test_{ds}_tog.jsonl", encoding="utf-8")]
        third[ds] = sum(1 for r in recs
                        if any(t.get("depth") == _D - 1 for t in r["trace"]))
    says(r"reached its third expansion on \$(\d+)\$ of \$400\$ WebQSP "
         r"questions and \$(\d+)\$ of \$400\$ on",
         "the third-expansion counts are the traced ones",
         (third["webqsp"], third["cwq"]))

    # -- the budget split within hop strata: every cell of tab:togstrata
    #    and the four sentences that read it --
    def _clipped(rec):
        return any(t.get("budget_exhausted") for t in rec["trace"])
    cells = {}
    for ds in ("webqsp", "cwq"):
        st = _strata(ds)
        togs = [json.loads(l) for l in
                open(P4 / f"test_{ds}_tog.jsonl", encoding="utf-8")]
        agrs = {json.loads(l)["qid"]: _hit(json.loads(l)) for l in
                open(P4 / f"test_{ds}_agr.jsonl", encoding="utf-8")}
        for s in ("h1", "h2", "h3plus"):
            for clipped in (False, True):
                sub = [r for r in togs
                       if _clipped(r) == clipped and st.get(r["qid"]) == s]
                cells[(ds, s, clipped)] = (
                    len(sub),
                    rnd(sum(_hit(r) for r in sub) / len(sub)),
                    rnd(sum(agrs[r["qid"]] for r in sub) / len(sub)))
    ROWS = (("webqsp", "h1", r"WebQSP\s*&\s*1"), ("webqsp", "h2", r"WebQSP\s*&\s*2"),
            ("cwq", "h1", r"CWQ\s*&\s*1"), ("cwq", "h2", r"CWQ\s*&\s*2"),
            ("cwq", "h3plus", r"CWQ\s*&\s*3\+"))
    for ds, s, lead in ROWS:
        m = re.search(lead + r"\s*&\s*(\d+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*&\s*"
                      r"(\d+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*\\\\", text)
        got = tuple(float(g) for g in m.groups()) if m else None
        want = tuple(float(v) for v in cells[(ds, s, False)] + cells[(ds, s, True)])
        ck(f"tab:togstrata row {ds}/{s} = {want}",
           got == want, f"table {got or 'NO ROW'}")
    w1f, w1c = cells[("webqsp", "h1", False)], cells[("webqsp", "h1", True)]
    says(r"\$(\d+)\$ of the \$(\d+)\$ clipped questions are single-hop, AGR "
         r"scores \$([\d.]+)\$ on them against \$([\d.]+)\$",
         "the WebQSP single-hop reading of the split is the computed one",
         (w1c[0], tog["webqsp"]["tog_clipped"]["n"], w1c[2], w1f[2]))
    says(r"baseline's fall from \$([\d.]+)\$ to \$([\d.]+)\$",
         "the baseline's single-hop fall across the split is the computed one",
         (w1f[1], w1c[1]))
    c1f, c1c = cells[("cwq", "h1", False)], cells[("cwq", "h1", True)]
    says(r"AGR scores \$([\d.]+)\$ on the clipped single-hop questions against "
         r"\$([\d.]+)\$ on the finished ones",
         "the CWQ single-hop reading of the split is the computed one",
         (c1c[2], c1f[2]))
    c2f = cells[("cwq", "h2", False)]
    says(r"only on single-hop questions, \$([\d.]+)\$ against \$([\d.]+)\$, and "
         r"trails on two-hop, \$([\d.]+)\$ against \$([\d.]+)\$",
         "the finished-half stratum comparison is the computed one",
         (c1f[1], c1f[2], c2f[1], c2f[2]))

    # -- the hop-depth curve on CWQ, with its stratum sizes --
    hs = d["main_results"]["by_hop_stratum"]["cwq/agr"]
    says(r"\$([\d.]+)\$ at one hop, \$([\d.]+)\$ at two, \$([\d.]+)\$ at three "
         r"or more, over strata of \$(\d+)\$, \$(\d+)\$, and \$(\d+)\$",
         "the CWQ hop curve and its stratum sizes are the committed ones",
         (hs["h1"]["hits_at_1"], hs["h2"]["hits_at_1"], hs["h3plus"]["hits_at_1"],
          hs["h1"]["n"], hs["h2"]["n"], hs["h3plus"]["n"]))

    # -- wall-clock: the JSON's cold-cache means, and the cache share
    #    among the records those means are taken over --
    secs = {k: v["mean_seconds_cold_cache"] for k, v in by.items()}
    says(r"a mean of \$([\d.]+)\$ and \$([\d.]+)\$ per question for AGR against "
         r"\$([\d.]+)\$ and \$([\d.]+)\$ for the baseline, and between "
         r"\$([\d.]+)\$ and \$([\d.]+)\$ for the three single-call",
         "the wall-clock means are the JSON's cold-cache figures",
         (secs["webqsp/agr"], secs["cwq/agr"], secs["webqsp/tog"], secs["cwq/tog"],
          min(secs[f"{ds}/{s}"] for ds in ("webqsp", "cwq")
              for s in ("noretrieval", "vectorrag", "graphrag")),
          max(secs[f"{ds}/{s}"] for ds in ("webqsp", "cwq")
              for s in ("noretrieval", "vectorrag", "graphrag"))))
    shares = []
    for ds in ("webqsp", "cwq"):
        for s in ("tog", "agr"):
            recs = [json.loads(l) for l in
                    open(P4 / f"test_{ds}_{s}.jsonl", encoding="utf-8")]
            # score_test.py's "warm": a record replayed entirely from cache
            nw = [r for r in recs if not (r["budget"].get("cache_hits", 0)
                                          >= r["budget"]["llm_calls"] > 0)]
            shares.append(rnd(100 * sum(r["budget"].get("cache_hits", 0) for r in nw)
                              / sum(r["budget"]["llm_calls"] for r in nw), 1))
    says(r"between \$([\d.]+)\\%\$ and \$([\d.]+)\\%\$ of the two navigators' "
         r"calls in the remaining records",
         "the cache-share caveat quotes the measured range",
         (min(shares), max(shares)))

    # -- answers emitted with zero supporting triples --
    zt = {}
    for ds in ("webqsp", "cwq"):
        recs = [json.loads(l) for l in
                open(P4 / f"test_{ds}_agr.jsonl", encoding="utf-8")]
        ans = [r for r in recs if r["answer_entities"]]
        zt[ds] = (sum(1 for r in ans if not r.get("n_supporting_triples")), len(ans))
    says(r"\$(\d+)\$ of AGR's \$(\d+)\$ answered WebQSP questions and \$(\d+)\$ "
         r"of its \$(\d+)\$ on",
         "the zero-triple answer counts are the recorded ones",
         zt["webqsp"] + zt["cwq"])

    # -- the census population and its coverage, recomputed the way
    #    scripts/synthesize_census.py computes them. The questions in the
    #    population that no label file reaches must be exactly the Stage B
    #    near-misses (strict-match failures that normalisation scores as
    #    hits), which dump_failure_packets.py sets aside by design; the
    #    paragraph says so, and a genuinely unread failure would fail here --
    pop, read, aside, unread = {}, {}, {}, {}
    for ds in ("webqsp", "cwq"):
        recs = [json.loads(l) for l in
                open(P4 / f"test_{ds}_agr.jsonl", encoding="utf-8")]
        popn = {r["qid"] for r in recs if not _hit(r)} - set(excl[ds])
        labelled = set()
        for name in (f"labels_{ds}.csv", f"ablations/noplanner_categories_{ds}.csv"):
            p = P4 / name
            if p.exists():
                labelled |= {r["qid"] for r in
                             _csv.DictReader(open(p, encoding="utf-8"))
                             if r["category"] and r["kind"] in ("wrong", "hedge")}
        near = {r["qid"] for r in
                json.load(open(P4 / f"prepass_wrongs_{ds}.json", encoding="utf-8"))
                if r["near_miss"]}
        pop[ds], read[ds] = len(popn), len(popn & labelled)
        aside[ds] = len((popn - labelled) & near)
        unread[ds] = len(popn - labelled - near)
    says(r"number \$(\d+)\$: \$(\d+)\$ on WebQSP and \$(\d+)\$ on "
         r"ComplexWebQuestions",
         "the census population is the non-hits less the exclusions",
         (pop["webqsp"] + pop["cwq"], pop["webqsp"], pop["cwq"]))
    WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
            7: "seven", 8: "eight", 9: "nine"}
    m = re.search(r"(\w+) of them, (\w+) and (\w+), are the surface-form "
                  r"near-misses".replace(" ", r"\s+"), text)
    ck("the questions set aside are named as near-misses, with the right counts",
       m is not None and m.groups() == tuple(
           WORD[n].capitalize() if i == 0 else WORD[n]
           for i, n in enumerate((aside["webqsp"] + aside["cwq"],
                                  aside["webqsp"], aside["cwq"]))),
       f"paper {m.groups() if m else 'NO MATCH'}, computed "
       f"{(aside['webqsp'] + aside['cwq'], aside['webqsp'], aside['cwq'])}")
    ck("every question in the population that no label file reaches is a near-miss",
       unread["webqsp"] + unread["cwq"] == 0,
       f"{unread['webqsp'] + unread['cwq']} genuinely unread")
    says(r"remaining \$(\d+)\$, \$(\d+)\$ and \$(\d+)\$, was read and labelled",
         "the census coverage is the population less the near-misses set aside",
         (read["webqsp"] + read["cwq"], read["webqsp"], read["cwq"]))
    ck("the histogram totals equal the read count",
       sum(hist[ds][k]["_n"] for ds in ("webqsp", "cwq") for k in ("wrong", "hedge"))
       == read["webqsp"] + read["cwq"])
    echo = sum(hist[ds][k].get("echo", 0) for ds in ("webqsp", "cwq")
               for k in ("wrong", "hedge"))
    says(r"accounts for \$(\d+)\$ of the \$(\d+)\$ failures read",
         "the echo count and its denominator are the census's own",
         (echo, read["webqsp"] + read["cwq"]))
    says(r"hedges on them more than three times as often as it asserts something "
         r"wrong, \$(\d+)\$ against \$(\d+)\$",
         "the CWQ environment-gap hedge/wrong counts are the census's own",
         (hist["cwq"]["hedge"]["kg_gap"], hist["cwq"]["wrong"]["kg_gap"]))
    ck("'more than three times' is arithmetically true",
       hist["cwq"]["hedge"]["kg_gap"] > 3 * hist["cwq"]["wrong"]["kg_gap"])

    # -- the consensus breakdown: every cell of tab:consensus and the
    #    sentences that read it, from the pre-pass rows --
    cons = {}
    for ds in ("webqsp", "cwq"):
        rows = json.load(open(P4 / f"prepass_goldnoise_{ds}.json", encoding="utf-8"))
        ok = [r for r in rows if r["verdict"] == "gold_ok"]
        fam = {}
        for r in ok:
            fam[r.get("family")] = fam.get(r.get("family"), 0) + 1
        echo_rows = [r for r in ok if r.get("family") == "echo"]
        cons[ds] = {
            "rows": len(ok), "questions": len({r["qid"] for r in ok}),
            "echo": fam.get("echo", 0), "relation": fam.get("relation_selection", 0),
            "constraint": fam.get("composite_claim", 0), "kg_gap": fam.get("kg_gap", 0),
            "ctrl": sum(1 for r in ok if "noretrieval" in r["systems"]),
            "navs": sum(1 for r in ok if {"agr", "tog"} <= set(r["systems"])),
            "echo_ctrl": sum(1 for r in echo_rows if "noretrieval" in r["systems"]),
            "echo_navs": sum(1 for r in echo_rows if {"agr", "tog"} <= set(r["systems"])),
            "five_ok": sum(1 for r in rows if r["n_systems"] == 5 and r["verdict"] == "gold_ok"),
            "five_all": sum(1 for r in rows if r["n_systems"] == 5),
        }
    TABLE = (("Consensus rows cleared as not a label defect", "rows"),
             (r"\\quad filed as echo attractor", "echo"),
             (r"\\quad filed as relation confusion", "relation"),
             (r"\\quad filed as constraint ignored", "constraint"),
             (r"\\quad filed as environment gap", "kg_gap"),
             ("Rows on which the no-retrieval control agrees", "ctrl"),
             ("Rows on which both navigators agree", "navs"),
             ("Echo rows on which the no-retrieval control agrees", "echo_ctrl"),
             ("Echo rows on which both navigators agree", "echo_navs"))
    for lead, key in TABLE:
        m = re.search(lead.replace(" ", r"\s+") + r"\s*&\s*(\d+)\s*&\s*(\d+)\s*\\\\", text)
        got = tuple(int(g) for g in m.groups()) if m else None
        want = (cons["webqsp"][key], cons["cwq"][key])
        ck(f"tab:consensus row '{key}' = {want}", got == want, f"table {got or 'NO ROW'}")
    cleared_q = cons["webqsp"]["questions"] + cons["cwq"]["questions"]
    # Whitespace-tolerant for the same reason as the verifier-arm check
    # above: the 72-column fill can break "cleared / questions", and a
    # plain substring test then reports a sentence that is present.
    ck("the cleared-question count equals flagged minus confirmed",
       cleared_q == flagged - confirmed
       and re.search(rf"\${cleared_q}\$\s+cleared\s+questions", text) is not None,
       f"{flagged} - {confirmed} = {flagged - confirmed}; pre-pass {cleared_q}")
    says(r"filed \$(\d+)\$ of the \$(\d+)\$ cleared rows as the echo mechanism",
         "the echo share of cleared rows is the pre-pass's own",
         (cons["webqsp"]["echo"] + cons["cwq"]["echo"],
          cons["webqsp"]["rows"] + cons["cwq"]["rows"]))
    says(r"on \$(\d+)\$ of the \$(\d+)\$ cleared rows and on \$(\d+)\$ of the "
         r"\$(\d+)\$ echo rows",
         "the CWQ control-participation sentence is the pre-pass's own",
         (cons["cwq"]["ctrl"], cons["cwq"]["rows"], cons["cwq"]["echo_ctrl"], cons["cwq"]["echo"]))
    says(r"the control joins \$(\d+)\$ of \$(\d+)\$ rows and \$(\d+)\$ of \$(\d+)\$ "
         r"echo rows, and the two navigators agree with each other on \$(\d+)\$ "
         r"of the \$(\d+)\$",
         "the WebQSP participation sentence is the pre-pass's own",
         (cons["webqsp"]["ctrl"], cons["webqsp"]["rows"], cons["webqsp"]["echo_ctrl"],
          cons["webqsp"]["echo"], cons["webqsp"]["echo_navs"], cons["webqsp"]["echo"]))
    says(r"Of the \$(\d+)\$ rows on which all five systems agreed, \$(\d+)\$ were "
         r"cleared",
         "the five-system rows are counted from the pre-pass",
         (cons["webqsp"]["five_all"] + cons["cwq"]["five_all"],
          cons["webqsp"]["five_ok"] + cons["cwq"]["five_ok"]))
    ck("the paper no longer calls the attractor a property of the graph alone",
       not re.search(r"property of the graph's neighbourhood structure rather than",
                     text))

    # -- the verification ablation is described as removing the CHECKING,
    #    with the drafting call unchanged (agr/nodes.py: verify_claims=False
    #    returns after the draft) --
    ck("the no-verification condition is described as draft-unchanged",
       re.search(r"leaving\s+the\s+drafting\s+call\s+unchanged", text) is not None
       and re.search(r"leaves\s+the\s+drafting\s+call\s+unchanged", text) is not None)

    print("\n== derived analyses of September 2026 (scripts/paper_analyses.py) ==")
    # Computed from the committed logs and the RoG distribution's published
    # subgraphs; nothing here ran a system. Each figure is pinned to the
    # sentence or table cell that quotes it.
    sys.path.insert(0, str(ROOT / "scripts"))
    import paper_analyses as pa

    # pa.gold_path_discards() (the baseline's 40-row cut read against the
    # gold path) is computed but NOT reported: the user chose on
    # 2026-09-18 to keep the paper's reading of sec:margin identical to the
    # thesis's, so nothing in the text quotes it and nothing here pins it.
    ck("sec:margin keeps the thesis's reading (no gold-path discard table)",
       "togdiscard" not in text and not re.search(r"neither\s+binds", text))

    # paired bootstrap intervals in tab:ablation, and the discordant union
    bs = {ds: pa.ablation_bootstrap(ds) for ds in ("webqsp", "cwq")}
    LABEL = {"noplanner": "Planner", "nobacktrack": "Backtracking",
             "noverifier": "Verification", "embonly": "Model scoring"}
    def _sgn(x):
        return f"{x:+.3f}"
    for cond, label in LABEL.items():
        m = re.search(label + r"\s*&\s*\$[+-]?[\d.]+\$\s*&\s*\$\[([+-][\d.]+), ([+-][\d.]+)\]\$"
                      r"\s*&\s*(?:\\textbf\{)?[\d.]+\}?\s*&\s*\$[+-]?\d+\\%\$"
                      r"\s*&\s*\$[+-]?[\d.]+\$\s*&\s*\$\[([+-][\d.]+), ([+-][\d.]+)\]\$",
                      text)
        got = tuple(m.groups()) if m else None
        lo_w, hi_w = bs["webqsp"][cond]["ci95"]
        lo_c, hi_c = bs["cwq"][cond]["ci95"]
        want = (_sgn(rnd(lo_w)), _sgn(rnd(hi_w)), _sgn(rnd(lo_c)), _sgn(rnd(hi_c)))
        ck(f"tab:ablation bootstrap interval for {label} = {want}",
           got == want, f"table {got or 'NO ROW'}")
    says(r"holds \$(\d+)\$ of the \$(\d+)\$ WebQSP questions and \$(\d+)\$ of the "
         r"\$(\d+)\$ on ComplexWebQuestions. On the remaining \$(\d+)\$ and \$(\d+)\$",
         "the discordant union and its complement are the computed ones",
         (bs["webqsp"]["discordant_union"], bs["webqsp"]["n"],
          bs["cwq"]["discordant_union"], bs["cwq"]["n"],
          bs["webqsp"]["n"] - bs["webqsp"]["discordant_union"],
          bs["cwq"]["n"] - bs["cwq"]["discordant_union"]))
    excl_zero = [(ds, cond) for ds in ("webqsp", "cwq") for cond in LABEL
                 if not (bs[ds][cond]["ci95"][0] <= 0 <= bs[ds][cond]["ci95"][1])]
    ck("only the planner's WebQSP interval excludes zero",
       excl_zero == [("webqsp", "noplanner")], str(excl_zero))

    # the development-set sweep, hits at tau = 0.20
    sw = pa.dev_sweep_hits()
    says(r"it scored \$(\d+)\$, \$(\d+)\$, \$(\d+)\$, and \$(\d+)\$ hits of \$80\$ "
         r"at \$\\alpha = 0\.3\$, \$0\.5\$, \$0\.7\$, and \$1\.0\$",
         "the sweep's hits are the phase-3 score log's",
         (sw[0.3], sw[0.5], sw[0.7], sw[1.0]))
    ck("dropping the model term cost five hits on the development set",
       sw[0.7] - sw[1.0] == 5 and re.search(r"cost\s+five\s+hits", text) is not None)

    print("\n== unbound literals in prose (read these) ==")
    accounted = {str(v) for v in bound.values()} | {
        str(v) for v in clip.values()} | {
        "400", "262", "256", "57", "2.59", "8.31", "0.083", "0.006", "31", "1",
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
