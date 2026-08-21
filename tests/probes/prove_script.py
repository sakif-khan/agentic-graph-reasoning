"""Prove the rehearsal script's own internals are held together.

Cases 1-3 reinstate the shipped backup references: "go to Backup 1", "(B2)"
and "Backup 4". The first two are slide ordinals, the third is a page
number, and the tables use pages. The backup file opens on a title page,
so the two systems are off by one -- counted as an ordinal, the fourth
backup slide is hedging rather than the census. That is a note read under
pressure, which is when landing on the wrong slide costs most.

Case 4 restores "The four bold slides" against three bold rows, and case 5
restores the shorter of two lists of slides not to shorten -- the script
carried both, naming different slides. Cases 6-9 break the couplings the
other way: a bold row with no star, a page reference to a page the table
does not list, a backup slide the table does not carry, and a row whose
contents no longer describe its slide.

Cases 10-11 cover the pooled census caption, from both ends.

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
DECK = ROOT / "thesis_presentation" / "content-main.tex"
BACKUP = ROOT / "thesis_presentation" / "content-backup.tex"
NUMS = ROOT / "results" / "phase4" / "thesis_numbers.json"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (SCRIPT, DECK, BACKUP, NUMS)
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
    ("shipped: a backup slide referred to by ordinal",
     edit(SCRIPT, "**If asked about budgets, go to backup page 2.**",
          "**If asked about budgets, go to Backup 1.**")),
    ("shipped: the (B2) shorthand",
     edit(SCRIPT, "on both datasets (backup page 3)",
          "on both datasets (B2)")),
    ("shipped: a page number written as an ordinal",
     edit(SCRIPT, "histogram is backup page 4 if anyone",
          "histogram is Backup 4 if anyone")),
    ("shipped: four bold slides, three of them bold",
     edit(SCRIPT, "The three **bold** slides are the ones the committee will "
                  "actually interrogate.",
          "The four **bold** slides are the ones the committee will actually "
          "interrogate.")),
    ("shipped: the two protected lists name different slides",
     edit(SCRIPT, "never from 11, 13, 14, 17 or 18.",
          "never from 11, 13, 17.")),
    ("a row goes bold without its section being starred",
     edit(SCRIPT, "| 12 | Accuracy against cost |",
          "| 12 | **Accuracy against cost** |")),
    ("a reference to a backup page the table does not list",
     edit(SCRIPT, "histogram is backup page 4 if anyone",
          "histogram is backup page 9 if anyone")),
    ("the backup deck gains a slide the table does not carry",
     edit(BACKUP, r"\begin{frame}{Backup: hedging behaviour}",
          "\\begin{frame}{Backup: something else}\n\\end{frame}\n"
          r"\begin{frame}{Backup: hedging behaviour}")),
    ("a table row stops describing its slide",
     edit(SCRIPT, "| 4 | Full 12-category failure histogram |",
          "| 4 | Assorted other material |")),
    # The pooled-census caption, from both ends.
    ("the slide stops saying its totals are pooled",
     edit(DECK, r"Totals. Wrong and hedge are \emph{never pooled} in the "
                r"thesis, and the shape flips: composite claim is $1$ on "
                r"WebQSP against $46$ on CWQ.",
          r"Totals across both datasets.")),
    ("the split moves and the caption does not follow",
     edit(NUMS, '"composite_claim": 1,', '"composite_claim": 3,')),
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
