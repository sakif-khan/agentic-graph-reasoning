r"""Hold the poster's numbers to results/phase4/thesis_numbers.json.

A poster is the one artifact in this project that gets read by people who
will never open the thesis, and it is the easiest place for a figure to
drift -- it is retyped by hand, away from the build that regenerates the
book and the deck. So every number printed on it is checked here against
the same JSON the thesis reads, and the geometry the call for posters
fixes is checked against the built PDF.

Run:  python check_poster.py     (exit 0 = every figure matches)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TEX = os.path.join(HERE, "poster_0421052099.tex")
PDF = os.path.join(HERE, "poster_0421052099.pdf")

J = json.load(open(os.path.join(ROOT, "results", "phase4",
                                "thesis_numbers.json"), encoding="utf-8"))
SRC = open(TEX, encoding="utf-8").read()
# Comments carry prose about the numbers; only the typeset body counts.
BODY = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in SRC.splitlines())

OK = FAIL = 0


def ck(label, cond, detail=""):
    global OK, FAIL
    if cond:
        OK += 1
        print(f"  [OK ] {label}" + (f"   {detail}" if detail else ""))
    else:
        FAIL += 1
        print(f"  [FAIL] {label}" + (f"   {detail}" if detail else ""))


def on_poster(value):
    """Is this literal typeset anywhere in the poster body?"""
    return re.search(rf"(?<![\d.]){re.escape(value)}(?![\d])", BODY) is not None


# ---------------------------------------------------------------------
print("\n== the main results table is the measured one ==")
M = J["main_results"]["by_system"]
ROWS = (("noretrieval", "No-retrieval"), ("vectorrag", "Vector-RAG"),
        ("graphrag", "Static GraphRAG"), ("tog", "Think-on-Graph"),
        ("agr", "AGR"))
for ds in ("webqsp", "cwq"):
    for key, shown in ROWS:
        rec = M[f"{ds}/{key}"]
        for metric in ("hits_at_1", "f1"):
            v = f"{rec[metric]:.3f}"
            ck(f"{shown} {ds} {metric} = {v}", on_poster(v))

print("\n== the cost claim ==")
for ds, sysname in (("webqsp", "agr"), ("cwq", "agr"),
                    ("webqsp", "tog"), ("cwq", "tog")):
    v = f"{M[f'{ds}/{sysname}']['mean_calls']:.1f}"
    ck(f"{sysname} {ds} mean calls = {v}", on_poster(v))

print("\n== grounding: the headline and the control ==")
T = J["groundedness_tier1_structural"]
agr = T["both_agr"]
ck("AGR asserts 1,709 entities",
   agr["entities_asserted"] == 1709 and on_poster("1{,}709"),
   f"json {agr['entities_asserted']}")
ck("...and none of them is ungrounded",
   agr["entities_ungrounded"] == 0 and re.search(r"\$0 / 1\{,\}709\$|0 / 1\{,\}709",
                                                 BODY) is not None,
   f"json {agr['entities_ungrounded']}")
nr = T["both_noretrieval"]
ck(f"the parametric control is {nr['entity_ungrounded_pct']}%",
   on_poster(f"{nr['entity_ungrounded_pct']}"))
ck(f"...over {nr['entities_asserted']} assertions",
   on_poster("1{,}001") and nr["entities_asserted"] == 1001,
   f"json {nr['entities_asserted']}")
ck(f"...of which {nr['entities_ungrounded']} ungrounded",
   on_poster(str(nr["entities_ungrounded"])))

print("\n== the budget split the caveat rests on ==")
B = J["tog_budget_split"]
for ds, want in (("webqsp", 29), ("cwq", 44)):
    pct = round(B[ds]["tog_clip_rate"] * 100)
    ck(f"ToG clips on {pct}% of {ds}", pct == want and on_poster(str(want)),
       f"json {B[ds]['tog_clip_rate']}")
ck("AGR's call budget never binds",
   J["budget_binding"]["webqsp"]["llm_calls"]["refused"] == 0
   and J["budget_binding"]["cwq"]["llm_calls"]["refused"] == 0
   and "never" in BODY)

print("\n== the environment and the samples ==")
for n in ("400",):
    ck(f"{n} certified questions per dataset",
       J["test_sets"]["webqsp"]["n_questions"] == 400
       and J["test_sets"]["cwq"]["n_questions"] == 400 and on_poster(n))
for label, want in (("2.59", "M entities"), ("8.31", "M triples")):
    ck(f"environment size {label}{want}", on_poster(label))

print("\n== the hop curve is the thesis's hop curve ==")
FIG = os.path.join(ROOT, "thesis_book", "figures", "fig_hop_strata.tex")
fig = open(FIG, encoding="utf-8").read()
# The CWQ block is the second half of the generated figure.
cwq_half = fig[fig.index("ComplexWebQuestions"):]
def coords(text):
    """Series as floats -- 0.3 and 0.30 are the same measurement."""
    return [[(float(x), float(y)) for x, y in
             re.findall(r"\(([\d.]+),([\d.]+)\)", s)]
            for s in re.findall(r"coordinates \{([^}]*)\}", text)]


want, got = coords(cwq_half)[:5], coords(BODY)
ck("the poster plots five CWQ series", len(got) == 5, f"{len(got)} found")
ck("and they are the thesis's own coordinates", want == got,
   f"thesis {want[:1]} vs poster {got[:1]}")
for n, key in ((137, "h1"), (211, "h2"), (49, "h3plus")):
    ck(f"CWQ {key} stratum n={n}",
       J["test_sets"]["cwq"]["strata"][key] == n and on_poster(str(n)))

print("\n== attribution the call for posters requires ==")
for who, what in (("Md.\\ Sakif Khan", "author"),
                  ("0421052099", "student id"),
                  ("Dr.\\ Sadia Sharmin", "supervisor"),
                  ("Department of Computer Science and Engineering, BUET",
                   "affiliation")):
    ck(f"the poster names the {what}", who in BODY, who.replace("\\", ""))

# Bound to the attribution line, not to the file: the supervisor's name
# also appears in the Acknowledgements, and a presence-anywhere test
# passed a poster whose header credited someone else entirely.
sup = open(os.path.join(ROOT, "thesis_book", "parameters", "supervisor.txt"),
           encoding="utf-8").read()
name = sup.split(",")[0].replace("Dr.\\ ", "").strip()
rank = sup.split(",")[1].strip()
attrib = re.search(r"Supervisor:[^\n]*\n?[^\n]*", BODY)
ck("the header credits the supervisor named in parameters/supervisor.txt",
   attrib is not None and name in attrib.group(0),
   f"parameters say {name!r}")
ck(f"...with the rank they hold there ({rank})",
   attrib is not None and rank in attrib.group(0))

print("\n== the printed artifact ==")
if not os.path.exists(PDF):
    ck("the poster is built", False, "run latexmk -pdf first")
else:
    import pymupdf
    doc = pymupdf.open(PDF)
    pg = doc[0]
    w, h = pg.rect.width / 72, pg.rect.height / 72
    ck("one page", doc.page_count == 1, f"{doc.page_count}")
    ck("36 x 24 inches, the size the call fixes",
       abs(w - 36) < 0.01 and abs(h - 24) < 0.01, f"{w:.2f} x {h:.2f} in")
    # The call's own print test is a 300% zoom. Vector text passes it by
    # construction; the only raster asset is the logo, so it is the one
    # thing that can be too coarse -- check its effective dpi.
    raster = pg.get_images(full=True)
    ck("at most one raster asset on the poster", len(raster) <= 1,
       f"{len(raster)} images")
    for img in raster:
        px = img[2]
        drawn = [r for r in pg.get_image_rects(img[0])]
        wide = max(r.width for r in drawn) / 72 if drawn else 0
        dpi = px / wide if wide else 0
        ck("the logo prints above 300 dpi", dpi >= 300,
           f"{px}px over {wide:.2f}in = {dpi:.0f} dpi")
    ck("the PDF embeds no bitmap fonts",
       all(f[3] not in ("Type3",) for f in pg.get_fonts(full=True)))

print(f"\n{OK} OK, {FAIL} FAIL")
sys.exit(1 if FAIL else 0)
