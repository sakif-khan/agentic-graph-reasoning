"""Prove the static-baseline claim-boundary checks fire.

Case 1 reinstates the forbidden claim verbatim. Cases 2-4 corrupt the
figures that replaced it. Files restored in a finally block.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
R = ROOT / "thesis_paper" / "sections" / "results.tex"
S = ROOT / "thesis_paper" / "sections" / "setup.tex"

CASES = [
    (R, "reinstate 'actively worse than parametric memory'",
     "Raw hits mislead on the static graph baseline",
     "It is actively worse than parametric memory because it floods the "
     "context. Raw hits mislead on the static graph baseline"),
    (R, "assertion precision 76.8 -> 77.8",
     r"or $76.8\%$", r"or $77.8\%$"),
    (R, "wrong-count 41 -> 42",
     "wrong on $41$", "wrong on $42$"),
    (S, "fanout reach 72.5 -> 62.5",
     r"on $72.5\%$ of the", r"on $62.5\%$ of the"),
]

orig = {p: io.open(p, encoding="utf-8").read() for p in (R, S)}
out = []
try:
    for path, name, find, repl in CASES:
        assert find in orig[path], f"anchor not found: {find!r}"
        io.open(path, "w", encoding="utf-8").write(
            orig[path].replace(find, repl, 1))
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        fails = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
        out.append((name, r.returncode, fails))
        io.open(path, "w", encoding="utf-8").write(orig[path])
finally:
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8").write(s)

for name, rc, fails in out:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails:
        print(f"          {f}")
r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
passed = all(rc for _, rc, _ in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
