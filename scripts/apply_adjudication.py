"""Propagate manual gold-noise verdicts across all rows of
results/phase4/prepass_goldnoise_{ds}.json that share a qid.

Verdict is per-qid, not per-row (it describes the gold, and a qid can have
several flagged rows -- one per disagreeing system). VERDICTS is populated
below by reading whatever verdict/subtype/note is already set for each qid,
then applied to any other row of that qid still marked "".

Idempotent: rows that already have a verdict are left untouched. CWQ qids
are the full "<qid>_<32-char hash>" strings as they appear in the JSON."""
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
