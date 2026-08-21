"""Prove the candidate-width and forward-promise checks fire.

Case 1 deletes the whole added passage, which is the state the paper was
actually in -- the forward promise dangling. Cases 2-4 corrupt the measured
rates. results.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
R = ROOT / "thesis_paper" / "sections" / "results.tex"

orig = io.open(R, encoding="utf-8").read()

# The state before the fix: passage absent, setup still promising it.
# Ends at the subsection that follows rather than at the passage's own
# last sentence -- that sentence later gained the clip-rate caveat, and
# an anchor on its old wording silently stopped matching.
without = re.sub(
    r"\\textbf\{One asymmetry bounds how far that reading extends\}[\s\S]*?"
    r"(?=\\subsection\{Accuracy by Hop Depth\})",
    "", orig)
assert without != orig, "could not locate the added passage"

CASES = [
    ("delete the passage (the dangling-promise state)", without),
    ("binding rate 31.6 -> 41.6", orig.replace("$31.6\\%$", "$41.6\\%$", 1)),
    ("entities expanded 1,651 -> 1,751",
     orig.replace("$1{,}651$", "$1{,}751$", 1)),
    ("AGR neighbour rate 3.3 -> 13.3", orig.replace("$3.3\\%$", "$13.3\\%$", 1)),
]
for name, text in CASES:
    assert text != orig, f"corruption was a no-op: {name}"

out = []
try:
    for name, text in CASES:
        io.open(R, "w", encoding="utf-8").write(text)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
finally:
    io.open(R, "w", encoding="utf-8").write(orig)

for name, rc, fails in out:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails:
        print(f"          {f}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
