"""Prove the static-baseline claim-boundary checks fire.

Case 1 reinstates the forbidden claim verbatim. Cases 2-4 corrupt the
figures that replaced it. Files restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
R = ROOT / "journal" / "sections" / "results.tex"
S = ROOT / "journal" / "sections" / "setup.tex"


def sub_once(text, find, repl):
    """Replace `find` even where the 72-column fill broke it across lines.

    Same fix as prove_power.py, prove_exclusions.py and prove_abstract.py
    carry. The first anchor below spans eight words and so was broken by
    almost any reflow of that paragraph; it reported the sentence missing
    while it sat there in full.
    """
    pat = r"\s+".join(map(re.escape, find.split()))
    m = re.search(pat, text)
    assert m, f"anchor not found: {find!r}"
    return text[:m.start()] + repl + text[m.end():]

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
        io.open(path, "w", encoding="utf-8").write(
            sub_once(orig[path], find, repl))
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
