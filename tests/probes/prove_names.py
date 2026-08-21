"""Prove the tool slide's operation names are checked against the code.

Case 1 reinstates the shipped cell: \\texttt{link_entity}, which is not the
name of anything. The operation is search_entity -- in kg_tools.py, in
app:tool-search, in tab:toolapi -- and "link_entity" appeared nowhere else
in the repository. Every number in the deck was bound to its source; the
identifiers were bound to nothing.

Cases 2-5 are the rest of that class: another invented name, the operation
sec:five-operations says no node calls listed among the live four, a fifth
row, and the code renaming an operation the slide does not follow.

The last block is the opposite shape and is the point of `uncomment`.
These slides carry comments quoting the exact wording a rule bans, so a
rule that reads comments as content fires on the note explaining itself.
The echo-attractor rule passed only because a line wrap put "%" between
"the" and "task" -- rewrapping a comment would have failed a correct
slide. That rewrap is applied here and asserted NOT to fail.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
DECK = ROOT / "thesis_presentation" / "content-main.tex"
KG = ROOT / "agr" / "kg_tools.py"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (DECK, KG)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0] if fail else r.stdout.strip()[-90:])


def edit(path, old, new):
    def go():
        pattern = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


CASES = [
    ("shipped: the slide names link_entity, which does not exist",
     edit(DECK, r"\texttt{search\_entity}", r"\texttt{link\_entity}")),
    ("a different invented name",
     edit(DECK, r"\texttt{search\_entity}", r"\texttt{resolve\_entity}")),
    ("the operation no node calls listed among the live four",
     edit(DECK, r"\texttt{search\_entity}", r"\texttt{verify\_triple}")),
    ("a fifth row appears on a slide that lists four",
     edit(DECK, r"\texttt{search\_entity}  & Surface form $\rightarrow$ node",
          r"\texttt{get\_relations} & Again & Again \\ "
          r"\texttt{search\_entity}  & Surface form $\rightarrow$ node")),
    ("the code renames an operation and the slide does not follow",
     edit(KG, "def search_entity(self, surface_form: str, k: int = 5):",
          "def resolve_entity(self, surface_form: str, k: int = 5):")),
]

out = []
try:
    for name, mutate in CASES:
        mutate()
        rc, first = run()
        out.append((name, rc, first))
        restore()

    # Must NOT fire: a comment quoting the banned wording is a comment.
    print("these must not fire:")
    io.open(DECK, "w", encoding="utf-8", newline="").write(
        orig[DECK].replace(
            '% This read "it appears across systems, so it is a property of the\n'
            "      % task, not of AGR\" -- defensive where the thesis is substantive.",
            '% This read "it appears across systems, so it is a property of'
            ' the task, not of AGR"\n'
            "      % -- defensive where the thesis is substantive."))
    assert io.open(DECK, encoding="utf-8").read() != orig[DECK], \
        "the rewrap was a no-op: the comment moved"
    rewrap_rc, rewrap_first = run()
    print(f"{'CLEAN' if rewrap_rc == 0 else 'FIRED':7s}  "
          f"the banned wording, quoted in a source comment")
    print(f"{'':9s}{rewrap_first[:96]}")
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{first[:96]}")

rc, first = run()
print(f"\nrestored -> rc={rc}  ({first[:70]})")
passed = all(rc for _, rc, _ in out) and rewrap_rc == 0 and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
