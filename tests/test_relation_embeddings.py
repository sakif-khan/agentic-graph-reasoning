"""Sec 4.5's functional check must still say what its archived run said.

The section quotes two cosine scores and an ordering to argue that the relation
verbaliser is not degenerate: place_of_birth first, the inverse relation second,
and the rest of the top five plausible. That is a claim about a committed
artifact, and the artifact is the log of
scripts/check_relation_embeddings.py.

Same argument test_kappa_agreement.py and test_citation_convention.py make: a
promise the project states to a reader is worth a test, not a habit. The check
reads the archived log rather than re-running the encoder, so it stays offline
and deterministic -- rerunning the probe needs the model and the two data files,
which is the script's job, not this one's.
"""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG = ROOT / "results" / "phase1" / "check_relation_embeddings_log.txt"
PROSE = ROOT / "thesis_book" / "chapters" / "environment.tex"

# "1. Score: 0.7085 -> people.person.place_of_birth"
ROW = re.compile(r"^\s*(\d+)\.\s*Score:\s*([0-9.]+)\s*->\s*(\S+)\s*$", re.M)

pytestmark = pytest.mark.skipif(
    not LOG.exists(), reason="probe log absent")


@pytest.fixture(scope="module")
def ranking():
    rows = ROW.findall(LOG.read_text(encoding="utf-8"))
    return [(int(r), float(s), n) for r, s, n in rows]


def test_the_probe_log_holds_a_descending_top_five(ranking):
    """The shape the section's argument rests on."""
    assert len(ranking) == 5, f"expected five ranked rows, got {len(ranking)}"
    assert [r for r, _, _ in ranking] == [1, 2, 3, 4, 5]
    scores = [s for _, s, _ in ranking]
    assert scores == sorted(scores, reverse=True), (
        f"the archived ranking is not descending: {scores}")


def test_prose_quotes_the_first_two_rows_of_the_log(ranking):
    """The two numbers and two relation names Sec 4.5 states.

    A degenerate verbaliser is the thing being ruled out, so the identity of the
    top two matters as much as their scores.
    """
    text = PROSE.read_text(encoding="utf-8")
    # the paragraph that reports the probe, not the whole chapter
    start = text.index("A functional check confirms")
    para = text[start:start + 900]

    for rank, score, name in ranking[:2]:
        tex_name = name.replace("_", r"\_")
        assert tex_name in para, (
            f"rank {rank} of the archived probe is {name}, which the "
            f"prose does not name")
        stated = f"{score:.3f}"
        assert stated in para, (
            f"rank {rank} scored {score} in "
            f"results/phase1/check_relation_embeddings_log.txt; the prose "
            f"does not quote it as {stated}")


def test_the_inverse_relation_is_actually_second(ranking):
    """Sec 4.5 calls rank two 'the inverse relation'; that is checkable."""
    assert ranking[0][2] == "people.person.place_of_birth"
    assert ranking[1][2] == "location.location.people_born_here"
