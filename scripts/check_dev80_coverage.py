# per-gold-entity graph coverage.
import json, os
from neo4j import GraphDatabase
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
questions = json.load(open("data/dev80.json", encoding="utf-8"))

report = []
with driver.session() as session:
    for question in questions:
        if not question["answers"]:            # fakes: nothing to check
            continue
        per_gold = {}
        for answer in question["answers"]:
            rec = session.run("""
                MATCH (b:Entity {name: $a})
                OPTIONAL MATCH (t:Entity) WHERE t.name IN $qs AND t <> b
                WITH b, t LIMIT 1
                RETURN b IS NOT NULL AS exists,
                       t IS NOT NULL AND
                       EXISTS { MATCH shortestPath((t)-[*..4]-(b)) } AS reachable
                """, a=answer, qs=question["gold_q_entities"]).single()
            per_gold[answer] = {"exists": rec["exists"],
                           "reachable": rec["reachable"]}
        n_ok = sum(v["reachable"] for v in per_gold.values())
        report.append({"qid": question["qid"], "bucket": question["bucket"],
                       "n_gold": len(per_gold), "n_reachable": n_ok,
                       "detail": per_gold})
        if n_ok < len(per_gold):
            print(f'[{question["qid"]}] {n_ok}/{len(per_gold)} gold reachable: '
                  f'{[a for a, v in per_gold.items() if not v["reachable"]]}')

json.dump(report, open("logs/dev80_coverage.json", "w"), indent=1)
full = sum(1 for r in report if r["n_reachable"] == r["n_gold"])
partial = sum(1 for r in report if 0 < r["n_reachable"] < r["n_gold"])
print(f"\nfull coverage: {full}, partial: {partial}, "
      f"zero: {len(report) - full - partial}")
driver.close()
