"""Prove tests/test_output_contract_claims.py fires.

Six cases reinstate the overclaim exactly as it shipped, in each of the six
places it had reached: two slides, the rehearsal transcript, the thesis
abstract, the manuscript's editing notes, and the highlights file.

Four more delete the bounds instead of restoring the claim -- the realistic
failure, since a bound is what gets cut when a slide runs long. A document
that still makes the claim and no longer bounds it must fail. What counts
as stating a bound is imported from the checker rather than restated here,
so the two cannot drift.

The last case is the one that keeps the exemption honest. The rule ignores a
match inside quotation marks, because every document that fixed this quotes
the old wording in order to retract it; that exemption is an escape hatch,
so the probe unquotes one and checks it is caught.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
TEST = "tests/test_output_contract_claims.py"

DECK = ROOT / "thesis_presentation" / "content-main.tex"
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
TABS = ROOT / "thesis_book" / "inputs" / "buetcsepgthesisabstract.tex"
PREADME = ROOT / "thesis_paper" / "README.md"
HIGH = ROOT / "thesis_paper" / "highlights.txt"

FILES = (DECK, SCRIPT, TABS, PREADME, HIGH)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def edit(path, old, new):
    """Replace `old' once, matching across line breaks.

    Every one of these files is hard-wrapped and several have flipped
    between LF and CRLF under git round-trips, so a literal multi-line
    anchor is a liability -- runs of whitespace become \\s+ and the anchor
    survives a rewrap. The replacement goes in through a lambda so that a
    backslash in the LaTeX does not read as a regex group reference.

    The gap also swallows a markdown blockquote marker. transcript.md is
    written as `> ' quoted speech, so a rewrap puts "\\n> " between two
    words and plain \\s+ stops at the `>'. That is not hypothetical: an
    unrelated edit to the same sentence moved the wrap by four words and
    this probe went from CAUGHT to raising, which run_all reported as a
    failure -- correctly, since a probe that cannot find its anchor proves
    nothing about the check.
    """
    gap = r"\s+(?:>\s*)?"
    pattern = re.compile(gap.join(re.escape(w) for w in old.split()))

    def go():
        s = orig[path]
        assert pattern.search(s), f"anchor not found in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, s, count=1))
    return go


# The checker's OWN definition of each bound, imported rather than
# restated. A first version of this probe kept parallel literal lists and
# they drifted immediately: the checker accepted "from one route of" and
# "verify_connection ... nothing attached", the probe's list did not name
# either, so two cases reported the bound removed while it was still there
# and the probe called a live check dead. Same failure as prove_clause
# reading the abstract without going through the shipped predicate.
sys.path.insert(0, str(ROOT))
from tests.test_output_contract_claims import (   # noqa: E402
    BOUND_ROUTE, BOUND_RECORD, CLAIM, flat)


def rewrapped(bound):
    """The checker's pattern, made to match across a line break.

    The checker flattens whitespace before matching; a probe has to edit the
    file, which is not flattened. So `one route of three' matches the
    checker's view and misses the source, where the deck wraps it as `one
    route of\\n            three'. Every literal space in the pattern becomes
    \\s+ -- strictly more permissive, and derived from the imported pattern
    rather than a second copy of it.
    """
    return re.compile(bound.pattern.replace(" ", r"\s+"), bound.flags)


def strip_bound(path, bound, label):
    """Excise every span the checker would accept as stating this bound.

    Substitution rather than line deletion: these patterns span line breaks
    (their `[^.]' classes match newlines), which is precisely why deleting
    whole lines left half a match behind. What remains must still make the
    claim, or the test would skip instead of fail -- asserted, not assumed.
    """
    def go():
        s = orig[path]
        assert bound.search(flat(s)), \
            f"{path.name} does not state the {label} bound"
        cut = rewrapped(bound).sub("[bound removed]", s)
        assert not bound.search(flat(cut)), \
            f"{label} bound survives in {path.name} after substitution"
        assert CLAIM.search(flat(cut)), \
            f"removing the {label} bound also removed the claim in {path.name}"
        io.open(path, "w", encoding="utf-8", newline="").write(cut)
    return go


def unquote_a_retraction():
    """Strip the quotation marks off a cited overclaim, making it a claim."""
    def go():
        s = orig[HIGH]
        m = re.search(r'"(pairs every answer[^"]*)"', s)
        assert m, "highlights.txt no longer quotes the retracted bullet"
        io.open(HIGH, "w", encoding="utf-8", newline="").write(
            s[:m.start()] + m.group(1) + s[m.end():])
    return go


CASES = [
    ("shipped: slide 15, evidence for every asserted claim",
     edit(DECK, r"\item Attaches \alert{supporting triples} --- from one route of",
          r"\item Attaches \alert{supporting triples} to every asserted claim %")),
    ("shipped: slide 6, returns every answer with its evidence",
     edit(DECK, "carries its evidence with the answer",
          "returns every answer with its evidence")),
    ("shipped: transcript, attaches to every claim it does assert",
     edit(SCRIPT, "It attaches supporting triples to the claims traversal",
          "It attaches supporting triples to every claim it does assert. Traversal")),
    ("shipped: thesis abstract, returns every answer paired with",
     edit(TABS, "And the claims its traversal\ngrounds come back paired with the triples that support them.",
          "And it returns every answer\npaired with the triples that support it.")),
    ("shipped: manuscript editing note, every answer arrives with",
     edit(PREADME, "is the output contract. Claiming that",
          "is the output contract: every answer arrives with the traversed "
          "triples supporting it. Claiming that")),
    ("shipped: highlights bullet 1, pairs every answer",
     edit(HIGH, "- Agentic KGQA framework returns answers with the traversed "
                "triples supporting them",
          "- Agentic KGQA framework pairs every answer with the triples that "
          "support it")),
    ("deck keeps the claim, loses the route bound",
     strip_bound(DECK, BOUND_ROUTE, "route")),
    ("deck keeps the claim, loses the record bound",
     strip_bound(DECK, BOUND_RECORD, "record")),
    ("transcript keeps the claim, loses the route bound",
     strip_bound(SCRIPT, BOUND_ROUTE, "route")),
    ("transcript keeps the claim, loses the record bound",
     strip_bound(SCRIPT, BOUND_RECORD, "record")),
    ("a retraction with its quotation marks removed",
     unquote_a_retraction()),
]

out = []
try:
    for name, mutate in CASES:
        mutate()
        r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                           cwd=ROOT, capture_output=True, text=True)
        first = next((l.strip() for l in r.stdout.splitlines()
                      if l.startswith("FAILED")), "")
        out.append((name, r.returncode, first))
        restore()
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    if first:
        print(f"{'':9s}{first[:96]}")

r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}  "
      f"({r.stdout.strip().splitlines()[-1]})")
passed = all(rc for _, rc, _ in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
