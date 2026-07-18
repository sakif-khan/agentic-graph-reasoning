import numpy as np

from agr.budget import BudgetMeter
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities
from agr.baselines.vectorrag import PROMPT   # same answering prompt, deliberately


def _words(rel: str) -> str:
    return rel.replace(".", " ").replace("_", " ")


class StaticGraphRAG:
    """One-shot 2-logical-hop neighborhood retrieval, no agency.
    CVT contract mirrors KGTools.get_neighbors: mediator nodes are hopped
    THROUGH (their two relations concatenated), never emitted as text."""

    BLOCK_PREFIXES = ["common.", "freebase.", "type.", "kg.",
                      "user.", "dataworld.", "rdf-schema#", "owl#"]

    def __init__(self, llm, driver, embed, resolver,
                 top_k=30, fanout_cap=100, cvt_cap=20):
        self.llm, self.driver, self.model = llm, driver, embed
        self.resolver = resolver
        self.top_k, self.cap, self.cvt_cap = top_k, fanout_cap, cvt_cap

    def subgraph(self, topic_names):
        pair2text = {}                    # (topic_name, endpoint_name) -> text

        def add(topic, endpoint, text):
            key = (topic, endpoint)
            if key not in pair2text or len(text) < len(pair2text[key]):
                pair2text[key] = text

        with self.driver.session() as s:
            topics = []                   # [(id, name)]
            for name in topic_names:
                _, hits = self.resolver(name, 1)
                if hits:
                    topics.append((hits[0][0], hits[0][1]))

            for eid, ename in topics:
                rows = s.run("""
                    MATCH (t:Entity {id:$id})-[r]-(n:Entity)
                    WHERE none(p IN $block WHERE r.fb_name STARTS WITH p)
                    RETURN n.id AS id, n.name AS name, n.is_cvt AS cvt,
                           r.fb_name AS rel
                    LIMIT $cap""",
                    id=eid, block=self.BLOCK_PREFIXES, cap=self.cap).data()
                for row in rows:
                    if not row["cvt"]:
                        add(ename, row["name"],
                            f'{ename} {_words(row["rel"])} {row["name"]}')
                    else:                 # hop through the mediator
                        for r2 in s.run("""
                            MATCH (c:Entity {id:$cid})-[r2]-(m:Entity)
                            WHERE m.id <> $orig AND m.is_cvt = false
                              AND none(p IN $block
                                       WHERE r2.fb_name STARTS WITH p)
                            RETURN m.name AS name, r2.fb_name AS rel2
                            LIMIT $cvt_cap""",
                            cid=row["id"], orig=eid,
                            block=self.BLOCK_PREFIXES,
                            cvt_cap=self.cvt_cap).data():
                            add(ename, r2["name"],
                                f'{ename} {_words(row["rel"])} '
                                f'{_words(r2["rel2"])} {r2["name"]}')

        return list(pair2text.values())

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
            facts="\n".join(f"- {t}" for t in texts) or "(none)",
            question=q["question"]), BASELINE_SCHEMA)
        return make_final(out.get("answer", ""), parse_entities(out), meter,
                          [{"node": "graphrag",
                            "n_facts": len(texts),
                            "facts_sample": texts[:10]}])
