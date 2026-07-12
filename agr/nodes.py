from typer.cli import state

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
        "anchors": list(state["anchors"]), "depth": meter.depth,
        "score": state.get("_frontier_max_score") or 0.0}]

    banned = {tuple(b) for b in state["banned"]}

    # ---- gather candidates from ALL anchors ----
    all_rows = []
    for anchor in state["anchors"]:
        for row in tools.get_relations(anchor["id"]):
            all_rows.append({**row, "anchor_id": anchor["id"],
                             "anchor_name": anchor["name"]})

    # ---- ONE scoring pass (hybrid: one batched LLM call inside) ----
    scored = scorer(objective, all_rows, state=state)

    # ---- per-anchor beam with ban filtering ----
    per_anchor, n_banned_skipped = {}, 0
    for row, score in scored:
        key = row["anchor_id"]
        bucket = per_anchor.setdefault(key, [])
        if len(bucket) >= meter.cfg.beam_width:
            continue
        if (key, row["rel"], row["dir"]) in banned:
            n_banned_skipped += 1
            continue
        bucket.append((row, score))

    new_triples, new_anchors, expanded, last_expanded = [], [], [], []
    max_score = 0.0
    for bucket in per_anchor.values():
        for row, score in bucket:
            max_score = max(max_score, score)
            last_expanded.append([row["anchor_id"], row["rel"], row["dir"]])
            res = tools.get_neighbors(row["anchor_id"], row["rel"],
                                      row["dir"])
            expanded.append({"anchor": row["anchor_name"], "rel": row["rel"],
                             "score": round(score, 3)})
            for nb in res["neighbors"]:
                new_triples.append({
                    "h": row["anchor_id"], "h_name": row["anchor_name"],
                    "r": nb["via"], "t": nb["id"], "t_name": nb["name"],
                    "rel_score": score})
                new_anchors.append({"id": nb["id"], "name": nb["name"],
                                    "score": score})

    seen, frontier = set(), []
    for a in sorted(new_anchors, key=lambda a: -a["score"]):
        if a["id"] not in seen:
            seen.add(a["id"])
            frontier.append({"id": a["id"], "name": a["name"]})

    meter.depth += 1
    return {"anchors": frontier[: meter.cfg.max_anchors] or state["anchors"],
            "backtrack_stack": stack,
            "banned": state["banned"],
            "last_expanded": last_expanded,
            "_last_n_new": len(new_triples),
            "_frontier_max_score": max_score,
            "traversed": new_triples,
            "trace": [{"node": "explorer", "objective": objective,
                       "expanded": expanded, "n_new": len(new_triples),
                       "max_score": round(max_score, 3),
                       "n_banned_skipped": n_banned_skipped}]}


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


def evaluator_node(state, llm, scorer):
    meter = state["budget"]
    idx = active_idx(state["plan"])
    objective = (render_objective(state["plan"], idx)
                 if idx is not None else state["question"])

    facts = scorer.top_facts(objective, state["traversed"], k=30)   # Fix 3
    facts_str = "\n".join(
        f'- {t["h_name"]} --{"/".join(t["r"])}--> {t["t_name"]}'
        for t in facts) or "(none)"

    try:
        out = llm(state, EVAL_PROMPT.format(
            objective=objective, facts=facts_str,
            d_left=meter.cfg.max_depth - meter.depth,
            b_left=meter.cfg.max_backtracks - meter.backtracks),
            '{"decision": "continue|backtrack|answer", '
            '"objective_done": true, "resolved": ["..."]}')
    except BudgetExhausted:
        out = {"decision": "answer", "objective_done": False, "resolved": []}
    except Exception as e:
        out = {"decision": "answer", "objective_done": False, "resolved": [],
               "error": repr(e)}

    plan = state["plan"]
    name_to_id = {t["t_name"]: t["t"] for t in state["traversed"]}
    resolved = [{"id": name_to_id[n], "name": n}
                for n in out.get("resolved", []) if n in name_to_id]

    # Fix 4: accumulate EVERY resolution, done or not
    cand = {c["id"]: c for c in state["candidate_answers"]}
    for r in resolved:
        cand.setdefault(r["id"], r)

    result = {"trace": [{"node": "evaluator", "out": out}],
              "candidate_answers": list(cand.values())}

    if out.get("objective_done") and idx is not None:
        plan[idx]["status"] = "done"
        plan[idx]["resolved"] = resolved
        if idx + 1 < len(plan):
            plan[idx + 1]["status"] = "active"
            out["decision"] = "continue"
            if resolved:
                result["anchors"] = resolved
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
    if state.get("_last_n_new", -1) == 0:
        # Explorer produced nothing new (ban list exhausted this anchor's
        # relations, or dead-end node). Nothing new exists to evaluate or
        # re-explore; force the answer path.
        return "answer"
    decision = state.get("_eval_decision") or "answer"
    if decision == "backtrack" and not meter.can("backtrack"):
        return "answer"
    return decision if decision in ("continue", "backtrack", "answer") else "answer"


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
    newly_banned = state["banned"] + [
        b for b in state["last_expanded"] if b not in state["banned"]]
    return {"anchors": snap["anchors"], "backtrack_stack": stack,
            "banned": newly_banned,
            "last_expanded": [],
            "trace": [{"node": "backtracker",
                       "restored": [a["name"] for a in snap["anchors"]],
                       "n_banned": len(newly_banned)}]}


# ------------------------------ verifier (Phase 2 stub) ------------------
def verifier_node(state, tools, llm):
    return {"unsupported_claims": [],
            "trace": [{"node": "verifier", "stub": True}]}


# ------------------------------ answerer ------------------------------
ANSWER_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}

Entities identified as promising during exploration:
{candidates}

Answer using ONLY these facts and candidates. Give the answer entity name(s)
exactly as they appear above. If the information is insufficient, state what
could not be determined."""


def answerer_node(state, llm):
    candidates = ", ".join(candidate["name"] for candidate in state["candidate_answers"][:25]) \
                 or "(none)"
    try:
        out = llm(state, ANSWER_PROMPT.format(
            question=state["question"],
            facts=_fmt_facts(state["traversed"], 60),
            candidates=candidates),
            '{"answer": "..."}')
        answer = out.get("answer") or "unable to answer"
        err = None
    except BudgetExhausted:
        done = [s for s in state["plan"] if s["status"] == "done"]
        names = [e["name"] for s in done for e in s["resolved"]]
        names = names or [c["name"] for c in state["candidate_answers"][:5]]
        answer = ", ".join(names) if names \
            else "unable to answer (budget exhausted)"
        err = "budget"
    except Exception as e:
        answer = "unable to answer (LLM error)"
        err = repr(e)

    trace_rec = {"node": "answerer", "answer": answer,
                 "budget": state["budget"].snapshot()}
    if err:
        trace_rec["error"] = err
    return {"answer": answer,
            "supporting_triples": list(state["traversed"]),
            "trace": [trace_rec]}
