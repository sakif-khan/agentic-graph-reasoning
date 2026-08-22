"""Prove tests/test_indent_drift.py fires, and does not overfire.

Four cases reinstate the drift as it actually landed, in the two shapes
it took. As a comment: at four spaces among neighbours at zero
(check_slides.py:1515), and at eight inside a block whose body sits at
four (:1544, :1618, :1647). As an element of a bracketed literal: at
sixteen among siblings at eight (units() in
test_output_contract_claims.py) and at twenty-two among siblings at
eleven (TARGETS in run_all.py). All nine arrived the same way -- a patch
anchored on a line's first non-whitespace character keeps that line's
indent and prepends the replacement's own.

The must-not-fire cases matter more than usual here. These rules scan
every Python file in the repository, so a version of either that flags
ordinary code would have to be suppressed somewhere, and a suppressed
rule is a dead one. Six shapes that look like the defect and are not: a
comment inside a bracketed literal, a comment introducing an indented
block, a comment two steps deeper -- which is alignment, not drift -- a
dict value wrapped onto its own line at twice its key's column, a string
continued on its own line at twice the element column, and an element
merely off the modal column rather than at twice it.

Only two of the six exclude anything in the repository as it stands,
where both rules flag nothing. Dropping the comment rule's bracket test
reports seventy-four comments. Dropping the element rule's test for what
continues an element rather than starting one reports six, every one of
them a wrapped dict value in prove_clause.py; drop that clause and the
doubling bound together and it reports thirty-one.

The other two clauses -- exactly twice rather than merely different, and
a modal column held by at least two lines -- exclude nothing here at
all. Removing either changes no count, on this commit or on the one
before it, where four element drifts were still live. They are not
filters earning their keep. They are the statement that doubling is the
signature of this defect and that a line at some other column is a style
question, and their cases are here so that stays a decision rather than
drifting into one by accident.

Not covered, and deliberately: a two-element literal whose second
element drifted. With one line at each column neither is the norm, so
the rule stays quiet rather than guess. The last must-not-fire case
pins that behaviour so it is a decision on record, not an accident.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
TEST = "tests/test_indent_drift.py"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"
RUNALL = ROOT / "tests" / "probes" / "run_all.py"
CONTRACT = ROOT / "tests" / "test_output_contract_claims.py"
THIS = ROOT / "tests" / "probes" / "prove_indent.py"

FILES = (CHECK, RUNALL, CONTRACT, THIS)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                       cwd=ROOT, capture_output=True, text=True)
    hit = next((l.strip() for l in r.stdout.splitlines()
                if re.search(r"\.py:\d+: col ", l)), "")
    return r.returncode, hit


def deepen(path, anchor, extra=4):
    """Push one standalone comment `extra` spaces further in.

    Located by its text, not by line number: the file it edits is under
    active development and every line number in it has moved this month.
    """
    def go():
        s = orig[path]
        m = re.search(rf"^([ \t]*)(# {re.escape(anchor)}.*)$", s, re.M)
        assert m, f"anchor gone in {path.name}: {anchor!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            s[:m.start()] + " " * (len(m.group(1)) + extra) + m.group(2)
            + s[m.end():])
    return go


def widen(path, anchor):
    """Double one element line's indent, which is what the patch did.

    Not `deepen` with a bigger step: the defect is the existing indent
    plus the replacement's own, so the reinstated column has to be twice
    whatever the line currently sits at, not a fixed number of spaces.
    """
    def go():
        s = orig[path]
        m = re.search(rf"^([ \t]+)({re.escape(anchor)})", s, re.M)
        assert m, f"anchor gone in {path.name}: {anchor!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            s[:m.start()] + m.group(1) * 2 + m.group(2) + s[m.end():])
    return go


def append_block(path, block):
    """Add a shape at the end of a file, to see whether it is flagged."""
    def go():
        s = orig[path]
        nl = "\r\n" if "\r\n" in s else "\n"
        io.open(path, "w", encoding="utf-8", newline="").write(
            s.rstrip("\r\n") + nl + nl + block.replace("\n", nl) + nl)
    return go


# Shapes that are deeper than the code around them and are correct. If
# any is flagged the rules cannot be run over the repository at all.
IN_BRACKETS = '''
_SHAPES = [
    # A comment annotating an element of a literal. Every CASES list in
    # this directory is written this way.
    ("a", 1),
    ("b", 2),
]
'''

BLOCK_INTRO = '''
def _shape():
    # A comment introducing the block it sits at the head of.
    return 1
'''

# In each of these the suspect line sits at exactly twice the modal
# column of its own bracket, so only the element test's other clause can
# hold it back. That is the point: they fail if that clause is dropped.
WRAPPED_VALUE = '''
_WRAPPED = {
    "a key whose value does not fit beside it":
        "the value, one step past the key and so twice its column",
    "a second key, so four is the modal column": 1,
    "a third": 2,
}
'''

CONTINUED_STRING = '''
_TEXT = [
    "an element ending in an implicit concatenation, "
        "continued on the next line at twice the element column",
    "a second element, so four is the modal column",
    "a third",
]
'''

OFF_MODAL = '''
_OFFSET = [
    "an element at the modal column",
    "a second at the modal column",
      "a third pushed in by two -- off the norm, but not a doubling",
]
'''

LONE_PAIR = '''
_PAIR = [
    "one element at four",
        "one at eight, so no column is held twice and neither is the norm",
]
'''

CASES = [
    ("shipped: a comment at 8 inside a block indented 4",
     deepen(CHECK, "`capped` and `named` come from the tool-slide block")),
    ("shipped: a module-level comment at 4",
     deepen(CHECK, "Named, not described as \"the static baselines\"")),
    ("shipped: a dict element at 16 among siblings at 8",
     widen(CONTRACT, '"thesis": _read(')),
    ("shipped: a tuple element at 22 among siblings at 11",
     widen(RUNALL, '"scripts/check_tex_roots.py",')),
]

MUST_NOT_FIRE = [
    ("a comment inside a bracketed literal", append_block(THIS, IN_BRACKETS)),
    ("a comment introducing an indented block", append_block(THIS,
                                                             BLOCK_INTRO)),
    # The comment bound is one step, and this is what buys that
    # narrowness: a comment aligned to something further in is
    # deliberate, so it is outside the rule rather than suppressed
    # inside it.
    ("a comment two steps deeper, which is alignment not drift",
     deepen(CHECK, "Both spellings, because the two artifacts count", 8)),
    ("a dict value wrapped onto its own line", append_block(THIS,
                                                            WRAPPED_VALUE)),
    ("a string continued on its own line", append_block(THIS,
                                                        CONTINUED_STRING)),
    ("an element off the modal column but not at twice it",
     append_block(THIS, OFF_MODAL)),
    ("a two-element literal, where no column is the norm",
     append_block(THIS, LONE_PAIR)),
]

rc, hit = run()
assert rc == 0, f"not clean before the probe: {hit}"

out, quiet = [], []
try:
    for name, mutate in CASES:
        mutate()
        out.append((name, *run()))
        restore()
    for name, mutate in MUST_NOT_FIRE:
        mutate()
        quiet.append((name, *run()))
        restore()
finally:
    restore()

for name, rc, hit in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{hit[:96]}")
for name, rc, hit in quiet:
    print(f"{'QUIET' if not rc else 'OVERFIRED':7s}  {name}")
    if rc:
        print(f"{'':9s}{hit[:96]}")

rc, hit = run()
print(f"\nrestored -> rc={rc}  ({hit[:70]})")
passed = (all(rc for _, rc, _ in out) and not any(rc for _, rc, _ in quiet)
          and rc == 0)
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
