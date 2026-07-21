"""Cohen's kappa between your blind labels and
the LLM judge, on the same 100 sampled items."""
import csv, json

your_labels = []
with open("data/kappa_sheet.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        val = row["your_label(1/0)"].strip()
        assert val in ("0", "1"), f"row {row['idx']} not labeled: {val!r}"
        your_labels.append(int(val))

judge_key = json.load(open("data/kappa_key.json", encoding="utf-8"))
judge_labels = [int(bool(r["supported"])) for r in judge_key]

assert len(your_labels) == len(judge_labels), "row count mismatch"
n = len(your_labels)

# 2x2 confusion counts
a = sum(1 for y, j in zip(your_labels, judge_labels) if y == 1 and j == 1)
b = sum(1 for y, j in zip(your_labels, judge_labels) if y == 1 and j == 0)
c = sum(1 for y, j in zip(your_labels, judge_labels) if y == 0 and j == 1)
d = sum(1 for y, j in zip(your_labels, judge_labels) if y == 0 and j == 0)

po = (a + d) / n                                  # observed agreement
p_yes = (a + b) / n * (a + c) / n                 # expected by chance, "1"
p_no  = (c + d) / n * (b + d) / n                 # expected by chance, "0"
pe = p_yes + p_no
kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")

print(f"n={n}  agree={a + d}/{n} ({po:.1%})  "
      f"you-1={a + b}  judge-1={a + c}")
print(f"Cohen's kappa = {kappa:.3f}")
