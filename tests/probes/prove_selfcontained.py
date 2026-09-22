"""Prove the self-containment tests fire.

Cases 1 and 2 reinstate the two escapes verbatim -- the exact strings that
built fine in the repository and would have broken on upload. The rest
exercise the drift and resolution guards the copies newly need.

Every file is restored in a finally block, including one that gets deleted.
"""
import io
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
PAPER = ROOT / "journal"
MAIN = PAPER / "journal_0421052099.tex"
# The two \input cases used to mutate framework.tex's
# \input{figures/fig_claim_path}. That figure was cut from the manuscript
# on 2026-09-23 when the paper was shortened, so there was no longer an
# \input there to corrupt and both cases failed on a missing anchor. They
# now use the failure histogram, which the manuscript does still \input.
# fig_claim_path.tex itself stays in journal/figures/ and stays pinned to
# the thesis's copy by test_the_copied_figure_has_not_drifted, so the
# drift case below is unaffected by the figure leaving the body.
ERRS = PAPER / "sections" / "error-analysis.tex"
BIB = PAPER / "journal.bib"
FIG = PAPER / "figures" / "fig_claim_path.tex"

orig = {p: io.open(p, encoding="utf-8", newline="").read()
        for p in (MAIN, ERRS, BIB, FIG)}


def edit(path, old, new):
    def go():
        s = orig[path]
        assert old in s, f"anchor not found in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
    return go


def delete(path):
    def go():
        path.unlink()
    return go


CASES = [
    ("shipped: bibliography escapes the directory",
     edit(MAIN, r"\bibliography{journal}",
          r"\bibliography{../thesis_book/buetcsepgthesis}")),
    ("shipped: a figure \\input escapes the directory",
     edit(ERRS, r"\input{figures/fig_failure_histogram}",
          r"\input{../thesis_book/figures/fig_failure_histogram}")),
    ("bibliography named but not present",
     delete(BIB)),
    ("bibliography copy drifts from the thesis",
     edit(BIB, "@article", "@ARTICLE")),
    ("figure copy drifts beyond its root line",
     edit(FIG, r"\definecolor{agrNode}{HTML}{0072B2}",
          r"\definecolor{agrNode}{HTML}{FF0000}")),
    ("an input points at a file that was never copied",
     edit(ERRS, r"\input{figures/fig_failure_histogram}",
          r"\input{figures/fig_failure_histogram_v2}")),
]

out = []
try:
    for name, mutate in CASES:
        mutate()
        r = subprocess.run([sys.executable, "-m", "pytest",
                            "tests/test_paper_self_contained.py", "-q"],
                           cwd=ROOT, capture_output=True, text=True)
        failed = [l.strip() for l in r.stdout.splitlines()
                  if l.startswith("FAILED") or "assert" in l.lower()][:1]
        out.append((name, r.returncode, failed))
        for p, s in orig.items():
            io.open(p, "w", encoding="utf-8", newline="").write(s)
finally:
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)

for name, rc, f in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")

r = subprocess.run([sys.executable, "-m", "pytest",
                    "tests/test_paper_self_contained.py", "-q"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}  ({r.stdout.strip().splitlines()[-1]})")
passed = all(rc for _, rc, _ in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
