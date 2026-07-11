from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

NAME = "Justin Bieber"          # <- an entity that exists in YOUR graph
REL = "people.person.parents"   # <- a relation it really has

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
tools = KGTools(driver, EntityResolver(driver, model), "logs/check_tools.jsonl")
tools.qid = "manual-check"

hits = tools.search_entity(NAME)
print("search:", hits[:2])
eid = hits[0]["id"]
rels = tools.get_relations(eid)
print("relations:", [r["rel"] for r in rels[:5]])
nbrs = tools.get_neighbors(eid, REL)
print("neighbors:", nbrs["neighbors"][:3])
if nbrs["neighbors"]:
    print("verify:", tools.verify_triple(eid, REL, nbrs["neighbors"][0]["id"]))
driver.close()
