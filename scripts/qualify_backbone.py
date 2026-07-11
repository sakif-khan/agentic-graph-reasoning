import hashlib, json, time
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.llm import LLMClient
from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.scorer import EmbeddingScorer
from agr.state import make_init_state
from agr.config import RunConfig
from agr.graph_build import build_graph
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY

CANDIDATES = {
    "gpt-4.1-mini-2025-04-14": dict(temperature=0.0, reasoning_effort=None),
    "gpt-5.4-mini-2026-03-17": dict(temperature=0.0, reasoning_effort="none"),
}
QUESTIONS = json.load(open("data/smoke20.json", encoding="utf-8"))
DETERMINISM_QIDS = [QUESTIONS[i]["id"] for i in (0, 6, 14)]  # 1-5 one-hop, 6-13 two-hop, 14-16 conjunction

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
scorer = EmbeddingScorer("data/relation_embeddings.npy",
                         "data/relation_names.json")


def decision_signature(trace) -> str:
    """Canonical hash of the agent's decisions, ignoring timing/noise."""
    core = []
    for t in trace:
        node = t.get("node")
        if node == "planner":
            core.append(("planner", tuple(t["plan"].get("sub_objectives", []))))
        elif node == "explorer":
            core.append(("explorer",
                         tuple((e["anchor"], e["rel"]) for e in t["expanded"])))
        elif node == "evaluator":
            o = t["out"]
            core.append(("eval", o.get("decision"),
                         tuple(sorted(o.get("resolved", [])))))
        elif node == "answerer":
            core.append(("answer", t.get("answer")))
    return hashlib.md5(json.dumps(core, ensure_ascii=False)
                       .encode()).hexdigest()[:12]


def run_question(agr, tools, q):
    tools.qid = q["id"]
    t0 = time.time()
    final = agr.invoke(
        make_init_state(q["id"], q["question"],
                        gold_q_entities=q["gold_q_entities"]),
        config={"recursion_limit": 60})
    snap = final["budget"].snapshot()
    errors = [t for t in final["trace"] if "error" in t or
              (isinstance(t.get("out"), dict) and "error" in t["out"])]
    return {"id": q["id"], "answer": final["answer"], "gold": q["answers"],
            "tokens": snap["tokens"], "reasoning_tokens":
                snap.get("reasoning_tokens", 0),
            "llm_calls": snap["llm_calls"],
            "seconds": round(time.time() - t0, 1),
            "n_errors": len(errors),
            "sig": decision_signature(final["trace"]),
            "trace": final["trace"]}


results = {}
for model, params in CANDIDATES.items():
    llm = LLMClient(model=model, api_key=OPENAI_API_KEY, **params)
    tools = KGTools(driver, EntityResolver(driver, embed),
                    f"logs/qualify_{model.replace('/', '_')}.jsonl")
    agr = build_graph(llm, tools, scorer, RunConfig(use_gold_entities=True))

    rows = [run_question(agr, tools, q) for q in QUESTIONS]
    # determinism probe: second run of 3 selected questions
    repeats = {q["id"]: run_question(agr, tools, q)
               for q in QUESTIONS if q["id"] in DETERMINISM_QIDS}

    with open(f"logs/qualify_{model.replace('/', '_')}_full.jsonl", "w",
              encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({**r, "backbone": llm.describe()},
                               ensure_ascii=False) + "\n")

    det_matches = sum(
        1 for qid, rep in repeats.items()
        if rep["sig"] == next(r["sig"] for r in rows if r["id"] == qid))
    results[model] = {
        "rows": rows,
        "determinism": f"{det_matches}/{len(repeats)}",
    }

# ---------------- comparison table ----------------
print(f"\n{'metric':<28}" + "".join(f"{m:>28}" for m in CANDIDATES))
def agg(model, fn):
    return fn(results[model]["rows"])
for label, fn in [
    ("mean tokens/question", lambda rs: round(sum(r["tokens"] for r in rs)/len(rs))),
    ("mean llm calls/question", lambda rs: round(sum(r["llm_calls"] for r in rs)/len(rs), 1)),
    ("mean seconds/question", lambda rs: round(sum(r["seconds"] for r in rs)/len(rs), 1)),
    ("total reasoning tokens", lambda rs: sum(r["reasoning_tokens"] for r in rs)),
    ("questions with errors", lambda rs: sum(1 for r in rs if r["n_errors"])),
]:
    print(f"{label:<28}" + "".join(f"{agg(m, fn):>28}" for m in CANDIDATES))
print(f"{'determinism (repeat sigs)':<28}" +
      "".join(f"{results[m]['determinism']:>28}" for m in CANDIDATES))
print("\nPer-question answers (eyeball for sensibleness):")
for i, q in enumerate(QUESTIONS):
    print(f'\n[{q["id"]}] {q["question"]}  gold={q["answers"]}')
    for m in CANDIDATES:
        r = results[m]["rows"][i]
        print(f'   {m[:24]:<26} -> {r["answer"]!r}')
driver.close()
