import operator
from typing import Annotated, Optional, TypedDict

from agr.budget import BudgetConfig, BudgetMeter


class AGRState(TypedDict):
    qid: str
    question: str
    gold_q_entities: list[str]
    plan: list[dict]              # [{text, status, resolved:[{id,name}]}]
    anchors: list[dict]           # current frontier [{id, name}]
    traversed: Annotated[list[dict], operator.add]   # append-only
    backtrack_stack: list[dict]
    budget: BudgetMeter           # mutated in place, never returned as delta
    unsupported_claims: list[str]
    answer: Optional[str]
    supporting_triples: list[dict]
    trace: Annotated[list[dict], operator.add]       # append-only
    _eval_decision: Optional[str]  # scratch key: evaluator -> router


def make_init_state(qid: str, question: str,
                    gold_q_entities: list[str] | None = None,
                    cfg: BudgetConfig | None = None) -> AGRState:
    return AGRState(
        qid=qid, question=question,
        gold_q_entities=gold_q_entities or [],
        plan=[], anchors=[], traversed=[], backtrack_stack=[],
        budget=BudgetMeter(cfg or BudgetConfig()),
        unsupported_claims=[], answer=None, supporting_triples=[],
        trace=[], _eval_decision=None,
    )

"""
Checkpoint — run:
s = make_init_state('t','q');
print(s['budget'].snapshot())
"""
