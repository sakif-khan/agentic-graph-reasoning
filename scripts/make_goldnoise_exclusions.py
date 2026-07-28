"""qids excluded from the census."""

def main():
    import json

    VALID = {"gold_ok", "gold_wrong", "ambiguous_question"}
    EXCLUDE = {"gold_wrong", "ambiguous_question"}   # not a system failure

    excl = {}
    for ds in ("webqsp", "cwq"):
        flags = json.load(open(f"results/phase4/prepass_goldnoise_{ds}.json",
                               encoding="utf-8"))
        bad = {f.get("verdict") for f in flags} - VALID - {""}
        assert not bad, f"{ds}: unrecognised verdict values {bad}"
        unfilled = [f["qid"] for f in flags if not f.get("verdict")]
        assert not unfilled, f"{ds}: {len(unfilled)} rows still unadjudicated"

        excl[ds] = sorted({f["qid"] for f in flags
                           if f["verdict"] in EXCLUDE})
        print(f"{ds}: {len(excl[ds])} qids excluded "
              f"({sum(1 for f in flags if f['verdict'] == 'gold_wrong')} gold_wrong rows, "
              f"{sum(1 for f in flags if f['verdict'] == 'ambiguous_question')} ambiguous rows)")

    json.dump(excl, open("results/phase4/census_exclusions.json", "w"), indent=1)

if __name__ == "__main__":
    main()
