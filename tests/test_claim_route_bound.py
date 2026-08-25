"""The relation-blind acceptance exposure must be quoted as a bound, not a number.

Both structural routes of the verification layer ignore the claim's relation
and its direction, which sec:verify-failure-modes calls the layer's principal
acceptance risk. How much of the layer's output that risk actually touches is
the question a reader asks next, and the committed record answers it only
partly:

  EXACT     claims decomposed, accepted and rejected, from the verifier trace
            entries; and every verify_connection call with its verdict, from the
            tool log, which carries one call per claim reaching that branch.

  NOT EXACT how the remaining acceptances split between traversed adjacency and
            the entailment check. A claim routed to entailment leaves no
            per-claim record, and n_structural counts entailment-accepted claims
            alongside structural ones -- which is exactly why sec:output-contract
            fences that counter.

So the relation-blind share of acceptances is an interval, and the first draft of
this work got the inequality backwards: it read the joint total as a lower bound
on relation-blind acceptances when the arithmetic makes it an upper bound on the
adjacency route alone. That error is easy to make, survives review because the
number is real, and inflates a limitation into a reassurance. The tests below fix
the direction of the inequality against the generated file, and refuse any prose
that states a point estimate where the interval belongs.

Same argument test_output_contract_claims.py makes about the output contract: a
bound the project states to a reader is worth a test, not a habit.
"""
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
NUMS = ROOT / "results" / "phase4" / "thesis_numbers.json"

PROSE = [
    ROOT / "thesis_book" / "chapters" / "verification.tex",
    ROOT / "thesis_book" / "chapters" / "erroranalysis.tex",
    ROOT / "thesis_paper" / "sections" / "discussion.tex",
    # The deck's own answer to "your verifier doesn't check the relation",
    # in both renderings. It is the shortest statement of the interval in the
    # project and the one delivered under questioning, which is the worst
    # place for it to have drifted to a floor.
    ROOT / "thesis_presentation" / "transcript.md",
    ROOT / "thesis_presentation" / "transcript.tex",
]


def forms(n):
    """Every spelling of n these documents use, longest first.

    Three, not two: LaTeX writes thousands as 2{,}008, prose writes 2,008, and
    both sit beside a bare 2008 elsewhere. The rule knew the first and third
    only, so adding transcript.md to PROSE without this would have failed on
    text that states the interval correctly.
    """
    return "|".join(sorted({re.escape(str(n)),
                            re.escape(f"{n:,}"),
                            re.escape(f"{n:,}".replace(",", "{,}"))},
                           key=len, reverse=True))


@pytest.fixture(scope="module")
def block():
    return json.load(NUMS.open(encoding="utf-8"))["claim_routes"]


def test_claims_partition_into_accepted_and_rejected(block):
    """n_structural is read as the accepted count; that only holds if it closes."""
    for scope in ("webqsp", "cwq", "total"):
        b = block[scope]
        assert b["claims_decomposed"] == b["claims_accepted"] + b["claims_rejected"], (
            f"{scope}: claims do not partition, so n_structural is not the "
            f"accepted count the prose reads it as")


def test_route_two_is_a_subset_of_the_accepted(block):
    t = block["total"]
    assert 0 < t["route2_accepted"] <= t["route2_calls"] <= t["claims_decomposed"]
    assert t["route2_accepted"] <= t["claims_accepted"]


def test_the_interval_is_bounded_the_right_way_round(block):
    """The joint total bounds the adjacency route ABOVE, not relation-blind below.

    The inequality this asserts is the one the first draft inverted. If
    adjacency_or_entailment_accepted is ever read as a lower bound on
    relation-blind acceptances, this fails.
    """
    t = block["total"]
    joint = t["adjacency_or_entailment_accepted"]
    assert joint == t["claims_accepted"] - t["route2_accepted"]
    # The interval endpoints are what the prose quotes.
    assert t["relation_blind_accepted_min"] == t["route2_accepted"]
    assert t["relation_blind_accepted_max"] == t["claims_accepted"]
    assert t["relation_blind_accepted_min"] < t["relation_blind_accepted_max"], (
        "a degenerate interval would mean the record does pin the share down, "
        "and the prose saying it cannot would be wrong")
    # The joint total is strictly inside the interval: it cannot be either end.
    assert t["relation_blind_accepted_min"] < joint < t["relation_blind_accepted_max"]


def test_the_totals_are_the_sum_of_the_datasets(block):
    for k in block["total"]:
        assert block["total"][k] == block["webqsp"][k] + block["cwq"][k], k


def test_firings_agree_with_the_verifier_route_block():
    """Two blocks count verifier firings independently and must agree."""
    doc = json.load(NUMS.open(encoding="utf-8"))
    assert (doc["claim_routes"]["total"]["verifier_firings"]
            == doc["verifier_route"]["total"]["verifier_invocations"])


@pytest.mark.parametrize("path", PROSE, ids=lambda p: p.name)
def test_prose_quoting_the_joint_total_says_it_is_a_bound(path, block):
    """1,969 may not appear as a count of anything relation-blind.

    It is the joint adjacency-or-entailment total. Stated as a quantity of
    relation-blind acceptances it is the inverted inequality, in prose.
    """
    joint = block["total"]["adjacency_or_entailment_accepted"]
    text = " ".join(path.read_text(encoding="utf-8").split())
    for form in forms(joint).split("|"):
        for m in re.finditer(form, text):
            window = text[m.start(): m.end() + 220]
            assert not re.search(r"relation-blind|relation blind", window), (
                f"{path.name}: {form} is quoted next to a relation-blind claim. "
                f"It bounds the traversed-adjacency route from above; it is not "
                f"a count of relation-blind acceptances.\n  ...{window}...")


@pytest.mark.parametrize("path", PROSE, ids=lambda p: p.name)
def test_prose_naming_the_exposure_gives_both_endpoints(path, block):
    """Wherever the exposure is characterised, both ends of the interval appear."""
    t = block["total"]
    text = " ".join(path.read_text(encoding="utf-8").split())
    # Three vocabularies reach the same claim, and a file using any of them is
    # characterising the exposure. Matching only "relation-blind" left
    # verification.tex -- which states the interval but phrases the mechanism as
    # "matches on the relation" -- outside the check that guards it.
    if not re.search(r"relation-blind|relation blind|matches on the relation"
                     r"|acceptance risk", text):
        pytest.skip("this file does not characterise the exposure")
    lo, hi = t["relation_blind_accepted_min"], t["relation_blind_accepted_max"]

    def positions(n):
        """Where this number appears, matched whole so 39 misses 1939.

        The lookarounds exclude digits and a decimal point but NOT a comma.
        LaTeX writes thousands as {,}, so a bare comma beside a number is
        punctuation -- and excluding it hid "$[39, 2{,}008]$" from this rule,
        which is the one form the rule most needs to see.
        """
        return [m.start() for m in
                re.finditer(rf"(?<![\d.])(?:{forms(n)})(?![\d.])", text)]

    lows, highs = positions(lo), positions(hi)
    assert lows, f"{path.name}: lower endpoint {lo} is not stated"

    # Presence anywhere in the file is the wrong question -- 2,008 is quoted
    # several times over for unrelated reasons, so a whole-file lookup passes
    # even when the sentence carrying the interval has lost its upper end.
    # Nearness alone is not enough either: both numbers legitimately appear
    # together while merely counting claims, and that co-occurrence satisfied
    # this rule on a paragraph whose interval had been deleted. So the pair has
    # to sit beside language that reads as an interval, not just beside itself.
    def reads_as_an_interval(a, b):
        """Interval language must lead into the pair, not merely be nearby.

        The window used to reach eighty characters either side, and the
        transcript's answer opens "every claim those two routes accept
        between them" a clause earlier. That stray "between" kept the rule
        green on a paragraph whose interval had been cut back to "at least
        39" -- the third time this rule has been passed by proximity, after
        whole-file presence and bare nearness. So the region is now the
        run-up to the first endpoint plus the span to the second: "[39,",
        "somewhere in", "between 39 and" all live there, and a connective
        belonging to a different sentence does not.
        """
        region = text[max(0, min(a, b) - 30): max(a, b)]
        return re.search(r"\[|between|interval|somewhere in|ranges|and at most",
                         region) is not None

    assert any(abs(a - b) <= 120 and reads_as_an_interval(a, b)
               for a in lows for b in highs), (
        f"{path.name}: {lo} and {hi} never appear together as an interval, so "
        f"the exposure reads as a floor rather than the range the record "
        f"actually supports")
