import re

MAX_SUBOBJECTIVES = 4

PLANNER_PROMPT = """You decompose questions into a minimal ordered chain of \
sub-objectives for navigating a knowledge graph. Each sub-objective must be \
answerable by following one relation (possibly through an event node). Use \
#N to reference the result of sub-objective N. Use as FEW sub-objectives as \
possible.

For topic_mentions, extract ONLY specific named entities that appear \
literally in the question (people, places, organizations, works, products). \
Do NOT extract generic type words such as "celebrity", "university", \
"country", "senator", "airport", or "currency" -- these describe what kind \
of answer is wanted, not where to start searching.

Example 1 (single hop -- do NOT decompose):
Question: "who is the president of France?"
{"sub_objectives": ["find the president of France"],
 "topic_mentions": ["France"]}

Example 2 (composition):
Question: "who directed the film that won Best Picture in 1998?"
{"sub_objectives": ["find the film that won Best Picture in 1998",
                    "find the director of #1"],
 "topic_mentions": ["Best Picture"]}

Example 3 (conjunction):
Question: "which countries border France and have Spanish as official language?"
{"sub_objectives": ["find countries that border France",
                    "find which of #1 have Spanish as an official language"],
 "topic_mentions": ["France", "Spanish"]}

Example 4 (superlative):
Question: "what is the largest city in the country where the Nile ends?"
{"sub_objectives": ["find the country where the Nile ends",
                    "find the largest city in #1"],
 "topic_mentions": ["Nile"]}

Question: "{question}"
"""


def validate_plan(plan: dict, question: str) -> list[str]:
    issues = []
    subs = plan.get("sub_objectives")
    if not subs or not isinstance(subs, list):
        return ["no sub_objectives"]
    if len(subs) > MAX_SUBOBJECTIVES:
        issues.append(f"too many sub_objectives ({len(subs)})")
    for i, s in enumerate(subs):
        for ref in re.findall(r"#(\d+)", str(s)):
            if int(ref) >= i + 1:
                issues.append(f"forward/self reference #{ref} in step {i+1}")
    if not plan.get("topic_mentions"):
        issues.append("no topic_mentions")
    return issues


def render_objective(plan: list[dict], idx: int) -> str:
    text = plan[idx]["text"]
    for m in re.findall(r"#(\d+)", text):
        j = int(m) - 1
        if 0 <= j < idx:
            names = [e["name"] for e in plan[j]["resolved"]][:5]
            if names:
                text = text.replace(f"#{m}", " / ".join(names))
    return text


def planner_node(state, tools, llm, run_config):
    assert hasattr(run_config, "use_gold_entities"), \
    f"planner got {type(run_config).__name__}, expected RunConfig"

    from agr.budget import BudgetExhausted
    ablated = not run_config.use_planner
    if ablated:
        plan_json = {"sub_objectives": [state["question"]],
                     "topic_mentions": list(state["gold_q_entities"])}
        issues = []
    else:
        try:
            plan_json = llm(state, PLANNER_PROMPT.replace(
                "{question}", state["question"]),
                '{"sub_objectives": ["..."], "topic_mentions": ["..."]}')
            issues = validate_plan(plan_json, state["question"])
        except (BudgetExhausted, Exception) as e:
            plan_json, issues = {}, [f"planner call failed: {e}"]

        if issues:
            plan_json = {"sub_objectives": [state["question"]],
                         "topic_mentions": list(state["gold_q_entities"])}

    anchors, linking = [], []
    mentions = (state["gold_q_entities"] if run_config.use_gold_entities
                else plan_json["topic_mentions"])
    for m in mentions:
        hits = tools.search_entity(m, k=3)
        if hits:
            anchors.append({"id": hits[0]["id"], "name": hits[0]["name"]})
        linking.append({"mention": m, "top": hits[:1]})

    plan = [{"text": s, "status": "active" if i == 0 else "pending",
             "resolved": []}
            for i, s in enumerate(plan_json["sub_objectives"])]

    return {"plan": plan, "anchors": anchors,
            "trace": [{"node": "planner", "plan": plan_json,
                       "anchors": anchors, "linking": linking,
                       "fallback": bool(issues), "ablated": ablated}]}
