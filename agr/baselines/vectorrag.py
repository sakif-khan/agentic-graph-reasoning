import json
import numpy as np
from sentence_transformers import SentenceTransformer

from agr.budget import BudgetMeter
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities
from agr.config import EMBED_MODEL

PROMPT = """Facts (retrieved from a knowledge graph):
{facts}

Question: {question}
Answer using ONLY the facts above. Name entities exactly as written in the
facts. If the facts are insufficient, say so and return []."""


class VectorRAG:
    def __init__(self, llm, index_dir, top_k=30, model=EMBED_MODEL):
        self.llm, self.top_k = llm, top_k
        n = json.load(open(f"{index_dir}/shape.json"))["n"]
        self.vecs = np.memmap(f"{index_dir}/vecs.fp16", dtype=np.float16,
                              mode="r", shape=(n, 384))
        self.texts = open(f"{index_dir}/texts.txt",
                          encoding="utf-8").read().split("\n")
        self.model = SentenceTransformer(model)

    def retrieve(self, question):
        qv = self.model.encode([question],
                               normalize_embeddings=True)[0].astype(np.float16)
        # chunked matmul keeps peak memory flat
        scores = np.empty(len(self.texts), dtype=np.float32)
        C = 500_000
        for i in range(0, len(self.texts), C):
            scores[i:i+C] = (self.vecs[i:i+C] @ qv).astype(np.float32)
        top = np.argpartition(scores, -self.top_k)[-self.top_k:]
        top = top[np.argsort(scores[top])[::-1]]
        return [self.texts[i] for i in top]

    def run(self, q, budget_cfg):
        meter = BudgetMeter(budget_cfg)
        state = {"budget": meter}
        facts = self.retrieve(q["question"])
        out = self.llm(state, PROMPT.format(
            facts="\n".join(f"- {t}" for t in facts),
            question=q["question"]), BASELINE_SCHEMA)
        return make_final(out.get("answer", ""), parse_entities(out), meter,
                          [{"node": "vectorrag", "n_facts": len(facts)}])
