"""qids excluded from the census."""

def main():
    import json
    from collections import defaultdict

    VALID = {"gold_ok", "gold_wrong", "ambiguous_question"}
    EXCLUDE = {"gold_wrong", "ambiguous_question"}   # not system failures

    excl, summary = {}, {}
    for ds in ("webqsp", "cwq"):
        flags = json.load(open(f"results/phase4/prepass_goldnoise_{ds}.json",
                               encoding="utf-8"))

        bad = {f.get("verdict") for f in flags} - VALID - {""}
        assert not bad, f"{ds}: unrecognised verdict values {bad}"
        unfilled = [f["qid"] for f in flags if not f.get("verdict")]
        assert not unfilled, f"{ds}: {len(unfilled)} rows still unadjudicated"

        # a verdict describes the GOLD, so every row of a qid must agree
        by_qid = defaultdict(set)
        for flag in flags:
            by_qid[flag["qid"]].add(flag["verdict"])
        conflicts = {q: v for q, v in by_qid.items() if len(v) > 1}
        assert not conflicts, f"{ds}: conflicting verdicts within a qid: {conflicts}"

        rows = defaultdict(int)
        qids = defaultdict(set)
        for flag in flags:
            rows[flag["verdict"]] += 1
            qids[flag["verdict"]].add(flag["qid"])

        excl[ds] = sorted({flag["qid"] for flag in flags if flag["verdict"] in EXCLUDE})

        print(f"\n=== {ds} ===")
        print(f"{'verdict':<20}{'rows':>6}{'questions':>11}")
        for v in VALID:
            print(f"{v:<20}{rows[v]:>6}{len(qids[v]):>11}")
        print(f"{'TOTAL':<20}{sum(rows.values()):>6}{len(by_qid):>11}")
        print(f"excluded from census: {len(excl[ds])} questions "
            f"({len(excl[ds]) / 400:.1%} of the {ds} test set)")

        summary[ds] = {"flag_rows": sum(rows.values()),
                       "flagged_questions": len(by_qid),
                       "gold_wrong_questions": len(qids["gold_wrong"]),
                       "ambiguous_questions": len(qids["ambiguous_question"]),
                       "gold_ok_questions": len(qids["gold_ok"]),
                       "excluded_questions": len(excl[ds])}

    json.dump(excl, open("results/phase4/census_exclusions.json", "w"), indent=1)
    json.dump(summary, open("results/phase4/goldnoise_summary.json", "w"), indent=1)
    print("\nwrote census_exclusions.json + goldnoise_summary.json")

if __name__ == "__main__":
    main()
