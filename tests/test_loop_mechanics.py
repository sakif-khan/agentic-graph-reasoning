import pytest
from tests.mockllm import MockLLM
from tests.known import KNOWN

from agr.budget import BudgetConfig
from agr.config import RunConfig
from agr.state import make_init_state
from agr.graph_build import build_graph

pytestmark = pytest.mark.integration


def run(script, tools, scorer, cfg=None, run_cfg=None, question="q",
        gold=(KNOWN["entity_name"],)):
    agr = build_graph(MockLLM(script), tools, scorer,
                      run_cfg or RunConfig(use_gold_entities=True,
                                           alpha=1.0, tau=0.0))
    tools.qid = "test"
    st = make_init_state("test", question, gold_q_entities=list(gold),
                         cfg=cfg or BudgetConfig())
    return agr.invoke(st, config={"recursion_limit": 60})


def test_happy_path(tools, fake_scorer):
    script = [
        {"sub_objectives": ["find parent"],
         "topic_mentions": [KNOWN["entity_name"]]},              # planner
        {"decision": "answer", "objective_done": True,
         "resolved": [KNOWN["neighbor_name"]]},                  # evaluator
        {"draft": KNOWN["neighbor_name"],                        # verifier draft
         "answer_entities": [KNOWN["neighbor_name"]],
         "claims": []},
    ]
    final = run(script, tools, fake_scorer)
    assert final["answer"] == KNOWN["neighbor_name"]
    assert final["answer_entities"] == [KNOWN["neighbor_name"]]
    assert final["traversed"]
    assert final["budget"].llm_calls == 3        # draft passed through free


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

def test_verifier_grounded_passthrough(tools, fake_scorer):
    hedge = "could not be determined from the graph"
    script = [
        {"sub_objectives": ["find x"],
         "topic_mentions": [KNOWN["entity_name"]]},              # planner
        {"decision": "answer", "objective_done": True,
         "resolved": []},                                        # evaluator
        {"draft": hedge, "claims": [],                           # verifier draft
         "answer_entities": []},
    ]
    final = run(script, tools, fake_scorer)
    assert final["answer"] == hedge                  # draft passed through
    assert final["answer_entities"] == []
    assert final["budget"].llm_calls == 3            # no rewrite consumed
    v = next(t for t in final["trace"] if t.get("node") == "verifier")
    assert v["outcome"] == "grounded"


def test_verifier_unsupported_bounded_and_rewritten(tools, fake_scorer):
    bad_draft = "Zxq Alpha is the parent of Zxq Beta."
    bad_claim = {"h": "Zxq Alpha", "r": "parent of", "t": "Zxq Beta"}
    rewritten = "This could not be verified against the knowledge graph."
    script = [
        {"sub_objectives": ["find x"],
         "topic_mentions": [KNOWN["entity_name"]]},              # planner
        {"decision": "answer", "objective_done": True,
         "resolved": []},                                        # evaluator 1
        {"draft": bad_draft, "claims": [bad_claim],              # draft 1
         "answer_entities": ["Zxq Beta"]},
        {"verdicts": [{"i": 0, "supported": False}]},            # entail 1
        {"decision": "answer", "objective_done": True,
         "resolved": []},                                        # evaluator 2
        {"draft": bad_draft, "claims": [bad_claim],              # draft 2
         "answer_entities": ["Zxq Beta"]},
        {"verdicts": [{"i": 0, "supported": False}]},            # entail 2
        {"answer": rewritten, "answer_entities": []}             # rewrite
    ]
    final = run(script, tools, fake_scorer)
    assert final["budget"].verify_iters == \
        final["budget"].cfg.max_verify_iters                     # bounded
    assert final["answer"] == rewritten
    assert final["answer"] != bad_draft                          # changed
    assert bad_draft != final["answer"]
    assert final["answer_entities"] == []


def test_tau_trigger_backtracks_with_reason(tools, low_scorer):
    script = [
        {"sub_objectives": ["find x"],
         "topic_mentions": [KNOWN["entity_name"]]},              # planner
    ] + [{"decision": "continue", "objective_done": False,
          "resolved": []}] * 20 \
      + [{"draft": "could not be determined", "claims": [],      # tail
          "answer_entities": []}]
    final = run(script, tools, low_scorer,
                run_cfg=RunConfig(alpha=1.0, tau=0.2),
                cfg=BudgetConfig(max_backtracks=2))
    bts = [t for t in final["trace"] if t.get("node") == "backtracker"]
    assert bts, "expected at least one backtrack"
    assert bts[0]["reason"] == "low_score"           # router overrode eval

def test_draft_only_ablation_skips_checking(tools, fake_scorer):
    bad_claim = {"h": "Zxq Alpha", "r": "parent of", "t": "Zxq Beta"}
    script = [
        {"sub_objectives": ["find x"],
         "topic_mentions": [KNOWN["entity_name"]]},              # planner
        {"decision": "answer", "objective_done": True,
         "resolved": []},                                        # evaluator
        {"draft": "Zxq Alpha is the parent of Zxq Beta.",
         "answer_entities": ["Zxq Beta"],
         "claims": [bad_claim]},                                 # draft
    ]
    final = run(script, tools, fake_scorer,
                run_cfg=RunConfig(alpha=1.0, tau=0.0,
                                  verify_claims=False))
    v = next(t for t in final["trace"] if t.get("node") == "verifier")
    assert v["outcome"] == "draft_only"
    assert final["budget"].llm_calls == 3        # no entailment, no rewrite
    assert final["answer_entities"] == ["Zxq Beta"]   # unchecked, passes through

# pytest -m integration
# Integration tests need Neo4j up and KNOWN filled in.
