"""Cohen's kappa between the human annotator's blind labels and the LLM judge,
over the same 100 sampled items.

Reads the hand-filled sheet and the hidden key produced by judge_support.py.
"""
import csv, json

human_labels = []
with open("results/phase4/tier2_judge/kappa_sheet.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        val = row["your_label(1/0)"].strip()
        assert val in ("0", "1"), f"row {row['idx']} not labeled: {val!r}"
        human_labels.append(int(val))

judge_key = json.load(open("results/phase4/tier2_judge/kappa_key.json",
                           encoding="utf-8"))
judge_labels = [int(bool(r["supported"])) for r in judge_key]

assert len(human_labels) == len(judge_labels), "row count mismatch"
n = len(human_labels)

# 2x2 confusion counts
a = sum(1 for y, j in zip(human_labels, judge_labels) if y == 1 and j == 1)
b = sum(1 for y, j in zip(human_labels, judge_labels) if y == 1 and j == 0)
c = sum(1 for y, j in zip(human_labels, judge_labels) if y == 0 and j == 1)
d = sum(1 for y, j in zip(human_labels, judge_labels) if y == 0 and j == 0)

po = (a + d) / n                                  # observed agreement
p_yes = (a + b) / n * (a + c) / n                 # expected by chance, "1"
p_no  = (c + d) / n * (b + d) / n                 # expected by chance, "0"
pe = p_yes + p_no
kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")

print(f"n={n}  agree={a + d}/{n} ({po:.1%})  "
      f"human-1={a + b}  judge-1={a + c}")
# Printed to four places deliberately. The pre-registered bar is 0.70 and this
# value misses it; rounding to three places prints "0.700", which reads as the
# bar being met and is the one presentation the thesis argues against.
print(f"Cohen's kappa = {kappa:.4f}  (pre-registered bar 0.70: "
      f"{'MET' if kappa >= 0.70 else 'MISSED'})")
