from pathlib import Path

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import EmbeddingScorer
from agr.state import make_init_state
from agr.config import run_cfg
from agr.graph_build import build_graph
from agr.runtime import get_driver, get_embedder, get_llm


def main():
    driver = get_driver()
    embed = get_embedder()
    llm = get_llm()

    # Single-question probe for manual inspection. Its tool log is not an
    # experiment artifact, so it is written to the untracked scratch directory.
    Path("scratch").mkdir(exist_ok=True)
    tools = KGTools(driver, EntityResolver(driver, embed), "scratch/tools.jsonl")
    scorer = EmbeddingScorer("data/relation_embeddings.npy", "data/relation_names.json")
    agr = build_graph(llm, tools, scorer, run_cfg)

    QID, Q, GOLD = "dev-001", "who is Justin Bieber's father?", ["Justin Bieber"]
    tools.qid = QID
    final = agr.invoke(make_init_state(QID, Q, gold_q_entities=GOLD),
                       config={"recursion_limit": 60})

    print("ANSWER:", final["answer"])
    print("BUDGET:", final["budget"].snapshot())
    for t in final["trace"]:
        print(t)
    driver.close()


if __name__ == "__main__":
    main()
