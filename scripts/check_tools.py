from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.runtime import get_driver, get_embedder

# Smoke-check the five KG tools against a live Neo4j instance. Set these to an
# entity present in the loaded graph and a relation that entity actually has.
NAME = "Justin Bieber"
REL = "people.person.parents"


def main():
    driver = get_driver()
    model = get_embedder()
    tools = KGTools(driver, EntityResolver(driver, model),
                    "results/phase2/check_tools.jsonl")
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


if __name__ == "__main__":
    main()
