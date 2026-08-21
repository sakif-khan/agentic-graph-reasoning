"""Prove the semantic-tier checks fire.

Case 1 restores the shipped text verbatim -- AGR quoted against the two
comparators it beats, Vector-RAG's leading CWQ cell omitted. Cases 2-4
corrupt individual cells and the band. results.tex restored in a finally.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
R = ROOT / "thesis_paper" / "sections" / "results.tex"
orig = io.open(R, encoding="utf-8").read()

SHIPPED = """The semantic tier separates the systems where the structural tier
cannot. Judging whether an asserted entity is supported \\emph{as the
answer}, AGR reaches $66.7\\%$ and $48.3\\%$ against Think-on-Graph's
$61.7\\%$ and $43.3\\%$, with the parametric control at $63.3\\%$ and
$36.7\\%$. These are conservative lower bounds by construction
(\\Cref{sec:protocol}) and the gaps are small relative to the sample of
$60$ per cell, so they are reported as consistent with the accuracy
ordering rather than as independent confirmation of it.
"""

# Replace the whole rewritten block with the version that shipped.
# lambda, not a plain string: re.sub treats the replacement as a template,
# so the LaTeX in SHIPPED ("\emph") raises "bad escape \e".
selective = re.sub(
    r"The semantic tier asks the harder question[\s\S]*?"
    r"one system within it\.\n",
    lambda _m: SHIPPED, orig)
assert selective != orig, "could not locate the rewritten block"

CASES = [
    ("restore the shipped selective quote", selective),
    ("Vector-RAG CWQ 50.0 -> 40.0", orig.replace("\\vecrag       & 61.7\\% & \\textbf{50.0\\%}",
                                                 "\\vecrag       & 61.7\\% & \\textbf{40.0\\%}", 1)),
    ("band top 66.7 -> 70.0", orig.replace("$36.7$--$66.7\\%$ band",
                                           "$36.7$--$70.0\\%$ band", 1)),
    ("drop 'it is second'", orig.replace("it is second", "it also does well", 1)),
]
for name, txt in CASES:
    assert txt != orig, f"corruption was a no-op: {name}"

out = []
try:
    for name, txt in CASES:
        io.open(R, "w", encoding="utf-8").write(txt)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
finally:
    io.open(R, "w", encoding="utf-8").write(orig)

for name, rc, fails in out:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails[:4]:
        print(f"          {f}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
print("ALL CASES CAUGHT" if all(rc for _, rc, _ in out) and r.returncode == 0
      else "SOME CASE MISSED")
