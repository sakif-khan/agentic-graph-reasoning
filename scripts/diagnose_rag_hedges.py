"""Among hedged questions, was gold in the retrieved sample?
High rate => implementation problem; low => paradigm limit."""
import json, unicodedata

def norm(s): return unicodedata.normalize("NFKC", s).strip().lower()


def main():
    paths = [
        "logs/test_webqsp_vectorrag.jsonl",
        "logs/test_cwq_vectorrag.jsonl",
        "logs/test_webqsp_graphrag.jsonl",
        "logs/test_cwq_graphrag.jsonl",
        "logs/test_webqsp_tog.jsonl",
        "logs/test_cwq_tog.jsonl",
        ]

    for path in paths:
        n_hedge = gold_in_sample = n_hit = n_assert = 0
        exhausted = 0
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            gold = [norm(g) for g in r["gold"]]
            pred = r.get("answer_entities", [])
            tr = r["trace"][0] if r["trace"] else {}
            sample = " | ".join(tr.get("facts_sample", [])).lower()
            if r["budget"]["exhausted"]:
                exhausted += 1
            if pred:
                n_assert += 1
            else:
                n_hedge += 1
                if any(g in sample for g in gold):
                    gold_in_sample += 1
        print(f"{path}: hedges={n_hedge}, gold-visible-in-top10-while-hedged="
              f"{gold_in_sample} ({gold_in_sample/max(n_hedge,1):.0%}), "
              f"exhausted={exhausted}")

    tog_paths = ["logs/test_webqsp_tog.jsonl", "logs/test_cwq_tog.jsonl"]

    for path in tog_paths:
        n = clip = 0
        for l in open(path, encoding="utf-8"):
            r = json.loads(l); n += 1
            clip += any(t.get("budget_exhausted") or t.get("degraded")
                        for t in r["trace"])
        print(f"{path}: {clip}/{n} budget-clipped")


if __name__ == "__main__":
    main()
