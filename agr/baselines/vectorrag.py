import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from agr.budget import BudgetMeter
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities
from agr.env import EMBED_MODEL

PROMPT = """Facts (retrieved from a knowledge graph):
{facts}

Question: {question}
Answer using ONLY the facts above. Name entities exactly as written in the
facts. If the facts are insufficient, say so and return []."""


class VectorRAG:
    def __init__(self, llm, index_dir, top_k=30, model=EMBED_MODEL):
        self.llm, self.top_k = llm, top_k
        self.texts = open(f"{index_dir}/texts.txt",
                          encoding="utf-8").read().split("\n")
        self.index = faiss.read_index(f"{index_dir}/flat.faiss")
        self.model = SentenceTransformer(model)

    def retrieve(self, question):
        qv = self.model.encode([question],
                               normalize_embeddings=True)[0].astype(np.float32)
        _, I = self.index.search(qv[None, :], self.top_k)
        return [self.texts[idx] for idx in I[0] if idx >= 0]

    def run(self, q, budget_cfg):
        meter = BudgetMeter(budget_cfg)
        state = {"budget": meter}
        facts = self.retrieve(q["question"])
        out = self.llm(state, PROMPT.format(
            facts="\n".join(f"- {t}" for t in facts),
            question=q["question"]), BASELINE_SCHEMA)
        return make_final(out.get("answer", ""), parse_entities(out), meter,
                          [{"node": "vectorrag", "n_facts": len(facts)}])
