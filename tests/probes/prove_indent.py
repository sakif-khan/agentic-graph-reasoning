"""Prove tests/test_comment_indent.py fires, and does not overfire.

Three cases reinstate the drift as it actually landed, in the two shapes
it took: a module-level comment at four spaces among neighbours at zero
(check_slides.py:1515, twice), and a comment at eight inside a block
whose body sits at four (:1544, :1618, :1647). All four arrived the same
way -- a patch anchored on a line's first non-whitespace character keeps
that line's indent and prepends the replacement's own.

The must-not-fire cases matter more than usual here. This rule scans
every Python file in the repository, so a version of it that flags
ordinary code would have to be suppressed somewhere, and a suppressed
rule is a dead one. Two shapes that look like the defect and are not: a
comment inside a bracketed literal, which every annotated CASES list in
this directory uses, and a comment introducing an indented block. The
first version of the rule reported about sixty of the former.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
TEST = "tests/test_comment_indent.py"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"
THIS = ROOT / "tests" / "probes" / "prove_indent.py"

FILES = (CHECK, THIS)
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


def append_block(path, block):
    """Add a shape at the end of a file, to see whether it is flagged."""
    def go():
        s = orig[path]
        nl = "\r\n" if "\r\n" in s else "\n"
        io.open(path, "w", encoding="utf-8", newline="").write(
            s.rstrip("\r\n") + nl + nl + block.replace("\n", nl) + nl)
    return go


# Two shapes that are one step deeper than the statement around them and
# are correct. If either is flagged the rule cannot be run over the repo.
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

CASES = [
    ("shipped: a comment at 8 inside a block indented 4",
     deepen(CHECK, "`capped` and `named` come from the tool-slide block")),
    ("shipped: a module-level comment at 4",
     deepen(CHECK, "Named, not described as \"the static baselines\"")),
]

MUST_NOT_FIRE = [
    ("a comment inside a bracketed literal", append_block(THIS, IN_BRACKETS)),
    ("a comment introducing an indented block", append_block(THIS,
                                                             BLOCK_INTRO)),
    # The bound is one step, and this is what buys that narrowness: a
    # comment aligned to something further in is deliberate, so it is
    # outside the rule rather than suppressed inside it.
    ("a comment two steps deeper, which is alignment not drift",
     deepen(CHECK, "Both spellings, because the two artifacts count", 8)),
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
