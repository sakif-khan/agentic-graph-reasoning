from agr.budget import BudgetExhausted
from agr.planner import render_objective


def active_idx(plan):
    return next((i for i, s in enumerate(plan) if s["status"] == "active"),
                None)


def _fmt_facts(triples, n):
    return "\n".join(
        f'- {t["h_name"]} --{"/".join(t["r"])}--> {t["t_name"]}'
        for t in triples[-n:]) or "(none)"


# ------------------------------ explorer ------------------------------
def explorer_node(state, tools, scorer):
    meter = state["budget"]
    idx = active_idx(state["plan"])
    objective = (render_objective(state["plan"], idx)
                 if idx is not None else state["question"])

    stack = state["backtrack_stack"] + [{
        "anchors": list(state["anchors"]), "depth": meter.depth}]

    new_triples, new_anchors, expanded = [], [], []
    for anchor in state["anchors"]:
        rels = tools.get_relations(anchor["id"])
        for rel_row, score in scorer(objective, rels)[: meter.cfg.beam_width]:
            res = tools.get_neighbors(anchor["id"], rel_row["rel"],
                                      rel_row["dir"])
            expanded.append({"anchor": anchor["name"],
                             "rel": rel_row["rel"],
                             "score": round(score, 3)})
            for nb in res["neighbors"]:
                new_triples.append({
                    "h": anchor["id"], "h_name": anchor["name"],
                    "r": nb["via"], "t": nb["id"], "t_name": nb["name"]})
                new_anchors.append({"id": nb["id"], "name": nb["name"]})

    seen, frontier = set(), []
    for a in new_anchors:
        if a["id"] not in seen:
            seen.add(a["id"])
            frontier.append(a)

    meter.depth += 1
    return {"anchors": frontier[: meter.cfg.max_anchors] or state["anchors"],
            "backtrack_stack": stack,
            "traversed": new_triples,
            "trace": [{"node": "explorer", "objective": objective,
                       "expanded": expanded, "n_new": len(new_triples)}]}


# ------------------------------ evaluator ------------------------------
EVAL_PROMPT = """Current sub-objective: {objective}
Recently retrieved facts:
{facts}
Remaining budget: {d_left} more expansions, {b_left} more backtracks.

Decide:
- "answer" if the facts complete the sub-objective (list satisfying entities \
in "resolved", exactly as named in the facts),
- "continue" if this direction is promising but incomplete,
- "backtrack" if this direction is a dead end."""


def evaluator_node(state, llm):
    meter = state["budget"]
    idx = active_idx(state["plan"])
    objective = (render_objective(state["plan"], idx)
                 if idx is not None else state["question"])
    try:
        out = llm(state, EVAL_PROMPT.format(
            objective=objective,
            facts=_fmt_facts(state["traversed"], 30),
            d_left=meter.cfg.max_depth - meter.depth,
            b_left=meter.cfg.max_backtracks - meter.backtracks),
            '{"decision": "continue|backtrack|answer", '
            '"objective_done": true, "resolved": ["..."]}')
    except (BudgetExhausted, Exception):
        out = {"decision": "answer", "objective_done": False, "resolved": []}

    plan = state["plan"]
    result = {"trace": [{"node": "evaluator", "out": out}]}

    if out.get("objective_done") and idx is not None:
        name_to_id = {t["t_name"]: t["t"] for t in state["traversed"]}
        resolved = [{"id": name_to_id[n], "name": n}
                    for n in out.get("resolved", []) if n in name_to_id]
        plan[idx]["status"] = "done"
        plan[idx]["resolved"] = resolved
        if idx + 1 < len(plan):
            plan[idx + 1]["status"] = "active"
            out["decision"] = "continue"
            if resolved:
                result["anchors"] = resolved     # next hop starts here
        else:
            out["decision"] = "answer"

    result["plan"] = plan
    result["_eval_decision"] = out.get("decision", "answer")
    return result


# ------------------------------ routers ------------------------------
def route_after_eval(state):
    meter = state["budget"]
    if not meter.can("time") or not meter.can("depth"):
        return "answer"
    d = state.get("_eval_decision") or "answer"
    if d == "backtrack" and not meter.can("backtrack"):
        return "answer"
    return d if d in ("continue", "backtrack", "answer") else "answer"


def route_after_verify(state):
    if not state["unsupported_claims"]:
        return "grounded"
    return "retry" if state["budget"].can("verify") else "give_up"


# ------------------------------ backtracker ------------------------------
def backtracker_node(state):
    meter = state["budget"]
    meter.backtracks += 1
    stack = list(state["backtrack_stack"])
    snap = stack.pop() if stack else {"anchors": state["anchors"],
                                      "depth": meter.depth}
    meter.depth = snap["depth"]
    return {"anchors": snap["anchors"], "backtrack_stack": stack,
            "trace": [{"node": "backtracker",
                       "restored": [a["name"] for a in snap["anchors"]]}]}


# ------------------------------ verifier (Phase 2 stub) ------------------
def verifier_node(state, tools, llm):
    return {"unsupported_claims": [],
            "trace": [{"node": "verifier", "stub": True}]}


# ------------------------------ answerer ------------------------------
ANSWER_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}

Answer using ONLY these facts. Give the answer entity name(s) exactly as they
appear in the facts. If the facts are insufficient, state what could not be
determined."""


def answerer_node(state, llm):
    try:
        out = llm(state, ANSWER_PROMPT.format(
            question=state["question"],
            facts=_fmt_facts(state["traversed"], 60)),
            '{"answer": "..."}')
        answer = out.get("answer") or "unable to answer"
    except (BudgetExhausted, Exception):
        done = [s for s in state["plan"] if s["status"] == "done"]
        names = [e["name"] for s in done for e in s["resolved"]]
        answer = ", ".join(names) if names \
            else "unable to answer (budget exhausted)"
    return {"answer": answer,
            "supporting_triples": list(state["traversed"]),
            "trace": [{"node": "answerer", "answer": answer,
                       "budget": state["budget"].snapshot()}]}
