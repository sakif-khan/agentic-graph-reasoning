"""Check every number typed into presentation.tex against its source.

The three data figures are \\input from thesis_book/figures/ and need no
checking -- scripts/build_figures.py generates them from the same JSON. This
script covers the numbers that appear as table text or prose in the deck,
which are transcribed and can therefore drift.

Run from anywhere:  python thesis_presentation/check_slides.py
"""
import csv
import json
import os
import re
import subprocess
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


def uncomment(tex):
    """Drop % comments before anything matches against the source.

    These slides carry long comments recording *why* a claim is worded the
    way it is, and those comments quote the retracted wording verbatim --
    so a rule banning a phrase was matching the note explaining the ban.
    The echo-attractor rule passed only because a line wrap happened to
    put "%" between "the" and "task"; rewrapping the comment would have
    failed a correct slide. \\% is a literal sign, not a comment.
    """
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in tex.splitlines())


FLAT = " ".join(uncomment(TEX).split())
ok = True


def ck(label, cond, detail=""):
    global ok
    print(f"  [{'OK ' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    ok &= bool(cond)


def has(s):
    """Is this literal present in the deck, ignoring LaTeX thousands markers?

    Whole-deck presence. That is the right question only when the value has
    exactly one home, and it is the wrong one everywhere else -- corrupting
    a cell whose value is also printed on a backup slide left this silent.
    Prefer cell() and row(); has() survives for values that genuinely may
    appear anywhere.
    """
    return s in FLAT or s.replace(",", "{,}") in FLAT


# Rows of every tabular in the deck, flattened. Splitting the whole source
# on \\ is crude and exactly enough: a row is the unit a reader sees a
# number in, and it is the unit a corruption lands in.
#
# A chunk begins after the previous row's \\, so it carries whatever rule
# command followed it -- "\midrule No-retrieval & 0.453 ..." does not start
# with its own label. Strip those first or every lookup returns nothing.
LEAD = re.compile(r"^(?:\\(?:top|mid|bottom)rule"
                  r"|\\cmidrule(?:\([lr]+\))?\{[^}]*\}"
                  r"|\\hline|\\addlinespace|\[[^\]]*\]|\s)+")


MD = open(os.path.join(HERE, "transcript.md"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(HERE, "transcript.md")) else ""


def plain(text):
    """Drop markdown emphasis and quote markers before matching prose.

    The shipped sentence read "*below* the no-retrieval control", and a
    rule spelled "below the no-retrieval" does not match that. The probe
    still reported CAUGHT, on a different check -- which is how a rule
    that never fires looks from the outside.
    """
    return " ".join(re.sub(r"[*`>]", "", text).split())


def answer(question):
    """One anticipated-questions entry: its heading and the prose under it.

    The Q&A section is not quoted speech, so spoken() does not reach it --
    and it was the one part of this material bound to nothing, which is
    where the arithmetic error this file now guards was written.
    """
    m = re.search(r"\*\*\"[^\"]*" + re.escape(question)
                  + r"[^\"]*\"\*\*(.*?)(?=\n\*\*\"|\n## |\Z)", MD, re.S)
    return " ".join(m.group(1).split()) if m else ""


def spoken(n):
    """The quoted lines of one transcript section, without the markers."""
    m = re.search(rf"^## {n} [^\n]*$(.*?)(?=^## |\Z)", MD, re.S | re.M)
    return plain(" ".join(l for l in m.group(1).splitlines()
                          if l.startswith(">"))) if m else ""


# Counts that appear as words on a slide -- nodes, cycles, modules -- are
# compared through this rather than spelled out at each site.
NUM = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
       6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}


def frame(title):
    """The one frame with this title, from \\begin{frame} to \\end{frame}."""
    m = re.search(r"\\begin\{frame\}\{" + re.escape(title) + r"\}(.*?)"
                  r"\\end\{frame\}", FLAT)
    return m.group(1) if m else ""


def frames(*titles):
    """Several frames' bodies, concatenated, as one scope.

    A rule written against a frame that has since been split into two would
    otherwise search only the half whose title it names -- and pass or fail
    for the wrong reason. The seven frames split this round each carry one
    argument across two slides, so the scope of a rule about that argument
    is the pair. Returns '' if any of them is missing, so a renamed frame
    fails the rule that needs it instead of quietly shrinking its scope.
    """
    got = [frame(t) for t in titles]
    return " ".join(got) if all(got) else ""


def row(scope, label):
    """The one table row in `scope` that begins with this label, or ''.

    Scoped to a frame, not to the deck: "No-retrieval" begins three rows
    across these two files -- the main table, the backup hedging table, and
    a bullet on the fairness slide -- and a deck-wide lookup is ambiguous
    for exactly the labels that matter most. Returns '' when the label is
    absent OR ambiguous within the scope, so the check fails rather than
    silently reading someone else's row.
    """
    hits = [LEAD.sub("", c).strip() for c in re.split(r"\\\\", scope)]
    hits = [r for r in hits if r.startswith(label)]
    return hits[0] if len(hits) == 1 else ""


def cell(scope, label, n):
    """Cell n of that row, counting the label as cell 0."""
    parts = [c.strip() for c in row(scope, label).split("&")]
    return parts[n] if len(parts) > n else ""


def holds(scope, label, n, value):
    """Does cell n of this row hold this value, as a whole number?

    Token-matched, not substring-matched. Scoping to the cell was not
    enough on its own: the call cap reads 0.0% in every column, and
    corrupting it to 40.0% still contained "0.0", so the check passed on
    the row it was written for. A digit or a dot on either side means this
    is part of a different number.
    """
    got = cell(scope, label, n)
    alts = "|".join(sorted({re.escape(value),
                            re.escape(value.replace(",", "{,}"))}))
    return bool(got) and re.search(rf"(?<![\d.])(?:{alts})(?![\d.])",
                                   got) is not None


print("== main results table ==")
B = J["main_results"]["by_system"]
NAME = {"noretrieval": "No-retrieval", "vectorrag": "Vector RAG",
        "graphrag": "Static GraphRAG", "tog": "Think-on-Graph", "agr": "AGR"}
# The label as the row actually begins, and the column each metric sits in:
# system, WebQSP Hits@1, WebQSP F1, CWQ Hits@1, CWQ F1, tokens, calls.
LABEL = dict(NAME, agr=r"\textbf{AGR}")
COL = {("webqsp", "hits_at_1"): 1, ("webqsp", "f1"): 2,
       ("cwq", "hits_at_1"): 3, ("cwq", "f1"): 4}
MAIN = frame("Main results")
ck("the main results frame is in the deck", bool(MAIN))
for s, label in NAME.items():
    ck(f"{label:15s} has one row there", bool(row(MAIN, LABEL[s])))
    for ds in ("webqsp", "cwq"):
        r = B[f"{ds}/{s}"]
        for metric in ("hits_at_1", "f1"):
            v = f"{r[metric]:.3f}"
            ck(f"{label:15s} {ds:6s} {metric:9s} = {v}",
               holds(MAIN, LABEL[s], COL[(ds, metric)], v),
               f"cell holds {cell(MAIN, LABEL[s], COL[(ds, metric)])!r}")

print("\n== cost figures quoted on the results slide ==")
# WebQSP cost is the last two columns of the same row; the CWQ costs are in
# a sentence under the table, so they are checked against that sentence.
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
    if ds == "webqsp":
        ck(f"{ds}/{s} tokens are in the cost column",
           holds(MAIN, LABEL[s], 5, f"{tok:,}"),
           f"cell holds {cell(MAIN, LABEL[s], 5)!r}")
        ck(f"{ds}/{s} calls are in the cost column",
           holds(MAIN, LABEL[s], 6, f"{calls}"),
           f"cell holds {cell(MAIN, LABEL[s], 6)!r}")
    else:
        # Build the number first and escape it on its own: applying the
        # thousands-marker substitution to the whole pattern rewrote the
        # comma inside {0,120} and the regex stopped meaning anything.
        num = re.escape(f"{tok:,}".replace(",", "{,}"))
        ck(f"{ds}/{s} cost is in the sentence under the table",
           re.search(rf"CWQ:.{{0,200}}?{num}.{{0,40}}?{re.escape(str(calls))}",
                     FLAT) is not None)

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
BIND = frame("Backup: which budgets actually bind")
ck("the budget-binding frame is in the backup deck", bool(BIND))
BINDROW = {"depth": "Depth cap", "backtracks": "Backtrack cap",
           "verify_iters": "Verify-iteration cap",
           "llm_calls": r"\textbf{Call cap}"}
for key, label in (("depth", "depth"), ("backtracks", "backtrack"),
                   ("verify_iters", "verify"), ("llm_calls", "call")):
    for n, pop in ((1, "webqsp"), (2, "cwq"), (3, "both")):
        v = f"{BB[pop][key]['refused_pct']:.1f}"
        # Cell-scoped: the call cap is 0.0% in all three columns, and "0.0"
        # occurs all over this deck, so whole-deck presence asserted nothing
        # about the row that matters most.
        ck(f"{label:10s} {pop:6s} {v}%", holds(BIND, BINDROW[key], n, v),
           f"cell holds {cell(BIND, BINDROW[key], n)!r}")


def num(text):
    """The numeric content of a cell, ignoring $, \\, and thousands marks."""
    return re.sub(r"[^0-9.]", "", text.replace("{,}", ""))


print("\n== test sets and environment ==")
# The graph statistics were quoted on a slide and checked nowhere. Their
# source of record is the thesis's own tab:graphstats, so they are held to
# that table cell for cell rather than to a number repeated here.
ENVSLIDE = frame("The environment and the question sets")
ck("the environment frame is in the deck", bool(ENVSLIDE))
envtex = " ".join(uncomment(
    open(os.path.join(ROOT, "thesis_book", "chapters", "environment.tex"),
         encoding="utf-8").read()).split())
for deck_label, thesis_label in (("Entities", "Entities (nodes)"),
                                 ("Triples", "Triples (relationships)"),
                                 ("Distinct relations",
                                  "Distinct relation types"),
                                 ("Import time", "Import wall-clock time")):
    want = num(cell(envtex, thesis_label, 1))
    got = num(cell(ENVSLIDE, deck_label, 1))
    ck(f"graph {deck_label.lower()} = {want}", bool(want) and got == want,
       f"thesis {want!r}, deck {got!r}")

for n, ds in ((1, "webqsp"), (2, "cwq")):
    t = J["test_sets"][ds]
    ck(f"{ds} n_questions 400", t["n_questions"] == 400)
    ck(f"{ds} questions cell", holds(ENVSLIDE, "Questions", n,
                                     str(t["n_questions"])),
       f"cell holds {cell(ENVSLIDE, 'Questions', n)!r}")
    ck(f"{ds} gold median {t['gold_median']}",
       holds(ENVSLIDE, "Gold (median)", n, f"{t['gold_median']:.1f}"),
       f"cell holds {cell(ENVSLIDE, 'Gold (median)', n)!r}")
    ck(f"{ds} reachable {t['reachable_pct']}%",
       holds(ENVSLIDE, "Reachable", n, f"{t['reachable_pct']:.1f}"),
       f"cell holds {cell(ENVSLIDE, 'Reachable', n)!r}")
    multi = t["strata"]["h2"] + t["strata"]["h3plus"]
    ck(f"{ds} multi-hop {multi}", holds(ENVSLIDE, "Multi-hop", n, str(multi)),
       f"cell holds {cell(ENVSLIDE, 'Multi-hop', n)!r}")

# The headline figures, wherever they are.
#
# They were bullets on the second slide, three slides before the talk
# defines "hallucination" and eighteen before it introduces the control
# they come from -- unreadable where they stood, and a second rate for a
# phenomenon the RQ2 table already reports pooled. The slide is gone and
# the numbers are an answer now, which is the right home for evidence you
# produce on demand and the worst-bound part of that file.
#
# So the rule follows them, and adds what the move makes necessary: an
# answer quoting 27.1% has to give the pooled figure beside it, or the
# questioner is left to reconcile it with the 22.1% on the slide.
print("\n== the opening claim's evidence, wherever it is stated ==")
PROBLEM = frame("The problem")
ck("the problem frame is in the deck", bool(PROBLEM))
ck("the deck no longer asserts a rate it cannot source on the slide",
   "27.1" not in FLAT, "the WebQSP slice belongs to the answer now")
G = J["groundedness_tier1_structural"]["test_webqsp_noretrieval"]
eq = answer("Where is your evidence?")
ck("the evidence question is in the anticipated questions", bool(eq))
for label, want in (("entities asserted", G["entities_asserted"]),
                    ("ungrounded", G["entities_ungrounded"]),
                    ("rate", f'{G["entity_ungrounded_pct"]} percent')):
    ck(f"the answer gives WebQSP {label} = {want}",
       re.search(rf"(?<![\d.]){re.escape(str(want))}(?![\d.])", eq)
       is not None, f"expected {want}")

# ...and the pooled row beside it, from the same source the slide uses, so
# the two rates are reconciled where they are both stated.
pool = {k: sum(J["groundedness_tier1_structural"]
               [f"test_{d}_noretrieval"][k] for d in ("webqsp", "cwq"))
        for k in ("entities_asserted", "entities_ungrounded")}
for label, want in (("asserted", pool["entities_asserted"]),
                    ("ungrounded", pool["entities_ungrounded"])):
    ck(f"and the pooled {label} = {want}",
       re.search(rf"(?<![\d.]){want:,}(?![\d.])".replace(",", ",?"), eq)
       is not None, f"expected {want:,}")
ck("and says why the two rates differ",
   re.search(r"slice runs higher|differ|because", eq, re.I) is not None,
   "27.1 against 22.1 needs a reason where both are stated")

# Per-category census counts. The slide prints the six largest as Totals;
# each is the sum of wrong and hedge over both datasets.
print("\n== the census categories are the measured ones ==")
CENSUS = frames("Every failure, read and labelled", "The echo attractor")
CATS = (("Relation selection", "relation_selection"),
        ("Composite claim", "composite_claim"),
        ("Knowledge-graph gap", "kg_gap"),
        ("Decomposition error", "decomposition_error"),
        ("Answer selection", "answer_selection"),
        (r"\alert{Echo attractor}", "echo"))
H2 = J["failure_histogram"]
for label, key in CATS:
    want = sum(H2[ds][k].get(key, 0)
               for ds in ("webqsp", "cwq") for k in ("wrong", "hedge"))
    ck(f"census {key} = {want}", holds(CENSUS, label, 1, str(want)),
       f"cell holds {cell(CENSUS, label, 1)!r}")
ck("the six listed are the six largest",
   [k for _, k in CATS] == [k for k, _ in sorted(
       ((k, sum(H2[ds][c].get(k, 0) for ds in ("webqsp", "cwq")
                for c in ("wrong", "hedge")))
        for k in {k for ds in ("webqsp", "cwq") for c in ("wrong", "hedge")
                  for k in H2[ds][c] if not k.startswith("_")}),
       key=lambda kv: -kv[1])[:6]],
   "the slide claims the top categories")

# The tool caps, printed on the tool slide and checked nowhere.
print("\n== the tool slide's caps come from the code ==")
kg = open(os.path.join(ROOT, "agr", "kg_tools.py"), encoding="utf-8").read()
caps = re.search(r"max_fanout=(\d+),\s*max_relations=(\d+)", kg)
TS = frame("Constrained tools, not free-form queries")
ck("kg_tools.py states the caps", caps is not None)
if caps:
    # Cell 3, not 2: a Node column was inserted after the operation, and
    # cell() counts from the row label. Reading cell 2 after that shift
    # asks "Candidate relations" whether it contains 300, which is a
    # question with a stable and useless answer.
    for label, want in ((r"\texttt{get\_relations}", caps.group(2)),
                        (r"\texttt{get\_neighbors}", caps.group(1))):
        ck(f"{label} is capped at {want} on the slide",
           want in cell(TS, label, 3),
           f"cell holds {cell(TS, label, 3)!r}")

# The backup budget table, transcribed from agr/budget.py and checked
# nowhere -- every row of it.
print("\n== the backup budget table is the code's ==")
bud = open(os.path.join(ROOT, "agr", "budget.py"), encoding="utf-8").read()
BUDGET = frame("Backup: budget configuration")
ck("the budget frame is in the backup deck", bool(BUDGET))
# BudgetConfig only. budget.py also defines BudgetMeter, whose fields are
# running counters that all default to 0 -- reading the whole file gave
# fifteen "defaults" and asked the slide to print cache_hits.
body_cfg = re.search(r"class BudgetConfig:\n(.*?)\n\n", bud, re.S)
ck("budget.py defines BudgetConfig", body_cfg is not None)
defaults = dict(re.findall(r"^    (\w+): \w+ = ([\d.]+)",
                           body_cfg.group(1) if body_cfg else "", re.M))
ck(f"budget.py states {len(defaults)} configured budgets", len(defaults) == 7,
   str(sorted(defaults)))
for field, value in sorted(defaults.items()):
    label = "\\texttt{" + field.replace("_", "\\_") + "}"
    got = num(cell(BUDGET, label, 1))
    # float(), not string equality: the code says 300.0 and the slide says
    # 300, and both are the same budget.
    ck(f"{field} = {value}",
       bool(got) and float(got) == float(value),
       f"code {value!r}, slide {cell(BUDGET, label, 1)!r}")

# Research questions are numbered, and a renumbering that the deck does
# not follow reads as a different set of questions.
print("\n== the research questions are numbered as the thesis numbers them ==")
asked = sorted({int(n) for n in re.findall(r"\bRQ(\d+)", FLAT)})
ck("the deck asks RQ1, RQ2 and RQ3", asked == [1, 2, 3], f"deck asks RQ{asked}")

# The three generated figures. check_slides used to say these "need no
# checking" because build_figures.py generates them -- but a generated
# file is only right until the JSON moves under it, and the deck keeps its
# own copies at a different geometry.
# ---------------------------------------------------------------------
# The module README describes this module.
#
# It said check_tex_roots.py "checks both this module and the book" -- it
# covers three, thesis_paper included -- and that "both documents \input
# [fig_claim_path] from thesis_book/figures/", when only the presented deck
# uses it and the backup deck does not. Prose about the repository goes
# stale the same way a transcribed number does, and nothing was reading it.
print("\n== the module README describes this module ==")
RM = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
roots = open(os.path.join(ROOT, "scripts", "check_tex_roots.py"),
             encoding="utf-8").read()
mods = re.search(r"MODULES\s*=\s*\(([^)]*)\)", roots, re.S)
n_mods = len(re.findall(r'"[^"]+"', mods.group(1))) if mods else 0
ck(f"check_tex_roots.py covers {n_mods} modules", n_mods in NUM, str(n_mods))
if n_mods in NUM:
    ck(f"the README says it checks all {NUM[n_mods].lower()}",
       re.search(rf"check_tex_roots\.py` checks all {NUM[n_mods].lower()}",
                 RM) is not None,
       f"it covers {n_mods}")

main_src = open(os.path.join(HERE, "content-main.tex"), encoding="utf-8").read()
back_src = open(os.path.join(HERE, "content-backup.tex"),
                encoding="utf-8").read()
claim = re.search(r"\\input\{([^}]*fig_claim_path[^}]*)\}", main_src)
ck("the presented deck inputs fig_claim_path", claim is not None)
if claim:
    # Whether the README should describe a cross-directory reach or a local
    # copy is decided by which one the deck actually does.
    crosses = claim.group(1).startswith("../")
    ck("the README describes where the figure comes from",
       ("across the directory boundary" in RM) == crosses,
       f"deck inputs {claim.group(1)!r}")
ck("the backup deck does not use it, and the README says so",
   ("fig_claim_path" in back_src)
   == ("backup deck does not use it" not in RM),
   "the README must match which decks input the figure")

# ---------------------------------------------------------------------
# The hedge-difference answer, recomputed from the paired records.
#
# The prepared answer said correctness "moved on exactly one of the 398
# paired questions, so at least five of those six were assertions that
# would have been wrong". Two errors and an omission: it moved on two of
# 398, one per dataset -- "one" is the CWQ-only figure against the pooled
# denominator -- and none of the six came back correct, not five, so the
# claim available was stronger than the one written. The omission was the
# one that mattered: on WebQSP the single question the layer hedged on is
# one the ablated run got right, which is the counter-example to the whole
# answer and was not mentioned.
#
# Computed from the records rather than from a number in a JSON file,
# because the paired sets are what the answer is about and nothing
# generated carries them.
print("\n== the hedge-difference answer is the paired records ==")
ABL = os.path.join(ROOT, "results", "phase4", "ablations")


def _pairs(ds):
    def load(cond):
        out = {}
        with open(os.path.join(ABL, f"test_{ds}_half_abl_{cond}.jsonl"),
                  encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    out[rec["qid"]] = rec
        return out

    def ents(rec):
        return {str(x).strip().lower()
                for x in (rec.get("answer_entities") or []) if str(x).strip()}

    full, abl = load("full"), load("noverifier")
    qids = sorted(set(full) & set(abl))
    stats = {"n": len(qids)}
    stats["full_only"] = [q for q in qids
                          if not ents(full[q]) and ents(abl[q])]
    stats["abl_only"] = [q for q in qids
                         if not ents(abl[q]) and ents(full[q])]
    stats["rescued"] = [q for q in stats["full_only"]
                        if ents(abl[q]) & {str(g).strip().lower()
                                           for g in (abl[q].get("gold") or [])}]
    hit = lambda r: bool(ents(r) & {str(g).strip().lower()
                                    for g in (r.get("gold") or [])})
    stats["discordant"] = sum(1 for q in qids if hit(full[q]) != hit(abl[q]))
    return stats


if not os.path.isdir(ABL):
    print("  [   ] ablation records absent")
else:
    qa = answer("How many questions is that hedge difference")
    ck("the hedge-difference answer is in the script", bool(qa))
    st = {ds: _pairs(ds) for ds in ("cwq", "webqsp")}
    paired = st["cwq"]["n"] + st["webqsp"]["n"]
    moved = st["cwq"]["discordant"] + st["webqsp"]["discordant"]
    ck(f"the answer states the {paired} paired questions",
       str(paired) in qa, f"{paired} paired")
    # "twice", not "two times": the answer is spoken aloud, and the rule
    # has to match the English a person would say.
    said = {1: "once", 2: "twice"}.get(
        moved, f"{NUM.get(moved, moved)} times".lower())
    ck(f"correctness moved {said}, and the answer says so",
       re.search(rf"moved {said}", qa, re.I) is not None,
       f"{st['cwq']['discordant']} on CWQ, {st['webqsp']['discordant']} on "
       f"WebQSP")
    ck(f"CWQ: the layer declined on {len(st['cwq']['full_only'])}",
       re.search(rf"\b{NUM[len(st['cwq']['full_only'])]}, on CWQ", qa)
       is not None, str(len(st["cwq"]["full_only"])))
    # The sets nest, so "exactly the six the ablated run answered" is a fact
    # about the records rather than an inference from a difference of rates.
    nests = not st["cwq"]["abl_only"] and not st["webqsp"]["abl_only"]
    ck("the sets nest, and the answer claims that", nests
       and "sets nest" in qa,
       f"cwq {len(st['cwq']['abl_only'])}, webqsp "
       f"{len(st['webqsp']['abl_only'])} the other way")
    ck(f"none of the {len(st['cwq']['full_only'])} came back correct",
       not st["cwq"]["rescued"] and "None of the six came back correct" in qa,
       f"{len(st['cwq']['rescued'])} were correct")
    # The counter-example. It is the half an examiner would find.
    ck(f"WebQSP: {len(st['webqsp']['full_only'])} hedged question, and the "
       f"ablated run got {len(st['webqsp']['rescued'])} right",
       len(st["webqsp"]["full_only"]) == 1
       and len(st["webqsp"]["rescued"]) == 1
       and "the ablated run got it right" in qa,
       "the answer must volunteer the question the layer cost")

print("\n== the deck's generated figures are current ==")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    import build_figures as BF
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        data = BF.load()
        cfg = BF.TARGETS["presentation"]
        for name, fn in (("fig_accuracy_cost", BF.accuracy_cost),
                         ("fig_hop_strata", BF.hop_strata),
                         ("fig_failure_histogram", BF.failure_histogram)):
            on_disk = open(os.path.join(HERE, "figures", f"{name}.tex"),
                           encoding="utf-8", newline="").read()
            ck(f"{name}.tex matches what build_figures would write now",
               on_disk.replace("\r\n", "\n") == fn(data, cfg),
               "re-run scripts/build_figures.py")
    finally:
        os.chdir(cwd)
except ImportError as e:
    ck("build_figures.py is importable", False, str(e))
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
# uncomment() first, for the same reason FLAT does: a comment recording
# why a size command was removed must not read as a size command.
body = re.sub(r"font=\\\w+", "", uncomment(TEX))
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
# ...and nothing on a rendered page prints on top of anything else.
#
# Everything above reads the build log, which is the record of whether
# material FIT. A negative \vspace does not make material too big for its
# box, so no overfull is issued and no warning of any class -- it simply
# moves the material somewhere else, possibly on top of something. The RQ3
# ablation frame shipped a round that way: \vspace{-5mm} put the
# interpretation blocks across the table's last rows and \vspace{-3mm} put
# the McNemar caption inside a block, under a checker printing "no
# warnings, of any class" three lines earlier.
#
# Measured on the page instead of in the log. Two text lines collide when
# their boxes overlap horizontally, and vertically by more than a quarter
# of the shorter line's height.
#
# A quarter rather than a fixed point: the first version used 1pt and fired
# on the backup census, where two monospace y-axis tick labels are set
# close enough that their ascender/descender boxes lap by 1.4pt with a
# clear gap between the ink. Relative to line height that is 14%, against
# 43% for the RQ3 collision -- and being scale-free, it reads the same on
# \small body text and on a frametitle. Lines sharing a baseline are one
# line set in several runs and are skipped.
print("\n== no text on any page prints on top of other text ==")
try:
    import pymupdf
except ImportError:
    print("  [   ] pymupdf not installed -- pages not measured")
    pymupdf = None
if pymupdf is not None:
    for drv in DRIVERS:
        pdf = os.path.join(HERE, os.path.splitext(drv)[0] + ".pdf")
        if not os.path.exists(pdf):
            print(f"  [   ] {drv}: no PDF to measure -- run latexmk first")
            continue
        clashes = []
        for page in pymupdf.open(pdf):
            boxes = [(pymupdf.Rect(l["bbox"]),
                      "".join(s["text"] for s in l["spans"]).strip())
                     for b in page.get_text("dict")["blocks"]
                     for l in b.get("lines", [])
                     if "".join(s["text"] for s in l["spans"]).strip()]
            for i, (ra, ta) in enumerate(boxes):
                for rb, tb in boxes[i + 1:]:
                    if abs(ra.y0 - rb.y0) < 0.6 and abs(ra.y1 - rb.y1) < 0.6:
                        continue
                    dy = min(ra.y1, rb.y1) - max(ra.y0, rb.y0)
                    if (min(ra.x1, rb.x1) - max(ra.x0, rb.x0) > 1.0
                            and dy > 1.0
                            and dy > 0.25 * min(ra.height, rb.height)):
                        clashes.append(f"page {page.number + 1}: "
                                       f"{ta[:34]!r} over {tb[:34]!r}")
        ck(f"{drv}: no overprinted text", not clashes,
           clashes[0] if clashes else "")

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
# also appears on slide 20, and matching the whole deck would pass a slide
# that had dropped it.
print("\n== the deck's contributions are the thesis's ==")
INTRO = os.path.join(ROOT, "thesis_book", "chapters", "introduction.tex")
CONTRIB_KEYS = [
    ("framework / verification layer", ("verification layer",)),
    ("component-level ablation", ("component-level ablation",)),
    ("stratum-dependent decomposition", ("stratum-dependent",)),
    ("echo attractor", ("echo attractor",)),
    ("benchmark defect rates", ("benchmark-defect", "benchmark defect")),
    ("pre-specified protocol", ("pre-specified",)),
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
DENIED = (r"(?:retrieval budget|bigger retrieval|retrieval width"
          r"|candidate (?:set|width)s?|same candidates?)")
OVERCLAIM = re.compile(
    r"attribut\w+[^.]{0,140}?\b(?:not|rather than)\b[^.]{0,140}?" + DENIED,
    re.I)


fair = frames("Making the comparison fair",
              r"What is \emph{not} held equal")
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
LIMIT_HEADS = [" ".join(h.split()).lower() for h in re.findall(
    r"\\textbf\{([^}]*)\}", conc[i:conc.index(r"\section", i + 10)])]
# Three answers cite an ordinal now, so a set equality against one rank
# would fail a correct script. Each is ranked off the thesis heading it
# is about, and the set is still closed: an ordinal quoted anywhere else
# in the script belongs to no ranked limitation and fails here.
RANKS = (("narrower candidate set", "Did both systems see the same"),
         ("entity linking is assumed", "topic entities come from"),
         ("depresses the reported accuracy", "Nine of your failures"))
used = set()
for head_key, question in RANKS:
    at = next((n for n, h in enumerate(LIMIT_HEADS, 1)
               if head_key in h), None)
    ck(f"the thesis ranks {head_key!r}", at is not None)
    said = answer(question)
    ck(f"the script prepares {question!r}", bool(said))
    if at and said:
        ck(f"and calls it limitation {at}", f"limitation {at}" in said,
           f"answer says {re.findall(r'limitation (.d+)', said) or 'nothing'}")
        used.add(str(at))
stated = set(re.findall(r"limitation (\d+)", MDF))
ck("no other limitation ordinal is quoted", stated == used,
   f"script says {sorted(stated)}, ranked {sorted(used)}")

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


# Retracting it is only half the job: the table puts 0.203 and 0.205 next
# to each other, so the script has to say which baseline carries the claim
# and why the other does not, or the audience pools them anyway.
#
# Bound to what is actually said on slide 12, not to the whole file. The
# first version searched the transcript and passed while section 20 had
# been stripped of it, because the speaker note below the section quotes
# the same phrase -- a second home, again.
s20 = spoken(20)
ck("section 20 is in the transcript", bool(s20))
ck("section 20 names the baseline the claim rests on",
   re.search(r"claim rests on vector RAG", s20, re.I) is not None)
ck("and says why GraphRAG's number does not carry it",
   re.search(r"radius confounds", s20, re.I) is not None)

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
# Whitespace-flattened. The old pattern needed `coordinates {` on the
# same line as `color=agrGraph`, which coupled this rule to a line
# break in a GENERATED file: when build_figures.py began folding its
# output to 80 columns, the rule stopped finding a figure that had not
# changed a digit. [^;]*? rather than [^\n]* because every \addplot
# ends in a semicolon, so the match still cannot reach the next plot.
fig = " ".join(open(FIG, encoding="utf-8").read().split())
for title, hop, want_label in (("WebQSP", 1, "WebQSP two-hop"),
                               ("ComplexWebQuestions", 1, "CWQ two-hop")):
    axis = next((a for a in fig.split(r"\begin{axis}")
                 if f"title={{{title}}}" in a), "")
    m = re.search(r"color=agrGraph[^;]*?coordinates \{([^}]*)\}", axis)
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

# ---------------------------------------------------------------------
# The echo attractor's point is about evaluation, not about blame.
#
# The slide said "It appears across systems, so it is a property of the
# task, not of AGR" -- defensive, and pointed the wrong way. sec:echo:
# "That is also why the echo attractor is invisible to any evaluation
# treating systems as independent." sec:contribution: the contribution is
# "the named mechanism itself and what it means for consensus-based
# evaluation, not the frequency." sec:limitations-final's chapter lists it
# as "shared attractors break consensus-based evaluation", because a
# majority-rescoring policy converts the failure into apparent
# correctness. Commit 2acfc2a moved the abstract off the independence
# framing -- "turns up across unrelated systems" became "which different
# systems fall into together" -- and the deck never followed.
print("\n== the echo attractor is framed as the thesis frames it ==")
echo = frames("Every failure, read and labelled", "The echo attractor")
bench = frame(r"Backup: the benchmark was wrong $57$ times")
# The benchmark-defect slide moved to the backup deck, so it has no
# spoken section any more. Its numbers are still checked, off the slide.
# The census and the attractor are two sections now, and the framing
# rules below are about the pair: the deflection this bans could be
# reintroduced in either one.
said = spoken(28) + " " + spoken(29)
ck("both frames are in the deck", bool(echo) and bool(bench))

RETRACTED = re.compile(r"propert\w+ of the task|across unrelated systems"
                       r"|not (?:a propert\w+ of )?AGR\b"
                       r"|rather than (?:of )?AGR\b", re.I)
for label, text in (("echo slide", echo), ("sections 28-29", said)):
    hit = RETRACTED.search(text)
    ck(f"{label} does not deflect it onto the task", hit is None,
       hit.group(0)[:60] if hit else "")
    ck(f"{label} says no independent evaluation can see it",
       re.search(r"independent", text, re.I) is not None
       and re.search(r"evaluation|see it", text, re.I) is not None)
    ck(f"{label} names what majority rescoring would do",
       re.search(r"majority|consensus", text, re.I) is not None
       and re.search(r"correctness", text, re.I) is not None)

# The framing is only right while the thesis frames it that way.
ck("the thesis still makes it a claim about evaluation",
   "what it means for consensus-based evaluation, not the" in
   " ".join(open(INTRO, encoding="utf-8").read().split()),
   "sec:contribution is what the slide answers to")

# Slides 19 and 20 are one finding. sec:benchmark-defects: "The gap
# between those figures is not measurement noise --- it is the echo
# attractor of sec:echo, operating across systems." The deck introduced
# the second as "Reading every failure also found...", which reads as an
# unrelated bonus.
GA = J["gold_adjudication"]
flagged = GA["webqsp"]["flagged_questions"] + GA["cwq"]["flagged_questions"]
confirmed = GA["webqsp"]["excluded_questions"] + GA["cwq"]["excluded_questions"]
ck(f"the flagged total is {flagged} and the confirmed total is {confirmed}",
   confirmed == J["benchmark_defects"]["excluded_before_census"],
   "the confirmed pair must be the count excluded before the census")
for label, text, fl, cf in (("benchmark slide", bench, f"${flagged}$",
                             f"${confirmed}$"),):
    ck(f"{label} gives both the flagged and the confirmed count",
       fl in text and cf in text, f"wants {fl} and {cf}")
    ck(f"{label} attributes the gap to the attractor",
       re.search(r"gap is the attractor|attractor I just described", text,
                 re.I) is not None,
       "the gap is the finding, not measurement noise")

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
# Every operation named on the tool slide is a def in kg_tools.py.
#
# The slide listed \texttt{link_entity}. There is no such operation --
# it is search_entity, in kg_tools.py, in app:tool-search and in
# tab:toolapi -- and "link_entity" appeared nowhere else in the
# repository. Set in monospace on a slide, a name reads as the literal
# API. Every number in this deck was bound to its source; the
# identifiers were not bound to anything.
print("\n== the tool slide names real operations ==")
TOOLSLIDE = frame("Constrained tools, not free-form queries")
defined = set(re.findall(r"^    def (\w+)\(", tools, re.M))
named = [n.replace("\\_", "_")
         for n in re.findall(r"\\texttt\{([a-z\\_]+)\}", TOOLSLIDE)]
ck("the tool slide is in the deck", bool(TOOLSLIDE))
ck("the slide names four operations", len(named) == 4, str(named))
for n in named:
    ck(f"{n} is defined in kg_tools.py", n in defined,
       f"kg_tools.py defines {sorted(defined)}")
# sec:five-operations is titled "The Five Operations, of Which Four Are
# Live": verify_triple is "not called by any node in the final design",
# so four is the right count and verify_triple is the wrong fourth.
ck("and not the one no node calls", "verify_triple" not in named)

# How many of them actually cap anything. Per operation body, because
# searching the whole file counts __init__, which is where max_relations
# is assigned.
bodies = dict(zip(re.findall(r"^    def (\w+)\(", tools, re.M),
                  re.split(r"^    def \w+\(", tools, flags=re.M)[1:]))
capped = [n for n in named
          if re.search(r"max_relations|max_fanout", bodies.get(n, ""))]
ck(f"{len(capped)} of the {len(named)} live tools truncate what they return",
   0 < len(capped) < len(named),
   f"{capped}, not {sorted(set(named) - set(capped))}")

# The third column's rows carry the two numeric limits, and its header
# generalises over all four. The values were pinned to the code and the
# header was not, so it could claim a cap for rows that name none --
# "Boolean; uncapped" and "Three-stage resolver" are not caps.
# app:toolapi says it correctly: "Two limits appear throughout".
numeric = [c for c in re.split(r"\\\\", TOOLSLIDE)
           if re.search(r"\\leq\s*\d+", c)]
ck(f"{len(numeric)} rows of the table name a numeric limit",
   len(numeric) == len(capped), f"{len(numeric)} rows, {len(capped)} capped")
colheads = re.findall(r"\\textbf\{([^}]*)\}", TOOLSLIDE)
ck("the table has a header for each column", len(colheads) == 4,
   str(colheads))
if len(colheads) == 4 and len(numeric) < len(named):
    ck("the last column does not claim a cap its rows do not have",
       "cap" not in colheads[3].lower(), f"header reads {colheads[3]!r}")

# The Node column is a claim about the program's topology, and it is the
# kind that rots silently: moving search_entity out of the planner would
# leave the slide asserting a shape the code no longer has, with nothing
# to say so. So it is derived, like every number on this deck, from the
# file that decides it -- the node functions themselves.
#
# capitalize() rather than a lookup table: the slide's labels ARE the node
# function names, and a mapping written here would be a second place for
# the answer to live.
print("\n== the tool slide's Node column is the call site ==")
NODEFN = {}
for mod in ("nodes.py", "planner.py"):
    # Per file. Concatenating them lets the tail of nodes.py run into
    # planner.py's module-level constants, which would attribute a call in
    # a prompt string to whichever node happened to be defined last.
    text = open(os.path.join(ROOT, "agr", mod), encoding="utf-8").read()
    chunks = re.split(r"^def (\w+)\(", text, flags=re.M)
    for fname, body in zip(chunks[1::2], chunks[2::2]):
        if fname.endswith("_node"):
            NODEFN[fname[:-len("_node")].capitalize()] = body
ck("the six node functions are in agr/", len(NODEFN) == 6, str(sorted(NODEFN)))
for op in named:
    callers = sorted(n for n, b in NODEFN.items()
                     if re.search(rf"\.{op}\(", b))
    ck(f"{op} is issued by exactly one node", len(callers) == 1, str(callers))
    if len(callers) == 1:
        label = "\\texttt{" + op.replace("_", "\\_") + "}"
        ck(f"the slide gives {op} to the {callers[0]}",
           cell(TOOLSLIDE, label, 1) == callers[0],
           f"slide says {cell(TOOLSLIDE, label, 1)!r}, agr/ says {callers[0]}")
# ...and the three that issue none are named as such, rather than left for
# the reader to work out from a column that only lists the other three.
silent = sorted(n for n, b in NODEFN.items()
                if not any(re.search(rf"\.{o}\(", b) for o in named))
ck(f"{len(silent)} nodes issue no graph call at all", len(silent) == 3,
   str(silent))
missing = [n for n in silent if n not in TOOLSLIDE]
ck("and the slide names each of them", not missing, str(missing))

# ---------------------------------------------------------------------
# The two bounds the "what structural does not mean" slide exists to say.
#
# paper_review_feedback.md records the asymmetry this frame was built to
# remove: the deck stated only the relevance limit -- a claim can be true
# and still be the wrong answer -- and never the relation limit, so if the
# committee had asked the supervisor's first question, the honest answer
# was on no slide. Both bounds now are, and nothing held them there. They
# have already been proposed for deletion once, on the reasonable-sounding
# ground that the slide was wordy; a bound is the last thing a crowded
# slide should give up, and the ground will sound just as reasonable next
# time.
#
# Checked on the slide AND in the spoken script, because a bound only on
# the slide is one the speaker can walk past without noticing.
print("\n== the structural bounds are stated, not just implied ==")
BOUNDS = frame(r"What \emph{structural} means --- and what it does not")
ck("the bounds frame is in the deck", bool(BOUNDS))
SAID = spoken(14)
for what, on_slide, in_script in (
        # Relation-blindness: supervisor issue 1. The mother/child pair is
        # the example the supervisor used and book Sec 6.8 repeats, so it
        # is checked as the example and not merely as the word "relation".
        ("the check does not read the relation",
         r"not the relation", r"read the relation|relation:"),
        ("...nor its direction", r"not its direction", r"either direction"),
        ("...with the mother/child example",
         r"mother.*child", r"mother.*child"),
        # Evidence contract: supervisor issue 2, the thesis's own "most
        # serious limitation". Sec 6.6 states it as two bolded sentences
        # and both are checked, because the slide once carried them as one
        # eleven-word clause that nobody could read.
        ("only one route records evidence",
         r"nothing attached|attaches? nothing|one route of three",
         r"attaches?\s+(the\s+)?triples|one route of three"),
        ("...and the log keeps the count, not the triples",
         r"keeps the \\emph\{count\}|keeps a count|count, not the",
         r"keeps a count|count, not the"),
        # The limit the deck already had. Kept in the list so a rewrite
        # cannot trade one bound for the other and still pass.
        ("a true claim can still be the wrong answer",
         r"wrong answer", r"wrong answer")):
    ck(f"the slide says {what}",
       re.search(on_slide, BOUNDS, re.I | re.S) is not None)
    ck(f"and the script says {what}",
       re.search(in_script, SAID, re.I | re.S) is not None)

# ---------------------------------------------------------------------
# The cycle count is whatever the diagram draws.
#
# The slide said "Two cycles" beside a diagram with three arrows returning
# to the Explorer -- continue, backtrack, retry -- and the script hardened
# it to "exactly two". The thesis caption says two and names two, but its
# own figure source calls the third one a cycle: "% backtracking cycle:
# evaluator to backtracker to explorer". A listener can count the arrows
# while the word is being said, so the deck is where it costs.
print("\n== the cycle count is what the diagram draws ==")
SM = frame("AGR: an explicit state machine")

# The node count, from the same diagram. START is a terminal, not a node
# of the machine, which is why box and vbox are counted and term is not.
nodes = len(re.findall(r"\\node\[v?box[,\]]", SM))
ck(f"the diagram draws {nodes} nodes", nodes in NUM, str(nodes))
if nodes in NUM:
    ck(f"the slide says {NUM[nodes]} nodes", f"{NUM[nodes]} nodes" in SM,
       f"diagram draws {nodes}")
    ck(f"the script says {NUM[nodes].lower()} nodes",
       re.search(rf"\b{NUM[nodes]} nodes\b", spoken(11), re.I) is not None)


def target(edge):
    """The last coordinate a tikz edge names -- where the arrow lands."""
    coords = re.findall(r"\(([^()]*)\)", edge)
    return coords[-1] if coords else ""


# A cycle is a flow edge landing back on the Explorer. The forward edge
# from the Planner lands there too and is not one.
edges = re.findall(r"\\draw\[flow\](.*?);", SM)
back = [e for e in edges if "expl" in target(e) and "plan" not in e]
ck("the state machine frame is in the deck", bool(edges))
ck(f"the diagram draws {len(back)} edges back to the Explorer",
   len(back) in NUM, f"{len(back)} of {len(edges)} flow edges")

m = re.search(r"(One|Two|Three|Four|Five) cycles(.*?)bounded by budgets", SM)
ck("the slide states a cycle count", m is not None)
if m and len(back) in NUM:
    ck(f"the slide says {NUM[len(back)]}, matching the diagram",
       m.group(1) == NUM[len(back)],
       f"slide says {m.group(1)}, diagram draws {len(back)}")
    # Naming them after the edge labels is what makes counting confirm the
    # sentence instead of contradicting it -- so the names have to be
    # labels the diagram actually carries.
    listed = re.findall(r"\\emph\{(\w+)\}", m.group(2))
    labels = set(re.findall(r"node\[lbl[^\]]*\]\s*\{(\w+)\}", SM))
    ck(f"the slide names {len(listed)} of them", len(listed) == len(back),
       f"names {listed}")
    ck("and every name is a label on the diagram",
       set(listed) <= labels, f"{sorted(set(listed) - labels)} not labelled")

s11 = spoken(11)
ck("the script does not harden the old count",
   re.search(r"exactly (?:one|two|three|four|five) cycles", s11, re.I) is None)
if len(back) in NUM:
    ck(f"the script also says {NUM[len(back)].lower()} cycles",
       re.search(rf"\b{NUM[len(back)].lower()} cycles\b", s11, re.I)
       is not None)

# The same diagram is drawn three times, and each copy's prose has to
# count what that copy draws. Correcting the deck to three left the deck
# as the outlier: the thesis caption still read "Two cycles exist" and
# the paper still said "with two cycles", against figure sources whose
# own comments call the third one a cycle. Each copy is held to its own
# tikzpicture rather than to the deck's number, so a diagram that changes
# in one document fails that document and not the other two.
print("\n== every copy of the state machine counts its own arrows ==")
# "Both cycles are bounded" is a count like any other, which is how the
# paper's caption stated two without ever writing the word.
WORD = {v.lower(): k for k, v in NUM.items()}
WORD["both"] = 2
COUNTED = re.compile(r"\b(" + "|".join(WORD) + r")\s+(?:\\emph\{)?cycles\b",
                     re.I)
for label, path in (("deck", os.path.join(HERE, "content-main.tex")),
                    ("thesis", os.path.join(ROOT, "thesis_book", "chapters",
                                            "framework.tex")),
                    ("paper", os.path.join(ROOT, "thesis_paper", "sections",
                                           "framework.tex"))):
    src = " ".join(uncomment(open(path, encoding="utf-8").read()).split())
    # The one picture that draws this machine. A file may hold several.
    pic = next((p for p in re.findall(
        r"\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}", src)
        if "(expl)" in p), "")
    ck(f"{label}: the state-machine figure is there", bool(pic))
    if not pic:
        continue
    ret = [e for e in re.findall(r"\\draw\[flow\](.*?);", pic)
           if "expl" in target(e) and "plan" not in e]
    ck(f"{label}: the diagram draws {len(ret)} arrows back to the Explorer",
       len(ret) in NUM, str(len(ret)))
    said = COUNTED.findall(src)
    ck(f"{label}: the prose counts the cycles", bool(said))
    wrong = [w for w in said if WORD[w.lower()] != len(ret)]
    ck(f"{label}: every count beside it says {NUM.get(len(ret), '?')}",
       not wrong,
       f"says {wrong[0]!r}, diagram draws {len(ret)}" if wrong else "")


# ---------------------------------------------------------------------
# The script's own internals: one backup numbering system, one protected
# set, and a bold count that matches what is bold.
#
# The script referred to backup slides two ways at once. "Go to Backup 1"
# and "(B2)" are ordinals; "Backup 4" was a page number, and the tables
# use pages. The file opens on a title page, so the two are off by one and
# an ordinal read resolves every reference one slide short -- "backup 4"
# lands on hedging rather than the census. That is a note consulted under
# pressure, which is when the wrong slide costs most.
print("\n== the script's own internals agree ==")
BACKUP = os.path.join(HERE, "content-backup.tex")
backup_titles = re.findall(r"\\begin\{frame\}\{Backup: ([^}]*)\}",
                           open(BACKUP, encoding="utf-8").read())
rows = re.findall(r"^\| (\d+) \| ([^|]+?) \| \"", MD, re.M)
ck(f"the backup table has a row per backup slide ({len(backup_titles)})",
   len(rows) == len(backup_titles), f"{len(rows)} rows")
ck("and the pages start at 2, after the title page",
   [int(p) for p, _ in rows] == list(range(2, len(backup_titles) + 2)),
   str([p for p, _ in rows]))


def stems(text):
    return {w[:5] for w in re.findall(r"[a-z]{4,}", text.lower())}


for (page, contents), title in zip(rows, backup_titles):
    ck(f"page {page} is {title!r}", bool(stems(contents) & stems(title)),
       f"table says {contents.strip()!r}")

ordinal = re.search(r"\bbackup\s+\d|\(B\d\)", MD, re.I)
ck("nothing refers to a backup slide by ordinal", ordinal is None,
   f"{ordinal.group(0)!r} -- say 'backup page N'" if ordinal else "")
for m in re.finditer(r"backup page (\d+)", MD, re.I):
    ck(f"backup page {m.group(1)} is a page the table lists",
       m.group(1) in [p for p, _ in rows])

# "The four bold slides" against three bold rows, and two lists of slides
# not to take time from that named different slides.
bold = [int(n) for n, _t in re.findall(r"^\| (\d+) \| (\*\*[^|]*\*\*) \|",
                                       MD, re.M)]
starred = [int(n) for n in re.findall(r"^## (\d+) [^\n]*★", MD, re.M)]
ck(f"the bold rows and the starred sections are the same {len(bold)}",
   bold == starred and bool(bold), f"{bold} vs {starred}")
if len(bold) in NUM:
    ck(f"the script calls them the {NUM[len(bold)].lower()} bold slides",
       re.search(rf"[Tt]he {NUM[len(bold)].lower()} \*\*bold\*\* slides", MD)
       is not None, f"{len(bold)} are bold")
# \s+ rather than a literal space: this file is hard-wrapped, and the
# first of these two lists had its numbers pushed onto the next line by an
# unrelated edit, which made the rule match one list and compare it with
# nothing.
protect = [set(re.findall(r"\d+", m.group(1)))
           for m in (re.search(r"never from\s+([^.]*)\.", MD),
                     re.search(r"Never compress\s+([^.]*)\.", MD)) if m]
ck("both lists of slides not to shorten name the same slides",
   len(protect) == 2 and protect[0] == protect[1],
   " vs ".join(str(sorted(p, key=int)) for p in protect))

# The census slide pools wrong with hedge and both datasets. Those are the
# thesis's own Total column, so the numbers are right -- but sec:taxonomy
# says three times that the two are "never pooled" and that "a pooled
# percentage would describe neither", and pooling hides the shape flip.
print("\n== the pooled census says it is pooled ==")
FH = J["failure_histogram"]
split = {ds: sum(FH[ds][k].get("composite_claim", 0) for k in ("wrong", "hedge"))
         for ds in ("webqsp", "cwq")}
census = frames("Every failure, read and labelled", "The echo attractor")
ck("the census slide says the totals are pooled",
   re.search(r"never pooled", census, re.I) is not None)
ck(f"and gives the shape flip, {split['webqsp']} against {split['cwq']}",
   re.search(rf"\${split['webqsp']}\$ on WebQSP against \${split['cwq']}\$ "
             rf"on CWQ", census) is not None,
   f"composite_claim is {split['webqsp']}/{split['cwq']}")
# The split census used to be offered here as "backup page 4". The main
# deck now names no backup page at all -- a slide that sends the audience
# to a file they cannot see reads as an admission, and the six backup
# slides are for answering questions, not for being advertised. Inverted
# into a rule so the reference cannot creep back: the split is still
# stated above, as the shape flip, which is the part that matters.
#
# content-main.tex alone, not FLAT: FLAT concatenates all three sources,
# and every frame in the backup deck is titled "Backup: ...", so the rule
# would fail on the file it is not about.
MAINONLY = " ".join(uncomment(
    open(os.path.join(HERE, "content-main.tex"), encoding="utf-8").read()
).split())
_bk = re.search(r".{0,40}backup.{0,40}", MAINONLY, re.I)
ck("the main deck sends nobody to a backup page", _bk is None,
   _bk.group(0) if _bk else "")

# ---------------------------------------------------------------------
# ...and the typeset transcript has to be the same script.
#
# transcript.tex is generated from transcript.md by build_transcript.py.
# Every other rule in this file reads the Markdown, which is why the .tex
# could sit nine sections behind through three resectionings with the whole
# suite green: it was the one artifact nothing looked at. Its own header
# said to regenerate it by hand, and by hand is how it went stale.
#
# Asked as "would regenerating change anything", so it is exact rather than
# a sample of properties -- and scoped to the generated body, so editing the
# preamble, which is still hand-authored, does not trip it.
print("\n== the typeset transcript is the same script ==")
GEN = os.path.join(HERE, "build_transcript.py")
if not os.path.exists(GEN):
    print("  [   ] build_transcript.py absent")
else:
    r = subprocess.run([sys.executable, GEN, "--check"],
                       capture_output=True, text=True, cwd=HERE)
    ck("transcript.tex matches transcript.md", r.returncode == 0,
       (r.stdout + r.stderr).strip().splitlines()[-1]
       if (r.stdout + r.stderr).strip() else "")

# ...and so does the speaking copy, which is the one that will be in your
# hand. Two renderings of one script is exactly the arrangement that let
# transcript.tex fall nine sections behind; the second one is checked from
# the day it exists rather than after it has drifted.
MIN = os.path.join(HERE, "build_min.py")
if not os.path.exists(MIN):
    print("  [   ] build_min.py absent")
else:
    r = subprocess.run([sys.executable, MIN, "--check"],
                       capture_output=True, text=True, cwd=HERE)
    ck("transcript-min.tex matches transcript.md", r.returncode == 0,
       (r.stdout + r.stderr).strip().splitlines()[-1]
       if (r.stdout + r.stderr).strip() else "")
# Both PDFs exist and are newer than the script they render. A .tex that
# matches while the PDF beside it was built two edits ago is the same
# staleness one level down, and the speaking copy is printed, not read
# from the source.
for pdf in ("transcript.pdf", "transcript-min.pdf"):
    p = os.path.join(HERE, pdf)
    ck(f"{pdf} is built and not older than transcript.md",
       os.path.exists(p) and
       os.path.getmtime(p) >= os.path.getmtime(os.path.join(
           HERE, "transcript.md")),
       "rebuild it" if os.path.exists(p) else "missing")

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
    # Off the built deck, not off a number kept here. WORDS is only for
    # the header sentence, which spells its body count out.
    WORDS = {20: "twenty", 30: "thirty", 40: "forty"}
    pages = None
    deck = os.path.join(HERE, os.path.splitext(DRIVERS[0])[0] + ".pdf")
    if pymupdf is not None and os.path.exists(deck):
        with pymupdf.open(deck) as d:
            pages = d.page_count
    if pages is None:
        print("  [   ] deck not measured -- row count checked against itself")
        ck("the table has a row per slide", len(rows) > 0, f"{len(rows)} rows")
    else:
        ck(f"the table has a row per slide ({pages} pages)",
           len(rows) == pages, f"{len(rows)} rows")
        # ...and the sentence that opens the file says the same thing.
        body = pages - 2                       # a title and a closing slide
        spelt = WORDS.get(body - body % 10, "") + \
            ("" if body % 10 == 0 else "-" + NUM[body % 10].lower())
        ck(f"the opening sentence says {pages} pages and {spelt} body slides",
           re.search(rf"{pages} pages: a title,\s+{spelt} body slides,"
                     rf"\s+a closing slide", md) is not None,
           f"deck is {pages} pages")

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

    # ...and every row is achievable at the rate the script claims for
    # itself. This is the rule the table lacked: its arithmetic was
    # checked three ways and never against the words, so a section could
    # grow by fifty words and stay green as long as the columns still
    # summed. Slide 19 reached 125 wpm against a stated 93 that way.
    #
    # The rate is read from the script rather than written down here, so
    # rehearsing at a different measured pace re-times the whole table
    # instead of quietly retiring the rule.
    #
    # Slack is allowed and is not flagged: a row legitimately holds time
    # for a pause or for letting a table land. Only the other direction
    # is a defect. The one-second tolerance is whole-second rounding of a
    # fractional requirement, nothing more.
    rate = re.search(r"(\d+)\s*wpm", md)
    ck("the script states its own speaking rate", rate is not None)
    if rate:
        wpm = int(rate.group(1))
        short = []
        for n in sorted(table, key=int):
            said = spoken(n)
            if not said:
                continue
            needs = len(said.split()) / wpm * 60
            if table[n] < needs - 1:
                short.append(f"slide {n}: {len(said.split())} words needs "
                             f"{needs:.0f}s, allotted {table[n]}s "
                             f"({round(len(said.split()) / table[n] * 60)} wpm)")
        ck(f"every row is achievable at {wpm} wpm", not short,
           f"{len(short)} row{'s' if len(short) > 1 else ''} short; "
           f"{short[0]}" if short else "")

    # The recovery marker names a slide and a cumulative, and they have to
    # be each other's. Nothing read this until it had been wrong twice:
    # first as a cumulative no row held at all, then as 15:05 against a
    # table saying 15:02, after a trim upstream moved every row after it.
    mk = re.search(r"If you hit \*\*(\d+):(\d\d) \(the end of slide (\d+)\)",
                   md)
    ck("the recovery notes name a marker", mk is not None)
    if mk:
        cum = dict((n, secs(mc, sc)) for n, _t, _a, _b, mc, sc in rows)
        ck(f"the marker's time is slide {mk.group(3)}'s cumulative",
           cum.get(mk.group(3)) == secs(mk.group(1), mk.group(2)),
           f"marker {mk.group(1)}:{mk.group(2)}, table "
           f"{cum.get(mk.group(3), 0) // 60}:"
           f"{cum.get(mk.group(3), 0) % 60:02d}")

    # The point of the budget is the limit it sits under.
    lim = re.search(r"against a (\d+)-minute limit", md)
    ck("the talk fits the limit it names",
       lim is not None and run <= int(lim.group(1)) * 60,
       f"{run}s vs {lim.group(1) if lim else '?'} min")

# ---------------------------------------------------------------------
# The deck's limitations are the thesis's, IN the thesis's order.
#
# Presence was checked and order was not, past the first item. Items 4
# and 5 had swapped against sec:limitations-final -- which opens "in
# order of severity", and which the slide's own comment claims to follow
# -- putting the candidate-width confound above the scoping of the whole
# evaluation. Ranked off the thesis headings, so a reordering there fails
# this until the slide follows.
print("\n== the deck's limitations keep the thesis's order ==")
RANKED = (("rejects", "wrongful acceptance"),
          ("detectable accuracy", "underpowered"),
          ("navigation", "structural grounding"),
          ("one environment", "single-environment"),
          ("candidate set", "narrower candidate set"))
order = []
for deck_key, head_key in RANKED:
    at = next((n for n, h in enumerate(LIMIT_HEADS) if head_key in h), None)
    ck(f"the thesis ranks {head_key!r}", at is not None)
    here = limits.find(deck_key)
    ck(f"the slide carries {deck_key!r}", here >= 0)
    if at is not None and here >= 0:
        order.append((here, at, deck_key))
order.sort()
swaps = [f"{y[2]!r} (thesis rank {y[1] + 1}) is listed below "
         f"{x[2]!r} (rank {x[1] + 1})"
         for x, y in zip(order, order[1:]) if x[1] > y[1]]
ck("the slide lists them in the thesis's severity order", not swaps,
   swaps[0] if swaps else "")

# ---------------------------------------------------------------------
# One deliberate wording divergence, said out loud.
#
# The slide writes contribution 6 as "pre-specified" where the thesis
# titles it "Pre-Registered", per the standing rule in
# thesis_paper/sections/setup.tex -- nothing was filed with a registry.
# That is a rigour point, and it read as a discrepancy: this is the one
# slide whose premise is that the six are the thesis's, in its order, and
# the script did not mention the change. Held only while the two
# documents actually differ, so reconciling either way retires the rule
# rather than leaving behind a check that cannot fail.
print("\n== the pre-specified wording is accounted for ==")
# The deck's own spelling is a rule, not a preference: the standing note
# in thesis_paper/sections/setup.tex says never "pre-registered", the
# slide comment repeats it, and section 30 now says it out loud. It was
# checked in none of the three -- CONTRIB_KEYS accepted either spelling,
# and the explanation rule below keyed off the deck, so a slide drifting
# back to the thesis's word ALSO switched off the rule that would have
# caught it. Keyed off the thesis now, which is the document that has
# not changed.
ck("the deck never writes pre-registered",
   "pre-registered" not in FLAT.lower(),
   "thesis_paper/sections/setup.tex fixes this spelling")
thesis_six = " ".join(intro[start:end].split()).lower()
if "pre-registered" in thesis_six:
    s30 = spoken(30)
    ck("the script names the thesis's word", "pre-registered" in s30.lower())
    ck("and the word the slide uses", "pre-specified" in s30.lower())
    ck("and gives the reason the slide diverges",
       re.search(r"registr(y|ies)", s30, re.I) is not None)
else:
    ck("the two documents still differ on this word", True,
       "reconciled -- rule retired")

# ---------------------------------------------------------------------
# Slide 13's hop curve, from the strata rather than from the figure.
#
# This was the last transcription in the deck bound to nothing. The
# numbers sit as prose beside a generated figure, so 0.46/0.55/0.57 could
# be corrupted to 0.96/0.95/0.97 with the whole suite still green -- and
# the shape claims around them ("the only system that ends above where it
# started", "three of the other four decay") are assertions about four
# other systems that no rule read at all.
print("\n== the hop curve is the strata ==")
TR = J["main_results"]["hop_trends"]["cwq"]
HOP = frame("RQ1: accuracy against hop count")
s21 = spoken(21)
agr = TR["agr"]["hits_at_1"]
arrow = r"\s*(?:\$?\\to\$?|\u2192|,)\s*".join(re.escape(f"{v}") for v in agr)
ck("the hop slide is in the deck", bool(HOP))
ck(f"the slide quotes AGR's CWQ curve {agr}",
   re.search(arrow, HOP) is not None, "in that order")
ck("the script quotes the same three", re.search(arrow, s21) is not None)

rising = TR["_systems_monotone_rising"]
ck("AGR is the only CWQ system that rises", rising == ["agr"], str(rising))
below = TR["_systems_ending_below_h1"]
ck(f"the other {len(below)} end below their one-hop score",
   sorted(below) == sorted(k for k in TR
                           if not k.startswith("_") and k != "agr"))
for label, text in (("slide", HOP), ("script", s21)):
    ck(f"the {label} says AGR alone ends above where it started",
       re.search(r"only\b[^.]*\bend(?:s|ing)? above where it started",
                 plain(text)) is not None)

falling = TR["_systems_monotone_falling"]
ck(f"{len(falling)} of the other four decay monotonically",
   len(falling) in NUM, str(sorted(falling)))
decay = re.compile(NUM[len(falling)] + r" of the other (\w+) decay", re.I)
for label, text in (("slide", HOP), ("script", s21)):
    m = decay.search(plain(text))
    ck(f"the {label} says {NUM[len(falling)].lower()} of the others decay",
       m is not None)
    if m:
        ck(f"and puts the others at {NUM[len(below)].lower()}",
           WORD.get(m.group(1).lower()) == len(below), f"says {m.group(1)!r}")

# The exception to the monotonicity, and by how much it misses.
net = TR["tog"]["net_hits_at_1"]
ck("ToG's CWQ curve is neither rising nor falling throughout",
   not TR["tog"]["monotone_falling"] and not TR["tog"]["monotone_rising"])
ck(f"the script says it ends {abs(net)} below its one-hop score",
   re.search(r"(?<![\d.])" + re.escape(str(abs(net)))
             + r"(?![\d.])[^.]*below its own one-hop", s21) is not None,
   f"hop_trends gives {net}")

# The strata the answer rests on, from the stratum table.
n = [J["main_results"]["by_hop_stratum"]["cwq/agr"][k]["n"]
     for k in ("h1", "h2", "h3plus")]
a4 = answer("n=4 in the three-hop WebQSP stratum")
# (?!\.\d) rather than (?![\d.]): the strata are spoken as "137, 211, and
# 49." and a plain token guard rejects the full stop that ends the
# sentence, while still having to reject the 49 inside 49.5.
ck("the n=4 answer names the CWQ strata",
   bool(a4) and all(re.search(rf"(?<![\d.]){v}(?!\d)(?!\.\d)", a4)
                    for v in n), str(n))

# ---------------------------------------------------------------------
# Two thesis limitations that reached neither document.
#
# sec:limitations-final lists eight and the slide carries five. #6 is
# answered under the GraphRAG question; #7 and #8 appeared nowhere in the
# deck or the script. #7 is a standard KGQA question with a one-line
# answer, and #8 only makes the reported numbers a floor -- both cheaper
# volunteered than extracted. Their ordinals are ranked above with the
# candidate-width one; what is checked here is the substance.
print("\n== limitations 7 and 8 reach the Q&A ==")
link = answer("topic entities come from")
CFG = open(os.path.join(ROOT, "agr", "config.py"), encoding="utf-8").read()
gold = re.search(r"use_gold_entities: bool = (True|False)", CFG)
ck("config.py sets use_gold_entities", gold is not None)
if gold:
    # The answer's whole premise is that this is on. Flip it and "they
    # are given by the datasets" stops being true.
    ck("mentions really do come from the dataset", gold.group(1) == "True",
       f"config says {gold.group(1)}")
    ck("the answer names the flag", "use_gold_entities" in link)
    ck("and the operation that resolves them to nodes",
       "search_entity" in link)
# Which systems the assumption binds. Vector-RAG and the parametric
# control never read the annotation, so claiming all five share it would
# be wrong in the other direction.
seeded = {b for b in ("tog", "graphrag", "vectorrag", "noretrieval")
          if "gold_q_entities" in open(
              os.path.join(ROOT, "agr", "baselines", b + ".py"),
              encoding="utf-8").read()}
ck("two baselines seed from the annotation", seeded == {"tog", "graphrag"},
   str(sorted(seeded)))
# Named, not described as "the static baselines": the deck calls GraphRAG
# "Static GraphRAG" on slides 2 and 10, and the answer names it two
# clauses earlier as one of the three that DO seed from the annotation.
ck("the answer names the two systems that seed from the annotation",
   all(k in link for k in ("Think-on-Graph", "GraphRAG")))
ck("and names the two that do not, rather than grouping them",
   "parametric control" in link and "Vector-RAG" in link
   and "static baselines" not in link)

# The extraction bug, counted from the committed label sheets -- the same
# files scripts/synthesize_census.py merges into the census.
SHEETS = [os.path.join(ROOT, "results", "phase4", f) for f in
          ("labels_webqsp.csv", "labels_cwq.csv", "labels_cwq_dropped.csv")]
SHEETS += [os.path.join(ROOT, "results", "phase4", "ablations",
                        "noplanner_categories_" + d + ".csv")
           for d in ("webqsp", "cwq")]
rows = [r for f in SHEETS if os.path.exists(f)
        for r in csv.DictReader(open(f, encoding="utf-8"))]
decomp = [r for r in rows if r["category"] == "decomposition_error"]
bug = [r for r in decomp if r["subtype"] == "extraction_bug"]
ck(f"the label sheets hold {len(decomp)} decomposition_error cases",
   len(decomp) == sum(J["failure_histogram"][d][k]["decomposition_error"]
                      for d in ("webqsp", "cwq") for k in ("wrong", "hedge")),
   "sheets vs the histogram")
ck(f"{len(bug)} of them carry the extraction_bug subtype", len(bug) in NUM)

ebug = answer("Nine of your failures")
ck("the extraction-bug question is prepared", bool(ebug))
if ebug:
    # \b on the number word as well as the digits. The digits were
    # guarded and the word was not, so "Nineteen of the 38" passed: Nine
    # matched inside it and \D{0,24} swallowed "teen of the ".
    ck(f"the answer says {NUM[len(bug)].lower()} of {len(decomp)}",
       re.search(r"\b" + NUM[len(bug)] + r"\b\D{0,24}(?<![\d.])"
                 + str(len(decomp)) + r"(?![\d.])", ebug, re.I) is not None,
       f"the sheets give {len(bug)} of {len(decomp)}")
    # The specimen, read from the sheet rather than from the prose.
    spec = next((r for r in bug if r["qid"] in ebug), None)
    ck("the answer names a labelled instance", spec is not None)
    if spec:
        m = re.search(r"only the subject '([^']+)'", spec["note"])
        ck("and the entity that question actually scored",
           m is not None and m.group(1) in ebug,
           f"{spec['qid']} scored {m.group(1) if m else '?'}")
    # The direction is the point: it costs AGR accuracy, not the baselines.
    ck("the answer says which way it cuts", "floor" in ebug)


# ---------------------------------------------------------------------
# The event card's prose.
#
# It reaches more people than the deck, the paper and the thesis put
# together, and it is read by people who will never open any of them. Its
# numbers come out of thesis_numbers.json and cannot drift; its prose is
# typed, and three sentences of it were wrong. Nothing here read it: the
# deck's SOURCES is its own three files, and the output-contract test is
# the only other rule that reaches the card at all.
#
# Each rule below asks the source, not the spelling. thumbnail.tex is
# generated -- a correction belongs in the template in
# thumbnail/build_thumbnail.py, and the file here is what that produced.
print("\n== the event card's prose ==")
CARDF = os.path.join(ROOT, "thumbnail", "thumbnail.tex")
if not os.path.exists(CARDF):
    print("  [   ] thumbnail.tex absent -- run thumbnail/build_thumbnail.py")
else:
    CARD = " ".join(uncomment(open(CARDF, encoding="utf-8").read()).split())

    def cell(value):
        """The one brace group on the card holding this value."""
        hits = [g for g in re.findall(r"\{([^{}]*)\}", CARD) if value in g]
        return hits[0] if len(hits) == 1 else ""

    # -- the 57 are not all label errors ---------------------------
    # goldnoise_summary counts them separately before the census and the
    # label sheets carry ambiguous_question inside it. The thesis keeps
    # the two apart deliberately -- they "carry opposite evidence
    # signatures" -- and titles the section "Gold Noise and Ambiguous
    # Questions". Saying "gold labels were wrong" of all 57 is wrong
    # about 22 of them.
    GN = json.load(open(os.path.join(ROOT, "results", "phase4",
                                     "goldnoise_summary.json"),
                        encoding="utf-8"))
    amb = sum(GN[d]["ambiguous_questions"] for d in ("webqsp", "cwq"))
    amb += sum(1 for r in rows if r["category"] == "ambiguous_question")
    total = J["benchmark_defects"]["distinct_questions"]
    ck(f"{amb} of the {total} benchmark defects are ambiguous questions",
       0 < amb < total, f"{amb} of {total}")
    ck("the card does not call all of them wrong labels",
       re.search(r"gold labels?[^.]{0,20}(?:were|are|was)?\s*wrong"
                 r"|wrong gold labels?", CARD, re.I) is None,
       "22 of the 57 are ambiguous questions, not label errors")

    # -- how many tools actually carry a cap -----------------------
    # get_relations truncates to max_relations and get_neighbors passes a
    # cap into its query. verify_connection returns two booleans, and
    # search_entity takes a caller's k. "No free-form queries" is the
    # claim all four support, and the card makes it.
    #
    # Held over the script as well as the card. Section 6 said "four
    # operations with fixed signatures and hard caps" and was left open
    # one round on the grounds that rewording a rehearsed line costs
    # speaking time -- which had it backwards: the fix was deleting three
    # words, and the timing rule only flags rows SHORT of their words, so
    # slide 6 keeps its slack and the table does not move.
    # `capped` and `named` come from the tool-slide block above, which is
    # where the count belongs; this is the third artifact held to it.
    # Both spellings, because the two artifacts count differently: the
    # card writes "4 tools" and the script says "four operations".
    allcaps = re.compile(rf"(?:{len(named)}|{NUM[len(named)]})\s+"
                         rf"(?:tools|operations)[^.]{{0,40}}hard caps", re.I)
    # spoken(8) until now, which is the state-machine section and has
    # never made this claim -- an earlier bulk renumber moved the
    # number without moving the rule. Section 12 is the tools section.
    for label, text in (("card", CARD), ("script", spoken(12))):
        ck(f"the {label} does not claim a cap on all of them",
           allcaps.search(text) is None,
           f"only {len(capped)} of {len(named)} cap anything")

    # -- the hedge rate counts questions ---------------------------
    # scripts/score_test.py takes `not pred` over per-question rows, so
    # hedge_pct is a share of questions -- and a hedge is by definition
    # not an answer, which made "of answers" contradict itself.
    ST = open(os.path.join(ROOT, "scripts", "score_test.py"),
              encoding="utf-8").read()
    ck("hedge_pct is a share of questions, from score_test.py",
       re.search(r"sum\(r\['hedge'\] for r in rows\)\s*/\s*n", ST)
       is not None)
    hedge = f"{J['main_results']['by_system']['webqsp/agr']['hedge_pct']}"
    line = cell(hedge)
    ck("the card's hedge line is on the card", bool(line), hedge)
    if line:
        ck("and counts questions rather than answers",
           "questions" in line and "answers" not in line, line[:70])


print("\n" + ("ALL SLIDE NUMBERS MATCH THEIR SOURCE"
              if ok else "SOMETHING DOES NOT MATCH"))
sys.exit(0 if ok else 1)
