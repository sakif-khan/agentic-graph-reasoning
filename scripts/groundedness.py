"""Tier-1 structural groundedness over run JSONLs.
Usage: python scripts/groundedness.py
(reads the fixed run list under results/phase4/)
Writes per-record sidecars to
results/phase4/tier1_groundedness/grounded_<runname>.jsonl (input to Tier 2).
"""
import json, unicodedata
from agr.runtime import get_driver

HOP_CAP = 4

# Written into the log so a consumer can tell which reading produced the rates.
SEMANTICS = "tier1-semantics: any-topic-entity"

exists_cache, reach_cache = {}, {}

def entity_exists(s, name):
    if name not in exists_cache:
        rec = s.run("MATCH (e:Entity {name:$n}) RETURN e.id LIMIT 1",
                    n=name).single()
        exists_cache[name] = rec is not None
    return exists_cache[name]

def reachable(s, name, topic_names):
    """Is `name` within HOP_CAP hops of ANY of the question's topic entities?

    Sec. 7.5.3 defines tier-1 grounding as connection to at least one topic
    entity, and this used to test something stricter: a `WITH t, b LIMIT 1`
    sat between the two MATCHes and cut the cartesian product to a single
    arbitrary row, so the topic set collapsed to one node before the path
    search ever ran. Only the topic set -- entity names are unique in this
    graph, so `b` matched exactly one node either way. On a single-topic
    question the two readings therefore coincide, which is why it survived; 204
    of the 800 questions carry two or three topic entities, and on those the
    test asked whether one arbitrary topic reached the answer.

    The bias was one-directional -- a stricter test can only manufacture
    ungrounded verdicts, never hide them -- so the 0.0% results were never at
    risk, and 26 of the 274 ungrounded verdicts were exposed, 19 of them in CWQ
    no-retrieval's 42. Rerunning under the corrected reading flipped none of
    them: every verdict in the sidecars is unchanged, so each rate the thesis
    reports is confirmed rather than corrected. The arbitrary topic node
    happened to reach whatever the answer was reachable from. That is luck, not
    equivalence, and it is why this now reads as Sec. 7.5.3 says it does.

    Both counts are over one population and are recomputable from the committed
    sidecars: 6,327 verdicts, being sum(len(r["entities"])) over the ten
    grounded_test_*.jsonl, of which 274 are false. The log's `asserted` column
    totals one higher, because it counts an entity twice where an answer list
    repeats one and the verdict dict keeps a single key.

    Existence is all the caller needs, so this returns the first path found
    rather than the shortest and lets Cypher stop there.
    """
    key = (name, tuple(sorted(topic_names)))
    if key not in reach_cache:
        rec = s.run("""
            MATCH (b:Entity {name:$n})
            MATCH (t:Entity) WHERE t.name IN $ts AND t <> b
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
        for q in json.load(open(f"results/phase4/test_{ds}.json",
                                encoding="utf-8")):
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

    # Stamped so the artifact records which reading of Sec. 7.5.3 produced it.
    # A log without this line was written by the pre-fix query, which collapsed
    # the topic set to one node; build_thesis_numbers.py flags that rather than
    # quoting the rates as though the definitions matched.
    print(f"# {SEMANTICS}")
    print(f"{'file':<38}{'asserted':<10}{'ungrounded':<12}{'ent-rate':<10}"
          f"{'q-answered':<11}{'q-any-ungr':<11}{'q-rate':<8}")
    
    driver = get_driver()
    with driver.session() as session:
        for path in files:
            n_ent = n_ungr = n_ans = n_q_ungr = 0
            runname = path.replace("\\", "/").split("/")[-1].replace(".jsonl", "")
            with open(f"results/phase4/tier1_groundedness/"
                      f"grounded_{runname}.jsonl", "w",
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
