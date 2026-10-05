"""Prove the rules added after the October 2026 review of the deck fire.

The review read the deck against the book and found defects that
check_slides.py had passed: every one of them shipped. Each case below
reinstates one, verbatim where the old wording survives in git, and asserts
the checker now fails on it.

  1-2  RoG's training splits as 2,830 and 16,900, on the backup slide and in
       the spoken answer. The thesis says 2,826 and 27,639.
  3    The defect breakdown as "17 found inside the census, 1 counted in
       both". The JSON says 16 and none; "16" was matched inside "16.5%".
  4    "All 256" over a census column summing to 220.
  5-6  The Backtracker as an undo, on the slide and in the script. The
       thesis says popping the most recent snapshot "would make
       backtracking a simple undo", and it pops the highest-scoring one.
  7-8  The worked example's counter printed as a count rather than a bound,
       and one relation "taken" where each Explorer pass kept three.
  9    A McNemar bound read off the book's rounded figure, which the largest
       p exceeds by 0.00002.
  10   A slide inserted ahead of the results while the script keeps its
       numbering: the rehearsal and the deck come apart.
  11   The dashed panel explained with the wrong n.

Every file is restored in a finally block.
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


CASES = [
    ("shipped: RoG's training splits as 2,830 and 16,900 on the slide",
     edit(DECK, r"$2{,}826$ and $27{,}639$ questions",
          r"$2{,}830$ and $16{,}900$ questions")),
    ("shipped: the same two sizes in the spoken answer",
     edit(SCRIPT, "2,826 WebQSP and 27,639 CWQ questions",
          "2,830 WebQSP and 16,900 CWQ questions")),
    ("shipped: 17 inside the census, 1 counted in both",
     edit(DECK, r"\item $16$ more found inside it, as gold-noise or "
                r"ambiguous rows \item No question counted in both",
          r"\item $17$ found inside the census \item $1$ counted in both")),
    ("shipped: All 256 over a column summing to 220",
     edit(DECK, r"\midrule Six smaller categories & 36 \\", "")),
    ("shipped: the slide calls the Backtracker an undo",
     edit(DECK, r"\textbf{Backtracker}: best earlier frontier, ban list",
          r"\textbf{Backtracker}: undo + ban list")),
    ("shipped: the script says it undoes a bad expansion",
     edit(SCRIPT, "The backtracker returns to the best-scoring earlier "
                  "frontier and bans the edges that failed.",
          "The backtracker undoes a bad expansion and bans the edge that "
          "caused it.")),
    ("shipped: the counter printed as a count of triples",
     edit(DECK, r"at most $18$ supporting triples",
          r"$18$ supporting triples")),
    ("shipped: one relation taken where three were kept",
     edit(DECK, r"keeps three relations. The best is\\",
          r"scores relations, takes\\")),
    ("a significance bound read off a rounded figure",
     edit(DECK, r"($p < 0.004$)", r"($p \leq 0.0035$)")),
    ("a slide inserted before the results, the script not renumbered",
     edit(DECK, r"\begin{frame}{Main results}",
          "\\begin{frame}{An inserted slide}\n\\end{frame}\n"
          r"\begin{frame}{Main results}")),
    ("the dashed panel explained with the wrong n",
     edit(DECK, r"Dashed: $n = 4$ at 3+.", r"Dashed: $n = 5$ at 3+.")),
]

rc, first = run()
assert rc == 0, f"not clean before the probe: {first}"

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
