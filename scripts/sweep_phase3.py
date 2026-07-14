import json, time
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from pathlib import Path

from agr.llm import LLMClient
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import HybridScorer
from agr.state import make_init_state
from agr.config import RunConfig, BACKBONE
from agr.budget import BudgetConfig
from agr.graph_build import build_graph
from agr.runlog import RunLogger
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY


CONDITIONS = [
    RunConfig(alpha=1.0, tau=0.0),                       # Phase 2 baseline
    RunConfig(alpha=1.0, tau=0.2),
    RunConfig(alpha=0.7, tau=0.0),
    RunConfig(alpha=0.7, tau=0.2),
    RunConfig(alpha=0.5, tau=0.0),
    RunConfig(alpha=0.5, tau=0.2),
    RunConfig(alpha=0.3, tau=0.0),
    RunConfig(alpha=0.3, tau=0.2),
    RunConfig(alpha=0.5, tau=0.2, verify_claims=False),
    RunConfig(alpha=0.7, tau=0.2, verify_claims=False),
]

QUESTIONS = json.load(open("data/dev80.json", encoding="utf-8"))
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
budget_cfg = BudgetConfig()

for rc in CONDITIONS:
    name = (f"dev80_a{rc.alpha}_t{rc.tau}"
            + ("" if rc.verify_claims else "_draftonly"))
    log_path = f"logs/{name}.jsonl"
    done = set()
    if Path(log_path).exists():
        done = {json.loads(l)["qid"]
                for l in open(log_path, encoding="utf-8")}
    llm = LLMClient(api_key=OPENAI_API_KEY, **BACKBONE)
    tools = KGTools(driver, EntityResolver(driver, embed),
                    f"logs/{name}_tools.jsonl")
    scorer = HybridScorer("data/relation_embeddings.npy",
                          "data/relation_names.json",
                          llm=llm, alpha=rc.alpha)
    agr = build_graph(llm, tools, scorer, rc)
    logger = RunLogger(f"logs/{name}.jsonl", llm.describe(),
                       budget_cfg, rc.as_dict())
    print(f"\n=== {name} ===")
    failures = []
    for q in QUESTIONS:
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

    print(f"=== {name}: {len(QUESTIONS) - len(done) - len(failures)} ok, "
          f"{len(failures)} failed ===")
    if failures:
        json.dump(failures, open(f"logs/{name}_failures.json", "w"), indent=1)

driver.close()
