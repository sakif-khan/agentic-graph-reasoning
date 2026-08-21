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


# A clause boundary: punctuation, or a conjunction that starts a new one.
CLAUSE = re.compile(r"[,;:.]|\bwhile\b|\band that\b|\bwhereas\b|\balthough\b"
                    r"|\bbut\b|\byet\b")
GAIN = re.compile(r"improv\w*\s+accuracy|rais\w*\s+accuracy"
                  r"|boost\w*\s+accuracy|increas\w*\s+accuracy"
                  r"|accuracy\s+(?:gain|improvement)")
VERIFY = re.compile(r"verification|verifier|verify|claim check")
NEGATED = re.compile(r"\b(?:no|not|never|without|cannot|nor)\b")
# ",X," where X is short and carries no sentence punctuation: an aside.
PARENTHETICAL = re.compile(r",\s*([^,.;:]{1,80}?),\s*")


def elide_parentheticals(text):
    """Rejoin a subject to its verb across an appositive.

    Splitting on commas alone puts "claim verification, which checks each
    claim against the traversed triples, improves accuracy" into three
    clauses, with the subject in the first and the verb in the third, and
    the rule sees neither together. Subject, non-restrictive relative,
    verb is the ordinary way an abstract introduces exactly this sentence
    -- the paper's own abstract uses the shape, with em dashes rather
    than commas, and words() drops em dashes, so it escaped by accident.

    An aside that itself mentions the component or a gain is kept, since
    removing it would lose the thing being tested.
    """
    prev = None
    while prev != text:
        prev = text
        text = PARENTHETICAL.sub(
            lambda m: m.group(0)
            if VERIFY.search(m.group(1)) or GAIN.search(m.group(1))
            else " ",
            text, count=1)
    return text


def test_the_abstract_does_not_promise_verification_raises_accuracy():
    """Section 6 reports the null. The comment states this rule; hold it.

    An abstract that oversells the verification layer turns the paper's
    own attribution section into a retraction.

    Checked per clause, not by proximity. This test used to take a
    +-120-character window around each mention of verification and fail
    if a gain phrase fell inside it. That measures distance, and the rule
    is about grammatical subject: the hazard is verification *being* the
    thing said to improve accuracy, not sitting near something else that
    does. The abstract legitimately says the planner improves accuracy in
    one clause and that verification shows no detectable accuracy effect
    in the next, and the window cleared that by five characters -- so any
    trim of the clause between them turned a correct abstract red. It is
    the clause that carries the claim, so the clause is what is read.

    Parentheticals are elided first, so an appositive between subject and
    verb does not hide one from the other; see elide_parentheticals.

    Known limits, both vocabulary rather than structure: passive voice
    ("accuracy is improved by the verification layer") and gain verbs
    outside GAIN ("lifts accuracy") are not caught. Chasing those is
    where this stops paying for itself.
    """
    text = elide_parentheticals(" ".join(words()).lower())
    for clause in CLAUSE.split(text):
        if not VERIFY.search(clause):
            continue
        g = GAIN.search(clause)
        if not g:
            continue
        # "verification does not improve accuracy" states the null; that
        # is the paper's finding, not a promise of a gain.
        if NEGATED.search(clause[:g.start()]):
            continue
        raise AssertionError(
            f"the abstract credits verification with an accuracy gain in "
            f"its own clause: {clause.strip()!r}")
