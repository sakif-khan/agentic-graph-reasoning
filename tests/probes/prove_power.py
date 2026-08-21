"""Prove the power checks fire, including on the exact error they exist for.

Each case rewrites attribution.tex, runs the checker, and restores the file
in a finally block.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
T = ROOT / "thesis_paper" / "sections" / "attribution.tex"

CASES = [
    ("ratio 4:1 -> 3:1 (the wrong value it shipped with)",
     "power is nearer $4{:}1$", "power is nearer $3{:}1$"),
    ("discordant 21 -> 22",
     "conditions produced $21$", "conditions produced $22$"),
    ("MDE gap 11 -> 12",
     "and $11$ and $10$ for model scoring", "and $12$ and $10$ for model scoring"),
    ("80%-power pairs 72 -> 30",
     "requires roughly $72$ discordant", "requires roughly $30$ discordant"),
    ("reinstate the original 20-to-10 claim",
     "Removing claim verification changed",
     "About $30$ discordant pairs split $20$ to $10$ rejects. "
     "Removing claim verification changed"),
    # Anchors must not span a line break -- the .tex is hard-wrapped.
    ("half-split denominator -> 400 (the error it shipped with)",
     "--- $200$ questions on", "--- $400$ questions on"),
    ("agreement 396/398 -> 399/400 (the error it shipped with)",
     "agreeing on $396$ of the $398$ paired", "agreeing on $399$ of the $400$ paired"),
]

orig = io.open(T, encoding="utf-8").read()
results = []
try:
    for name, find, repl in CASES:
        assert find in orig, f"anchor not found: {find!r}"
        io.open(T, "w", encoding="utf-8").write(orig.replace(find, repl, 1))
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        fails = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
        results.append((name, r.returncode, fails))
finally:
    io.open(T, "w", encoding="utf-8").write(orig)

for name, rc, fails in results:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails:
        print(f"          {f}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in results) and r.returncode == 0
      else "SOME CASE MISSED")
