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
import io
import pathlib
import re
import subprocess
import sys

# run_all.py invokes every probe as `probe.py <ROOT>`; honour that rather than
# deriving the root, so the probe works the same run standalone or swept.
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
TEST = "tests/test_claim_route_bound.py"

FILES = {
    # The keys keep the OLD chapter names because the CASES below address
    # them by key; only the paths moved. d79a945 folded verification.tex
    # into framework.tex and 15140dd folded results/setup/erroranalysis
    # into evaluation.tex, so from September 2026 this probe opened two
    # files that no longer existed and died before its first case.
    "verification.tex": ROOT / "thesis_book" / "chapters" / "framework.tex",
    "erroranalysis.tex": ROOT / "thesis_book" / "chapters" / "evaluation.tex",
    # The paper's arithmetic, which is no longer in discussion.tex: the
    # [39, 2,008] interval moved to Appendix D on 2026-09-23 when the
    # manuscript went on a hard page budget. discussion.tex still states the
    # limitation, without numbers, so there is nothing there to corrupt.
    "appendix-measurements.tex":
        ROOT / "journal" / "sections" / "appendix-measurements.tex",
    # The rehearsal script answers this question out loud, and it spells
    # thousands the way prose does rather than the way LaTeX does. Both
    # renderings, because nothing derives one from the other.
    "transcript.md": ROOT / "thesis_presentation" / "transcript.md",
    "transcript.tex": ROOT / "thesis_presentation" / "transcript.tex",
}

# (label, file, find, replace) -- each is the mistake the rule exists to catch.
CORRUPTIONS = [
    # The inverted inequality, in prose: the joint total sold as relation-blind.
    # A full stop again: the sentence read "was made by a relation-blind test
    # --- \Cref{...} shows" from the chapter merge until the book traded its
    # em-dashes for sentence breaks (2026-09-29), and now reads "test.
    # \Cref{...} shows". A missing anchor SKIPs here rather than failing, so
    # this line has to move with the sentence.
    ("inverted inequality / erroranalysis", "erroranalysis.tex",
     "relation-blind test. \\Cref{sec:structural-check} shows",
     "relation-blind test. At least $1{,}969$ were relation-blind, and "
     "\\Cref{sec:structural-check} shows"),
    ("inverted inequality / appendix-measurements",
     "appendix-measurements.tex",
     "acceptances, and the rest were made either by traversed adjacency",
     "acceptances, and the other $1{,}969$ relation-blind ones were made "
     "either by traversed adjacency"),
    # Dropping the upper endpoint, which turns an interval into reassurance.
    ("upper endpoint dropped / verification", "verification.tex",
     "somewhere in $[39, 2{,}008]$ of the $2{,}008$ accepted",
     "at least $39$ of the accepted"),
    ("upper endpoint dropped / erroranalysis", "erroranalysis.tex",
     "beyond the interval $[39, 2{,}008]$",
     "beyond a floor of $39$"),
    ("upper endpoint dropped / appendix-measurements",
     "appendix-measurements.tex",
     "relation lies somewhere in $[39, 2{,}008]$",
     "relation is at least $39$"),
    # Under questioning the floor is the tempting number, and the sentence
    # that follows would go with it -- so the corruption takes both. Leaving
    # "That is an interval two orders of magnitude wide" behind would park the
    # word "interval" within eighty characters of a surviving 2,008 and let a
    # gutted paragraph pass, which is the near-miss this rule already learned
    # once on discussion.tex.
    ("upper endpoint dropped / transcript.md", "transcript.md",
     "somewhere between 39 and all 2,008 were certified without any test of the\n"
     "asserted relation. That is an interval two orders of magnitude wide and I "
     "report\nit as one rather than choose a point inside it.",
     "at least 39 were certified without any test of the asserted relation.\n"
     "That is a floor rather than a guess."),
    ("upper endpoint dropped / transcript.tex", "transcript.tex",
     "somewhere between 39 and all 2,008 were certified without\n"
     "any test of the asserted relation. That is an interval two orders of\n"
     "magnitude wide and I report it as one rather than choose a point inside\n"
     "it.",
     "at least 39 were certified without any test of the\n"
     "asserted relation. That is a floor rather than a guess."),
    # And the inverted inequality, in the register it would actually be said
    # in: the joint total offered as the reassuring half of the answer.
    ("inverted inequality / transcript.md", "transcript.md",
     "and the log does not separate them: on test, of 2,008 accepted",
     "and 1,969 of them were relation-blind: on test, of 2,008 accepted"),
]


def run():
    r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode


def read(p):
    """Read without translating line endings, so restoring cannot change them.

    Path.read_text/write_text translate both ways on Windows, which turned
    every file this probe touched into CRLF -- including on the restore, and
    including on a clean pass. prove_residuals.py looks for an LF-joined block
    in transcript.md and could not find one afterwards.
    """
    return io.open(p, encoding="utf-8", newline="").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="").write(s)


def native(s, text):
    """The anchor, spelled in the line ending `text` actually uses."""
    return s.replace("\n", "\r\n" if "\r\n" in text else "\n")


# transcript.tex is a RENDERING of transcript.md, produced by
# build_transcript.py, which is frozen with the pre-defense -- so between
# defenses the file simply does not exist. Same treatment as OPTIONAL in
# tests/test_claim_route_bound.py: a rendering that has not been built
# cannot state the interval wrongly, and the .md beside it is corrupted
# either way. Reading it unconditionally aborted this probe before its
# first case, which is how it came to prove nothing at all.
originals = {k: read(v) for k, v in FILES.items() if v.exists()}
assert run() == 0, "suite is not green before the probe"

caught = missed = 0
try:
    for label, fname, find, repl in CORRUPTIONS:
        if fname not in originals:
            print(f"  [SKIP  ] {label}: {fname} is not generated")
            continue
        path = FILES[fname]
        text = originals[fname]
        # Whitespace-tolerant, not a plain substring test. Every file here is
        # hard-wrapped -- the book at 80 columns, the paper at 72 -- so an
        # anchor of more than a few words is hostage to wherever the fill
        # last put a line break. Four of these cases were reporting "anchor
        # not present" against sentences sitting in the file in full, which
        # makes a probe claim a rule is unreachable when it is not.
        pattern = re.compile(r"\s+".join(map(re.escape, find.split())))
        m = pattern.search(text)
        if not m:
            print(f"  [SKIP  ] {label}: anchor not present")
            continue
        write(path, text[:m.start()] + native(repl, text) + text[m.end():])
        red = run() != 0
        write(path, text)
        print(f"  [{'CAUGHT' if red else 'MISSED'}] {label}")
        caught += red
        missed += not red
finally:
    for k, v in FILES.items():
        if k in originals:
            write(v, originals[k])

print(f"\ncaught {caught}, missed {missed}")
assert run() == 0, "files not restored cleanly"
# run_all.py reads the LAST non-empty line as the verdict and matches it against
# a fixed vocabulary, so a probe that passes while signing off in its own words
# is reported as a failure. Say the phrase the sweep is looking for.
print("all files restored; suite green")
print("ALL CASES CAUGHT" if not missed else f"MISSED {missed}")
sys.exit(1 if missed else 0)
