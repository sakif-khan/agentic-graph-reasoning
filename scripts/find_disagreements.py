"""extract rater-vs-judge disagreement rows.

Joins kappa_sheet.csv (your blind labels) with kappa_key.json (the judged
sample, in sheet order), verifies alignment, enriches from judge_support.json,
and writes logs/kappa_disagreements.json with a manual annotation placeholder.
"""
import csv, json, sys

def main():
    SHEET = "data/kappa_sheet.csv"
    KEY = "data/kappa_key.json"
    FULL = "logs/judge_support.json"
    OUT = "logs/kappa_disagreements.json"

    # ---- load your labels, keyed by sheet idx ----
    your = {}
    with open(SHEET, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            val = row["your_label(1/0)"].strip()
            if val not in ("0", "1"):
                sys.exit(f"row idx={row['idx']} not labeled (got {val!r}) -- "
                         "finish the sheet first")
            your[int(row["idx"])] = {"label": int(val), "sheet_row": row}

    key = json.load(open(KEY, encoding="utf-8"))
    if len(key) != len(your):
        sys.exit(f"count mismatch: sheet has {len(your)}, key has {len(key)}")

    # ---- full judge file, for enrichment (keyed on identity fields) ----
    full = json.load(open(FULL, encoding="utf-8"))
    full_by = {(r["run"], r["qid"], r["entity"]): r for r in full}

    disagreements = []
    for idx, rec in enumerate(key):
        # alignment guard: sheet row idx must describe the same item as key[idx]
        srow = your[idx]["sheet_row"]
        if (srow["question"] != rec["question"]
                or srow["entity"] != rec["entity"]):
            sys.exit(f"ALIGNMENT FAILURE at idx={idx}: sheet says "
                     f"{srow['entity']!r}, key says {rec['entity']!r} -- "
                     "sheet was reordered or edited; do not trust the join")

        judge_label = int(bool(rec["supported"]))
        if your[idx]["label"] == judge_label:
            continue

        enriched = dict(full_by.get((rec["run"], rec["qid"], rec["entity"]), rec))
        enriched.update({
            "sheet_idx": idx,
            "your_label": your[idx]["label"],
            "judge_label": judge_label,
            "direction": ("you-1/judge-0" if your[idx]["label"] == 1
                        else "you-0/judge-1"),
            "disagreement_note": "",          # <- fill in manually
        })
        disagreements.append(enriched)

    json.dump(disagreements, open(OUT, "w", encoding="utf-8"),
            indent=1, ensure_ascii=False)

    d10 = sum(1 for d in disagreements if d["direction"] == "you-1/judge-0")
    d01 = len(disagreements) - d10
    print(f"{len(disagreements)} disagreements -> {OUT}")
    print(f"  you-1/judge-0 (judge stricter): {d10}")
    print(f"  you-0/judge-1 (judge more lenient): {d01}")
    for d in disagreements:
        print(f'  [{d["sheet_idx"]:>3}] {d["direction"]}  '
              f'{d["question"][:55]!r}  -> {d["entity"][:35]!r}')

if __name__ == "__main__":
    main()
