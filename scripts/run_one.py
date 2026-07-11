import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.llm import LLMClient
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import EmbeddingScorer
from agr.state import make_init_state
from agr.config import RunConfig
from agr.graph_build import build_graph

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

llm = LLMClient(model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
tools = KGTools(driver, EntityResolver(driver, embed), "logs/tools.jsonl")
scorer = EmbeddingScorer("data/relation_embeddings.npy", "data/relation_names.json")
agr = build_graph(llm, tools, scorer, RunConfig(use_gold_entities=True))

QID, Q, GOLD = "dev-001", "who is Justin Bieber's father?", ["Justin Bieber"]
tools.qid = QID
final = agr.invoke(make_init_state(QID, Q, gold_q_entities=GOLD),
                   config={"recursion_limit": 60})

print("ANSWER:", final["answer"])
print("BUDGET:", final["budget"].snapshot())
for t in final["trace"]:
    print(t)
driver.close()
