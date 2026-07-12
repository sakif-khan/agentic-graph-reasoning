import json
import numpy as np
from sentence_transformers import SentenceTransformer

from agr.budget import BudgetExhausted


class EmbeddingScorer:
    """alpha=1.0 baseline / ablation scorer. Also the base class for Hybrid."""

    def __init__(self, npy_path, names_path,
                 model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.vecs = np.load(npy_path)
        names = json.load(open(names_path, encoding="utf-8"))
        self.index = {n: i for i, n in enumerate(names)}
        self.model = SentenceTransformer(model_name)

    def _emb_scores(self, objective: str, rel_rows: list[dict]) -> list[float]:
        q = self.model.encode([objective], normalize_embeddings=True)[0]
        return [float(self.vecs[i] @ q) if (i := self.index.get(r["rel"]))
                is not None else 0.0 for r in rel_rows]

    def __call__(self, objective: str, rel_rows: list[dict], state=None):
        scores = self._emb_scores(objective, rel_rows)
        return sorted(zip(rel_rows, scores), key=lambda x: -x[1])

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

SCORE_PROMPT = """Sub-objective: {objective}

Candidate knowledge-graph edges (anchor entity --relation-->):
{candidates}

For EACH candidate, rate from 0.0 to 1.0 how likely following that edge from
that anchor leads toward completing the sub-objective. 1.0 = directly
answers it, 0.0 = irrelevant. Judge the RELATION MEANING in context of the
anchor, not surface word overlap."""


class HybridScorer(EmbeddingScorer):
    """alpha-blend of embedding similarity and batched LLM edge scoring.

    Scores candidates ACROSS anchors in one LLM call: pass rel_rows where
    each row also carries 'anchor_name'. Falls back to embedding-only on any
    LLM failure or exhausted budget (logged via the returned rows' source)."""

    def __init__(self, npy_path, names_path, llm,
                 alpha: float = 0.5, llm_top_k: int = 20,
                 model_name="sentence-transformers/all-MiniLM-L6-v2"):
        super().__init__(npy_path, names_path, model_name)
        self.llm = llm
        self.alpha = alpha
        self.llm_top_k = llm_top_k

    def __call__(self, objective, rel_rows, state=None):
        emb = self._emb_scores(objective, rel_rows)
        if state is None or self.alpha >= 1.0 or not rel_rows:
            return sorted(zip(rel_rows, emb), key=lambda x: -x[1])

        order = np.argsort(emb)[::-1]
        top = [int(i) for i in order[: self.llm_top_k]]
        cand_lines = "\n".join(
            f'{j}. {rel_rows[i].get("anchor_name", "?")} '
            f'--{rel_rows[i]["rel"]}--> (fanout {rel_rows[i].get("n", "?")})'
            for j, i in enumerate(top))

        llm_scores = {}
        try:
            out = self.llm(state,
                           SCORE_PROMPT.format(objective=objective,
                                               candidates=cand_lines),
                           '{"scores": [{"i": 0, "s": 0.0}, ...]} '
                           '(one entry per candidate, in order)')
            for entry in out.get("scores", []):
                j = int(entry["i"])
                if 0 <= j < len(top):
                    llm_scores[top[j]] = max(0.0, min(1.0, float(entry["s"])))
        except (BudgetExhausted, Exception):
            llm_scores = {}          # fall back to embedding-only blend

        blended = [self.alpha * e + (1 - self.alpha) * llm_scores.get(i, 0.0)
                   for i, e in enumerate(emb)]
        return sorted(zip(rel_rows, blended), key=lambda x: -x[1])
