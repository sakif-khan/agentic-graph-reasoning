r"""Prove the population/ratio checks fire.

Cases 1, 4 and 6 reinstate the shipped text verbatim -- the main-run 6.2%
attached to half-split backtrack counts, "roughly half" where the counts
say three-fifths, and one call ratio quoted for two datasets that do not
share it. The rest are near-miss corruptions of the same sentences.

Regex anchors, not literals. Every one of the three was a multi-line
string copied out of the sections, and all three stopped matching: the
shortening passes re-punctuated two of the sentences (both em-dashes
became commas) and the 72-column fill moved every line break inside
them. A literal anchor here is a promise that nobody will ever rewrap a
paragraph. What these cases actually depend on is the numbers and the
handful of words the checker itself matches on, so they anchor on those
and treat the connective prose as `[\s\S]{0,90}?` -- the same shape
check_paper_numbers.py uses for the same sentence.

Read and written with newline="" so a substitution cannot flip a file's
line endings; \s+ covers CRLF in the anchors either way.

All three sections are restored in a finally block. Written with the
Write tool: a heredoc halves the backslashes in every LaTeX literal
below.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
SEC = ROOT / "journal" / "sections"
A, E, R = SEC / "attribution.tex", SEC / "error-analysis.tex", SEC / "results.tex"
orig = {p: io.open(p, encoding="utf-8", newline="").read()
        for p in (A, E, R)}

# The whole rarity claim: two counts, the population they are over, the
# refusal count, and the rate. Anchored end to end because case 1 replaces
# all of it, and loosely in the middle because the connective was an
# em-dash when this probe was written and is a comma now.
BT = (r"\$38\$\s+and\s+\$108\$\s+backtracks\s+over\s+the\s+\$398\$\s+"
      r"paired\s+questions[\s\S]{0,90}?\$7\.0\\%\$\.")
COUNT = r"attempt\s+on\s+\$28\$\s+of\s+them"
RATE = r"of\s+them,\s+\$7\.0\\%\$"
FLAG = (r"The\s+pass\s+flagged\s+\$105\$\s+questions\s+and\s+adjudication\s+"
        r"confirmed\s+\$41\$,\s+so\s+roughly\s+three-fifths\s+of\s+what\s+"
        r"it\s+flagged")
FLAGGED = r"pass\s+flagged\s+\$105\$"
RATIO = r"ratios\s+of\s+\$0\.48\$\s+and\s+\$0\.49\$"

CASES = [
    (A, "shipped: main-run 6.2% on half-split counts", BT,
     r"$38$ and $108$ backtracks across the half-splits --- and the "
     r"backtrack budget refuses further attempts on only $6.2\%$ of "
     r"questions."),
    (A, "refusal count dropped, rate kept", COUNT,
     r"attempt on $20$ of them"),
    (A, "rate rounded the wrong way", RATE,
     r"of them, $7.5\%$"),
    (E, "shipped: 'roughly half' against 105/41", FLAG,
     r"Roughly half of what the consensus pass flagged"),
    (E, "flagged count corrupted 105 -> 100", FLAGGED,
     r"pass flagged $100$"),
    (R, "shipped: one ratio for both datasets", RATIO,
     r"a ratio of $0.48$ on both"),
    (R, "ratios transposed", RATIO,
     r"ratios of $0.49$ and $0.48$"),
]

out = []
try:
    for path, name, pattern, new in CASES:
        txt, n = re.subn(pattern, lambda _m: new, orig[path], count=1)
        assert n == 1, f"anchor missed, so the corruption is a no-op: {name}"
        io.open(path, "w", encoding="utf-8", newline="").write(txt)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
        io.open(path, "w", encoding="utf-8", newline="").write(orig[path])
finally:
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)

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
