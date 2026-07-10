import re, json, os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from collections import Counter
from datasets import load_dataset

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

LUCENE_SPECIALS = r'[\+\-\!\(\)\{\}\[\]\^"~\*\?:\\/]|&&|\|\|'
def lucene_escape(s: str) -> str:
    return re.sub(LUCENE_SPECIALS, lambda m: "\\" + m.group(0), s)

def search_entity(q_entity: str, k: int = 5):
    """Returns (tier, [(id, name, score), ...])"""
    q_entity = q_entity.strip()
    with driver.session() as session:
        # Tier 1: exact match
        rows = session.run("MATCH (e:Entity {name: $m}) RETURN e.id AS id, e.name AS name",
                           m=q_entity).data()
        if rows:
            return 1, [(row["id"], row["name"], 1.0) for row in rows]

        # Tier 2: full-text
        rows = session.run("""CALL db.index.fulltext.queryNodes('entity_name', $q)
                              YIELD node, score
                              RETURN node.id AS id, node.name AS name, score
                              LIMIT $k""",
                           q=lucene_escape(q_entity), k=k).data()
        if rows and rows[0]["score"] > 1.0:      # tune this threshold on dev data
            return 2, [(row["id"], row["name"], row["score"]) for row in rows]

        # Tier 3: vector fallback
        vec = model.encode([q_entity], normalize_embeddings=True)[0].tolist()
        rows = session.run("""CALL db.index.vector.queryNodes('entity_embedding', $k, $v)
                        YIELD node, score
                        RETURN node.id AS id, node.name AS name, score""",
                     k=k, v=vec).data()
        return 3, [(row["id"], row["name"], row["score"]) for row in rows]

tiers, misses = Counter(), []
for ds_name in ["webqsp", "cwq"]:
    path = f"../RoG-{ds_name}/data"
    ds = load_dataset("parquet", data_files={"test": f"{path}/test-*.parquet"})
    for example in ds["test"]:
        for q_entity in example["q_entity"]:
            q_entity = str(q_entity).strip()
            if not q_entity:
                continue
            tier, results = search_entity(q_entity)
            hit = results and results[0][1] == q_entity
            tiers[(ds_name, tier, hit)] += 1
            if not hit:
                misses.append((ds_name, q_entity, results[:3] if results else []))

print(tiers)
json.dump(misses, open("linking_misses.json", "w"), indent=1)
