"""Tier-1 structural groundedness over run JSONLs.
Usage: python scripts/groundedness.py logs/test_webqsp_*.jsonl logs/test_cwq_*.jsonl
Writes per-record sidecars to logs/grounded_<runname>.jsonl (input to Tier 2).
"""
import json, unicodedata
from agr.runtime import get_driver

HOP_CAP = 4

exists_cache, reach_cache = {}, {}

def entity_exists(s, name):
    if name not in exists_cache:
        rec = s.run("MATCH (e:Entity {name:$n}) RETURN e.id LIMIT 1",
                    n=name).single()
        exists_cache[name] = rec is not None
    return exists_cache[name]

def reachable(s, name, topic_names):
    key = (name, tuple(sorted(topic_names)))
    if key not in reach_cache:
        rec = s.run("""
            MATCH (b:Entity {name:$n})
            MATCH (t:Entity) WHERE t.name IN $ts AND t <> b
            WITH t, b LIMIT 1
            MATCH p = shortestPath((t)-[*..""" + str(HOP_CAP) + """]-(b))
            RETURN length(p) AS h LIMIT 1""",
            n=name, ts=topic_names).single()
        # topic == asserted entity counts as grounded (0 hops)
        self_match = any(name == t for t in topic_names)
        reach_cache[key] = (rec is not None) or self_match
    return reach_cache[key]

def main():
    # question -> topic entities, from the locked test files
    topics = {}
    for ds in ("webqsp", "cwq"):
        for q in json.load(open(f"data/test_{ds}.json", encoding="utf-8")):
            topics[q["qid"]] = q["gold_q_entities"]

    files = [
        "results/phase4/test_webqsp_noretrieval.jsonl",
        "results/phase4/test_cwq_noretrieval.jsonl",
        "results/phase4/test_webqsp_vectorrag.jsonl",
        "results/phase4/test_cwq_vectorrag.jsonl",
        "results/phase4/test_webqsp_graphrag.jsonl",
        "results/phase4/test_cwq_graphrag.jsonl",
        "results/phase4/test_webqsp_tog.jsonl",
        "results/phase4/test_cwq_tog.jsonl",
        "results/phase4/test_webqsp_agr.jsonl",
        "results/phase4/test_cwq_agr.jsonl",
    ]

    print(f"{'file':<38}{'asserted':<10}{'ungrounded':<12}{'ent-rate':<10}"
          f"{'q-answered':<11}{'q-any-ungr':<11}{'q-rate':<8}")
    
    driver = get_driver()
    with driver.session() as session:
        for path in files:
            n_ent = n_ungr = n_ans = n_q_ungr = 0
            runname = path.replace("\\", "/").split("/")[-1].replace(".jsonl", "")
            with open(f"logs/grounded_{runname}.jsonl", "w",
                      encoding="utf-8") as out:
                for line in open(path, encoding="utf-8"):
                    r = json.loads(line)
                    ents = [unicodedata.normalize("NFKC", e).strip()
                            for e in r.get("answer_entities", []) if str(e).strip()]
                    if not ents:
                        continue
                    n_ans += 1
                    tnames = topics.get(r["qid"], [])
                    verdicts = {}
                    for e in ents:
                        ok = entity_exists(session, e) and reachable(session, e, tnames)
                        verdicts[e] = ok
                        n_ent += 1
                        n_ungr += (not ok)
                    any_ungr = any(not v for v in verdicts.values())
                    n_q_ungr += any_ungr
                    out.write(json.dumps({
                        "qid": r["qid"], "gold": r["gold"],
                        "entities": verdicts, "any_ungrounded": any_ungr,
                        "hit": bool(set(map(str.lower, r["gold"]))
                                    & set(e.lower() for e in ents)),
                    }, ensure_ascii=False) + "\n")
            print(f"{runname:<38}{n_ent:<10}{n_ungr:<12}"
                 f"{n_ungr/max(n_ent,1):<10.1%}{n_ans:<11}{n_q_ungr:<11}"
                 f"{n_q_ungr/max(n_ans,1):<8.1%}")
    driver.close()

if __name__ == "__main__":
    main()
