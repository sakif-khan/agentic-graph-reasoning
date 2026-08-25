"""Reinstate the two ways the claim-route bound gets misreported.

The layer's structural routes ignore the claim's relation, and how much of
its output that touches is an interval the committed record does not narrow.
Two mistakes turn that interval into something more comfortable, and both
shipped in a draft of this work:

  INVERTED  the joint adjacency-or-entailment total, 1,969, read as a lower
            bound on relation-blind acceptances. The arithmetic makes it an
            upper bound on the adjacency route alone. Stated the wrong way
            round it converts a limitation into a reassurance, and the number
            is real either way, so review does not catch it.

  TRUNCATED the upper endpoint dropped, leaving "at least 39" where the
            record supports [39, 2,008]. Two orders of magnitude of exposure
            disappear and the sentence still reads as a measurement.

Both were missed by the first version of the guarding test, for the two
reasons the deck's own checker learned earlier: whole-file presence passes
when a value appears more than once, and nearness alone passes when the two
numbers co-occur for an unrelated reason. The corruptions below are the ones
that exposed each gap.

Every file is restored in a finally block.
"""
import pathlib
import subprocess
import sys

# run_all.py invokes every probe as `probe.py <ROOT>`; honour that rather than
# deriving the root, so the probe works the same run standalone or swept.
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
TEST = "tests/test_claim_route_bound.py"

FILES = {
    "verification.tex": ROOT / "thesis_book" / "chapters" / "verification.tex",
    "erroranalysis.tex": ROOT / "thesis_book" / "chapters" / "erroranalysis.tex",
    "discussion.tex": ROOT / "thesis_paper" / "sections" / "discussion.tex",
}

# (label, file, find, replace) -- each is the mistake the rule exists to catch.
CORRUPTIONS = [
    # The inverted inequality, in prose: the joint total sold as relation-blind.
    ("inverted inequality / erroranalysis", "erroranalysis.tex",
     "relation-blind test. \\Cref{sec:structural-check} shows",
     "relation-blind test. At least $1{,}969$ were relation-blind, and "
     "\\Cref{sec:structural-check} shows"),
    ("inverted inequality / discussion", "discussion.tex",
     "acceptances; the rest were made either by traversed adjacency",
     "acceptances; the other $1{,}969$ relation-blind ones were made "
     "either by traversed adjacency"),
    # Dropping the upper endpoint, which turns an interval into reassurance.
    ("upper endpoint dropped / verification", "verification.tex",
     "somewhere in $[39, 2{,}008]$ of the $2{,}008$ accepted",
     "at least $39$ of the accepted"),
    ("upper endpoint dropped / erroranalysis", "erroranalysis.tex",
     "beyond the interval $[39, 2{,}008]$",
     "beyond a floor of $39$"),
    ("upper endpoint dropped / discussion", "discussion.tex",
     "lies somewhere in\n$[39, 2{,}008]$",
     "is at least\n$39$"),
]


def run():
    r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode


originals = {k: v.read_text(encoding="utf-8") for k, v in FILES.items()}
assert run() == 0, "suite is not green before the probe"

caught = missed = 0
try:
    for label, fname, find, repl in CORRUPTIONS:
        path = FILES[fname]
        text = originals[fname]
        if find not in text:
            print(f"  [SKIP  ] {label}: anchor not present")
            continue
        path.write_text(text.replace(find, repl, 1), encoding="utf-8")
        red = run() != 0
        path.write_text(text, encoding="utf-8")
        print(f"  [{'CAUGHT' if red else 'MISSED'}] {label}")
        caught += red
        missed += not red
finally:
    for k, v in FILES.items():
        v.write_text(originals[k], encoding="utf-8")

print(f"\ncaught {caught}, missed {missed}")
assert run() == 0, "files not restored cleanly"
# run_all.py reads the LAST non-empty line as the verdict and matches it against
# a fixed vocabulary, so a probe that passes while signing off in its own words
# is reported as a failure. Say the phrase the sweep is looking for.
print("all files restored; suite green")
print("ALL CASES CAUGHT" if not missed else f"MISSED {missed}")
sys.exit(1 if missed else 0)
