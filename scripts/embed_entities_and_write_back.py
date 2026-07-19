"""
Expect a few hours on CPU for a few million entities; storage adds roughly 1.5 KB per node.
"""
from agr.runtime import get_driver, get_embedder

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


def main():
    driver = get_driver()
    model = get_embedder()

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


if __name__ == "__main__":
    main()
