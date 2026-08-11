"""The question identifiers the thesis cites must obey the convention it states.

erroranalysis.tex opens Chapter 9 with a promise to the reader: cases are cited
as stem plus the first eight hash characters, "which is unique within both
samples", because a bare stem does not identify a CWQ question. That is a
checkable claim about the .tex sources and the committed samples, and until now
nothing checked it -- the audit that caught two violations lived outside the
repo, so the next reader had to rewrite it to confirm anything.

Same argument test_kappa_agreement.py makes about the agreement claim: a promise
the project states to a reader is worth a test, not a habit.

Appendix C is excluded because it *lists* every identifier in full rather than
citing any, which is the thing that makes the eight-character form checkable.
"""
import json
import pathlib
import re
from collections import Counter

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOK = ROOT / "thesis_book"
SPLITS = [ROOT / "results" / "phase4" / f"test_{ds}.json"
          for ds in ("webqsp", "cwq")]

# In LaTeX the underscore is escaped: WebQTest-989\_4b6636a0
CITE = re.compile(r"WebQ(?:Test|Trn)-\d+(?:\\_[0-9a-f]{6,32})?")

# Appendix C is generated from the splits; the template files ship with the
# BUET class and are not \input by the build.
SKIP = {"samples.tex", "buetcsepgthesisciteexamples.tex",
        "buetcsepgthesischapterwithmathintitle.tex"}

pytestmark = pytest.mark.skipif(
    not all(p.exists() for p in SPLITS), reason="test splits absent")


@pytest.fixture(scope="module")
def qids():
    out = set()
    for p in SPLITS:
        out |= {r["qid"] for r in json.load(open(p, encoding="utf-8"))}
    return out


# Chapter 9 discusses one stem *as* a stem -- "all three questions sharing the
# stem WebQTrn-1770" -- and then gives each hash separately. That is the
# convention being explained, not broken, so a citation introduced by the word
# "stem" is held to a different rule below.
STEM_INTRO = re.compile(r"\bstems?\b[^.]{0,40}$")


@pytest.fixture(scope="module")
def citations():
    """Every identifier cited in prose, mapped to files and to how it was used.

    Returns {identifier: {"files": {...}, "as_stem": bool}}. as_stem is true only
    when every occurrence is introduced as a stem.
    """
    out = {}
    for p in BOOK.rglob("*.tex"):
        if p.name in SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        for m in CITE.finditer(text):
            key = m.group(0).replace("\\_", "_")
            lead = text[max(0, m.start() - 60):m.start()].replace("\n", " ")
            rec = out.setdefault(key, {"files": set(), "as_stem": True})
            rec["files"].add(p.name)
            rec["as_stem"] &= bool(STEM_INTRO.search(lead))
    return out


def _resolve(cite, qids):
    """Questions a citation names. Bare stems are handled as the prose says."""
    if "_" in cite:                       # stem + hash prefix
        return [q for q in qids if q.startswith(cite)], False
    exact = cite in qids                  # a whole WebQSP identifier
    cwq = [q for q in qids if q.startswith(cite + "_")]
    return cwq + ([cite] if exact else []), (not exact and bool(cwq))


def test_every_citation_resolves_to_exactly_one_question(citations, qids):
    assert citations, "no identifiers found -- the regex or the paths are wrong"
    broken = {}
    for c, rec in citations.items():
        hits, _ = _resolve(c, qids)
        if rec["as_stem"]:
            if not hits:                  # a stem must still name something
                broken[c] = (0, sorted(rec["files"]))
        elif len(hits) != 1:
            broken[c] = (len(hits), sorted(rec["files"]))
    assert not broken, (
        f"identifiers not naming exactly one question in the evaluated "
        f"splits (count, files): {broken}")


def test_no_cwq_question_is_cited_by_bare_stem(citations, qids):
    """The failure Chapter 9's preamble exists to prevent.

    A bare stem can resolve uniquely today and still be wrong tomorrow, which is
    why the convention is stem plus eight, not stem where that happens to work.
    """
    bare = {c: sorted(rec["files"]) for c, rec in citations.items()
            if _resolve(c, qids)[1] and not rec["as_stem"]}
    assert not bare, f"CWQ questions cited by bare stem: {bare}"


def test_eight_hash_characters_are_unique_within_both_samples(qids):
    """The property the convention rests on, stated in the same paragraph."""
    prefixes = Counter(q.split("_")[0] + "_" + q.split("_")[1][:8]
                       for q in qids if "_" in q)
    collisions = {p: n for p, n in prefixes.items() if n > 1}
    assert not collisions, (
        f"eight hash characters no longer disambiguate: {collisions}")


def test_preamble_counts_still_describe_the_samples(qids):
    """Chapter 9 quotes two counts as motivation; both are recomputable."""
    cwq = {q for q in qids if "_" in q}
    stems = Counter(q.split("_")[0] for q in cwq)
    assert max(stems.values()) == 12, (
        f"prose says one stem covers up to twelve CWQ questions; "
        f"the maximum is now {max(stems.values())}")
    shared = len(set(stems) & {q for q in qids if "_" not in q})
    assert shared == 13, (
        f"prose says thirteen stems are themselves WebQSP identifiers; "
        f"there are now {shared}")


# The reference list is maintained in two files: buetcsepgthesis.bib is what
# \bibliography builds against, and agr.bib is the annotated copy carrying the
# provenance comments. The bibliography preamble documents the arrangement and
# invites switching between them, which is exactly the condition under which a
# second copy drifts: the build reads one, a reader edits the other, and nothing
# complains until a citation resolves in one file and not the other.
KEY = re.compile(r"^@\w+\{([^,]+),", re.M)


def _keys(name):
    return KEY.findall((BOOK / name).read_text(encoding="utf-8"))


def test_the_two_bibliographies_have_not_drifted():
    built, annotated = _keys("buetcsepgthesis.bib"), _keys("agr.bib")
    assert built, "no entries parsed out of the built bibliography"
    missing = set(built) - set(annotated)
    extra = set(annotated) - set(built)
    assert not missing and not extra, (
        f"agr.bib and buetcsepgthesis.bib have diverged; only in the built "
        f"file: {sorted(missing)}; only in the annotated copy: {sorted(extra)}")
    assert built == annotated, (
        "the two bibliographies hold the same keys in a different order, so a "
        "diff between them is no longer readable")
