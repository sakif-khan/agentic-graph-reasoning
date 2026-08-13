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

print("\n" + ("ALL SLIDE NUMBERS MATCH THEIR SOURCE"
              if ok else "SOMETHING DOES NOT MATCH"))
sys.exit(0 if ok else 1)
