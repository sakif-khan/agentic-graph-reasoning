"""Prove check_slides.py catches the retracted GraphRAG paradigm claim.

Case 1 reinstates the shipped section 11 verbatim: "look at vector RAG and
GraphRAG on ComplexWebQuestions -- 0.203 and 0.205, below the no-retrieval
control at 0.307. On genuinely multi-hop questions, single-shot retrieval
is worse than not retrieving at all", on the slide marked "Slow down
here". The thesis refuses that pooling in the same paragraph as the
numbers, and the paper retracted it in two commits.

Cases 2-3 are the same defect pooled the other way round and attributed to
GraphRAG alone, which is why the rule is bound to the sentence. Cases 4-5
remove the half that makes the retraction usable -- which baseline carries
the claim, and why the other does not. Case 6 drops the thesis's own
refusal, which is what the deck's caveat answers to. Cases 7-10 corrupt
the strata and the fanout bound from both ends.

Every file is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
RES = ROOT / "thesis_book" / "chapters" / "results.tex"
FIG = ROOT / "thesis_book" / "figures" / "fig_hop_strata.tex"
GRAPHRAG = ROOT / "agr" / "baselines" / "graphrag.py"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (SCRIPT, RES, FIG, GRAPHRAG)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0] if fail else r.stdout.strip()[-90:])


def edit(path, old, new):
    """Substitute, tolerating rewrap and the transcript's '>' markers."""
    def go():
        gap = r"\s+(?:>\s*)?"
        pattern = re.compile(gap.join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


# The spoken paragraph as it shipped, and as it reads now.
SHIPPED = ("First, look at vector RAG and GraphRAG on ComplexWebQuestions "
           "— 0.203 and 0.205, *below* the no-retrieval control at 0.307. "
           "On genuinely multi-hop questions, single-shot retrieval is worse "
           "than not retrieving at all. It fills the context with plausible "
           "but wrong material.")
CURRENT = ("First, vector RAG on ComplexWebQuestions — 0.203, *below* the "
           "no-retrieval control at 0.307. One verbalised triple cannot "
           "contain a chain, so single-shot retrieval is worse there than not "
           "retrieving at all. GraphRAG is beside it at 0.205, but its "
           "one-hop radius confounds the paradigm, so the claim rests on "
           "vector RAG.")

CASES = [
    ("shipped: the two static baselines pooled under the claim",
     edit(SCRIPT, CURRENT, SHIPPED)),
    ("pooled the other way round",
     edit(SCRIPT, CURRENT,
          "First, GraphRAG and vector RAG on ComplexWebQuestions are both "
          "below the no-retrieval control at 0.307.")),
    ("the claim credited to GraphRAG alone",
     edit(SCRIPT, CURRENT,
          "First, GraphRAG at 0.205 shows single-shot retrieval is worse "
          "than not retrieving at all.")),
    ("the script stops naming which baseline carries it",
     edit(SCRIPT, "so the claim rests on vector RAG.",
          "so I would not lean on it.")),
    ("and stops saying why the other does not",
     edit(SCRIPT, "but its one-hop radius confounds the paradigm",
          "but it is a different retriever")),
    ("the thesis drops its own refusal",
     edit(RES, "the weaker evidence of the two: it confounds the paradigm "
               "with the radius",
          "further evidence of the same thing")),
    # The strata, from both ends.
    ("the figure moves and the script does not follow",
     edit(FIG, "color=agrGraph, very thick] coordinates {(0,0.3) (1,0.44) "
               "(2,0.25)}",
          "color=agrGraph, very thick] coordinates {(0,0.3) (1,0.55) "
          "(2,0.25)}")),
    ("a stratum drifts in the spoken answer",
     edit(SCRIPT, "against 0.16 on", "against 0.26 on")),
    # The fanout bound, from both ends.
    ("GraphRAG's fanout cap changes in code",
     edit(GRAPHRAG, "fanout_cap=100", "fanout_cap=150")),
    ("the share of questions above that degree drifts",
     edit(SCRIPT, "on 72.5 percent of questions at least one topic entity",
          "on 62.5 percent of questions at least one topic entity")),
]

out = []
try:
    for name, mutate in CASES:
        mutate()
        rc, first = run()
        out.append((name, rc, first))
        restore()
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{first[:96]}")

rc, first = run()
print(f"\nrestored -> rc={rc}  ({first[:70]})")
passed = all(rc for _, rc, _ in out) and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
