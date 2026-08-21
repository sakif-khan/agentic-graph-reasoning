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
PAPER = ROOT / "thesis_paper"
MAIN = PAPER / "agr-paper.tex"
FRAME = PAPER / "sections" / "framework.tex"
BIB = PAPER / "agr-paper.bib"
FIG = PAPER / "figures" / "fig_claim_path.tex"

orig = {p: io.open(p, encoding="utf-8", newline="").read()
        for p in (MAIN, FRAME, BIB, FIG)}


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
     edit(MAIN, r"\bibliography{agr-paper}",
          r"\bibliography{../thesis_book/buetcsepgthesis}")),
    ("shipped: claim-path figure escapes the directory",
     edit(FRAME, r"\input{figures/fig_claim_path}",
          r"\input{../thesis_book/figures/fig_claim_path}")),
    ("bibliography named but not present",
     delete(BIB)),
    ("bibliography copy drifts from the thesis",
     edit(BIB, "@article", "@ARTICLE")),
    ("figure copy drifts beyond its root line",
     edit(FIG, r"\definecolor{agrNode}{HTML}{0072B2}",
          r"\definecolor{agrNode}{HTML}{FF0000}")),
    ("an input points at a file that was never copied",
     edit(FRAME, r"\input{figures/fig_claim_path}",
          r"\input{figures/fig_claim_path_v2}")),
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
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
