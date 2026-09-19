"""Prove the abstract tests fire.

Case 1 restores the shipped abstract verbatim from git -- 215 words with
the unverified Elsevier attribution in its comment, the state that stood
because nothing counted it. The rest are targeted corruptions.

journal_0421052099.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
MAIN = ROOT / "journal" / "journal_0421052099.tex"
orig = io.open(MAIN, encoding="utf-8", newline="").read()

# Pinned, not HEAD: 33dfbde is the last commit carrying the 215-word
# abstract and the Elsevier attribution. Reading HEAD silently turned this
# case into a no-op the moment the fix was committed -- the probe went on
# reporting a pass while corrupting nothing.
SHIPPED_REV = "33dfbde"
shipped = subprocess.run(["git", "show", f"{SHIPPED_REV}:thesis_paper/agr-paper.tex"],
                         cwd=ROOT, capture_output=True, text=True).stdout
assert "\\begin{abstract}" in shipped, "could not read the shipped abstract"
assert "Elsevier's limit" in shipped, (
    f"{SHIPPED_REV} does not carry the defect this case is meant to restore")


def swap_block(into, frm):
    """Put frm's abstract block into `into`."""
    pat = r"\\begin\{abstract\}.*?\\end\{abstract\}"
    src = re.search(pat, frm, re.S).group(0)
    return re.sub(pat, lambda _m: src, into, count=1, flags=re.S)


CASES = [
    ("shipped: 215 words, limit attributed to Elsevier",
     lambda s: swap_block(s, shipped)),
    # \s+ inside the anchor: the 72-column fill may break the line there.
    ("padded past the word line",
     lambda s: re.sub(
         r"grounding\s+check\s+passes\s+it\.",
         lambda _m: "grounding check passes it. This finding has implications for "
         "how future work should design and report evaluation protocols "
         "over knowledge graphs, and we discuss several of them at length "
         "in the paper, together with the questions it leaves open and the "
         "experiments that would settle them.",
         s, count=1)),
    ("the Elsevier attribution reinstated",
     lambda s: s.replace(
         "% AT MOST 250 WORDS -- OUR line, not a quoted requirement (the KBS guide",
         "% ~200 words, Elsevier's limit for these journals.", 1)),
    # \s+ for the line breaks, not "\n": the file is CRLF, so a literal
    # newline in a multi-line anchor never matches.
    ("abstract credits verification with an accuracy gain",
     lambda s: re.sub(
         r"The\s+other\s+three\s+parts,\s+claim\s+verification\s+among\s+"
         r"them,\s+show\s+no\s+effect\s+our\s+tests\s+could\s+detect\.",
         lambda _m: "Claim verification improves accuracy measurably.",
         s, count=1)),
]

out = []
try:
    for name, mutate in CASES:
        txt = mutate(orig)
        assert txt != orig, f"corruption was a no-op: {name}"
        io.open(MAIN, "w", encoding="utf-8", newline="").write(txt)
        r = subprocess.run([sys.executable, "-m", "pytest",
                            "tests/test_paper_abstract.py", "-q"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode))
        io.open(MAIN, "w", encoding="utf-8", newline="").write(orig)
finally:
    io.open(MAIN, "w", encoding="utf-8", newline="").write(orig)

for name, rc in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")

r = subprocess.run([sys.executable, "-m", "pytest",
                    "tests/test_paper_abstract.py", "-q"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}  ({r.stdout.strip().splitlines()[-1]})")
passed = all(rc for _, rc in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
