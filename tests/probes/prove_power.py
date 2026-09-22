"""Prove the power checks fire, including on the exact error they exist for.

Each case rewrites attribution.tex, runs the checker, and restores the file
in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
T = ROOT / "journal" / "sections" / "attribution.tex"


def sub_once(text, find, repl):
    """Replace `find` even where the 72-column fill broke it across lines.

    The anchors below used to be literal substrings, which made every one
    of them hostage to the wrap: the September 2026 shortening moved a
    line break into "for / model scoring" and the probe reported an anchor
    missing while the sentence sat there in full. Matching on \\s+ between
    the words is the same fix prove_abstract.py already carries.
    """
    pat = r"\s+".join(map(re.escape, find.split()))
    m = re.search(pat, text)
    assert m, f"anchor not found: {find!r}"
    return text[:m.start()] + repl + text[m.end():]

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
    ("half-split denominator -> 400 (the error it shipped with)",
     "--- $200$ questions on", "--- $400$ questions on"),
    ("agreement 396/398 -> 399/400 (the error it shipped with)",
     "agreeing on $396$ of the $398$ paired", "agreeing on $399$ of the $400$ paired"),
]

orig = io.open(T, encoding="utf-8").read()
results = []
try:
    for name, find, repl in CASES:
        io.open(T, "w", encoding="utf-8").write(sub_once(orig, find, repl))
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
passed = all(rc for _, rc, _ in results) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
