import json
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingScorer:
    """Phase 2 placeholder: cosine(objective, relation). Phase 3 replaces
    this with the alpha-blend hybrid; the call signature must not change."""

    def __init__(self, npy_path, names_path,
                 model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.vecs = np.load(npy_path)
        names = json.load(open(names_path, encoding="utf-8"))
        self.index = {n: i for i, n in enumerate(names)}
        self.model = SentenceTransformer(model_name)

    def __call__(self, objective: str, rel_rows: list[dict]):
        q = self.model.encode([objective], normalize_embeddings=True)[0]
        scored = []
        for row in rel_rows:
            i = self.index.get(row["rel"])
            s = float(self.vecs[i] @ q) if i is not None else 0.0
            scored.append((row, s))
        return sorted(scored, key=lambda x: -x[1])

    def top_facts(self, objective: str, triples: list[dict], k: int = 30):
        """Rank traversed triples by relevance to the objective."""
        if len(triples) <= k:
            return triples
        texts = [f'{t["h_name"]} {" ".join(t["r"])} {t["t_name"]}'
                 for t in triples]
        q = self.model.encode([objective], normalize_embeddings=True)[0]
        vecs = self.model.encode(texts, batch_size=256,
                                 normalize_embeddings=True)
        order = np.argsort(vecs @ q)[::-1][:k]
        return [triples[i] for i in sorted(order)]   # keep traversal order

"""
Checkpoint — run:

sc = EmbeddingScorer('data/relation_embeddings.npy','data/relation_names.json');
print(sc('where was the person born', [{'rel':'people.person.place_of_birth','dir':'out','n':1},{'rel':'film.film.genre','dir':'out','n':1}])[0])

The birth relation must outscore the genre relation.
"""
