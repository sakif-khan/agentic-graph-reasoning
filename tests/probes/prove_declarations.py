"""Prove the declaration tests fire.

Cases 1-4 restore the shipped state exactly: the four items that were
absent while the manuscript built to 47 pages with no errors. The rest are
near misses -- a corref with no matching cortext, an invented CRediT role,
an AI declaration that discloses without accepting responsibility, and one
pushed out of its required position.

agr-paper.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
MAIN = ROOT / "thesis_paper" / "agr-paper.tex"
orig = io.open(MAIN, encoding="utf-8", newline="").read()


def cut(pattern):
    """Delete a whole \\section* block by its heading."""
    def go(s):
        m = re.search(r"\\section\*\{" + pattern + r"[\s\S]*?(?=\\section\*|"
                      r"\\bibliographystyle)", s)
        assert m, f"could not find section {pattern!r}"
        return s[:m.start()] + s[m.end():]
    return go


def sub(old, new):
    def go(s):
        assert old in s, f"anchor missing: {old!r}"
        return s.replace(old, new, 1)
    return go


def resub(pattern, new):
    """Whitespace-tolerant variant for anchors that span a line break."""
    def go(s):
        out, n = re.subn(pattern, lambda _m: new, s, count=1)
        assert n, f"anchor missing: {pattern!r}"
        return out
    return go


CASES = [
    ("shipped: no corresponding author designated",
     sub(r"\author[buet]{Md. Sakif Khan\corref{cor1}}",
         r"\author[buet]{Md. Sakif Khan}")),
    ("shipped: no CRediT statement",
     cut("CRediT")),
    ("shipped: no funding statement",
     cut("Funding")),
    ("shipped: no generative-AI declaration",
     cut("Declaration of generative AI")),
    ("corref present but cortext label removed",
     sub(r"\cortext[cor1]{Corresponding author}", "")),
    ("an invented CRediT role",
     sub("Formal analysis", "Experimentation")),
    # Regex, not a literal: this anchor spans a line break, and the file's
    # endings flipped from LF to CRLF under a git round-trip, so "\n"
    # stopped matching. Multi-line anchors must be whitespace-tolerant.
    ("AI declaration drops the responsibility clause",
     resub(r"and take full responsibility for the content of the\s+publication\.",
           "and are satisfied with it.")),
    ("AI declaration no longer immediately before the references",
     sub(r"\bibliographystyle{elsarticle-num}",
         "\\section*{Appendix A}\nLate addition.\n\n"
         r"\bibliographystyle{elsarticle-num}")),
]

out = []
try:
    for name, mutate in CASES:
        io.open(MAIN, "w", encoding="utf-8", newline="").write(mutate(orig))
        r = subprocess.run([sys.executable, "-m", "pytest",
                            "tests/test_paper_declarations.py", "-q"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode))
        io.open(MAIN, "w", encoding="utf-8", newline="").write(orig)
finally:
    io.open(MAIN, "w", encoding="utf-8", newline="").write(orig)

for name, rc in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")

r = subprocess.run([sys.executable, "-m", "pytest",
                    "tests/test_paper_declarations.py", "-q"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}  ({r.stdout.strip().splitlines()[-1]})")
passed = all(rc for _, rc in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
