"""Run one baseline system over one test file.
Usage: python scripts\run_baseline.py <system> <test_file.json>
  system in {noretrieval, vectorrag, graphrag, tog}
"""
import json, sys, time
from pathlib import Path

from agr.config import run_cfg
from agr.budget import BudgetConfig
from agr.runlog import RunLogger
from agr.runtime import get_driver, get_embedder, get_llm


def main():
    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()

    budget_cfg = BudgetConfig()

    SYSTEMS = ["noretrieval", "vectorrag", "graphrag", "tog"]
    TEST_FILES = ["data/test_webqsp.json", "data/test_cwq.json"]

    for system in SYSTEMS:
        for test_file in TEST_FILES:
            tag = Path(test_file).stem
            name = f"{tag}_{system}"

            if system == "noretrieval":
                from agr.baselines.noretrieval import NoRetrieval
                runner = NoRetrieval(llm)
            elif system == "vectorrag":
                from agr.baselines.vectorrag import VectorRAG
                runner = VectorRAG(llm, "data/triple_index")
            elif system == "graphrag":
                from agr.baselines.graphrag import StaticGraphRAG
                from agr.resolver import EntityResolver
                runner = StaticGraphRAG(llm, driver, embed,
                                        EntityResolver(driver, embed))
            elif system == "tog":
                from agr.baselines.tog import ToG
                from agr.resolver import EntityResolver
                from agr.kg_tools import KGTools
                tools = KGTools(driver, EntityResolver(driver, embed),
                                f"logs/{name}_tools.jsonl")
                runner = ToG(llm, tools)
            else:
                sys.exit(f"unknown system {system}")

            log_path = f"logs/{name}.jsonl"
            logger = RunLogger(log_path, llm.describe(), budget_cfg,
                               {**run_cfg.as_dict(), "system": system})

            done = set()
            if Path(log_path).exists():
                done = {json.loads(l)["qid"] for l in open(log_path, encoding="utf-8")}

            questions = json.load(open(test_file, encoding="utf-8"))
            failures = []
            for q in questions:
                if q["qid"] in done:
                    continue
                if hasattr(runner, "tools"):
                    runner.tools.qid = q["qid"]
                t0 = time.time()
                try:
                    final = runner.run(q, budget_cfg)
                    logger.write(q["qid"], q["question"], q["answers"], final,
                                time.time() - t0)
                except Exception as e:
                    failures.append((q["qid"], repr(e)))
                    print(f'  [{q["qid"]}] FAILED: {e!r}')
            print(f"=== {name}: {len(failures)} failures ===")
            if failures:
                json.dump(failures, open(f"logs/{name}_failures.json", "w"), indent=1)

    driver.close()


if __name__ == "__main__":
    main()
