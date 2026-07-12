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
TAU = 0.20   # low-score backtrack threshold; tuned with alpha (Step 3.5)

def route_after_eval(state):
    meter = state["budget"]
    if not meter.can("time") or not meter.can("depth"):
        return "answer"

    reason = None
    if state.get("_last_n_new", -1) == 0:
        reason = "dead_end"
    elif (state.get("_frontier_max_score") or 1.0) < TAU:
        reason = "low_score"
    elif (state.get("_eval_decision") or "") == "backtrack":
        reason = "evaluator"

    if reason:
        if meter.can("backtrack"):
            state["_backtrack_reason"] = reason
            return "backtrack"
        return "answer"          # budget-forced downgrade, still logged

    d = state.get("_eval_decision") or "answer"
    return d if d in ("continue", "answer") else "answer"


def route_after_verify(state):
    if not state["unsupported_claims"]:
        return "grounded"
    return "retry" if state["budget"].can("verify") else "give_up"


# ------------------------------ backtracker ------------------------------
def backtracker_node(state):
    meter = state["budget"]
    meter.backtracks += 1
    stack = list(state["backtrack_stack"])
    if stack:
        best = max(range(len(stack)), key=lambda i: stack[i].get("score", 0.0))
        snap = stack.pop(best)
    else:
        snap = {"anchors": state["anchors"], "depth": meter.depth}
    meter.depth = snap["depth"]
    reason = state.get("_backtrack_reason") or "unspecified"
    newly_banned = state["banned"] + [
        b for b in state["last_expanded"] if b not in state["banned"]]
    return {"anchors": snap["anchors"], "backtrack_stack": stack,
            "banned": newly_banned, "last_expanded": [],
            "_backtrack_reason": None,
            "trace": [{"node": "backtracker", "reason": reason,
                       "restored": [a["name"] for a in snap["anchors"]],
                       "restored_depth": snap["depth"],
                       "n_banned": len(newly_banned)}]}


# ------------------------------ verifier ------------------
DRAFT_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}
Entities identified as promising during exploration:
{candidates}

1. Draft an answer using ONLY the facts and candidates above. Use entity
names exactly as written. If insufficient, say what could not be determined.
2. Decompose your draft into atomic factual claims, each as
   {{"h": entity name, "r": short relation phrase, "t": entity name}}.
   Only include claims your draft actually asserts. A hedged draft
   ("could not be determined") has zero claims."""

ENTAIL_PROMPT = """Retrieved knowledge-graph triples:
{facts}

For each claim below, answer whether it is directly supported by the triples
above (true) or not (false). Unsupported includes: plausible but absent,
contradicted, or only inferable via outside knowledge.
Claims:
{claims}"""


def verifier_node(state, tools, llm, scorer):
    meter = state["budget"]
    facts = scorer.top_facts(state["question"], state["traversed"], k=60)
    facts_str = _fmt_facts(facts, 60)
    cands = ", ".join(c["name"] for c in state["candidate_answers"][:25]) \
            or "(none)"
    name_to_id = {}
    for t in state["traversed"]:
        name_to_id.setdefault(t["h_name"], t["h"])
        name_to_id.setdefault(t["t_name"], t["t"])

    # ---- (1) draft + claims, one call ----
    try:
        out = llm(state, DRAFT_PROMPT.format(question=state["question"],
                                             facts=facts_str,
                                             candidates=cands),
                  '{"draft": "...", "claims": [{"h": "...", "r": "...", '
                  '"t": "..."}]}')
        draft = out.get("draft") or "unable to answer"
        claims = [c for c in out.get("claims", [])
                  if isinstance(c, dict) and c.get("h") and c.get("t")]
    except (BudgetExhausted, Exception) as e:
        return {"draft": None, "unsupported_claims": [],
                "trace": [{"node": "verifier", "error": repr(e),
                           "outcome": "skipped"}]}

    # ---- (2) structural checks ----
    adjacent = set()
    for t in state["traversed"]:
        adjacent.add((t["h"], t["t"]))
        adjacent.add((t["t"], t["h"]))

    supported, pending, supporting = [], [], []
    for c in claims:
        h_id, t_id = name_to_id.get(c["h"]), name_to_id.get(c["t"])
        if h_id is None or t_id is None:
            pending.append(c)               # names not even retrieved
            continue
        if (h_id, t_id) in adjacent:
            supported.append(c)
            supporting.extend(t for t in state["traversed"]
                              if {t["h"], t["t"]} == {h_id, t_id})
        elif tools.verify_connection(h_id, t_id)["connected"]:
            supported.append(c)
        else:
            pending.append(c)

    # ---- (3) entailment fallback, one batched call ----
    unsupported = []
    if pending:
        try:
            claims_str = "\n".join(
                f'{i}. {c["h"]} -- {c["r"]} -- {c["t"]}'
                for i, c in enumerate(pending))
            ent = llm(state, ENTAIL_PROMPT.format(facts=facts_str,
                                                  claims=claims_str),
                      '{"verdicts": [{"i": 0, "supported": true}, ...]}')
            verdicts = {int(v["i"]): bool(v["supported"])
                        for v in ent.get("verdicts", [])}
            for i, c in enumerate(pending):
                (supported if verdicts.get(i, False)
                 else unsupported).append(c)
        except (BudgetExhausted, Exception):
            unsupported = pending           # conservative: unverified = unsupported

    unsupported_strs = [f'{c["h"]} {c["r"]} {c["t"]}' for c in unsupported]

    # ---- (4) retry targeting, if budget remains ----
    result = {"draft": draft,
              "unsupported_claims": unsupported_strs,
              "supporting_triples": supporting,
              "trace": [{"node": "verifier",
                         "n_claims": len(claims),
                         "n_structural": len(supported) - 0,
                         "unsupported": unsupported_strs,
                         "outcome": ("grounded" if not unsupported
                                     else "unsupported")}]}
    if unsupported and meter.can("verify"):
        meter.verify_iters += 1
        c = unsupported[0]
        repair = {"text": f'verify whether {c["h"]} {c["r"]} {c["t"]}',
                  "status": "active", "resolved": []}
        plan = state["plan"]
        for s_ in plan:
            if s_["status"] == "active":
                s_["status"] = "done"
        plan.append(repair)
        result["plan"] = plan
        h_id = name_to_id.get(c["h"])
        if h_id:
            result["anchors"] = [{"id": h_id, "name": c["h"]}]
    return result


# ------------------------------ answerer ------------------------------
ANSWER_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}

Entities identified as promising during exploration:
{candidates}

Answer using ONLY these facts and candidates. Give the answer entity name(s)
exactly as they appear above. If the information is insufficient, state what
could not be determined."""


REWRITE_PROMPT = """Question: {question}
Draft answer: {draft}
The following claims in the draft are NOT supported by the knowledge graph:
{unsupported}

Rewrite the answer removing or explicitly hedging the unsupported claims.
Keep everything that was supported. If nothing supported remains, state that
the answer could not be verified against the knowledge graph."""


def answerer_node(state, llm):
    draft = state.get("draft")
    unsupported = state.get("unsupported_claims") or []

    if draft and not unsupported:            # verified: zero-cost finalize
        answer, err = draft, None
    elif draft and unsupported:              # give_up path: one rewrite call
        try:
            out = llm(state, REWRITE_PROMPT.format(
                question=state["question"], draft=draft,
                unsupported="\n".join(f"- {u}" for u in unsupported)),
                '{"answer": "..."}')
            answer = out.get("answer") or "unable to answer"
            err = None
        except (BudgetExhausted, Exception) as e:
            answer = ("could not be fully verified against the knowledge "
                      "graph")
            err = repr(e)
    else:                                    # verifier skipped/failed: legacy path
        cands = ", ".join(c["name"] for c in state["candidate_answers"][:25]) \
                or "(none)"
        try:
            out = llm(state, ANSWER_PROMPT.format(
                question=state["question"],
                facts=_fmt_facts(state["traversed"], 60),
                candidates=cands),
                '{"answer": "..."}')
            answer, err = out.get("answer") or "unable to answer", None
        except (BudgetExhausted, Exception) as e:
            done = [s for s in state["plan"] if s["status"] == "done"]
            names = ([e_["name"] for s in done for e_ in s["resolved"]]
                     or [c["name"] for c in state["candidate_answers"][:5]])
            answer = ", ".join(names) if names else "unable to answer"
            err = repr(e)

    rec = {"node": "answerer", "answer": answer, "from_draft": bool(draft),
           "budget": state["budget"].snapshot()}
    if err:
        rec["error"] = err
    return {"answer": answer,
            "supporting_triples": state.get("supporting_triples")
                                  or list(state["traversed"]),
            "trace": [rec]}
