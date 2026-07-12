# Score a RunLogger JSONL: hits / hedges / wrong + cost columns.
# Usage: python scripts\score_run.py logs\smoke20_a0.5_t0.2.jsonl [more.jsonl ...]

import json, sys, unicodedata


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).strip().lower()


def score_file(path):
    n = hits = hedges = wrong = unans_ok = 0
    tokens = calls = backtracks = 0
    verifier = {}
    for line in open(path, encoding="utf-8"):
        rec = json.loads(line)
        n += 1
        gold = {norm(g) for g in rec["gold"]}
        pred = {norm(a) for a in rec.get("answer_entities", [])}
        if not gold:                       # unanswerable question
            unans_ok += (not pred)
            wrong += bool(pred)            # asserting anything = confabulation
        elif not pred:
            hedges += 1
        elif gold & pred:
            hits += 1                      # Hits@1-style: any gold asserted
        else:
            wrong += 1
        b = rec["budget"]
        tokens += b["tokens"]; calls += b["llm_calls"]
        backtracks += len(rec.get("backtracks", []))
        v = rec.get("verifier_outcome")
        verifier[v] = verifier.get(v, 0) + 1
    return {"file": path, "n": n, "hits": hits, "hedges": hedges,
            "wrong": wrong, "unanswerable_ok": unans_ok,
            "mean_tokens": round(tokens / max(n, 1)),
            "mean_calls": round(calls / max(n, 1), 1),
            "total_backtracks": backtracks, "verifier": verifier}


if __name__ == "__main__":
    rows = [score_file(p) for p in sys.argv[1:]]
    cols = ["file", "n", "hits", "hedges", "wrong", "unanswerable_ok",
            "mean_tokens", "mean_calls", "total_backtracks", "verifier"]
    for r in rows:
        print("  ".join(f"{c}={r[c]}" for c in cols))
