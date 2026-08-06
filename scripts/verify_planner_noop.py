"""Confirm that an edit to planner_node left the frozen configuration
(use_planner=True) untouched.

Replays one question that was run many times during the Phase 3 sweep at the
frozen settings, so every prompt it issues should already be in the cache. If
the run is served entirely from cache, the edit did not perturb the prompt path.
Run after editing agr/planner.py; not part of the pipeline.
"""
import json
from pathlib import Path

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.state import make_init_state
from agr.config import RunConfig       # constructed explicitly rather than
                                       # reusing the package-level singleton, so
                                       # this check exercises the same object
                                       # build_graph receives
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.runtime import get_driver, get_embedder, get_llm, get_scorer

def main():
    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()

    rc = RunConfig()            # defaults are the frozen values: alpha=0.7,
                                # tau=0.2, verify_claims and use_planner both on
    budget_cfg = BudgetConfig()
    # the result of this check is the printed assertion; the tool log is
    # incidental and goes to the untracked scratch directory
    Path("scratch").mkdir(exist_ok=True)
    tools = KGTools(driver, EntityResolver(driver, embed),
                    "scratch/_verify_planner_tools.jsonl")
    scorer = get_scorer(rc.alpha)
    agr = build_graph(llm, tools, scorer, rc)

    # Any dev80 question works; this one was run repeatedly during the Phase 3
    # sweep at this configuration, so its prompts are certain to be cached.
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
        "not fully cached: the planner edit changed the frozen prompt path"
    print("pass: fully cache-replayed, frozen path unaffected by the edit.")

    driver.close()

if __name__ == "__main__":
    main()
