import re


LUCENE_SPECIALS = r'[\+\-\!\(\)\{\}\[\]\^"~\*\?:\\/]|&&|\|\|'


def lucene_escape(s: str) -> str:
    return re.sub(LUCENE_SPECIALS, lambda m: "\\" + m.group(0), s)


class EntityResolver:
    """Three-tier entity linking: exact -> full-text -> vector."""

    def __init__(self, driver, embed_model, fulltext_threshold: float = 1.0):
        self.driver = driver
        self.model = embed_model
        self.threshold = fulltext_threshold

    def __call__(self, mention: str, k: int = 5):
        mention = mention.strip()
        with self.driver.session() as s:
            rows = s.run(
                "MATCH (e:Entity {name:$m}) RETURN e.id AS id, e.name AS name",
                m=mention).data()
            if rows:
                return 1, [(r["id"], r["name"], 1.0) for r in rows]

            rows = s.run(
                """CALL db.index.fulltext.queryNodes('entity_name', $q)
                   YIELD node, score
                   RETURN node.id AS id, node.name AS name, score LIMIT $k""",
                q=lucene_escape(mention), k=k).data()
            if rows and rows[0]["score"] > self.threshold:
                return 2, [(r["id"], r["name"], r["score"]) for r in rows]

            vec = self.model.encode([mention],
                                    normalize_embeddings=True)[0].tolist()
            rows = s.run(
                """CALL db.index.vector.queryNodes('entity_embedding', $k, $v)
                   YIELD node, score
                   RETURN node.id AS id, node.name AS name, score""",
                k=k, v=vec).data()
            return 3, [(r["id"], r["name"], r["score"]) for r in rows]
