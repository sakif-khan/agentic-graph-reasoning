"""Stage E1: merged failure histogram (Stage A + Stage D), per dataset,
wrong and hedge always kept separate.

Sources merged, none double-counted (each qid lives in exactly one):
  - labels_{ds}.csv            Stage D's main census
  - labels_{ds}_dropped.csv    Stage-D-discovered gold_noise/ambiguous_question
                                cases later promoted to formal Stage-C
                                exclusions -- kept here so a case like
                                WebQTrn-64_d8e43a... (found during Stage D
                                reading, then excluded from re-generated
                                census) doesn't silently vanish from the count
  - ablations/noplanner_categories_{ds}.csv   Stage A (run
      pull_noplanner_categories.py first; skipped with a note if missing)

Prints wrong and hedge as separate histograms per dataset -- never pooled
into one, per this project's own sampling guideline (wrong = reasoning
error, hedge = usually a retrieval/coverage gap; pooling them conflates
two different failure classes).
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
            for cat, n in c.most_common():
                print(f"    {cat:<24} {n:>3}  ({n / max(total, 1):.0%})")


if __name__ == "__main__":
    main()
