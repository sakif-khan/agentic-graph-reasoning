"""Check every number typed into presentation.tex against its source.

The three data figures are \\input from thesis_book/figures/ and need no
checking -- scripts/build_figures.py generates them from the same JSON. This
script covers the numbers that appear as table text or prose in the deck,
which are transcribed and can therefore drift.

Run from anywhere:  python thesis_presentation/check_slides.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NUMS = os.path.join(ROOT, "results", "phase4", "thesis_numbers.json")
# Both decks share a preamble, so all three files are read together: a figure
# quoted on a backup slide is as much a transcription as one on a main slide.
SOURCES = ["preamble.tex", "content-main.tex", "content-backup.tex"]
DRIVERS = ["pre-defense-0421052099.tex", "pre-defense-0421052099-backup.tex"]

J = json.load(open(NUMS, encoding="utf-8"))
TEX = "\n".join(open(os.path.join(HERE, f), encoding="utf-8").read()
                for f in SOURCES)
FLAT = " ".join(TEX.split())
ok = True


def ck(label, cond, detail=""):
    global ok
    print(f"  [{'OK ' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    ok &= bool(cond)


def has(s):
    """Is this literal present in the deck, ignoring LaTeX thousands markers?"""
    return s in FLAT or s.replace(",", "{,}") in FLAT


print("== main results table ==")
B = J["main_results"]["by_system"]
NAME = {"noretrieval": "No-retrieval", "vectorrag": "Vector RAG",
        "graphrag": "Static GraphRAG", "tog": "Think-on-Graph", "agr": "AGR"}
for s, label in NAME.items():
    for ds in ("webqsp", "cwq"):
        r = B[f"{ds}/{s}"]
        for metric in ("hits_at_1", "f1"):
            v = f"{r[metric]:.3f}"
            ck(f"{label:15s} {ds:6s} {metric:9s} = {v}", has(v))

print("\n== cost figures quoted on the results slide ==")
for ds, s, tok, calls in (("webqsp", "noretrieval", 113, 1.0),
                          ("webqsp", "vectorrag", 527, 1.0),
                          ("webqsp", "graphrag", 531, 1.0),
                          ("webqsp", "tog", 3615, 12.8),
                          ("webqsp", "agr", 4511, 6.2),
                          ("cwq", "tog", 5572, 18.2),
                          ("cwq", "agr", 6818, 8.9)):
    r = B[f"{ds}/{s}"]
    ck(f"{ds}/{s} tokens {tok}", r["mean_tokens"] == tok, str(r["mean_tokens"]))
    ck(f"{ds}/{s} calls {calls}", r["mean_calls"] == calls, str(r["mean_calls"]))
    ck(f"{ds}/{s} tokens appear in deck", has(f"{tok:,}"))

print("\n== hedge rates (backup slide) ==")
for s, label in NAME.items():
    for ds in ("webqsp", "cwq"):
        v = f"{B[f'{ds}/{s}']['hedge_pct']:.1f}"
        ck(f"{label:15s} {ds:6s} hedge {v}", has(v))

# A hedge rate is a refusal to assert. Presence alone does not say the deck
# calls it that, and for one release it did not: slide 15 read "AGR hedges
# on 8.2% of WebQSP against no-retrieval's 12.2% error rate". 12.2 is
# no-retrieval's hedge_pct -- backup slide 5 prints it under "WebQSP hedge
# %" -- and its error rate is 170 wrong out of the 351 it asserts on. The
# check above passed the whole time, because 12.2 was indeed present.
#
# Worse than the label: hedge against hedge is 8.2 < 12.2, so the sentence
# meant to show verification converting error into abstention showed AGR
# abstaining LESS than the unverified control, and contradicted the thesis
# sentence that calls 8.2% "the lowest of the five systems".
print("\n== hedge rates are not called error rates ==")
MISLABEL = re.compile(r"(?:error|wrong|accuracy|hallucination)\s+rate")
for s, label in NAME.items():
    for ds in ("webqsp", "cwq"):
        v = f"{B[f'{ds}/{s}']['hedge_pct']:.1f}"
        near = []
        for m in re.finditer(re.escape(v), FLAT):
            window = FLAT[m.start():m.end() + 60]
            if MISLABEL.search(window):
                near.append(window[:70])
        ck(f"{label:15s} {ds:6s} hedge {v} not labelled an error rate",
           not near, near[0] if near else "")

# The one comparison that isolates the verification layer, quoted on slide
# 15. Bound to the sentence rather than to the four values appearing
# somewhere: each is also a cell in the ablation table on another slide.
print("\n== verifier hedge deltas (slide 15) ==")
AB = J["ablations"]["by_condition"]
for ds, name in (("cwq", "CWQ"), ("webqsp", "WebQSP")):
    full = f"{AB[f'{ds}/half_abl_full']['hedge_pct']:.1f}"
    none = f"{AB[f'{ds}/half_abl_noverifier']['hedge_pct']:.1f}"
    pat = re.compile(rf"\${re.escape(full)}\\%\s*\\to\s*{re.escape(none)}"
                     rf"\\%\$\s*on\s*{name}")
    ck(f"{name:6s} verifier hedge {full} -> {none} stated as such",
       bool(pat.search(FLAT)), f"{full} -> {none}")
    ck(f"{name:6s} removing the verifier lowers hedging",
       float(none) < float(full), f"{full} vs {none}")

print("\n== ablation table ==")
A = J["ablations"]["by_condition"]
COND = {"full": "Full system", "noplanner": "No planner",
        "nobacktrack": "No backtracking", "noverifier": "No verifier",
        "embonly": "Embedding-only"}
for c, label in COND.items():
    for ds in ("webqsp", "cwq"):
        v = f"{A[f'{ds}/half_abl_{c}']['f1']:.3f}"
        ck(f"{label:16s} {ds:6s} F1 {v}", has(v))
for c in ("full", "noplanner", "nobacktrack", "noverifier", "embonly"):
    t = A[f"webqsp/half_abl_{c}"]["mean_tokens"]
    ck(f"webqsp {c:12s} tokens {t}", has(f"{t:,}"))

print("\n== McNemar p-values ==")
P = {(m["dataset"], m["system_b"].replace("half_abl_", "")): m["p"]
     for m in J["ablations"]["mcnemar_vs_full"]}
for (ds, c), p in sorted(P.items()):
    shown = f"{p:.3f}"
    ck(f"{ds:6s} vs {c:12s} p={p} shown as {shown}", has(shown), f"raw {p}")

print("\n== planner effect quoted in prose ==")
d_wq = A["webqsp/half_abl_noplanner"]["f1"] - A["webqsp/half_abl_full"]["f1"]
d_cwq = A["cwq/half_abl_noplanner"]["f1"] - A["cwq/half_abl_full"]["f1"]
ck(f"WebQSP planner delta +{d_wq:.3f}", has(f"{d_wq:.3f}"), f"{d_wq:+.3f}")
ck(f"CWQ planner delta {d_cwq:.3f}", has(f"{abs(d_cwq):.3f}"), f"{d_cwq:+.3f}")
tf, tn = (A["webqsp/half_abl_full"]["mean_tokens"],
          A["webqsp/half_abl_noplanner"]["mean_tokens"])
cut = round(100 * (tf - tn) / tf)
ck(f"token cut {cut}% ", has(f"{cut}\\%"), f"{100*(tf-tn)/tf:.1f}%")
ck("call drop 6.2 -> 4.0",
   A["webqsp/half_abl_full"]["mean_calls"] == 6.2
   and A["webqsp/half_abl_noplanner"]["mean_calls"] == 4.0)

print("\n== Think-on-Graph budget split ==")
T = J["tog_budget_split"]
for ds in ("webqsp", "cwq"):
    d = T[ds]
    for blk in ("tog_finished", "tog_clipped"):
        for k in ("tog_hits_at_1", "agr_hits_at_1"):
            v = f"{d[blk][k]:.3f}"
            ck(f"{ds:6s} {blk:12s} {k:14s} {v}", has(v))
    ck(f"{ds} clip n {d['tog_clipped']['n']}", has(str(d["tog_clipped"]["n"])))
    ck(f"{ds} clip rate {d['tog_clip_rate']*100:.1f}%",
       has(f"{d['tog_clip_rate']*100:.1f}\\%"))

print("\n== groundedness, pooled over both datasets ==")
G = J["groundedness_tier1_structural"]
for s, label in NAME.items():
    a = sum(G[f"test_{d}_{s}"]["entities_asserted"] for d in ("webqsp", "cwq"))
    u = sum(G[f"test_{d}_{s}"]["entities_ungrounded"] for d in ("webqsp", "cwq"))
    pct = f"{100 * u / a:.1f}"
    ck(f"{label:15s} asserted {a:,}", has(f"{a:,}"))
    ck(f"{label:15s} ungrounded {u}", has(str(u)) if u else True)
    ck(f"{label:15s} rate {pct}%", has(f"{pct}\\%"))

print("\n== budget binding (backup slide) ==")
BB = J["budget_binding"]
for key, label in (("depth", "depth"), ("backtracks", "backtrack"),
                   ("verify_iters", "verify"), ("llm_calls", "call")):
    for pop in ("webqsp", "cwq", "both"):
        v = f"{BB[pop][key]['refused_pct']:.1f}"
        ck(f"{label:10s} {pop:6s} {v}%", has(f"{v}\\%"))

print("\n== test sets and environment ==")
for ds in ("webqsp", "cwq"):
    t = J["test_sets"][ds]
    ck(f"{ds} n_questions 400", t["n_questions"] == 400)
    ck(f"{ds} gold median {t['gold_median']}", has(f"{t['gold_median']:.1f}"))
    ck(f"{ds} reachable {t['reachable_pct']}%",
       has(f"{t['reachable_pct']:.1f}\\%"))
    multi = t["strata"]["h2"] + t["strata"]["h3plus"]
    ck(f"{ds} multi-hop {multi}", has(str(multi)))
ck("WebQSP h3plus is 4 (quoted as a limitation)",
   J["test_sets"]["webqsp"]["strata"]["h3plus"] == 4)

print("\n== benchmark defects ==")
D = J["benchmark_defects"]
for k in ("excluded_before_census", "census_rows_in_defect_categories",
          "distinct_questions"):
    ck(f"{k} = {D[k]}", has(str(D[k])))
ck("41 + 17 - 1 = 57",
   D["excluded_before_census"] + D["census_rows_in_defect_categories"]
   - len(D["counted_in_both"]) == D["distinct_questions"])

print("\n== failure census total ==")
H = J["failure_histogram"]
total = sum(H[d][k]["_n"] for d in ("webqsp", "cwq") for k in ("wrong", "hedge"))
ck(f"census total {total}", total == 259 and has("259"), str(total))

print("\n== deck hygiene ==")
# body text must not shrink below \small. Font sizes set inside a TikZ/pgfplots
# style declaration (font=\scriptsize) label a diagram, not prose, so strip
# those before looking.
body = re.sub(r"font=\\\w+", "", TEX)
body = re.sub(r"agrplot/\.style=\{.*?\}\}", "", body, flags=re.S)
ck("no body text smaller than \\small",
   not re.search(r"\\(footnotesize|scriptsize|tiny)\b", body),
   (re.search(r".{0,50}\\(footnotesize|scriptsize|tiny).{0,30}", body)
    or [""])[0])
ck("aspect ratio is 16:9", "aspectratio=169" in TEX)
ck("base font is 12pt", "12pt]{beamer}" in TEX)

# Body text is justified, and it takes both hooks: \raggedright covers prose,
# columns and lists, while a block body is a beamercolorbox that sets
# \rightskip from its own key and needs the template hook. Losing either one
# silently un-justifies part of the deck, which is exactly the defect this
# deck was corrected for.
PRE = open(os.path.join(HERE, "preamble.tex"), encoding="utf-8").read()
ck("prose, columns and lists are justified",
   r"\let\raggedright\justifying" in PRE)
ck("block bodies are justified too (beamercolorbox needs its own hook)",
   r"\addtobeamertemplate{block begin}{}{\justifying}" in PRE)
ck("table cells kept ragged: L is bound before \\raggedright is repointed",
   PRE.index(r"\let\agrraggedright\raggedright") < PRE.index(r"\newcolumntype{L}")
   and r"{>{\agrraggedright\arraybackslash}p{#1}}" in PRE)
ck("the accepted looseness is stated, not left open",
   re.search(r"\\hbadness=(\d+)", PRE) is not None
   and int(re.search(r"\\hbadness=(\d+)", PRE).group(1)) <= 2000,
   (re.search(r"\\hbadness=\d+", PRE) or [""])[0])
for drv in DRIVERS:
    ck(f"{drv} exists and shares the preamble",
       os.path.exists(os.path.join(HERE, drv))
       and r"\input{preamble}" in open(os.path.join(HERE, drv),
                                       encoding="utf-8").read())
ck("no backup slide leaked into the presented deck",
   "Backup:" not in open(os.path.join(HERE, "content-main.tex"),
                         encoding="utf-8").read())

# The three data figures have slide-geometry variants under figures/; the claim
# path is hand-drawn and shared with the thesis, so it is read from there.
slide_figs = re.findall(r"\\input\{figures/([\w.]+)\}", TEX)
book_figs = re.findall(r"\\input\{\.\./thesis_book/figures/([\w.]+)\}", TEX)
ck(f"three generated figures come from figures/: {sorted(slide_figs)}",
   sorted(slide_figs) == ["fig_accuracy_cost.tex", "fig_failure_histogram.tex",
                          "fig_hop_strata.tex"])
ck(f"the hand-drawn one is shared with the book: {book_figs}",
   book_figs == ["fig_claim_path.tex"])
for f in slide_figs:
    p = os.path.join(HERE, "figures", f)
    ck(f"  {f} exists", os.path.exists(p))
    ck(f"  {f} is generated, not hand-edited",
       "GENERATED by scripts/build_figures.py"
       in open(p, encoding="utf-8").read())
for f in book_figs:
    ck(f"  {f} exists",
       os.path.exists(os.path.join(ROOT, "thesis_book", "figures", f)))
ck("slide figures are colourised, not greyscale",
   all("black!55" not in open(os.path.join(HERE, "figures", f),
                              encoding="utf-8").read() for f in slide_figs))

print("\n== build logs ==")
# Warnings were being counted by grepping for the literal "LaTeX Warning",
# which is one class out of several: a "Package hyperref Warning" about \quad
# reaching the PDF metadata sat in a build reported as clean for two rounds.
# Match every class instead.
#
# Underfull needs no threshold here -- the preamble sets \hbadness, so a line
# only reaches the log if it is looser than the ceiling declared there.
# Three details, each learned from a false result:
#   [Ww]arning  - pdfTeX spells its own lowercase.
#   (?!:)       - "Package: infwarerr ... Providing info/warning" is a package
#                 identification line, not a warning. A real one has no colon
#                 after the leading keyword.
#   trailing :  - every genuine warning reads "Warning:" or "warning (ext4):",
#                 which keeps the word from matching inside running prose.
WARNING = re.compile(
    r"^(?:Package|Class|LaTeX|pdfTeX)(?!:)[^\n]*?\b[Ww]arning\b[^:\n]*:", re.M)
for drv in DRIVERS:
    log = os.path.join(HERE, os.path.splitext(drv)[0] + ".log")
    if not os.path.exists(log):
        print(f"  [   ] {drv}: no build log to read -- run latexmk first")
        continue
    t = open(log, encoding="utf-8", errors="replace").read()
    ck(f"{drv}: no overfull boxes", "Overfull" not in t)
    ck(f"{drv}: nothing looser than the badness ceiling",
       "Underfull" not in t)
    hits = WARNING.findall(t)
    ck(f"{drv}: no warnings, of any class", not hits,
       "; ".join(sorted(set(hits))))

# ---------------------------------------------------------------------
# The deck's six contributions must be the thesis's six.
#
# They were not. sec:contribution has one \subsection per contribution;
# the deck had split the framework and its verification layer into two
# items, promoted the five-system comparison and the hop-count shape from
# results to contributions, and dropped the ablation, the decomposition
# finding and the protocol -- while both lists said "six". Only two mapped.
# 49a85cb had already audited this inside the thesis, where the conclusion
# counted four; nothing was holding the deck to the same standard.
#
# Held to the thesis rather than to a list repeated here, so adding a
# seventh contribution to sec:contribution fails this until the deck says
# so. The keys are alternatives per contribution, not a spelling test, and
# they are matched inside the contributions block alone -- "echo attractor"
# also appears on slide 19, and matching the whole deck would pass a slide
# that had dropped it.
print("\n== the deck's contributions are the thesis's ==")
INTRO = os.path.join(ROOT, "thesis_book", "chapters", "introduction.tex")
CONTRIB_KEYS = [
    ("framework / verification layer", ("verification layer",)),
    ("component-level ablation", ("component-level ablation",)),
    ("stratum-dependent decomposition", ("stratum-dependent",)),
    ("echo attractor", ("echo attractor",)),
    ("benchmark defect rates", ("benchmark-defect", "benchmark defect")),
    ("pre-specified protocol", ("pre-specified", "pre-registered")),
]


def block(after, environment):
    """The one list environment following a marker in the deck source."""
    i = FLAT.find(after)
    if i < 0:
        return ""
    m = re.search(r"\\begin\{" + environment + r"\}(.*?)\\end\{"
                  + environment + r"\}", FLAT[i:])
    return m.group(1) if m else ""


intro = open(INTRO, encoding="utf-8").read()
start = intro.index(r"\section{Our Contribution}")
end = intro.index(r"\section", start + 10)
claimed = re.findall(r"\\subsection\{", intro[start:end])
contrib = block(r"\textbf{Contributions}", "enumerate").lower()
# \itemsep is not an \item. Counting it made a six-item list read as seven.
listed = re.findall(r"\\item(?![a-zA-Z])", contrib)

ck(f"thesis claims {len(claimed)} contributions, deck lists {len(listed)}",
   len(claimed) == len(listed) == len(CONTRIB_KEYS),
   f"{len(claimed)} vs {len(listed)}")
for label, keys in CONTRIB_KEYS:
    ck(f"contribution present: {label}",
       any(k in contrib for k in keys))

# Every limitation on the slide answers to a heading in the thesis's
# ordered list. "ToG leads on the questions it finishes" stood alone here
# and is not one of them; the thesis's item is the candidate-width
# confound, which is the caveat on that disclosure.
print("\n== the deck's limitations are the thesis's ==")
LIMIT_KEYS = ("rejects", "detectable accuracy", "navigation",
              "candidate set", "one environment")
limits = block(r"\textbf{Limitations I state plainly}", "itemize").lower()
for key in LIMIT_KEYS:
    ck(f"limitation present: {key}", key in limits)
ck("the first-ranked limitation leads the list",
   limits.find("rejects") >= 0
   and all(limits.find("rejects") < limits.find(k)
           for k in LIMIT_KEYS if k != "rejects" and k in limits))

# The fairness slide may not deny a confound the thesis lists.
#
# It read: differences are attributable to architecture, "not to model
# capacity or to a bigger retrieval budget". No source document claims
# that. The thesis abstract claims only "architecture, not model capacity";
# setup.tex Sec 7.4.3 names the candidate widths as one of two things
# deliberately NOT held constant and as "where a reader should look first
# for a confound"; and it is limitation #5 in sec:limitations-final. The
# denial sat on the slide titled "Making the comparison fair", with the
# widths named nowhere on it -- and it bought nothing, because a narrower
# candidate set is cheaper and so cuts against the baseline, not for it.
#
# Bound to the attribution clause rather than to the phrase: what is wrong
# is denying a confound, and a rewrite that denies a different one ("the
# same candidate sets") is the same defect.
print("\n== the fairness slide does not deny a stated confound ==")
MD = open(os.path.join(HERE, "transcript.md"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(HERE, "transcript.md")) else ""
DENIED = (r"(?:retrieval budget|bigger retrieval|retrieval width"
          r"|candidate (?:set|width)s?|same candidates?)")
OVERCLAIM = re.compile(
    r"attribut\w+[^.]{0,140}?\b(?:not|rather than)\b[^.]{0,140}?" + DENIED,
    re.I)


def frame(title):
    """The one frame with this title, from \\begin{frame} to \\end{frame}."""
    m = re.search(r"\\begin\{frame\}\{" + re.escape(title) + r"\}(.*?)"
                  r"\\end\{frame\}", FLAT)
    return m.group(1) if m else ""


fair = frame("Making the comparison fair")
ck("the fairness frame is in the deck", bool(fair))
for label, text in (("deck", FLAT), ("transcript", MD)):
    hit = OVERCLAIM.search(text)
    ck(f"{label} does not deny the candidate-width confound",
       hit is None, hit.group(0)[:88] if hit else "")

# Disclosing it is not enough if the disclosure invites the wrong
# inference: a reader who learns the widths differ and nothing else will
# assume the confound could explain the clipping. It cannot -- thinner is
# cheaper -- and the slide has to say which way it cuts.
ck("the fairness frame names what is not held equal",
   re.search(r"not\}? held equal", fair, re.I) is not None)
ck("and says which way the difference cuts",
   "cheaper" in fair.lower() and "lower bound" in fair.lower(),
   "a narrower set cannot explain the clipping; it bounds the unclipped score")
ck("the transcript answers the sharp form of the cap question",
   re.search(r"same candidate sets\?", MD, re.I) is not None,
   'anticipated questions must carry "did both systems see the same '
   'candidate sets?"')

# That answer quotes five measured figures, and a spoken figure is as much
# a transcription as one on a slide. Bound to the sentence rather than
# matched loose: 3.3 and 1,651 both have other homes in this repository,
# and "does the number appear" is how the hedge-rate mislabel survived.
MDF = " ".join(MD.split())
CC = J["candidate_caps"]
m = re.search(r"the (\d+)-relation cut binds on ([\d.]+) percent of the "
              r"([\d,]+) entities it expanded and the (\d+)-neighbour cut on "
              r"([\d.]+) percent of its neighbour calls; AGR's relation cap "
              r"binds once in ([\d,]+) expansions and its neighbour cap on "
              r"([\d.]+) percent", MDF)
ck("the transcript states the binding rates", m is not None,
   "the anticipated-questions answer must give them in one sentence")
if m:
    got = [int(m.group(1)), float(m.group(2)), int(m.group(3).replace(",", "")),
           int(m.group(4)), float(m.group(5)),
           int(m.group(6).replace(",", "")), float(m.group(7))]
    want = [CC["tog"]["relation_cap"],
            CC["tog"]["entities_at_relation_cap_pct"],
            CC["tog"]["entities_expanded"],
            CC["tog"]["neighbor_cap"],
            CC["tog"]["neighbor_calls_at_cap_pct"],
            CC["agr"]["entities_expanded"],
            CC["agr"]["neighbor_calls_at_cap_pct"]]
    ck("and they are the measured ones", got == want, f"{got} vs {want}")
    # "binds once" is a word, not a number, so nothing above would catch it
    # drifting away from the measured count of 1.
    ck("AGR's relation cap is described as binding once",
       CC["agr"]["entities_at_relation_cap"] == 1,
       f"measured {CC['agr']['entities_at_relation_cap']}, transcript says once")

# The transcript ranks this limitation. An ordinal typed into a script is a
# transcription like any other, and the thesis's list is the source.
CONC = os.path.join(ROOT, "thesis_book", "chapters", "conclusion.tex")
conc = open(CONC, encoding="utf-8").read()
i = conc.index(r"\section{Limitations}")
heads = re.findall(r"\\textbf\{([^}]*)\}", conc[i:conc.index(r"\section", i + 10)])
rank = next((n for n, h in enumerate(heads, 1)
             if "narrower candidate set" in " ".join(h.split())), None)
ck("the thesis ranks the candidate-width limitation", rank is not None)
if rank:
    stated = set(re.findall(r"limitation (\d+)", MDF))
    ck(f"the transcript calls it limitation {rank}",
       stated == {str(rank)}, f"transcript says {sorted(stated) or 'nothing'}")

# ---------------------------------------------------------------------
# The deck may not make a claim the paper retracted.
#
# The script pooled the two static baselines on CWQ -- "vector RAG and
# GraphRAG ... 0.203 and 0.205, below the no-retrieval control at 0.307.
# On genuinely multi-hop questions, single-shot retrieval is worse than
# not retrieving at all" -- on the slide marked "Slow down here". The
# thesis refuses that pooling in the same paragraph as the numbers:
# GraphRAG's CWQ figure "is the weaker evidence of the two: it confounds
# the paradigm with the radius ... The claim rests on the first
# baseline", which is Vector-RAG, whose single verbalised triple cannot
# contain a chain at any radius. The paper retracted it outright, in two
# commits titled "Paper: retract the GraphRAG paradigm claim".
#
# Bound per sentence, not per window. A distance rule cannot tell the
# pooled claim from the sentence that disowns it -- both name GraphRAG
# within a few words of the numbers -- and the sentence splitter has to
# leave decimals alone, which "0.203" and "0.205" would otherwise break.
print("\n== the GraphRAG paradigm claim stays retracted ==")


def sents(text):
    """Sentences, splitting only on periods that end one.

    A decimal point is always followed by a digit and never by a space,
    so this never cuts 0.203 in half -- which a plain [^.] window does,
    silently truncating the very defect this is meant to catch.
    """
    return re.split(r"\.(?=\s|$)", text)


def plain(text):
    """Drop markdown emphasis and quote markers before matching prose.

    The shipped sentence read "*below* the no-retrieval control", and a
    rule spelled "below the no-retrieval" does not match that. The probe
    still reported CAUGHT, on a different check -- which is how a rule
    that never fires looks from the outside.
    """
    return " ".join(re.sub(r"[*`>]", "", text).split())


POOLED = re.compile(r"vector[\s-]*RAG\s+and\s+(?:static\s+)?GraphRAG"
                    r"|(?:static\s+)?GraphRAG\s+and\s+vector[\s-]*RAG", re.I)
CLAIM = re.compile(r"below the no-retrieval|worse than not retrieving"
                   r"|worse than no retrieval", re.I)
for label, text in (("deck", plain(FLAT)), ("transcript", plain(MDF))):
    pooled = [s for s in sents(text) if CLAIM.search(s) and POOLED.search(s)]
    ck(f"{label} never pools the two static baselines under the claim",
       not pooled, pooled[0].strip()[:80] if pooled else "")
    credited = [s for s in sents(text)
                if re.search(r"worse than not retrieving", s, re.I)
                and re.search(r"GraphRAG", s, re.I)]
    ck(f"{label} never credits GraphRAG with the paradigm claim",
       not credited, credited[0].strip()[:80] if credited else "")


def spoken(n):
    """The quoted lines of one transcript section, without the markers."""
    m = re.search(rf"^## {n} [^\n]*$(.*?)(?=^## |\Z)", MD, re.S | re.M)
    return plain(" ".join(l for l in m.group(1).splitlines()
                          if l.startswith(">"))) if m else ""


# Retracting it is only half the job: the table puts 0.203 and 0.205 next
# to each other, so the script has to say which baseline carries the claim
# and why the other does not, or the audience pools them anyway.
#
# Bound to what is actually said on slide 11, not to the whole file. The
# first version searched the transcript and passed while section 11 had
# been stripped of it, because the speaker note below the section quotes
# the same phrase -- a second home, again.
s11 = spoken(11)
ck("section 11 is in the transcript", bool(s11))
ck("section 11 names the baseline the claim rests on",
   re.search(r"claim rests on vector RAG", s11, re.I) is not None)
ck("and says why GraphRAG's number does not carry it",
   re.search(r"radius confounds", s11, re.I) is not None)

# The deck's caveat is correct only while the thesis holds that position.
RES = os.path.join(ROOT, "thesis_book", "chapters", "results.tex")
res = " ".join(open(RES, encoding="utf-8").read().split())
ck("the thesis still refuses the pooling",
   "weaker evidence of the two" in res
   and "claim rests on the first baseline" in res,
   "sec:cwq-results is what the deck's caveat answers to")

# The strata the answer quotes are the figure's own, and the figure is
# generated from thesis_numbers.json by scripts/build_figures.py.
FIG = os.path.join(ROOT, "thesis_book", "figures", "fig_hop_strata.tex")
fig = open(FIG, encoding="utf-8").read()
for title, hop, want_label in (("WebQSP", 1, "WebQSP two-hop"),
                               ("ComplexWebQuestions", 1, "CWQ two-hop")):
    axis = next((a for a in fig.split(r"\begin{axis}")
                 if f"title={{{title}}}" in a), "")
    m = re.search(r"color=agrGraph[^\n]*coordinates \{([^}]*)\}", axis)
    pt = re.search(rf"\({hop},([\d.]+)\)", m.group(1)) if m else None
    ck(f"the figure gives GraphRAG's {want_label} stratum", pt is not None)
    if pt:
        ck(f"the script quotes {want_label} = {pt.group(1)}",
           re.search(rf"{re.escape(pt.group(1))}[^.]{{0,60}}?"
                     rf"{'WebQSP' if title == 'WebQSP' else 'CWQ'}", MDF)
           is not None, f"figure says {pt.group(1)}")

# The second bound on that baseline: its fanout cap, from the code, and
# the share of questions it binds on, from the measurement.
g = re.search(r"fanout_cap=(\d+)",
              open(os.path.join(ROOT, "agr", "baselines", "graphrag.py"),
                   encoding="utf-8").read())
ck("graphrag.py states its fanout cap", g is not None)
deg = J["candidate_caps"]["expanded_entity_degree"]
if g:
    ck(f"the script quotes the {g.group(1)}-edge cap and "
       f"{deg['questions_any_topic_over_100_pct']}% above it",
       re.search(rf"at most {g.group(1)} edges per topic entity", MDF)
       is not None
       and re.search(rf"on {deg['questions_any_topic_over_100_pct']} percent "
                     rf"of questions at least one topic entity", MDF)
       is not None)

# The candidate widths are configuration, not results, so they are read
# from the code that sets them rather than from thesis_numbers.json.
#
# Checked in each block that needs them, not once against the whole deck:
# the widths now have two homes (the fairness frame and the limitations
# list), and "does this value appear somewhere" would pass a deck that had
# dropped either one.
print("\n== candidate widths come from the code ==")
tog = open(os.path.join(ROOT, "agr", "baselines", "tog.py"),
           encoding="utf-8").read()
tools = open(os.path.join(ROOT, "agr", "kg_tools.py"), encoding="utf-8").read()
WHERE = (("fairness frame", fair), ("limitations list", limits))
m = re.search(r"MAX_RELATIONS,\s*MAX_NEIGHBORS\s*=\s*(\d+),\s*(\d+)", tog)
ck("tog.py states its caps", m is not None)
if m:
    for where, txt in WHERE:
        ck(f"{where} quotes ToG {m.group(1)}/{m.group(2)}",
           f"${m.group(1)}$/${m.group(2)}$" in txt)
a = re.search(r"max_fanout=(\d+),\s*max_relations=(\d+)", tools)
ck("kg_tools.py states AGR's caps", a is not None)
if a:
    for where, txt in WHERE:
        ck(f"{where} quotes AGR {a.group(2)}/{a.group(1)}",
           f"${a.group(2)}$/${a.group(1)}$" in txt)

# ---------------------------------------------------------------------
# The rehearsal transcript's timing table has to add up.
#
# It is three numbers deep -- a per-slide time, a running cumulative, and a
# total quoted in the budget line -- and every edit to the script moves all
# three. That is exactly the shape that goes stale silently: a table still
# claiming 22:30 while the script has grown past 24 minutes is worse than
# no table, because it is consulted under pressure and believed.
print("\n== the transcript's timing table adds up ==")
SCRIPT = os.path.join(HERE, "transcript.md")
if not os.path.exists(SCRIPT):
    print("  [   ] transcript.md absent")
else:
    md = open(SCRIPT, encoding="utf-8").read()

    def secs(m, s):
        return int(m) * 60 + int(s)

    rows = re.findall(r"^\| (\d+) \| ([^|]*?) \| (\d+):(\d\d) \| (\d+):(\d\d) \|",
                      md, re.M)
    ck("the table has a row per slide", len(rows) == 22, f"{len(rows)} rows")

    run = 0
    drift = []
    for n, _t, ms, ss, mc, sc in rows:
        run += secs(ms, ss)
        if run != secs(mc, sc):
            drift.append(f"row {n}: sum {run}s vs stated {secs(mc, sc)}s")
    ck("cumulative column is the running sum", not drift,
       drift[0] if drift else "")

    # Each section heading repeats its slide's time; both have to move.
    heads = dict((n, secs(m, s)) for n, m, s in
                 re.findall(r"^## (\d+) — .*?\*\((\d+):(\d\d)\)\*", md, re.M))
    table = dict((n, secs(ms, ss)) for n, _t, ms, ss, _c, _d in rows)
    mism = [f"slide {n}: heading {heads[n]}s vs table {table[n]}s"
            for n in sorted(table, key=int)
            if n in heads and heads[n] != table[n]]
    ck("section headings match the table", not mism, mism[0] if mism else "")

    b = re.search(r"\*\*Budget: (\d+) min (\d+) s of speaking", md)
    ck("the budget line states the table's total",
       b is not None and secs(b.group(1), b.group(2)) == run,
       f"stated {b.group(0) if b else '?'} vs {run//60}:{run % 60:02d}")

    # The point of the budget is the limit it sits under.
    lim = re.search(r"against a (\d+)-minute limit", md)
    ck("the talk fits the limit it names",
       lim is not None and run <= int(lim.group(1)) * 60,
       f"{run}s vs {lim.group(1) if lim else '?'} min")

print("\n" + ("ALL SLIDE NUMBERS MATCH THEIR SOURCE"
              if ok else "SOMETHING DOES NOT MATCH"))
sys.exit(0 if ok else 1)
