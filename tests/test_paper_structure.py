"""No section may open straight into a subsection.

A reader arriving at "4. Experimental Setup" immediately followed by
"4.1. Knowledge Environment" has been given a number and no orientation:
nothing says what the section establishes or why its parts are in that
order. Three sections did this -- Related Work, Experimental Setup, and
Results -- and it is invisible in the source, where the heading and the
subheading are two adjacent lines that both look deliberate.

The lead-in is not required to be long. It is required to exist, to be a
sentence, and to say something: the threshold below is set so that a
stray fragment left behind by an edit does not satisfy it.
"""
import io
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "thesis_paper" / "sections"

pytestmark = pytest.mark.skipif(not SECTIONS.exists(), reason="manuscript absent")

COMMENT = re.compile(r"(?<!\\)%.*")
MIN_WORDS = 15


def _lead_in(raw, start):
    """Prose between a section heading and whatever heading comes next."""
    rest = raw[start:]
    nxt = re.search(r"\\(sub)?section\{", rest)
    return (rest[:nxt.start()] if nxt else rest), bool(nxt and nxt.group(1))


def _words(tex):
    plain = re.sub(r"\\[a-zA-Z]+|[{}$]", " ", tex)
    return [w for w in plain.split() if re.search(r"[A-Za-z0-9]", w)]


def test_no_section_opens_with_a_subsection():
    bare = []
    for p in sorted(SECTIONS.glob("*.tex")):
        raw = COMMENT.sub("", io.open(p, encoding="utf-8").read())
        for m in re.finditer(r"\\section\{([^}]*)\}\s*\\label\{[^}]*\}", raw):
            lead, has_sub = _lead_in(raw, m.end())
            if not has_sub:
                continue          # no subsections; the section is its own prose
            words = _words(lead)
            if len(words) < MIN_WORDS or "." not in lead:
                title = re.sub(r"\s+", " ", m.group(1))
                bare.append(f"{p.name}: {title!r} -- {len(words)} words "
                            f"before its first subsection")
    assert not bare, (
        "these sections run straight into a subsection, giving the reader a "
        "number and no orientation:\n  " + "\n  ".join(bare))
