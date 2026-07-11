from functools import partial

from langgraph.graph import StateGraph, END

from agr.state import AGRState
from agr.planner import planner_node
from agr import nodes


def build_graph(llm, tools, scorer, run_config):
    g = StateGraph(AGRState)
    g.add_node("planner", partial(planner_node, tools=tools, llm=llm,
                                  run_config=run_config))
    g.add_node("explorer", partial(nodes.explorer_node, tools=tools,
                                   scorer=scorer))
    g.add_node("evaluator", partial(nodes.evaluator_node, llm=llm))
    g.add_node("backtracker", nodes.backtracker_node)
    g.add_node("verifier", partial(nodes.verifier_node, tools=tools, llm=llm))
    g.add_node("answerer", partial(nodes.answerer_node, llm=llm))

    g.set_entry_point("planner")
    g.add_edge("planner", "explorer")
    g.add_edge("explorer", "evaluator")
    g.add_conditional_edges("evaluator", nodes.route_after_eval,
                            {"continue": "explorer",
                             "backtrack": "backtracker",
                             "answer": "verifier"})
    g.add_edge("backtracker", "explorer")
    g.add_conditional_edges("verifier", nodes.route_after_verify,
                            {"grounded": "answerer",
                             "retry": "explorer",
                             "give_up": "answerer"})
    g.add_edge("answerer", END)
    return g.compile()

"""
Checkpoint — run:
python -c "from agr.graph_build import build_graph; print('ok')"
"""
