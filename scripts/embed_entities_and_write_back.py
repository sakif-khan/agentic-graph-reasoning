"""
Expect a few hours on CPU for a few million entities; storage adds roughly 1.5 KB per node.
"""
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

BATCH = 2000

def fetch_batch(tx, skip):
    q = """MATCH (e:Entity) WHERE e.is_cvt = false AND e.embedding IS NULL
           RETURN e.id AS id, e.name AS name LIMIT $lim"""
    return [(r["id"], r["name"]) for r in tx.run(q, lim=BATCH)]

def write_batch(tx, rows):
    tx.run("""UNWIND $rows AS row
              MATCH (e:Entity {id: row.id})
              CALL db.create.setNodeVectorProperty(e, 'embedding', row.vec)""",
           rows=rows)

with driver.session() as session:
    total = 0
    while True:
        batch = session.execute_read(fetch_batch, 0)
        if not batch:
            break
        vecs = model.encode([n for _, n in batch],
                            batch_size=256, normalize_embeddings=True)
        session.execute_write(write_batch,
                              [{"id": i, "vec": v.tolist()}
                               for (i, _), v in zip(batch, vecs)])
        total += len(batch)
        if total % 50000 == 0:
            print(f"{total:,} embedded")
