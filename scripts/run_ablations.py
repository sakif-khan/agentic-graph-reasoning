import json, time
from pathlib import Path

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.state import make_init_state
from agr.config import RunConfig
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.runlog import RunLogger
from agr.runtime import get_driver, get_embedder, get_llm, get_scorer


def main():
    CONDITIONS = [
        ("noplanner",   RunConfig(use_planner=False),   BudgetConfig()),
        ("nobacktrack", RunConfig(),                    BudgetConfig(max_backtracks=0)),
        ("noverifier",  RunConfig(verify_claims=False), BudgetConfig()),
        ("embonly",     RunConfig(alpha=1.0),           BudgetConfig()),
    ]

    TEST_FILES = ["results/phase4/test_webqsp_half.json", "results/phase4/test_cwq_half.json"]

    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()

    for test_file in TEST_FILES:
        tag = Path(test_file).stem                    # test_cwq_half
        questions = json.load(open(test_file, encoding="utf-8"))

        for label, rc, budget_cfg in CONDITIONS:
            name = f"{tag}_abl_{label}"
            log_path = f"logs/{name}.jsonl"
            done = set()
            if Path(log_path).exists():
                done = {json.loads(l)["qid"]
                        for l in open(log_path, encoding="utf-8")}
            tools = KGTools(driver, EntityResolver(driver, embed),
                            f"logs/{name}_tools.jsonl")
            scorer = get_scorer(rc.alpha)
            agr = build_graph(llm, tools, scorer, rc)
            logger = RunLogger(log_path, llm.describe(), budget_cfg,
                               {**rc.as_dict(), "system": f"agr_abl_{label}"})
            print(f"\n=== {name} ===")
            failures = []
            for q in questions:
                if q["qid"] in done:
                    continue
                tools.qid = q["qid"]
                t0 = time.time()
                try:
                    final = agr.invoke(
                        make_init_state(q["qid"], q["question"],
                                        gold_q_entities=q["gold_q_entities"],
                                        cfg=budget_cfg),
                        config={"recursion_limit": 60})
                    logger.write(q["qid"], q["question"], q["answers"],
                                final, time.time() - t0)
                    print(f'  [{q["qid"]}] ok')
                except Exception as e:
                    failures.append((q["qid"], repr(e)))     # log and continue;
                    print(f'  [{q["qid"]}] FAILED: {e!r}')   # never lose a sweep to one question

            print(f"=== {name}: {len(questions) - len(done) - len(failures)} ok, "
                f"{len(failures)} failed ===")
            if failures:
                json.dump(failures, open(f"logs/{name}_failures.json", "w"), indent=1)

    driver.close()


if __name__ == "__main__":
    main()
