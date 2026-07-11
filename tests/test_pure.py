from agr.budget import BudgetConfig, BudgetMeter
from agr.planner import validate_plan, render_objective
from agr.resolver import lucene_escape


def test_forward_reference_rejected():
    bad = {"sub_objectives": ["find director of #1", "find the film"],
           "topic_mentions": ["x"]}
    assert any("forward" in i for i in validate_plan(bad, "q"))


def test_single_objective_ok():
    good = {"sub_objectives": ["find the president of France"],
            "topic_mentions": ["France"]}
    assert validate_plan(good, "q") == []


def test_render_substitutes_resolved():
    plan = [{"text": "find the film", "status": "done",
             "resolved": [{"id": "1", "name": "Titanic"}]},
            {"text": "find the director of #1", "status": "active",
             "resolved": []}]
    assert "Titanic" in render_objective(plan, 1)


def test_lucene_escape_hostile_names():
    for s in ["AC/DC", "Batman (1989 film)", "M*A*S*H", "a:b~c"]:
        lucene_escape(s)          # must not raise


def test_meter_records_exhaustion():
    m = BudgetMeter(BudgetConfig(max_depth=2))
    m.depth = 2
    assert not m.can("depth")
    assert "depth" in m.exhausted

# pytest tests\test_pure.py
# Pure tests must pass with no Neo4j running.
