"""stratified sample of AGR's main-matrix non-near-miss wrongs
and hedges, dumped as reviewable packets + a labels.csv."""
import csv, json, random

def main():
    random.seed(42)
    N_PER_DATASET = 60

    for ds in ("webqsp", "cwq"):
        recs = {r["qid"]: r for r in
                (json.loads(l) for l in
                open(f"results/phase4/test_{ds}_agr.jsonl", encoding="utf-8"))}
        prepass = {r["qid"]: r for r in
                json.load(open(f"results/phase4/prepass_wrongs_{ds}.json",
                                encoding="utf-8"))}

        wrong_qids = [qid for qid, r in prepass.items() if not r["near_miss"]]
        hedge_qids = [r["qid"] for r in recs.values()
                    if not r.get("answer_entities") and r["gold"]]

        n_wrong = min(len(wrong_qids), N_PER_DATASET * 2 // 3)
        n_hedge = min(len(hedge_qids), N_PER_DATASET - n_wrong)
        sample = (random.sample(wrong_qids, n_wrong) +
                random.sample(hedge_qids, n_hedge))

        with open(f"results/phase4/failures_{ds}.md", "w", encoding="utf-8") as f, \
            open(f"results/phase4/labels_{ds}.csv", "w", newline="",
                encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(["qid", "kind", "category", "note"])
            for qid in sample:
                r = recs[qid]
                kind = "wrong" if qid in prepass else "hedge"
                f.write(f"## {qid} ({kind})\n\n**Q:** {r['question']}\n\n"
                        f"**gold:** {r['gold']}\n\n**answer:** {r['answer']}\n\n"
                        f"**entities:** {r['answer_entities']}\n\n")
                for t in r["trace"]:
                    if t.get("node") == "planner":
                        f.write(f"plan: {t['plan'].get('sub_objectives')}\n\n")
                    if t.get("node") == "explorer":
                        f.write(f"explored: {[e['rel'] for e in t['expanded']]} "
                            f"(score max {t.get('max_score')})\n\n")
                    if t.get("node") == "backtracker":
                        f.write(f"backtrack: {t['reason']}\n\n")
                    if t.get("node") == "verifier":
                        f.write(f"verifier: {t.get('outcome')}\n\n")
                f.write("---\n\n")
                w.writerow([qid, kind, "", ""])
        print(f"{ds}: {n_wrong} wrong + {n_hedge} hedge -> failures_{ds}.md")

if __name__ == "__main__":
    main()
