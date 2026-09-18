"""Stage E1: merge the Stage A and Stage D failure censuses into one
histogram per dataset, keeping wrong answers and hedges separate.

The census population is every question AGR did not answer correctly on
the test sample, LESS the adjudicated gold-defect exclusions in
census_exclusions.json. That is what the thesis and the paper say it is
("all 41 were removed before the census began"), so an excluded question
must not appear in the histogram whatever label file it sits in.

Three label sources are merged, in this order, and a question ID is
counted once, from the first source that carries it:

  - labels_{ds}.csv
        Stage D's main census.
  - ablations/noplanner_categories_{ds}.csv
        Stage A. Run pull_noplanner_categories.py first; if the file is
        absent this source is skipped and the omission is noted.
  - labels_{ds}_dropped.csv
        Cases found during Stage D reading that were later promoted to
        formal Stage C exclusions. Read for completeness of the audit
        trail; every row in it is excluded and so none is counted.

Until September 2026 the dropped file WAS counted, and two Stage A rows
that name excluded questions were counted too, so the histogram carried
three excluded questions and read as 259 while the population it claims
to cover held 262, six of which no label file had reached. The coverage
block at the end of each dataset's report now states the population, the
number read, and the identifiers still unread, so that "the census is a
population, not a sample" is a checked claim rather than a remembered one.

Wrong answers and hedges are printed as separate histograms and are never
pooled: a wrong answer is a reasoning error, whereas a hedge is usually a
retrieval or coverage gap, and combining them would hide that distinction.
"""
import csv
import json
import unicodedata
from collections import Counter
from pathlib import Path

DIR = Path("results/phase4")


def _norm(s):
    return unicodedata.normalize("NFKC", s).casefold().strip()


def _hit(rec):
    return bool({_norm(g) for g in rec["gold"]}
                & {_norm(a) for a in rec.get("answer_entities", [])})


def population(ds, excluded):
    """AGR's non-hits on the test sample, less the exclusions."""
    recs = [json.loads(l) for l in
            open(DIR / f"test_{ds}_agr.jsonl", encoding="utf-8") if l.strip()]
    return {r["qid"] for r in recs if not _hit(r)} - excluded


def add_rows(hist, path, excluded, seen, counted_ids):
    """Add one label file. Returns (rows counted, rows skipped as excluded,
    rows skipped as already counted)."""
    if not path.exists():
        return 0, 0, 0
    n = n_ex = n_dup = 0
    for row in csv.DictReader(open(path, encoding="utf-8")):
        if not (row["category"] and row["kind"] in ("wrong", "hedge")):
            continue
        if row["qid"] in excluded:
            n_ex += 1
            continue
        if row["qid"] in seen:
            n_dup += 1
            continue
        seen.add(row["qid"])
        counted_ids.add(row["qid"])
        hist[row["kind"]][row["category"]] += 1
        n += 1
    return n, n_ex, n_dup


def main():
    exclusions = json.load(open(DIR / "census_exclusions.json",
                                encoding="utf-8"))
    for ds in ("webqsp", "cwq"):
        excluded = {q if isinstance(q, str) else q["qid"]
                    for q in exclusions[ds]}
        hist = {"wrong": Counter(), "hedge": Counter()}
        seen, counted = set(), set()

        n_d, ex_d, _ = add_rows(hist, DIR / f"labels_{ds}.csv",
                                excluded, seen, counted)
        stage_a_path = DIR / "ablations" / f"noplanner_categories_{ds}.csv"
        n_a, ex_a, dup_a = add_rows(hist, stage_a_path, excluded, seen,
                                    counted)
        n_dropped, ex_dropped, _ = add_rows(
            hist, DIR / f"labels_{ds}_dropped.csv", excluded, seen, counted)

        print(f"\n=== {ds} ===")
        print(f"  Stage D: {n_d}   Stage A: {n_a}"
              f"{'' if stage_a_path.exists() else ' (missing -- run pull_noplanner_categories.py)'}"
              f"   Stage-D-dropped: {n_dropped}"
              f"   total: {n_d + n_a + n_dropped}")
        print(f"  skipped as excluded: {ex_d + ex_a + ex_dropped}"
              f"   skipped as duplicate: {dup_a}")

        for kind in ("wrong", "hedge"):
            c = hist[kind]
            total = sum(c.values())
            print(f"  -- {kind} (n={total}) --")
            # most_common() breaks ties by insertion order, which is the order
            # the label files happened to be read in. Equal-count categories
            # then swap places between runs that changed nothing, and the log
            # is a committed artifact that build_thesis_numbers.py parses. Sort
            # ties by name so a diff of this file means a number moved.
            for cat, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"    {cat:<24} {n:>3}  ({n / max(total, 1):.0%})")

        pop = population(ds, excluded)
        unread = sorted(pop - counted)
        stray = sorted(counted - pop)
        print(f"  -- coverage --")
        print(f"    population: {len(pop)}   read: {len(pop & counted)}"
              f"   unread: {len(unread)}")
        for q in unread:
            print(f"    unread {q}")
        for q in stray:
            print(f"    STRAY (labelled but not a remaining failure) {q}")


if __name__ == "__main__":
    main()
