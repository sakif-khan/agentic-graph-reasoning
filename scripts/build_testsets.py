"""Build certified, stratified test samples from the RoG TEST splits.
Outputs: scripts/test_webqsp.json, scripts/test_cwq.json (+ certification).
Run ONCE. Never edit the outputs. Seed and sample IDs are the record.
"""
import json, random
from collections import Counter, defaultdict

from agr.runtime import get_driver
from datasets import load_dataset

SEED = 42
SAMPLE_SIZE = 400            # per dataset; set to None for full test sets
HOP_CAP = 4


def classify(session, q_names, a_names):
    rec = session.run("""
        MATCH (a:Entity) WHERE a.name IN $qs
        MATCH (b:Entity) WHERE b.name IN $ans
        WITH a, b WHERE a <> b
        MATCH p = shortestPath((a)-[*..""" + str(HOP_CAP) + """]-(b))
        RETURN length(p) AS hops LIMIT 1""",
        qs=q_names, ans=a_names).single()
    return rec["hops"] if rec else None


def gold_coverage(session, q_names, a_names):
    per = {}
    for a in a_names:
        rec = session.run("""
            OPTIONAL MATCH (b:Entity {name:$a})
            OPTIONAL MATCH (t:Entity) WHERE t.name IN $qs AND (b IS NULL OR t <> b)
            WITH b, t LIMIT 1
            RETURN b IS NOT NULL AS ex,
                   b IS NOT NULL AND t IS NOT NULL AND
                   EXISTS { MATCH shortestPath((t)-[*..""" + str(HOP_CAP) + """]-(b)) }
                   AS reach""", a=a, qs=q_names).single()
        per[a] = {"exists": rec["ex"], "reachable": rec["reach"]}
    return per


def main():
    driver = get_driver()

    dev80_qids = {q["qid"] for q in
                  json.load(open("data/dev80.json", encoding="utf-8"))}

    random.seed(SEED)

    for ds_name in ["webqsp", "cwq"]:
        path = f"../RoG-{ds_name}/data"
        ds = load_dataset("parquet", data_files={"test": f"{path}/test-*.parquet"})
        pool, skipped = [], Counter()
        with driver.session() as session:
            for example in ds["test"]:
                qid = str(example.get("id", ""))
                if qid in dev80_qids:
                    skipped["dev_overlap"] += 1
                    continue
                q_entity = [str(x).strip() for x in example["q_entity"] if str(x).strip()]
                a_entity = [str(x).strip() for x in example["a_entity"] if str(x).strip()]
                if not q_entity or not a_entity:
                    skipped["missing_entities"] += 1
                    continue
                hops = classify(session, q_entity, a_entity)
                stratum = ("h1" if hops == 1 else "h2" if hops == 2
                           else "h3plus" if hops else "unreachable")
                pool.append({"qid": qid, "dataset": ds_name,
                             "question": example["question"],
                             "gold_q_entities": q_entity, "answers": a_entity,
                             "hops": hops, "stratum": stratum})

        dist = Counter(r["stratum"] for r in pool)
        print(f"[{ds_name}] pool={len(pool)} skipped={dict(skipped)} strata={dict(dist)}")

        if SAMPLE_SIZE is None or SAMPLE_SIZE >= len(pool):
            sample = pool
        else:
            # proportional allocation, unreachable stratum included deliberately
            by = defaultdict(list)
            for r in pool:
                by[r["stratum"]].append(r)
            sample, alloc = [], {}
            for st, rows in sorted(by.items()):
                k = round(SAMPLE_SIZE * len(rows) / len(pool))
                alloc[st] = k
                sample.extend(random.sample(rows, min(k, len(rows))))
            # top up rounding shortfall from the largest stratum
            while len(sample) < SAMPLE_SIZE:
                st = max(by, key=lambda x: len(by[x]))
                extra = [r for r in by[st] if r not in sample]
                if not extra:
                    break
                sample.append(random.choice(extra))
            print(f"[{ds_name}] allocation={alloc} -> sampled={len(sample)}")

        # certification: per-gold-entity coverage on the sample
        with driver.session() as session:
            full = partial = zero = 0
            for r in sample:
                per = gold_coverage(session, r["gold_q_entities"], r["answers"])
                n_ok = sum(v["reachable"] for v in per.values())
                r["n_gold"] = len(per)
                r["n_gold_reachable"] = n_ok
                full += (n_ok == len(per))
                partial += (0 < n_ok < len(per))
                zero += (n_ok == 0)
        ceiling = sum(1 for r in sample if r["n_gold_reachable"] > 0) / len(sample)
        print(f"[{ds_name}] coverage: full={full} partial={partial} zero={zero} "
              f"Hits@1 ceiling={ceiling:.1%}")

        json.dump(sample, open(f"data/test_{ds_name}.json", "w",
                               encoding="utf-8"), indent=1, ensure_ascii=False)

    driver.close()


if __name__ == "__main__":
    main()
