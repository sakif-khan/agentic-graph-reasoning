from sentence_transformers import SentenceTransformer
import numpy as np

from agr.budget import BudgetMeter
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities
from agr.baselines.vectorrag import PROMPT   # same answering prompt, deliberately


class StaticGraphRAG:
    def __init__(self, llm, driver, embed, top_k=30, fanout_cap=100):
        self.llm, self.driver, self.model = llm, driver, embed
        self.top_k, self.cap = top_k, fanout_cap

    def subgraph(self, topic_names):
        q = """
        MATCH (t:Entity) WHERE t.name IN $names
        CALL (t) {
          MATCH (t)-[r1]-(n1:Entity)
          RETURN t AS a, r1, n1 AS b LIMIT $cap
        }
        WITH collect({h:a.name, r:r1.fb_name, t:b.name, mid:b}) AS hop1
        UNWIND hop1 AS x
        WITH hop1, x WHERE x.mid.is_cvt = false
        CALL (x) {
          MATCH (m:Entity {id:x.mid.id})-[r2]-(n2:Entity)
          RETURN r2, n2 LIMIT 20
        }
        RETURN hop1, collect({h:x.t, r:r2.fb_name, t:n2.name}) AS hop2
        """
        with self.driver.session() as s:
            rec = s.run(q, names=topic_names, cap=self.cap).single()
        triples = []
        if rec:
            triples = [t for t in rec["hop1"]] + [t for t in rec["hop2"]]
        return [f'{t["h"]} {t["r"].replace(".", " ").replace("_", " ")} '
                f'{t["t"]}' for t in triples if t.get("h") and t.get("t")]

    def run(self, q, budget_cfg):
        meter = BudgetMeter(budget_cfg)
        state = {"budget": meter}
        texts = self.subgraph(q["gold_q_entities"])
        if len(texts) > self.top_k:
            qv = self.model.encode([q["question"]],
                                   normalize_embeddings=True)[0]
            tv = self.model.encode(texts, batch_size=256,
                                   normalize_embeddings=True)
            order = np.argsort(tv @ qv)[::-1][: self.top_k]
            texts = [texts[i] for i in order]
        out = self.llm(state, PROMPT.format(
            facts="\n".join(f"- {t}" for t in texts),
            question=q["question"]), BASELINE_SCHEMA)
        return make_final(out.get("answer", ""), parse_entities(out), meter,
                          [{"node": "graphrag", "n_facts": len(texts)}])
