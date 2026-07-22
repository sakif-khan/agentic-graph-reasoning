"""One-off: prove the planner.py edit didn't change frozen (use_planner=True)
behavior. Run once after any edit to planner_node; not part of the pipeline."""
import json

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.state import make_init_state
from agr.config import RunConfig       # NOT FROZEN's package-level singleton --
                                       # construct explicitly so this check
                                       # doesn't accidentally exercise a
                                       # different object than build_graph gets
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.runtime import get_driver, get_embedder, get_llm, get_scorer

def main():
    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()

    rc = RunConfig()            # defaults ARE the frozen values: a=0.7, t=0.2,
                                # verify_claims=True, use_planner=True
    budget_cfg = BudgetConfig()
    tools = KGTools(driver, EntityResolver(driver, embed),
                    "logs/_verify_planner_tools.jsonl")
    scorer = get_scorer(rc.alpha)
    agr = build_graph(llm, tools, scorer, rc)

    # any dev80 qid -- it was run many times across the Phase 3 sweep at exactly
    # this config, so its prompts are guaranteed to be cache-resident
    q = next(q for q in json.load(open("results/phase3/dev80.json",
                                    encoding="utf-8"))
            if q["qid"] == "WebQTrn-3525")   # "where did mendeleev died"

    tools.qid = q["qid"]
    final = agr.invoke(
        make_init_state(q["qid"], q["question"],
                        gold_q_entities=q["gold_q_entities"], cfg=budget_cfg),
        config={"recursion_limit": 60})

    snap = final["budget"].snapshot()
    print("answer:", final["answer"])
    print("llm_calls:", snap["llm_calls"], " cache_hits:", snap["cache_hits"])
    assert snap["cache_hits"] == snap["llm_calls"] > 0, \
        "NOT fully cached -- planner.py edit changed the frozen prompt path!"
    print("PASS: fully cache-replayed, frozen path unaffected by planner.py edit.")

    driver.close()

if __name__ == "__main__":
    main()
