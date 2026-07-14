from agr.budget import BudgetMeter, BudgetExhausted
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities

WIDTH, DEPTH = 3, 3

REL_PRUNE = """Question: {question}
Current entity: {entity}
Available relations (relation, direction, fanout):
{relations}
Select up to {w} relations most likely to lead to the answer.
Return {{"relations": [{{"rel": "...", "dir": "in|out"}}]}}."""

ENT_PRUNE = """Question: {question}
Candidate entities reached (via {entity} --{rel}-->):
{entities}
Select up to {w} entities most likely on the path to the answer.
Return {{"entities": ["..."]}}."""

SUFFICIENT = """Question: {question}
Knowledge triples gathered so far:
{triples}
Can the question be answered from these triples alone?
Return {{"sufficient": true|false}}."""

ANSWER = """Question: {question}
Knowledge triples:
{triples}
Answer using ONLY these triples; name entities exactly as written.
If insufficient, say so and return []."""


class ToG:
    def __init__(self, llm, tools):
        self.llm, self.tools = llm, tools

    def run(self, q, budget_cfg):
        meter = BudgetMeter(budget_cfg)
        state = {"budget": meter}
        frontier, triples, trace = [], [], []
        for name in q["gold_q_entities"]:
            hits = self.tools.search_entity(name, k=1)
            if hits:
                frontier.append({"id": hits[0]["id"], "name": hits[0]["name"]})

        try:
            for depth in range(DEPTH):
                nxt = []
                for ent in frontier[:WIDTH]:
                    rels = self.tools.get_relations(ent["id"])[:40]
                    rel_out = self.llm(state, REL_PRUNE.format(
                        question=q["question"], entity=ent["name"], w=WIDTH,
                        relations="\n".join(
                            f'- {r["rel"]} ({r["dir"]}, {r["n"]})'
                            for r in rels)),
                        '{"relations": [{"rel": "...", "dir": "..."}]}')
                    for sel in rel_out.get("relations", [])[:WIDTH]:
                        res = self.tools.get_neighbors(
                            ent["id"], sel.get("rel", ""),
                            sel.get("dir", "out"))
                        nbrs = res["neighbors"][:20]
                        if not nbrs:
                            continue
                        ent_out = self.llm(state, ENT_PRUNE.format(
                            question=q["question"], entity=ent["name"],
                            rel=sel["rel"], w=WIDTH,
                            entities="\n".join(f'- {n["name"]}'
                                               for n in nbrs)),
                            '{"entities": ["..."]}')
                        keep = set(ent_out.get("entities", [])[:WIDTH])
                        for n in nbrs:
                            if n["name"] in keep:
                                triples.append(
                                    f'{ent["name"]} '
                                    f'{"/".join(n["via"])} {n["name"]}')
                                nxt.append(n)
                trace.append({"node": "tog", "depth": depth,
                              "frontier": [e["name"] for e in nxt][:10]})
                if not nxt:
                    break
                suf = self.llm(state, SUFFICIENT.format(
                    question=q["question"],
                    triples="\n".join(f"- {t}" for t in triples[-60:])),
                    '{"sufficient": true}')
                frontier = nxt[:WIDTH]
                if suf.get("sufficient"):
                    break
        except BudgetExhausted:
            trace.append({"node": "tog", "budget_exhausted": True})

        out = self.llm(state, ANSWER.format(
            question=q["question"],
            triples="\n".join(f"- {t}" for t in triples[-60:]) or "(none)"),
            BASELINE_SCHEMA)
        return make_final(out.get("answer", ""), parse_entities(out), meter,
                          [*trace, {"node": "tog_answer"}])
