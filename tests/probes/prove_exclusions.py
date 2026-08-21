"""Prove the exclusion-sensitivity checks fire.

Cases 1-2 reinstate the retracted claims verbatim; 3-4 corrupt the measured
range. error-analysis.tex is restored in a finally block.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
E = ROOT / "thesis_paper" / "sections" / "error-analysis.tex"

CASES = [
    ("reinstate 'roughly the defect rate'",
     "moves each system by between",
     "raises every system by roughly the defect rate and moves each by between"),
    ("reinstate the label-defect floor claim",
     "which is a fact",
     "The samples carry a label-defect floor of five per cent. This is a fact"),
    ("sensitivity top of range 0.020 -> 0.055 (the defect rate)",
     "and $+0.020$", "and $+0.055$"),
    ("sensitivity bottom of range 0.001 -> 0.010",
     "between $+0.001$", "between $+0.010$"),
    # The 57 decomposition: 41 + 17 - 1.
    ("reinstate '57 as 22 and 19 reconciled'",
     "All $41$ were removed",
     "and $57$ distinct questions once the one question appearing in both "
     "counts is resolved. All $41$ were removed"),
    ("drop the 17 census-found defects",
     "found $17$ more that the pre-pass had missed --- $3$",
     "found some more that the pre-pass had missed --- $3$"),
    ("census-defect split 14 -> 15",
     "and $14$ on ComplexWebQuestions", "and $15$ on ComplexWebQuestions"),
    ("exclusion total 41 -> 40",
     "All $41$ were removed", "All $40$ were removed"),
]

orig = io.open(E, encoding="utf-8").read()
out = []
try:
    for name, find, repl in CASES:
        assert find in orig, f"anchor not found: {find!r}"
        io.open(E, "w", encoding="utf-8").write(orig.replace(find, repl, 1))
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
finally:
    io.open(E, "w", encoding="utf-8").write(orig)

for name, rc, fails in out:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails:
        print(f"          {f}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
