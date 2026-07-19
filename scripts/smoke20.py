import json
import time

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.state import make_init_state
from agr.config import run_cfg
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.runtime import get_driver, get_embedder, get_llm, get_scorer
from agr.runlog import RunLogger


def main():
    # ---- experimental condition: the ONLY thing you edit between sweep runs ----
    budget_cfg = BudgetConfig()          # max_llm_calls now defaults to 25
    RUN_NAME = f"smoke20_a{run_cfg.alpha}_t{run_cfg.tau}"

    # ---- construction ----
    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()
    tools = KGTools(driver, EntityResolver(driver, embed), f"logs/{RUN_NAME}_tools.jsonl")
    scorer = get_scorer(run_cfg.alpha)
    agr = build_graph(llm, tools, scorer, run_cfg)

    logger = RunLogger(path=f"logs/{RUN_NAME}.jsonl",
                       backbone=llm.describe(),
                       budget_cfg=budget_cfg,
                       run_config=run_cfg.as_dict())

    # hand-pick from your dev splits: 6x 1-hop, 8x 2-hop composition,
    # 3x conjunction, 2x CVT-heavy, 1x unanswerable(fake entity)
    QUESTIONS = json.load(open("data/smoke20.json", encoding="utf-8"))
    # each: {"qid":..., "question":..., "gold_q_entities":[...], "answers":[...]}

    for question in QUESTIONS:
        tools.qid = question["id"]
        t0 = time.time()
        final = agr.invoke(
            make_init_state(question["id"], question["question"],
                            gold_q_entities=question["gold_q_entities"],
                            cfg=budget_cfg),
            config={"recursion_limit": 60})
        logger.write(qid=question["id"], question=question["question"], gold=question["answers"],
                     final=final, wall_seconds=time.time() - t0)
        print(f'[{question["id"]}] {final["answer"]!r}  gold={question["answers"]}  '
              f'verifier={next((t.get("outcome") for t in final["trace"] if t.get("node") == "verifier"), None)}  '
              f'{final["budget"].snapshot()}')

    driver.close()


if __name__ == "__main__":
    main()
