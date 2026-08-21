"""Nothing may claim the output contract without stating what bounds it.

The contract -- "an answer paired with the triples that support it" -- is
the verification layer's whole deliverable, since the ablation shows it
does not move accuracy. It is also narrower than the phrase, in two
independent ways that the thesis spends a section (sec:output-contract)
withdrawing it down to:

  ROUTE   Only traversed adjacency attaches evidence. A claim certified by
          verify_connection or by the entailment fallback is accepted with
          nothing attached (agr/nodes.py, the three branches of the
          structural check). On the 80-question development set, 13 answers
          carry no supporting triples and two of those did assert a claim.

  RECORD  RunLogger writes n_supporting_triples -- an integer -- and drops
          the list (agr/runlog.py). No committed artifact in this
          repository contains a single supporting triple: verified across
          112,901 run records. A reader can confirm the answers came from a
          system that tracked its evidence; they cannot inspect it.

The thesis ranks this its most serious limitation, above the underpowered
ablations. It reached the deck and the rehearsal transcript anyway, in the
unbounded form and with nothing anywhere to bound it -- "attaches
supporting triples to every asserted claim", "you can check the system's
work" -- and from the manuscript's editing notes it was on its way into
the manuscript as guidance. A long document can make the claim in Sec 1
and bound it in Sec 6 because Sec 6 is always there to be read. A
twenty-two slide deck has no Sec 6.

So the rule is per *document*, not per file: whatever a reader receives as
one artifact must carry both bounds if it makes the claim at all. Where
the bounds live inside that artifact is an editorial matter.
"""
import io
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.skipif(
    not (ROOT / "thesis_presentation").exists(), reason="deck absent")


def _read(*globs):
    out = []
    for g in globs:
        for p in sorted(ROOT.glob(g)):
            out.append((p, io.open(p, encoding="utf-8", errors="replace").read()))
    return out


# What a reader receives in one piece. highlights.txt is deliberately not a
# unit of its own: it is five bullets under an 85-character limit, which
# cannot carry a bound, so it is held to the no-universal rule below and
# exempted from this one. It ships beside the manuscript, which does carry
# them.
def units():
    return {
        "deck": _read("thesis_presentation/content-*.tex"),
        "transcript": _read("thesis_presentation/transcript.md"),
        "manuscript": _read("thesis_paper/*.tex", "thesis_paper/sections/*.tex",
                            "thesis_paper/README.md"),
        "thesis": _read("thesis_book/chapters/*.tex",
                        "thesis_book/inputs/*abstract*.tex"),
    }


def flat(text):
    return " ".join(text.split())


# Claiming the contract. Any of these is enough to owe the bounds.
CLAIM = re.compile(
    r"output contract"
    r"|(?:attach|pair|carr|keep)\w*[^.]{0,70}supporting triples"
    r"|supporting triples[^.]{0,70}(?:attach|pair|carr|kept|keep)\w*"
    r"|paired with (?:the |its |whatever )?(?:traversed )?triples"
    r"|answers? (?:carry|carries) the traversed triples",
    re.I)

# Stating the route bound. Several wordings, because four documents say it
# four ways and pinning one phrasing would make this a spelling test.
BOUND_ROUTE = re.compile(
    r"one route of three"
    r"|one of the three routes"
    r"|only the first route"
    r"|uniquely among the three"
    r"|routes? records? evidence"
    r"|verify.connection[^.]{0,90}(?:attach|record|nothing|none|no evidence)"
    r"|entailment[^.]{0,60}attach (?:none|nothing)",
    re.I)

# Stating the record bound.
BOUND_RECORD = re.compile(
    r"n_supporting_triples"
    r"|count of supporting triples"
    r"|supporting triples[^.]{0,40}(?:rather than|not) the triples"
    r"|keeps? the .{0,12}count.{0,12} of supporting"
    r"|(?:drops|discards)[^.]{0,30}the list"
    r"|cannot (?:inspect|be audited)",
    re.I)


@pytest.mark.parametrize("unit", sorted(units()))
def test_a_document_that_claims_the_contract_states_both_bounds(unit):
    files = units()[unit]
    assert files, f"unit {unit!r} matched no files"

    claimed = [p for p, t in files if CLAIM.search(flat(t))]
    if not claimed:
        pytest.skip(f"{unit} does not claim the output contract")

    body = flat("\n".join(t for _, t in files))
    missing = []
    if not BOUND_ROUTE.search(body):
        missing.append(
            "ROUTE: that only traversed adjacency attaches evidence -- "
            "verify_connection and the entailment fallback attach none")
    if not BOUND_RECORD.search(body):
        missing.append(
            "RECORD: that the logger keeps the count of supporting triples "
            "and drops the list, so the evidence cannot be inspected")

    where = ", ".join(p.relative_to(ROOT).as_posix() for p in claimed[:4])
    assert not missing, (
        f"{unit} claims the output contract ({where}) and does not bound "
        f"it. Missing:\n  " + "\n  ".join(missing) +
        f"\n\nThis is the thesis's first-ranked limitation. A reader who "
        f"receives {unit} alone gets the claim and no way to discover it is "
        f"narrower than it sounds.")


# The specific false form, as it shipped: a universal quantifier governing
# what receives evidence. "every traversed triple joining the pair is
# attached" is TRUE and must keep passing, so the quantifier has to govern
# answers or claims rather than triples.
#
# The quantifier is bound to the verb that does the pairing, not merely
# placed near the word "evidence". A first version allowed any 90
# characters in between and reported two sentences that say the opposite of
# the overclaim -- "one had every claim rejected ... the route that records
# no evidence", and framework.tex's "the model adjudicates a residue rather
# than every claim, and only the first route yields evidence", which is the
# sentence that states the bound. Distance is not grammar; this is the same
# lesson the abstract's verification-gain rule already carries.
NOUN = r"(?:asserted\s+|single\s+)?(?:answer|claim|assertion)s?"
EVIDENCE = (r"(?:evidence|supporting triples|triples that support"
            r"|triples supporting)")
PAIRS = (r"(?:paired|pairs|carries|carry|carrying|comes?|arrives?|keeps?"
         r"|returns?|holds?|has|have|gets?|with)")

UNIVERSAL = re.compile(
    # "every answer arrives with ... evidence" -- quantified subject, then
    # the verb, with nothing but its own auxiliaries in between.
    rf"\bevery\s+{NOUN}\b\s+(?:that\s+|which\s+|it\s+|is\s+|are\s+|was\s+"
    rf"|were\s+|AGR\s+|the\s+system\s+)*{PAIRS}\b[^.]{{0,60}}?{EVIDENCE}"
    # "returns every answer paired with ... evidence" -- quantified object.
    rf"|(?:returns?|pairs?|attach\w*|emits?|deliver\w*)\s+(?:back\s+)?"
    rf"every\s+{NOUN}\b[^.]{{0,60}}?{EVIDENCE}"
    # "attaches supporting triples to every asserted claim" -- the dative.
    rf"|(?:attach|pair)\w*[^.]{{0,50}}?\bto\s+every\s+{NOUN}",
    re.I)

# Quoting the overclaim in order to retract it is not making it, and every
# document that fixed this now carries the old wording verbatim so the next
# reader knows what changed. A match wholly inside quotation marks -- plain
# or typographic, LaTeX's `` '' included -- is a citation.
#
# This is the ONLY exemption, and that is deliberate. The first version of
# this file also skipped any sentence containing a negation, which sounded
# reasonable and was vacuous: a beamer frame has almost no full stops, so
# all 22 slides collapsed into 64 "sentences", one of them 1,378 characters
# long, and "What it does not do" three bullets away suppressed the catch on
# "Attaches supporting triples to every asserted claim". Two of the six
# shipped overclaims went undetected that way. A retraction quotes what it
# retracts; that is a structural signal and a nearby "not" is not.
QUOTED = re.compile(r'"[^"]{0,400}"|``[^\']{0,400}\'\'|“[^”]{0,400}”')


def cited(text, span):
    """Does the match lie wholly inside a pair of quotation marks?

    Run over the whole document rather than over a sentence, because the
    documents this scans do not reliably have sentences.
    """
    return any(q.start() <= span[0] and span[1] <= q.end()
               for q in QUOTED.finditer(text))


@pytest.mark.parametrize("unit", sorted(list(units()) + ["highlights"]))
def test_nothing_promises_evidence_for_every_answer_or_claim(unit):
    files = (_read("thesis_paper/highlights.txt") if unit == "highlights"
             else units()[unit])
    bad = []
    for p, text in files:
        body = flat(text)
        for m in UNIVERSAL.finditer(body):
            if cited(body, m.span()):
                continue
            bad.append(f"{p.relative_to(ROOT).as_posix()}: "
                       f"...{body[max(0, m.start() - 40):m.end() + 40]}...")
    assert not bad, (
        "these promise evidence for every answer or every claim, and two of "
        "three verification routes attach none:\n  " + "\n  ".join(bad))
