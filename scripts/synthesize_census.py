"""Stage E1: merge the Stage A and Stage D failure censuses into one
histogram per dataset, keeping wrong answers and hedges separate.

Three label sources are merged. Each question ID appears in exactly one of
them, so nothing is double-counted:

  - labels_{ds}.csv
        Stage D's main census.
  - labels_{ds}_dropped.csv
        Cases found during Stage D reading that were later promoted to formal
        Stage C exclusions. They are counted here so that a case removed from
        the regenerated census still appears in the totals.
  - ablations/noplanner_categories_{ds}.csv
        Stage A. Run pull_noplanner_categories.py first; if the file is absent
        this source is skipped and the omission is noted in the output.

Wrong answers and hedges are printed as separate histograms and are never
pooled: a wrong answer is a reasoning error, whereas a hedge is usually a
retrieval or coverage gap, and combining them would hide that distinction.
"""
import csv
from collections import Counter
from pathlib import Path

DIR = Path("results/phase4")


def add_rows(hist, path):
    if not path.exists():
        return 0
    n = 0
    for row in csv.DictReader(open(path, encoding="utf-8")):
        if row["category"] and row["kind"] in ("wrong", "hedge"):
            hist[row["kind"]][row["category"]] += 1
            n += 1
    return n


def main():
    for ds in ("webqsp", "cwq"):
        hist = {"wrong": Counter(), "hedge": Counter()}

        n_d = add_rows(hist, DIR / f"labels_{ds}.csv")
        n_dropped = add_rows(hist, DIR / f"labels_{ds}_dropped.csv")
        stage_a_path = DIR / "ablations" / f"noplanner_categories_{ds}.csv"
        n_a = add_rows(hist, stage_a_path)

        print(f"\n=== {ds} ===")
        print(f"  Stage D: {n_d}   Stage-D-dropped: {n_dropped}   "
              f"Stage A: {n_a}{'' if stage_a_path.exists() else ' (missing -- run pull_noplanner_categories.py)'}"
              f"   total: {n_d + n_dropped + n_a}")

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


if __name__ == "__main__":
    main()
