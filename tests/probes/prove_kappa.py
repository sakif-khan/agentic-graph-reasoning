"""Prove the kappa guard fires -- including on the forms it currently misses.

Case 1 reinstates the shipped setup.tex sentence verbatim.
Case 2 does the same but hard-wrapped, the way the .tex actually wraps.
Case 3 deletes setup.tex's kappa statement outright, leaving no value.
Case 4 rounds it to 0.700, which the thesis names as the deceptive form.
Case 5 keeps 0.6995 but cuts the statement that it MISSES the bar.
setup.tex restored in a finally block.

Every LaTeX literal below is a raw string. Writing "$\kappa" unraw makes
python warn and makes re treat \k as a bad escape -- the same hazard the
checker's own patterns carry.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
S = ROOT / "thesis_paper" / "sections" / "setup.tex"
orig = io.open(S, encoding="utf-8").read()

# anchor spans plain prose to plain prose: no LaTeX in the pattern, so
# no backslash for the shell or for re to disagree about.
CURRENT = re.search(r"agreement and Cohen's [\s\S]*?rounding it away\.", orig)
assert CURRENT, "could not locate the kappa sentence"
cur = CURRENT.group(0)

CASES = [
    ("shipped form: kappa = 0.70, miss cut",
     r"agreement and Cohen's $\kappa = 0.70$."),
    ("same, hard-wrapped across the ' = '",
     "agreement and Cohen's $\\kappa =\n0.70$."),
    ("setup states no kappa at all",
     r"agreement."),
    ("rounded to 0.700, the form the thesis names",
     r"agreement and Cohen's $\kappa = 0.700$."),
    ("0.6995 kept, the miss cut",
     r"agreement and Cohen's $\kappa = 0.6995$."),
]

out = []
try:
    for name, repl in CASES:
        txt = orig.replace(cur, repl, 1)
        assert txt != orig, f"corruption was a no-op: {name}"
        io.open(S, "w", encoding="utf-8").write(txt)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
finally:
    io.open(S, "w", encoding="utf-8").write(orig)

for name, rc, f in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    for line in f[:3]:
        print(f"           {line}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
