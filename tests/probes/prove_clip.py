"""Prove the equal-width clip-rate caveat is enforced.

Case 1 restores the shipped sentence verbatim -- the re-run proposed as
though it varied one thing. The rest remove each half of the caveat.
results.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
R = ROOT / "thesis_paper" / "sections" / "results.tex"
orig = io.open(R, encoding="utf-8", newline="").read()

m = re.search(r"make in a follow-up\. That re-run[\s\S]*?invisibly\.", orig)
assert m, "could not locate the caveat"
caveat = m.group(0)

CASES = [
    ("shipped: re-run proposed with no confound named",
     "make in a follow-up."),
    ("clip rate named, 'read apart' dropped",
     "make in a follow-up. Wider candidate sets make each pruning call "
     "dearer, so equal widths would also raise the baseline's clip rate."),
    ("caveat kept, the aggregate warning dropped",
     "make in a follow-up. That re-run would not vary one thing, though. "
     "Wider candidate sets make each pruning call dearer, so equal widths "
     "would also raise the baseline's clip rate. The two effects have to "
     "be read apart."),
]

out = []
try:
    for name, repl in CASES:
        txt = orig.replace(caveat, repl, 1)
        assert txt != orig, f"corruption was a no-op: {name}"
        io.open(R, "w", encoding="utf-8", newline="").write(txt)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
        io.open(R, "w", encoding="utf-8", newline="").write(orig)
finally:
    io.open(R, "w", encoding="utf-8", newline="").write(orig)

for name, rc, f in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    for line in f[:2]:
        print(f"           {line}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
passed = all(rc for _, rc, _ in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
