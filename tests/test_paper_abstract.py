"""The abstract must hold the line the manuscript sets for it.

The abstract's own comment set a 200-word target and the abstract ran to
215, because nothing counted it. Nothing counted it because the target
looked like an external requirement rather than a rule of ours, and an
external requirement feels like someone else's job to enforce.

It was not external. The comment called 200 "Elsevier's limit for these
journals"; that was never checked, and Elsevier's generic guide for
authors asks only for "a concise and factual abstract" while setting no
word limit at all (checked August 2026). The KBS guide 403s to an
automated fetch by every route, so a journal-specific limit cannot be
ruled out -- but it cannot be cited either, and it was being cited.

So 200 is house style, and the second test below keeps the justification
honest: no comment in the abstract block may attribute the limit to
Elsevier unless someone has actually read a page that says so.
"""
import io
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN = ROOT / "thesis_paper" / "agr-paper.tex"

pytestmark = pytest.mark.skipif(not MAIN.exists(), reason="manuscript absent")

MAX_WORDS = 200


def _block():
    s = io.open(MAIN, encoding="utf-8").read()
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", s, re.S)
    assert m, "no abstract found"
    return m.group(1)


def words():
    """Count as a submission system would.

    $400$ and $0.755$ are one word each; \\emph{improves} counts as the
    word it emphasises; "---" is an em dash and not a word at all, which
    is worth two on its own in this abstract.
    """
    a = re.sub(r"(?<!\\)%.*", "", _block())
    a = re.sub(r"\\(?:emph|textbf|textit)\{([^}]*)\}", r"\1", a)
    a = a.replace("{,}", "")
    a = re.sub(r"\\[a-zA-Z]+", " ", a)
    a = a.replace("$", "").replace("{", " ").replace("}", " ")
    return [w for w in a.split() if re.search(r"[0-9A-Za-z]", w)]


def test_the_abstract_is_within_the_stated_limit():
    n = len(words())
    assert n <= MAX_WORDS, (
        f"the abstract runs to {n} words against the {MAX_WORDS} its own "
        f"comment sets. Trim it or move the line deliberately -- but the "
        f"comment and the text have to agree.")


def test_the_limit_is_not_attributed_to_elsevier_unverified():
    """Guard against reinstating the claim that was there before.

    Three separate Elsevier requirements were asserted in this manuscript
    without being read: author-supplied line numbers, Editorial Manager
    building the reviewer PDF, and this word limit. The pattern is citing
    a plausible rule from memory, so the citation is what gets checked.
    """
    comments = "\n".join(re.findall(r"(?<!\\)%.*", _block())).lower()
    claims_elsevier = re.search(r"elsevier'?s? (?:limit|requirement|maximum)"
                                r"|limit for these journals", comments)
    assert not claims_elsevier, (
        "the abstract comment attributes its word limit to Elsevier. "
        "Elsevier's generic guide sets no abstract word limit and the KBS "
        "guide is unfetchable, so this is house style: say so.")


def test_the_abstract_does_not_promise_verification_raises_accuracy():
    """Section 6 reports the null. The comment states this rule; hold it.

    An abstract that oversells the verification layer turns the paper's
    own attribution section into a retraction.
    """
    text = " ".join(words()).lower()
    for m in re.finditer(r"verification|verify|claim check", text):
        window = text[max(0, m.start() - 120):m.end() + 120]
        assert not re.search(r"improv\w*\s+accuracy|rais\w*\s+accuracy"
                             r"|accuracy\s+gain", window), (
            f"the abstract appears to credit verification with an accuracy "
            f"gain: ...{window}...")
