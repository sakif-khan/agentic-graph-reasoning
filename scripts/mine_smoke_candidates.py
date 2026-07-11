"""Mine smoke-test candidates from TRAIN splits, classified by path shape."""
import json, random
from datasets import load_dataset
from neo4j import GraphDatabase
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

SAMPLE_PER_DATASET = 200      # random candidates to classify per dataset
random.seed(42)

def classify(session, q_names, a_names):
    """Returns (raw_hops, via_cvt) for the shortest q->a path, or None."""
    rec = session.run("""
        MATCH (a:Entity) WHERE a.name IN $qs
        MATCH (b:Entity) WHERE b.name IN $ans
        WITH a, b WHERE a <> b
        MATCH p = shortestPath((a)-[*..4]-(b))
        RETURN length(p) AS hops,
               any(n IN nodes(p) WHERE n.is_cvt) AS via_cvt
        ORDER BY hops LIMIT 1""",
        qs=q_names, ans=a_names).single()
    return (rec["hops"], rec["via_cvt"]) if rec else None

buckets = {"one_hop": [], "two_hop": [], "conjunction": [], "cvt_heavy": []}

with driver.session() as session:
    for ds_name in ["webqsp", "cwq"]:
        path = f"../RoG-{ds_name}/data"
        ds = load_dataset("parquet",
                          data_files={"train": f"{path}/train-*.parquet"})
        rows = list(ds["train"])
        for example in random.sample(rows, min(SAMPLE_PER_DATASET, len(rows))):
            q_entity = [str(x).strip() for x in example["q_entity"] if str(x).strip()]
            a_entity = [str(x).strip() for x in example["a_entity"] if str(x).strip()]
            if not q_entity or not a_entity:
                continue
            res = classify(session, q_entity, a_entity)
            if res is None:
                continue
            hops, via_cvt = res
            rec = {"dataset": ds_name, "id": str(example.get("id", "")),
                   "question": example["question"],
                   "gold_q_entities": q_entity, "answers": a_entity,
                   "raw_hops": hops, "via_cvt": via_cvt}
            if len(q_entity) >= 2:
                buckets["conjunction"].append(rec)
            elif via_cvt:
                buckets["cvt_heavy"].append(rec)      # logical hop count is
            elif hops == 1:                           # lower than raw_hops
                buckets["one_hop"].append(rec)
            elif hops == 2:
                buckets["two_hop"].append(rec)

json.dump(buckets, open("data/smoke_candidates.json", "w",
                        encoding="utf-8"), indent=1, ensure_ascii=False)
for category, values in buckets.items():
    print(f"{category:<12} {len(values):>4} candidates")
    for r in values[:3]:
        print(f"    [{r['dataset']}] {r['question']!r} -> {r['answers'][:2]}"
              f" (raw_hops={r['raw_hops']}, cvt={r['via_cvt']})")
driver.close()
