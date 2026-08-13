from pathlib import Path

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
    # KGTools opens its log in append mode, so pointing this at the committed
    # results/phase2/check_tools.jsonl grew that record on every re-run. That
    # file is the archived Phase 2 certification; this is an install check, so
    # its output is incidental and goes to the untracked scratch directory.
    Path("scratch").mkdir(exist_ok=True)
    tools = KGTools(driver, EntityResolver(driver, model),
                    "scratch/check_tools.jsonl")
    tools.qid = "manual-check"

    hits = tools.search_entity(NAME)
    print("search:", hits[:2])
    eid = hits[0]["id"]
    rels = tools.get_relations(eid)
    print("relations:", [r["rel"] for r in rels[:5]])
    nbrs = tools.get_neighbors(eid, REL)
    print("neighbors:", nbrs["neighbors"][:3])
    if nbrs["neighbors"]:
        tail = nbrs["neighbors"][0]["id"]
        print("verify_triple:", tools.verify_triple(eid, REL, tail))
        # verify_connection is the route the final design actually calls
        # (nodes.py); verify_triple is kept in the API but reached by no node,
        # so checking only the latter would leave the live one uncovered.
        print("verify_connection:", tools.verify_connection(eid, tail))
    driver.close()


if __name__ == "__main__":
    main()
