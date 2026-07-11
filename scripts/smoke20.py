import json
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.llm import LLMClient
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import EmbeddingScorer
from agr.state import make_init_state
from agr.config import RunConfig
from agr.graph_build import build_graph
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_MODEL, OPENAI_API_KEY

# hand-pick from your dev splits: 6x 1-hop, 8x 2-hop composition,
# 3x conjunction, 2x CVT-heavy, 1x unanswerable(fake entity)
QUESTIONS = json.load(open("data/smoke20.json", encoding="utf-8"))
# each: {"qid":..., "question":..., "gold_q_entities":[...], "answers":[...]}

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
llm = LLMClient(model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
tools = KGTools(driver, EntityResolver(driver, embed), "logs/smoke20_tools.jsonl")
scorer = EmbeddingScorer("data/relation_embeddings.npy", "data/relation_names.json")
agr = build_graph(llm, tools, scorer, RunConfig(use_gold_entities=True))

with open("logs/smoke20_traces.jsonl", "w", encoding="utf-8") as out:
    for question in QUESTIONS:
        tools.qid = question["id"]
        final = agr.invoke(
            make_init_state(question["id"], question["question"],
                            gold_q_entities=question["gold_q_entities"]),
            config={"recursion_limit": 60})
        rec = {"qid": question["id"], "question": question["question"],
               "gold": question["answers"], "answer": final["answer"],
               "budget": final["budget"].snapshot(),
               "trace": final["trace"]}
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f'[{question["id"]}] {final["answer"]!r}  '
              f'gold={question["answers"]}  {final["budget"].snapshot()}')
driver.close()
