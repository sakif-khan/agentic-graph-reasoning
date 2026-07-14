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

    info = getattr(scorer, "last_info", {})
    signal_max = max(max_score,
                     info.get("emb_max", 0.0),
                     info.get("llm_max", 0.0))

    meter.depth += 1
    return {"anchors": frontier[: meter.cfg.max_anchors] or state["anchors"],
            "backtrack_stack": stack,
            "banned": state["banned"],
            "last_expanded": last_expanded,
            "_last_n_new": len(new_triples),
            "_frontier_max_score": signal_max,
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
                cap = state["budget"].cfg.max_anchors
                result["anchors"] = resolved[:cap]
        else:
            out["decision"] = "answer"

    result["plan"] = plan
    result["_eval_decision"] = out.get("decision", "answer")
    return result


# ------------------------------ routers ------------------------------
def _backtrack_trigger(state, tau: float) -> str | None:
    """Priority-ordered backtrack triggers. Returns reason code or None."""
    if state.get("_last_n_new", -1) == 0:
        return "dead_end"
    if (state.get("_frontier_max_score") or 1.0) < tau:
        return "low_score"
    if (state.get("_eval_decision") or "") == "backtrack":
        return "evaluator"
    return None

def route_after_eval(state, run_config):
    meter = state["budget"]
    if not meter.can("time") or not meter.can("depth"):
        return "answer"

    if _backtrack_trigger(state, run_config.tau):
        return "backtrack" if meter.can("backtrack") else "answer"

    d = state.get("_eval_decision") or "answer"
    return d if d in ("continue", "answer") else "answer"


def route_after_verify(state):
    meter = state["budget"]
    if not state["unsupported_claims"]:
        return "grounded"
    if meter.can("verify") and meter.can("depth") and meter.can("time"):
        return "retry"
    return "give_up"


# ------------------------------ backtracker ------------------------------
def backtracker_node(state, run_config):
    meter = state["budget"]
    meter.backtracks += 1
    stack = list(state["backtrack_stack"])
    if stack:
        best = max(range(len(stack)), key=lambda i: stack[i].get("score", 0.0))
        snap = stack.pop(best)
    else:
        snap = {"anchors": state["anchors"], "depth": meter.depth}
    meter.depth = snap["depth"]
    reason = _backtrack_trigger(state, run_config.tau) or "unspecified"
    newly_banned = state["banned"] + [
        b for b in state["last_expanded"] if b not in state["banned"]]
    return {"anchors": snap["anchors"], "backtrack_stack": stack,
            "banned": newly_banned, "last_expanded": [],
            "trace": [{"node": "backtracker", "reason": reason,
                       "restored": [a["name"] for a in snap["anchors"]],
                       "restored_depth": snap["depth"],
                       "n_banned": len(newly_banned)}]}


# ------------------------------ verifier ------------------

# CACHE INVARIANT: this prompt must NOT contain alpha, tau, or any RunConfig
# value. Alpha blends AFTER the LLM call, so scorer responses are shared
# across all sweep conditions via the cache. Adding config-dependent wording
# here silently multiplies sweep cost by the number of conditions.
DRAFT_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}
Entities identified as promising during exploration:
{candidates}

1. Draft an answer using ONLY the facts and candidates above. Use entity
   names exactly as written. If insufficient, say what could not be
   determined.
2. List the answer entities themselves in "answer_entities", copied EXACTLY
   as they are named in the facts above -- these are the entities your draft
   asserts as the answer, not every entity it mentions. If your draft is a
   hedge ("could not be determined"), "answer_entities" MUST be [].
   IMPORTANT: "answer_entities" must be specific entities of the kind the
   question asks for (a person for "who", a place for "where", etc.).
   Never restate the question or name entity types/categories as the
   answer. If you cannot name specific answer entities from the facts,
   your draft must be a hedge and "answer_entities" must be [].
3. Decompose your draft into atomic factual claims, each as
   {{"h": entity name, "r": short relation phrase, "t": entity name}}.
   Only include claims your draft actually asserts. A hedged draft has zero
   claims."""

ENTAIL_PROMPT = """Retrieved knowledge-graph triples:
{facts}

For each claim below, answer whether it is directly supported by the triples
above (true) or not (false). Unsupported includes: plausible but absent,
contradicted, or only inferable via outside knowledge.
Claims:
{claims}"""


def verifier_node(state, tools, llm, scorer, run_config):
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
                  '{"draft": "...", "answer_entities": ["..."], '
                  '"claims": [{"h": "...", "r": "...", "t": "..."}]}')
        draft = out.get("draft") or "unable to answer"
        answer_entities = [str(a).strip()
                           for a in out.get("answer_entities", [])
                           if str(a).strip()]
        claims = [c for c in out.get("claims", [])
                  if isinstance(c, dict) and c.get("h") and c.get("t")]
        
        if not run_config.verify_claims:
            return {"draft": draft,
                    "answer_entities": answer_entities,
                    "unsupported_claims": [],
                    "supporting_triples": [],
                    "trace": [{"node": "verifier", "n_claims": len(claims),
                            "outcome": "draft_only"}]}
    except (BudgetExhausted, Exception) as e:
        return {"draft": None, "answer_entities": [],
                "unsupported_claims": [],
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
              "answer_entities": answer_entities,
              "unsupported_claims": unsupported_strs,
              "supported_claims": supported,
              "unsupported_claim_objs": unsupported,
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
def filter_answer_entities(draft_entities, supported, unsupported):
    """Deterministic entity selection for the give_up path.
    Keep a draft entity iff it appears in >=1 supported claim, OR appears in
    no unsupported claim (conservative: entities the decomposer never
    claimed are retained -- we punish unsupported assertions, not
    decomposition recall). Strings are copied verbatim; nothing is ever
    added that was not in the draft's own list."""
    sup = {c["h"] for c in supported} | {c["t"] for c in supported}
    unsup = {c["h"] for c in unsupported} | {c["t"] for c in unsupported}
    return [e for e in draft_entities if e in sup or e not in unsup]

ANSWER_PROMPT = """Question: {question}
Facts retrieved from the knowledge graph:
{facts}

Entities identified as promising during exploration:
{candidates}

Answer using ONLY these facts and candidates. Give the answer entity name(s)
exactly as they appear above. If the information is insufficient, state what
could not be determined.
Also list in "answer_entities" the entities your answer
asserts (exactly as named above); [] if it asserts nothing."""


REWRITE_PROMPT = """Question: {question}
Draft answer: {draft}
The following claims in the draft are NOT supported by the knowledge graph:
{unsupported}
The following entities remain verified and MUST be kept in the answer,
named exactly as written: {kept}

Rewrite the draft: keep the verified entities and their supported claims,
and remove or explicitly hedge the unsupported claims. If the kept list is
empty, state that the answer could not be verified against the knowledge
graph. Respond with prose only."""


def answerer_node(state, llm):
    draft = state.get("draft")
    unsupported = state.get("unsupported_claims") or []
    answer_entities = state.get("answer_entities") or []

    if draft and not unsupported:            # verified: zero-cost finalize
        answer, err = draft, None
    elif draft and unsupported:              # give_up: deterministic entities,
        answer_entities = filter_answer_entities(   # LLM for prose only
            answer_entities,
            state.get("supported_claims") or [],
            state.get("unsupported_claim_objs") or [])
        kept = ", ".join(answer_entities) or "(none)"
        try:
            out = llm(state, REWRITE_PROMPT.format(
                question=state["question"], draft=draft,
                unsupported="\n".join(f"- {u}" for u in unsupported),
                kept=kept),
                '{"answer": "..."}')
            answer = out.get("answer") or "unable to answer"
            err = None
        except (BudgetExhausted, Exception) as e:
            # entities are already decided; only the prose degrades
            answer = (f"Verified: {kept}. Other parts of the answer could "
                      f"not be verified against the knowledge graph."
                      if answer_entities else
                      "could not be fully verified against the knowledge "
                      "graph")
            err = repr(e)
    else:                                    # verifier skipped: legacy path
        cands = ", ".join(c["name"] for c in state["candidate_answers"][:25]) \
                or "(none)"
        try:
            out = llm(state, ANSWER_PROMPT.format(
                question=state["question"],
                facts=_fmt_facts(state["traversed"], 60),
                candidates=cands),
                '{"answer": "...", "answer_entities": ["..."]}')
            answer = out.get("answer") or "unable to answer"
            answer_entities = [str(a).strip()
                               for a in out.get("answer_entities", [])
                               if str(a).strip()]
            err = None
        except (BudgetExhausted, Exception) as e:
            done = [s for s in state["plan"] if s["status"] == "done"]
            names = ([e_["name"] for s in done for e_ in s["resolved"]]
                     or [c["name"] for c in state["candidate_answers"][:5]])
            answer = ", ".join(names) if names else "unable to answer"
            answer_entities = names
            err = repr(e)

    supp = state.get("supporting_triples")
    if supp is None:
        supp = list(state["traversed"])

    rec = {"node": "answerer", "answer": answer,
           "answer_entities": answer_entities,
           "from_draft": bool(draft),
           "budget": state["budget"].snapshot()}
    if err:
        rec["error"] = err
    return {"answer": answer,
            "answer_entities": answer_entities,
            "supporting_triples": supp,
            "trace": [rec]}
