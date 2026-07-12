import json
import time

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.llm import LLMClient
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import HybridScorer
from agr.state import make_init_state
from agr.config import RunConfig, BACKBONE
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY
from agr.runlog import RunLogger

# ---- experimental condition: the ONLY thing you edit between sweep runs ----
run_cfg = RunConfig(use_gold_entities=True, alpha=0.5, tau=0.20)
budget_cfg = BudgetConfig()          # max_llm_calls now defaults to 25
RUN_NAME = f"smoke20_a{run_cfg.alpha}_t{run_cfg.tau}"

# ---- construction ----
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
llm = LLMClient(api_key=OPENAI_API_KEY, **BACKBONE)
tools = KGTools(driver, EntityResolver(driver, embed), f"logs/{RUN_NAME}_tools.jsonl")
scorer = HybridScorer("data/relation_embeddings.npy", "data/relation_names.json",
                      llm=llm, alpha=run_cfg.alpha)
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
