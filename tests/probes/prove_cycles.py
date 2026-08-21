"""Prove the stated cycle count is held to the diagram that is drawn.

Cases 1-2 reinstate the shipped wording: "Two cycles" on the slide and
"There are exactly two cycles" in the script, beside a diagram with three
arrows returning to the Explorer. The thesis caption says two and names
two, but its own figure source calls the third one a cycle -- "%
backtracking cycle: evaluator to backtracker to explorer" -- so the count
was inherited. The deck is where a listener can count the arrows while the
word is being said.

Cases 3-4 move the diagram under a sentence that does not follow, in both
directions. Cases 5-6 break the naming that makes counting confirm the
sentence: a name the diagram does not label, and fewer names than cycles.
Case 7 desynchronises slide and script.

Deck and transcript are restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
DECK = ROOT / "thesis_presentation" / "content-main.tex"
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (DECK, SCRIPT)
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


CURRENT = (r"Three cycles --- \emph{continue}, \emph{backtrack}, "
           r"\emph{retry} --- all bounded by budgets rather than by model "
           r"behaviour.")
RETRY_EDGE = (r"\draw[flow] (ver.west) -- ++(-28mm,0) node[lbl, below, "
              r"pos=0.5] {retry} |- ([yshift=-1.8mm] expl.west);")

CASES = [
    ("shipped: the slide says two beside three arrows",
     edit(DECK, CURRENT,
          r"Two cycles, both bounded by budgets rather than by model "
          r"behaviour.")),
    ("shipped: the script hardens it to exactly two",
     edit(SCRIPT, "There are three cycles — the three arrows going back to the "
                  "Explorer: continue, backtrack, retry.",
          "There are exactly two cycles — explorer-to-evaluator, and verifier "
          "back to explorer.")),
    ("an arrow is removed and the sentence does not follow",
     edit(DECK, RETRY_EDGE, "")),
    ("an arrow is added and the sentence does not follow",
     edit(DECK, RETRY_EDGE,
          RETRY_EDGE + r" \draw[flow] (ans.west) -- (expl.west);")),
    ("the slide names a cycle the diagram does not label",
     edit(DECK, r"\emph{continue}", r"\emph{restart}")),
    ("the slide names fewer cycles than it counts",
     edit(DECK, r"\emph{continue}, \emph{backtrack}, \emph{retry}",
          r"\emph{continue}, \emph{backtrack}")),
    ("slide and script disagree on the count",
     edit(SCRIPT, "There are three cycles", "There are two cycles")),
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
