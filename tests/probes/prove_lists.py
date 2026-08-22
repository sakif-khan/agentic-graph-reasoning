"""Prove check_slides.py holds the deck's two lists to the thesis's.

Case 1 reinstates the shipped contributions block verbatim. It said "six"
and listed a different six from sec:contribution: the framework and its
verification layer split into two items, the five-system comparison and
the hop-count shape promoted from results, and the ablation, the
decomposition finding and the protocol dropped. Only two of six mapped.

The rest are the ways such a list drifts one item at a time -- an item
deleted, an item replaced by a result, the count padded, the thesis
growing a seventh contribution the deck does not carry -- plus the
limitation the deck had instead of the thesis's, and the candidate widths
going stale against the code that sets them.

The thesis file is mutated in one case and restored with the deck.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
DECK = ROOT / "thesis_presentation" / "content-main.tex"
INTRO = ROOT / "thesis_book" / "chapters" / "introduction.tex"
TOG = ROOT / "agr" / "baselines" / "tog.py"
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (DECK, INTRO, TOG, SCRIPT)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0] if fail else r.stdout.strip()[-90:])


# The enumerate under "Contributions", whitespace-tolerantly: the deck is
# hard-wrapped and rewrapping it must not turn this probe into a no-op.
BODY = re.compile(r"(?<=\\begin\{enumerate\}\\setlength\{\\itemsep\}\{0pt\})"
                  r".*?(?=\\end\{enumerate\})", re.S)


def set_contributions(items):
    def go():
        assert BODY.search(orig[DECK]), "the contributions enumerate moved"
        body = "\n" + "\n".join("        \\item " + i for i in items) + "\n      "
        io.open(DECK, "w", encoding="utf-8", newline="").write(
            BODY.sub(lambda _: body, orig[DECK], count=1))
    return go


def edit(path, old, new):
    def go():
        pattern = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


def stretch_row(n, delta):
    """Add delta seconds to row n's slide time, leaving the cumulative.

    Self-locating on purpose. Hard-coding the row verbatim -- times and all
    -- put a computed value in the anchor, so the probe raised the first
    time an unrelated slide grew and shifted the cumulative column. An
    anchor must not contain anything the document derives.
    """
    def go():
        row = re.compile(rf"^\| {n} \|([^|]*)\| (\d+):(\d\d) \| (\d+):(\d\d) \|",
                         re.M)
        m = row.search(orig[SCRIPT])
        assert m, f"no timing row {n} in transcript.md"
        ms, ss = divmod(int(m.group(2)) * 60 + int(m.group(3)) + delta, 60)
        io.open(SCRIPT, "w", encoding="utf-8", newline="").write(
            orig[SCRIPT][:m.start()]
            + f"| {n} |{m.group(1)}| {ms}:{ss:02d} | {m.group(4)}:{m.group(5)} |"
            + orig[SCRIPT][m.end():])
    return go


def desync_heading(n):
    """Move one section heading off its row, whatever the row now says.

    The anchor here used to be the heading verbatim, "*(1:45)*" and all.
    That is a value the table derives, so re-timing slide 21 turned this
    probe from CAUGHT into a raise -- the third time an anchor carrying a
    derived value has done that. Read the time, then change it.
    """
    def go():
        head = re.compile(rf"^(## {n} — .*?\*\()(\d+):(\d\d)(\)\*)", re.M)
        m = head.search(orig[SCRIPT])
        assert m, f"no section heading {n} in transcript.md"
        was = int(m.group(2)) * 60 + int(m.group(3))
        ms, ss = divmod(was + 40, 60)
        io.open(SCRIPT, "w", encoding="utf-8", newline="").write(
            orig[SCRIPT][:m.start()]
            + f"{m.group(1)}{ms}:{ss:02d}{m.group(4)}"
            + orig[SCRIPT][m.end():])
    return go


def rewrite_budget(mins, secs):
    """Quote a total in the budget line that the table does not add up to."""
    def go():
        line = re.compile(r"\*\*Budget: (\d+) min (\d+) s of speaking")
        m = line.search(orig[SCRIPT])
        assert m, "no budget line in transcript.md"
        assert (int(m.group(1)), int(m.group(2))) != (mins, secs), \
            "the corruption is a no-op: pick a total the table does not have"
        io.open(SCRIPT, "w", encoding="utf-8", newline="").write(
            line.sub(f"**Budget: {mins} min {secs} s of speaking",
                     orig[SCRIPT], count=1))
    return go


SHIPPED = [
    r"AGR: a state machine over a constrained graph tool API",
    r"The Structural Verification Layer and its output contract",
    r"A controlled five-system comparison, one backbone, one budget",
    r"The hop-count shape answering RQ1",
    r"The \emph{echo attractor}, named",
    r"A counted benchmark-defect rate ($57$)",
]

CURRENT = [
    r"AGR and its \alert{Structural Verification Layer}",
    r"A \alert{component-level ablation} of four mechanisms",
    r"\alert{Stratum-dependent decomposition} --- planning hurts",
    r"The \emph{\alert{echo attractor}}, named",
    r"\alert{Benchmark-defect rates} for WebQSP and CWQ ($57$)",
    r"\alert{Pre-specified} evaluation thresholds",
]

CASES = [
    ("shipped: a different six, only two of them the thesis's",
     set_contributions(SHIPPED)),
    ("one contribution dropped, five listed",
     set_contributions(CURRENT[:5])),
    ("the ablation replaced by a result",
     set_contributions([CURRENT[0], r"A controlled five-system comparison"]
                       + CURRENT[2:])),
    ("count padded back to six with a duplicate",
     set_contributions(CURRENT[:5] + [CURRENT[4]])),
    ("the thesis grows a seventh the deck does not carry",
     edit(INTRO, r"\subsection{The Echo Attractor as a Named Failure Mode}",
          "\\subsection{A Seventh Thing}\n\nText.\n\n"
          r"\subsection{The Echo Attractor as a Named Failure Mode}")),
    ("the thesis's limitation swapped back for the deck's own",
     edit(DECK, r"ToG leads where it finishes, from a \alert{narrower "
                r"candidate set}: $40$/$20$ vs $300$/$200$",
          r"ToG leads on the questions it finishes")),
    ("first-ranked limitation demoted below the others",
     edit(DECK, r"\item The verifier logs only what it \alert{rejects}: "
                r"wrongful acceptance is unmeasured, and the evidence is "
                r"not persisted",
          r"\item One more thing")),
    ("ToG's caps change in code and the slide does not follow",
     edit(TOG, "MAX_RELATIONS, MAX_NEIGHBORS = 40, 20",
          "MAX_RELATIONS, MAX_NEIGHBORS = 60, 30")),
    # The timing table, which has gone stale twice while being edited and
    # is consulted under pressure. Each of its three depths, separately.
    ("a slide runs longer and the cumulative column does not follow",
     stretch_row(16, 60)),
    ("the budget line still quotes the old total",
     rewrite_budget(22, 30)),
    ("a section heading disagrees with its row", desync_heading(21)),
    # Edits the limit rather than the times: changing a slide's time
    # desynchronises the cumulative column, and that check fires first,
    # leaving this one unproven. The limit is the only free variable that
    # isolates it.
    ("the talk no longer fits the limit it names",
     edit(SCRIPT, "against a 25-minute limit", "against a 20-minute limit")),
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
