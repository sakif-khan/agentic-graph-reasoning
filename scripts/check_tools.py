from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.runtime import get_driver, get_embedder

NAME = "Justin Bieber"          # <- an entity that exists in YOUR graph
REL = "people.person.parents"   # <- a relation it really has

driver = get_driver()
model = get_embedder()
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
