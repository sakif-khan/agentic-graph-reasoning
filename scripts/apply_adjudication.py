"""Propagate manual gold-noise verdicts across all rows of
results/phase4/prepass_goldnoise_{ds}.json that share a qid.

A verdict is recorded per question ID rather than per row, because it
describes the gold answer and one question can have several flagged rows, one
for each disagreeing system. VERDICTS below is filled from whatever verdict,
subtype and note is already set for a question ID, then applied to any
remaining row of that question that is still blank.

Re-runnable: rows that already carry a verdict are left untouched. CWQ question
IDs are the full "<qid>_<32-char hash>" strings as they appear in the JSON."""
import json

VERDICTS = {}
for ds in ("webqsp", "cwq"):
    path = f"results/phase4/prepass_goldnoise_{ds}.json"
    flags = json.load(open(path, encoding="utf-8"))
    VERDICTS[ds] = {
        f["qid"]: [f["verdict"], f.get("subtype", ""), f.get("note", "")]
        for f in flags
        if f.get("verdict")
    }


def main():
    for ds, table in VERDICTS.items():
        path = f"results/phase4/prepass_goldnoise_{ds}.json"
        flags = json.load(open(path, encoding="utf-8"))
        hit = 0
        for f in flags:
            if f.get("verdict"):
                continue
            row = table.get(f["qid"])
            if row:
                f["verdict"], f["subtype"], f["note"] = row
                hit += 1
        json.dump(flags, open(path, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        left = sum(1 for f in flags if not f.get("verdict"))
        print(f"{ds}: filled {hit}, remaining {left}")


if __name__ == "__main__":
    main()
