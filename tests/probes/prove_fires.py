"""Prove check_paper_numbers.py fails on a mistranscribed table cell.

Corrupts one value in results.tex, runs the checker, restores the file in a
finally block so an exception cannot leave the manuscript edited.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
TARGET = ROOT / "thesis_paper" / "sections" / "results.tex"

# graphrag WebQSP hedge_pct, 55.8 -> 55.9. One digit, and 55.9 appears
# nowhere else in the paper, so only the binding can catch it.
ORIG, BAD = "55.8\\%", "55.9\\%"


def run():
    r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout


text = io.open(TARGET, encoding="utf-8").read()
assert ORIG in text, f"anchor {ORIG!r} not found; update this probe"
try:
    io.open(TARGET, "w", encoding="utf-8").write(text.replace(ORIG, BAD, 1))
    rc, out = run()
    hit = [ln for ln in out.splitlines() if "FAIL" in ln]
    print(f"with 55.8 -> 55.9 :  rc={rc}")
    for ln in hit:
        print("   ", ln.strip())
finally:
    io.open(TARGET, "w", encoding="utf-8").write(text)

rc, out = run()
print(f"restored          :  rc={rc}")
passed = hit and rc == 0
print("PROBE PASSED" if passed else "PROBE FAILED -- check is vacuous")
sys.exit(0 if passed else 1)
