"""highlights.txt must obey Elsevier's format and the paper's own claims.

This file was the one part of the manuscript nothing checked, and it is
the part an editor reads first. It had drifted: bullet 3 said "removing
the planner improves accuracy and cuts tokens by 31%" with no scope,
when both halves are WebQSP-only and the accuracy effect *reverses* on
ComplexWebQuestions. The body names the dataset in bold and spends a
paragraph on why pooling the two would be wrong; the abstract says "on
the shallower benchmark"; only the highlight dropped the qualifier.

Format verified against Elsevier's highlights guidance (August 2026):
three to five bullets, "no more than 85 characters, including spaces".

The interesting check is not the character count. It is that a claim
whose sign depends on the dataset must say so -- and that is derived
from the run records, so it starts failing on its own if a re-run ever
makes the effect consistent.
"""
import io
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HL = ROOT / "thesis_paper" / "highlights.txt"
NUMBERS = ROOT / "results" / "phase4" / "thesis_numbers.json"

pytestmark = pytest.mark.skipif(not HL.exists(), reason="highlights absent")

MAX_CHARS = 85
DATASETS = ("webqsp", "cwq")
# Ways a bullet can legitimately scope a claim to one benchmark.
SCOPE = re.compile(r"WebQSP|shallower benchmark|single-hop benchmark", re.I)


def bullets():
    return [l[2:].rstrip("\n") for l in io.open(HL, encoding="utf-8")
            if l.startswith("- ")]


def numbers():
    return json.load(io.open(NUMBERS, encoding="utf-8"))


def test_bullet_count_is_within_elseviers_range():
    n = len(bullets())
    assert 3 <= n <= 5, f"Elsevier allows three to five highlights; there are {n}"


def test_no_bullet_exceeds_the_character_limit():
    over = [(len(b), b) for b in bullets() if len(b) > MAX_CHARS]
    assert not over, "\n".join(
        f"{n} chars (limit {MAX_CHARS}): {b}" for n, b in over)


def test_no_bullet_claims_the_verification_layer_raises_accuracy():
    """The file states this exclusion itself; hold it to it.

    Section 6 reports the null. A highlight promising the opposite would
    be contradicted by the paper it introduces.
    """
    for b in bullets():
        low = b.lower()
        claims_gain = re.search(r"improv|rais|boost|increas|gain", low)
        about_verify = re.search(r"verif|grounding check|claim check", low)
        assert not (claims_gain and about_verify), (
            f"bullet claims verification improves accuracy: {b!r}")


def test_a_dataset_dependent_claim_names_its_dataset():
    """Derived from the records, not hard-coded.

    If removing the planner helps on one benchmark and hurts on the
    other, a bullet mentioning the planner has to scope itself. If a
    re-run ever makes the sign agree, this stops demanding the qualifier
    on its own rather than ossifying today's result.
    """
    abl = numbers()["ablations"]["by_condition"]
    deltas = {ds: abl[f"{ds}/half_abl_noplanner"]["f1"]
                  - abl[f"{ds}/half_abl_full"]["f1"] for ds in DATASETS}
    signs = {d > 0 for d in deltas.values()}
    dataset_dependent = len(signs) > 1
    planner = [b for b in bullets() if "planner" in b.lower()]
    if not dataset_dependent:
        pytest.skip(f"planner effect now agrees in sign: {deltas}")
    for b in planner:
        assert SCOPE.search(b), (
            f"the planner effect reverses between benchmarks "
            f"({', '.join(f'{k} {v:+.3f}' for k, v in deltas.items())}), "
            f"so this bullet must name which one: {b!r}")


def test_a_quoted_percentage_appears_in_the_paper():
    """Floor, not the real check: a highlight may not invent a figure.

    Weak on its own -- the paper is full of percentages, so a bullet can
    quote a real number from an unrelated claim and pass. The test below
    binds the one percentage that matters to its source.
    """
    body = "\n".join(
        io.open(p, encoding="utf-8").read()
        for p in sorted((ROOT / "thesis_paper" / "sections").glob("*.tex")))
    body += io.open(ROOT / "thesis_paper" / "agr-paper.tex", encoding="utf-8").read()
    for b in bullets():
        for pct in re.findall(r"(\d+)%", b):
            assert re.search(rf"{pct}\\?%", body), (
                f"highlight quotes {pct}% but the paper never states it: {b!r}")


def test_the_planner_token_cut_is_that_datasets_own_figure():
    """31% is WebQSP's token reduction; CWQ's is 21%.

    Presence-matching cannot tell those apart from any other percentage
    in the paper -- 44% is a real clip rate and would sail through. So
    the figure is recomputed from the records for whichever dataset the
    bullet scopes itself to.
    """
    abl = numbers()["ablations"]["by_condition"]

    def cut(ds):
        f = abl[f"{ds}/half_abl_full"]["mean_tokens"]
        n = abl[f"{ds}/half_abl_noplanner"]["mean_tokens"]
        return round(100 * (f - n) / f)

    for b in bullets():
        if "planner" not in b.lower():
            continue
        pcts = [int(p) for p in re.findall(r"(\d+)%", b)]
        if not pcts:
            continue
        ds = "webqsp" if SCOPE.search(b) else None
        assert ds, f"an unscoped planner bullet cannot quote a figure: {b!r}"
        assert pcts == [cut(ds)], (
            f"bullet says {pcts}%, {ds} token cut is {cut(ds)}% "
            f"(the other benchmark's is {cut('cwq')}%): {b!r}")
