"""Prove check_slides.py catches the fairness slide denying a confound.

Case 1 reinstates the shipped right-hand column verbatim: "attributable to
architecture, not to model capacity or to a bigger retrieval budget", with
no mention anywhere on the slide of the one thing that is not equal. Case 2
is the same defect worded differently, which is why the rule is bound to
the attribution clause and not to the phrase. Case 3 is the spoken copy.

Cases 4-5 cover a disclosure that invites the wrong inference -- widths
named, but not which way they cut -- and the anticipated-questions entry
going missing. Cases 6-8 are the presence-matching trap: the widths now
have two homes on the deck, so "40/20 appears somewhere" would pass a deck
that had dropped either one.

Cases 9-11 corrupt the five measured binding rates the spoken answer
quotes, from both ends -- the script drifting, and the measurement moving
under a script that does not follow. Cases 12-13 do the same for the
ordinal it gives that limitation.

Deck, transcript, tog.py, conclusion.tex and thesis_numbers.json are
restored in a finally block.
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
TOG = ROOT / "agr" / "baselines" / "tog.py"
CONC = ROOT / "thesis_book" / "chapters" / "conclusion.tex"
NUMS = ROOT / "results" / "phase4" / "thesis_numbers.json"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (DECK, SCRIPT, TOG, CONC, NUMS)
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
    """Substitute, tolerating the rewrap that hard-wrapped sources undergo.

    The deck is wrapped to a column and transcript.md is a markdown
    blockquote, so a literal anchor stops matching the moment a line moves
    and the probe goes quietly blind. '>' is not whitespace: the gap has to
    admit it explicitly.
    """
    def go():
        gap = r"\s+(?:>\s*)?"
        pattern = re.compile(gap.join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


def deck_edits(*pairs):
    """Two edits to the deck in one case, composed rather than each on orig."""
    def go():
        text = orig[DECK]
        for old, new in pairs:
            gap = r"\s+(?:>\s*)?"
            pattern = re.compile(gap.join(re.escape(w) for w in old.split()))
            assert pattern.search(text), f"anchor gone: {old!r}"
            text = pattern.sub(lambda _: new, text, count=1)
        io.open(DECK, "w", encoding="utf-8", newline="").write(text)
    return go


# The shipped column, verbatim from the commit that had it.
SHIPPED_CLAIM = (r"Differences are attributable to \textbf{architecture}, "
                 r"not to model capacity or to a bigger retrieval budget.")
CURRENT_CLAIM = (r"Differences are attributable to \textbf{architecture}, "
                 r"not to model capacity or spend.")
DISCLOSURE = (r"\begin{block}{What is \emph{not} held equal} \small ToG prunes "
              r"to $40$/$20$ candidates per step, AGR to $300$/$200$ --- "
              r"\alert{narrower is cheaper}, so it cannot explain ToG's "
              r"clipping, but its unclipped score is a \alert{lower bound}. "
              r"\end{block}")

CASES = [
    ("shipped: denies a retrieval-budget control, widths absent",
     deck_edits((CURRENT_CLAIM, SHIPPED_CLAIM), (DISCLOSURE, ""))),
    ("the same denial, worded as candidate parity",
     edit(DECK, CURRENT_CLAIM,
          r"Differences are attributable to \textbf{architecture}, not to "
          r"model capacity and not to a bigger candidate set.")),
    ("the spoken copy keeps the retrieval-budget claim",
     edit(SCRIPT, "capacity or to spend. One thing is *not* equal",
          "capacity or to somebody getting a bigger retrieval budget. "
          "One thing is *not* equal")),
    ("widths disclosed, but not which way they cut",
     edit(DECK, r"--- \alert{narrower is cheaper}, so it cannot explain ToG's "
                r"clipping, but its unclipped score is a \alert{lower bound}.",
          r"--- a difference of configuration.")),
    ("the anticipated-questions entry goes missing",
     edit(SCRIPT, '**"Did both systems see the same candidate sets?"**',
          '**"An unrelated question."**')),
    # The two-homes trap. Either of these passed the old whole-deck check.
    ("widths dropped from the fairness slide, kept on slide 21",
     edit(DECK, r"ToG prunes to $40$/$20$ candidates per step, AGR to "
                r"$300$/$200$",
          r"ToG prunes to a narrower candidate set than AGR")),
    ("widths dropped from slide 21, kept on the fairness slide",
     edit(DECK, r"\alert{narrower candidate set}: $40$/$20$ vs $300$/$200$",
          r"\alert{narrower candidate set}")),
    ("ToG's caps change in code and neither slide follows",
     edit(TOG, "MAX_RELATIONS, MAX_NEIGHBORS = 40, 20",
          "MAX_RELATIONS, MAX_NEIGHBORS = 60, 30")),
    # The five measured figures the spoken answer quotes.
    ("a binding rate drifts in the spoken answer",
     edit(SCRIPT, "binds on 31.6 percent of the 1,651 entities",
          "binds on 41.6 percent of the 1,651 entities")),
    ("the measurement moves and the answer does not follow",
     edit(NUMS, '"entities_at_relation_cap_pct": 31.6',
          '"entities_at_relation_cap_pct": 29.4')),
    ("AGR's relation cap stops binding exactly once",
     edit(NUMS, '"entities_at_relation_cap": 1,',
          '"entities_at_relation_cap": 4,')),
    # The ordinal, at both ends.
    ("the two spoken ordinals disagree with each other",
     edit(SCRIPT, "the conclusion ranks it limitation 5.",
          "the conclusion ranks it limitation 3.")),
    ("the thesis reorders its limitations and the script does not follow",
     edit(CONC, r"\textbf{The agentic baseline prunes from a narrower "
                r"candidate set.}",
          "\\textbf{An unrelated limitation.} Text.\n\n"
          r"\textbf{The agentic baseline prunes from a narrower "
          r"candidate set.}")),
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
