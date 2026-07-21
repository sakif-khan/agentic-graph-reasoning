"""Tier-2 semantic support judge.
Samples assertions from grounded_* sidecars, fetches connecting relation
paths from Neo4j, asks the backbone LLM to judge support-as-answer.
Also emits a blind hand-labeling sheet for the kappa protocol.
"""
import csv, glob, json, random
from agr.budget import BudgetConfig, BudgetMeter
from agr.runtime import get_driver, get_llm

HOP_CAP = 4

def paths(s, topic_names, entity, k=3):
    """Up to k shortest connecting paths, verbalized as relation chains."""
    recs = s.run("""
        MATCH (t:Entity) WHERE t.name IN $ts
        MATCH (b:Entity {name:$e}) WHERE t <> b
        MATCH p = allShortestPaths((t)-[*..""" + str(HOP_CAP) + """]-(b))
        RETURN [n IN nodes(p) | CASE WHEN n.is_cvt THEN '[event]'
                                     ELSE n.name END] AS ns,
               [r IN relationships(p) | r.fb_name] AS rs
        LIMIT $k""", ts=topic_names, e=entity, k=k).data()
    out = []
    for r in recs:
        seg = []
        for i, rel in enumerate(r["rs"]):
            seg.append(f'{r["ns"][i]} --{rel.replace(".", " ")}--> '
                       f'{r["ns"][i + 1]}')
        out.append("; ".join(seg))
    return out

def main():
    JUDGE_PROMPT = """Question: {question}
    Asserted answer entity: {entity}
    Knowledge-graph paths connecting the question's topic to this entity:
    {paths}

    Judge: do these paths semantically support "{entity}" as an answer to the
    question? "Supported" requires the path relations to actually express the
    relationship the question asks about -- mere connectedness is NOT support.
    Return {{"supported": true|false, "reason": "<one short sentence>"}}"""

    random.seed(42)
    PER_RUN = 60          # sampled assertions per system x dataset

    driver = get_driver()
    llm = get_llm()

    qmeta = {}
    for ds in ("webqsp", "cwq"):
        for q in json.load(open(f"data/test_{ds}.json", encoding="utf-8")):
            qmeta[q["qid"]] = q

    rows = []
    with driver.session() as session:
        for path in sorted(glob.glob("logs/grounded_test_*.jsonl")):
            recs = [json.loads(l) for l in open(path, encoding="utf-8")]
            # sampling frame: one row per asserted entity, stratified hit/miss
            frame = [(r, e, ok) for r in recs
                    for e, ok in r["entities"].items()]
            sample = random.sample(frame, min(PER_RUN, len(frame)))
            runname = path.split("grounded_")[-1].replace(".jsonl", "")
            for r, ent, structurally_ok in sample:
                meta = qmeta[r["qid"]]
                ps = paths(session, meta["gold_q_entities"], ent) \
                    if structurally_ok else []
                meter = BudgetMeter(BudgetConfig(max_llm_calls=2))
                try:
                    out = llm({"budget": meter}, JUDGE_PROMPT.format(
                        question=meta["question"], entity=ent,
                        paths="\n".join(f"- {p}" for p in ps) or "(none found)"),
                        '{"supported": true, "reason": "..."}')
                    supported = bool(out.get("supported"))
                    reason = str(out.get("reason", ""))[:200]
                except Exception as e:
                    supported, reason = None, f"judge-error {e!r}"
                rows.append({"run": runname, "qid": r["qid"],
                            "question": meta["question"], "entity": ent,
                            "structural": structurally_ok,
                            "n_paths": len(ps), "paths": ps,
                            "supported": supported, "reason": reason,
                            "was_hit": r["hit"]})

    json.dump(rows, open("logs/judge_support.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    # summary
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["supported"] is not None:
            agg[r["run"]][0] += r["supported"]
            agg[r["run"]][1] += 1
    print(f"{'run':<32}{'semantically-supported':<24}")
    for run, (sup, n) in sorted(agg.items()):
        print(f"{run:<32}{sup}/{n} = {sup / n:.1%}")

    # blind hand-label sheet for kappa: 100 random judged items, verdicts hidden
    lab = random.sample([r for r in rows if r["supported"] is not None], 100)
    with open("data/kappa_sheet.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["idx", "question", "entity", "paths", "your_label(1/0)"])
        for i, r in enumerate(lab):
            w.writerow([i, r["question"], r["entity"], " || ".join(r["paths"]), ""])
    json.dump(lab, open("data/kappa_key.json", "w", encoding="utf-8"), indent=1)

if __name__ == "__main__":
    main()
