from agr.budget import BudgetMeter
from agr.baselines.common import BASELINE_SCHEMA, make_final, parse_entities

PROMPT = """Answer this question with the name(s) of the answer entity or
entities. Be concise. If you do not know, say so and return [].

Question: {question}"""


class NoRetrieval:
    def __init__(self, llm):
        self.llm = llm

    def run(self, q, budget_cfg):
        meter = BudgetMeter(budget_cfg)
        state = {"budget": meter}
        out = self.llm(state, PROMPT.format(question=q["question"]),
                       BASELINE_SCHEMA)
        ents = parse_entities(out)
        return make_final(out.get("answer", ""), ents, meter,
                          [{"node": "noretrieval", "out": out}])
