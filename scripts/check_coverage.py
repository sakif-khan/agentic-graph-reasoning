import json, random
from agr.runtime import get_driver


def path_exists(session, q_entity, a_entity, cap=4):
    # Case 1: topic entity IS the answer -> reachable at 0 hops
    record = session.run("""
        MATCH (a:Entity)
        WHERE a.name IN $qs AND a.name IN $ans
        RETURN a.id LIMIT 1""",
        qs=q_entity, ans=a_entity).single()
    if record:
        return 0

    # Case 2: genuine path search, guaranteed distinct endpoints
    record = session.run("""
        MATCH (a:Entity) WHERE a.name IN $qs
        MATCH (b:Entity) WHERE b.name IN $ans
        WITH a, b WHERE a <> b
        MATCH p = shortestPath((a)-[*..""" + str(cap) + """]-(b))
        RETURN length(p) AS hops
        ORDER BY hops LIMIT 1""",
        qs=q_entity, ans=a_entity).single()
    return record["hops"] if record else None


def main():
    report = json.load(open("coverage_report.json", encoding="utf-8"))
    reachable_qs = [question for question in report["per_question"] if question["reachable"]]
    random.seed(42)
    sample = random.sample(reachable_qs, min(400, len(reachable_qs)))

    driver = get_driver()

    ok, fail = 0, []
    with driver.session() as session:
        for question in sample:
            hops = path_exists(session, question["q_entity"], question["a_entity"])
            if hops is not None:
                ok += 1
            else:
                fail.append(question)

    print(f"Neo4j-verified: {ok}/{len(sample)}")
    json.dump(fail, open("gate_failures.json", "w"), indent=1)


if __name__ == "__main__":
    main()
