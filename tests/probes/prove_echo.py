"""Prove check_slides.py holds the echo attractor to the thesis's framing.

Cases 1-2 reinstate the shipped sentence, on the slide and in the script:
"It appears across systems, so it is a property of the task, not of AGR."
Defensive where the thesis is substantive -- sec:echo calls the attractor
"invisible to any evaluation treating systems as independent", and
sec:contribution says the contribution is the mechanism "and what it means
for consensus-based evaluation, not the frequency". Commit 2acfc2a moved
the abstract off exactly that framing and the deck never followed.

Cases 3-5 remove the half that replaced it -- the independence clause, the
majority-rescoring consequence, and the thesis sentence the slide answers
to. Cases 6-7 restore the deck's "Reading every failure also found...",
which presented sec:benchmark-defects as an unrelated second finding when
the gap between flagged and confirmed IS the attractor. Cases 8-10 corrupt
the two counts from both ends.

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
INTRO = ROOT / "thesis_book" / "chapters" / "introduction.tex"
NUMS = ROOT / "results" / "phase4" / "thesis_numbers.json"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (DECK, SCRIPT, INTRO, NUMS)
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


SHIPPED_SLIDE = (r"{\small It appears across systems, so it is a property of "
                 r"the task, not of AGR. Naming it is what lets future work "
                 r"target it.}")
CURRENT_SLIDE = (r"{\small Different systems fall into it \alert{together}, so "
                 r"no evaluation treating them as independent can see it --- "
                 r"and a policy of rescoring on majority agreement turns it "
                 r"into apparent \alert{correctness}.}")
CURRENT_SPOKEN = ("Different systems fall into it together, so no evaluation "
                  "treating them as independent can see it. Rescore whenever "
                  "a majority agree — a natural thing to want — and this "
                  "becomes apparent correctness. That is the contribution: "
                  "the mechanism, not the count.")
SHIPPED_BENCH = (r"The same cross-system agreement is also a "
                 r"\alert{\mbox{detector}}: consensus flagged $105$ questions, "
                 r"adjudication confirmed $41$, and the gap is the attractor "
                 r"above rather than label noise.")
CURRENT_S20 = ("Same pass, same cross-system agreement: consensus flagged 105 "
               "questions, adjudication confirmed 41 — and the gap is the "
               "attractor I just described, not label noise.")

CASES = [
    ("shipped: the slide deflects it onto the task",
     edit(DECK, CURRENT_SLIDE, SHIPPED_SLIDE)),
    ("shipped: the script deflects it too",
     edit(SCRIPT, CURRENT_SPOKEN,
          "It appears across systems, so it's a property of the task rather "
          "than of AGR. Naming it is what lets future work target it.")),
    ("the majority-rescoring consequence is dropped",
     edit(DECK, r"--- and a policy of rescoring on majority agreement turns "
                r"it into apparent \alert{correctness}.", r"--- a shared "
                r"failure mode.")),
    ("the independence clause is dropped from the script",
     edit(SCRIPT, "so no evaluation treating them as independent can see it.",
          "which is worth knowing.")),
    ("the thesis stops making it a claim about evaluation",
     edit(INTRO, "the contribution is\nthe named mechanism itself and what it "
                 "means for consensus-based evaluation, not\nthe frequency.",
          "the contribution is the named mechanism itself.")),
    # The two slides are one finding.
    ("the benchmark slide goes back to an unrelated second finding",
     edit(DECK, SHIPPED_BENCH,
          r"Reading every failure also found questions where the "
          r"\emph{benchmark}, not the system, was at fault:")),
    ("and the script does too",
     edit(SCRIPT, CURRENT_S20,
          "One more thing came out of reading every failure.")),
    # The counts, from both ends.
    ("the flagged total drifts on the slide",
     edit(DECK, r"consensus flagged $105$ questions",
          r"consensus flagged $100$ questions")),
    ("the pass flags more and neither slide follows",
     edit(NUMS, '"flagged_questions": 58,', '"flagged_questions": 60,')),
    ("the confirmed pair stops matching the census exclusions",
     edit(NUMS, '"excluded_before_census": 41,',
          '"excluded_before_census": 45,')),
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
