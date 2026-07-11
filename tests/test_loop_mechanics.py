import pytest
from tests.mockllm import MockLLM
from tests.known import KNOWN

from agr.budget import BudgetConfig
from agr.config import RunConfig
from agr.state import make_init_state
from agr.graph_build import build_graph

pytestmark = pytest.mark.integration


def run(script, tools, scorer, cfg=None, question="q",
        gold=(KNOWN["entity_name"],)):
    agr = build_graph(MockLLM(script), tools, scorer,
                      RunConfig(use_gold_entities=True))
    tools.qid = "test"
    st = make_init_state("test", question, gold_q_entities=list(gold),
                         cfg=cfg or BudgetConfig())
    return agr.invoke(st, config={"recursion_limit": 60})


def test_happy_path(tools, fake_scorer):
    script = [
        {"sub_objectives": ["find parent"], "topic_mentions": [KNOWN["entity_name"]]},
        {"decision": "answer", "objective_done": True,
         "resolved": [KNOWN["neighbor_name"]]},
        {"answer": KNOWN["neighbor_name"]},
    ]
    final = run(script, tools, fake_scorer)
    assert final["answer"] == KNOWN["neighbor_name"]
    assert final["traversed"]


def test_depth_budget_halts_runaway(tools, fake_scorer):
    script = [{"sub_objectives": ["x"], "topic_mentions": [KNOWN["entity_name"]]}] \
           + [{"decision": "continue", "objective_done": False,
               "resolved": []}] * 50 + [{"answer": "y"}]
    final = run(script, tools, fake_scorer, cfg=BudgetConfig(max_depth=3))
    assert final["budget"].depth == 3
    assert "depth" in final["budget"].exhausted


def test_backtrack_cap_downgrades(tools, fake_scorer):
    script = [{"sub_objectives": ["x"], "topic_mentions": [KNOWN["entity_name"]]}] \
           + [{"decision": "backtrack", "objective_done": False,
               "resolved": []}] * 50 + [{"answer": "y"}]
    final = run(script, tools, fake_scorer, cfg=BudgetConfig(max_backtracks=2))
    assert final["budget"].backtracks == 2
    assert final["answer"] is not None

def test_backtrack_bans_reexpansion(tools, fake_scorer):
    script = [{"sub_objectives": ["x"], "topic_mentions": [KNOWN["entity_name"]]}] \
           + [{"decision": "backtrack", "objective_done": False,
               "resolved": []}] * 50 + [{"answer": "y"}]
    final = run(script, tools, fake_scorer, cfg=BudgetConfig(max_backtracks=3))
    ex = [t for t in final["trace"] if t.get("node") == "explorer"]
    first = {(e["anchor"], e["rel"]) for e in ex[0]["expanded"]}
    second = {(e["anchor"], e["rel"]) for e in ex[1]["expanded"]}
    assert first.isdisjoint(second), \
        "explorer re-expanded banned (anchor, relation) pairs after backtrack"

# pytest -m integration
# Integration tests need Neo4j up and KNOWN filled in.
