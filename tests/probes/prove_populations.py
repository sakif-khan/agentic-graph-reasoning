"""Prove the population/ratio checks fire.

Cases 1, 4 and 6 reinstate the shipped text verbatim -- the main-run 6.2%
attached to half-split backtrack counts, "roughly half" where the counts
say three-fifths, and one call ratio quoted for two datasets that do not
share it. The rest are near-miss corruptions of the same sentences.

All three sections are restored in a finally block. Written with the Write
tool: a heredoc halves the backslashes in every LaTeX literal below.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
SEC = ROOT / "thesis_paper" / "sections"
A, E, R = SEC / "attribution.tex", SEC / "error-analysis.tex", SEC / "results.tex"
orig = {p: io.open(p, encoding="utf-8").read() for p in (A, E, R)}

BT = ("$38$\nand $108$ backtracks over the $398$ paired questions --- and on those\n"
      "same runs the meter refuses a further attempt on $28$ of them, $7.0\\%$.")
FLAG = ("The pass flagged $105$ questions and\nadjudication confirmed $41$, so "
        "roughly three-fifths of what it flagged")
RATIO = "ComplexWebQuestions --- ratios of $0.48$ and $0.49$."

CASES = [
    (A, "shipped: main-run 6.2% on half-split counts",
     BT, "$38$\nand $108$ backtracks across the half-splits --- and the backtrack "
         "budget\nrefuses further attempts on only $6.2\\%$ of questions."),
    (A, "refusal count dropped, rate kept",
     BT, "$38$\nand $108$ backtracks over the $398$ paired questions --- and on those\n"
         "same runs the meter refuses a further attempt on $20$ of them, $7.0\\%$."),
    (A, "rate rounded the wrong way",
     BT, "$38$\nand $108$ backtracks over the $398$ paired questions --- and on those\n"
         "same runs the meter refuses a further attempt on $28$ of them, $7.5\\%$."),
    (E, "shipped: 'roughly half' against 105/41",
     FLAG, "Roughly half of what the consensus pass\nflagged"),
    (E, "flagged count corrupted 105 -> 100",
     FLAG, "The pass flagged $100$ questions and\nadjudication confirmed $41$, so "
           "roughly three-fifths of what it flagged"),
    (R, "shipped: one ratio for both datasets",
     RATIO, "ComplexWebQuestions, a ratio of $0.48$ on both."),
    (R, "ratios transposed",
     RATIO, "ComplexWebQuestions --- ratios of $0.49$ and $0.48$."),
]

out = []
try:
    for path, name, old, new in CASES:
        txt = orig[path].replace(old, new, 1)
        assert txt != orig[path], f"corruption was a no-op: {name}"
        io.open(path, "w", encoding="utf-8").write(txt)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
        io.open(path, "w", encoding="utf-8").write(orig[path])
finally:
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8").write(s)

for name, rc, f in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    for line in f[:2]:
        print(f"           {line}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
