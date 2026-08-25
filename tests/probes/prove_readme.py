"""Prove the module README is held to the module it describes.

Cases 1-2 reinstate the shipped sentences. check_tex_roots.py "checks both
this module and the book" -- it covers three, thesis_paper included since
that module was added. And "both documents \\input [fig_claim_path] from
thesis_book/figures/" -- only the presented deck does; the backup deck does
not use the figure at all.

Prose about the repository goes stale exactly the way a transcribed number
does, and nothing was reading it. Cases 3-5 move the module under the
prose instead: a fourth module, the deck switching to a local copy the way
thesis_paper did, and the backup deck starting to use the figure.

README, both decks and check_tex_roots.py are restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
RM = ROOT / "thesis_presentation" / "README.md"
MAIN = ROOT / "thesis_presentation" / "content-main.tex"
BACK = ROOT / "thesis_presentation" / "content-backup.tex"
ROOTS = ROOT / "scripts" / "check_tex_roots.py"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (RM, MAIN, BACK, ROOTS)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0][:88] if fail else "")


def edit(path, old, new):
    """Substitute, tolerating the wrap and the CRLF this README is stored in."""
    def go():
        gap = r"\s+"
        pattern = re.compile(gap.join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


CASES = [
    # The anchor stops at "the paper" rather than at a full stop. That sentence
    # gained a second clause -- "and confirms transcript.tex is correctly seen
    # as its own document" -- when the transcript became the fifth document, and
    # this anchor still ended in the full stop the clause displaced. The probe
    # had been failing on an unmodified README ever since, which is the failure
    # mode a probe can least afford: it reports on a rule that is fine while
    # itself being the thing that is broken.
    ("shipped: the README undercounts the modules checked",
     edit(RM, "`python scripts/check_tex_roots.py` checks all three modules "
              "— this one, the book, and the paper",
          "`python scripts/check_tex_roots.py` checks both this module and "
          "the book")),
    ("shipped: the README says both decks input the figure",
     edit(RM, "the backup deck does not use it at all.",
          "and so does the backup deck.")),
    ("a fourth module is checked and the README does not follow",
     edit(ROOTS, 'MODULES = ("thesis_book", "thesis_presentation", '
                 '"thesis_paper")',
          'MODULES = ("thesis_book", "thesis_presentation", "thesis_paper", '
          '"thesis_extra")')),
    ("the deck takes a local copy and the README still says it reaches out",
     edit(MAIN, r"\input{../thesis_book/figures/fig_claim_path.tex}",
          r"\input{figures/fig_claim_path.tex}")),
    ("the backup deck starts using the figure",
     edit(BACK, r"\begin{frame}{Backup: budget configuration}",
          "\\begin{frame}{Backup: budget configuration}\n"
          r"\input{../thesis_book/figures/fig_claim_path.tex}")),
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
