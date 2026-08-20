"""thesis_paper/ must build from its own directory alone.

The manuscript is uploaded as a package: the publisher receives that
directory and nothing above it. Two dependencies used to escape it --
\\bibliography{../thesis_book/buetcsepgthesis} and
\\input{../thesis_book/figures/fig_claim_path} -- and both built fine here,
because here the parent directory exists. Nothing in the repository
noticed, since every check ran from the repository root.

Copying them in fixes the upload and creates the hazard the repository
already knows about from its two bibliographies: a second copy that drifts.
So the copies are pinned to their originals rather than merely made once.
The figure is exempted on one line, its `% !TEX root', which necessarily
differs -- that is the only difference permitted, and the test says which.
"""
import io
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAPER = ROOT / "thesis_paper"
BOOK = ROOT / "thesis_book"

pytestmark = pytest.mark.skipif(not PAPER.exists(), reason="manuscript absent")

# A LaTeX comment, unless the % is escaped.
COMMENT = re.compile(r"(?<!\\)%.*")


def _sources():
    return sorted(PAPER.glob("*.tex")) + sorted(PAPER.glob("sections/*.tex")) \
        + sorted(PAPER.glob("figures/*.tex"))


def test_no_source_reaches_outside_the_manuscript():
    """No \\input, \\bibliography or \\includegraphics may name a parent path.

    Comments are stripped first: every fragment carries a `% !TEX root =
    ../agr-paper.tex' line, which is a relative path out of sections/ and
    figures/ but stays inside thesis_paper/, and the header comments quote
    the old cross-directory paths while describing why they are gone.
    """
    bad = []
    for p in _sources():
        body = COMMENT.sub("", io.open(p, encoding="utf-8").read())
        for m in re.finditer(r"\\(input|include|bibliography|addbibresource|"
                             r"includegraphics|lstinputlisting)"
                             r"(?:\[[^\]]*\])?\{([^}]*)\}", body):
            if "../" in m.group(2):
                bad.append(f"{p.relative_to(ROOT).as_posix()}: "
                           f"\\{m.group(1)}{{{m.group(2)}}}")
    assert not bad, (
        "these escape thesis_paper/ and will not resolve once the directory "
        "is uploaded on its own:\n  " + "\n  ".join(bad))


def test_every_input_resolves_inside_the_manuscript():
    """The counterpart: what the sources do name must actually be there.

    A path can stay inside the directory and still be wrong. Checked against
    the filesystem so that repointing an \\input at a file that was never
    copied fails here rather than at upload.
    """
    missing = []
    for p in _sources():
        body = COMMENT.sub("", io.open(p, encoding="utf-8").read())
        for m in re.finditer(r"\\(?:input|include)\{([^}]*)\}", body):
            target = m.group(1)
            # \input is resolved relative to the main file's directory
            cand = PAPER / (target if target.endswith(".tex") else target + ".tex")
            if not cand.exists():
                missing.append(f"{p.relative_to(ROOT).as_posix()}: {target}")
    assert not missing, "\\input names a file that is not there:\n  " + \
        "\n  ".join(missing)


def test_the_bibliography_it_builds_against_is_present():
    m = re.search(r"\\bibliography\{([^}]*)\}",
                  io.open(PAPER / "agr-paper.tex", encoding="utf-8").read())
    assert m, "agr-paper.tex names no bibliography"
    assert (PAPER / (m.group(1) + ".bib")).exists(), \
        f"\\bibliography{{{m.group(1)}}} has no .bib beside it"


def test_the_copied_bibliography_has_not_drifted():
    """The paper's .bib is a copy of the thesis's; keep them byte-identical.

    Not a key-set comparison like test_citation_convention's: that one
    compares a built file against an annotated mirror, which legitimately
    differ in their comments. This is a straight copy, so any difference at
    all is drift.
    """
    a = io.open(PAPER / "agr-paper.bib", encoding="utf-8").read()
    b = io.open(BOOK / "buetcsepgthesis.bib", encoding="utf-8").read()
    assert a == b, (
        "thesis_paper/agr-paper.bib and thesis_book/buetcsepgthesis.bib have "
        "diverged. Re-copy rather than editing one of them: a reference added "
        "to the thesis will not otherwise reach the manuscript.")


def test_the_copied_figure_has_not_drifted():
    """Identical to the thesis's figure except for the one root line."""
    a = io.open(PAPER / "figures" / "fig_claim_path.tex", encoding="utf-8").read()
    b = io.open(BOOK / "figures" / "fig_claim_path.tex", encoding="utf-8").read()
    ROOTLINE = re.compile(r"^% !TEX root = .*$", re.M)
    assert ROOTLINE.search(a) and ROOTLINE.search(b), \
        "a copy lost its % !TEX root line"
    assert ROOTLINE.sub("", a) == ROOTLINE.sub("", b), (
        "thesis_paper/figures/fig_claim_path.tex has diverged from "
        "thesis_book/figures/fig_claim_path.tex in more than its root line.")
