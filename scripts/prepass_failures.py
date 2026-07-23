"""surface-form near-miss + gold-noise flags over AGR's
main-matrix wrong answers, to focus manual reading."""
import json, re, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = re.sub(r"[.,;:'\"()\[\]]", "", s)
    return s

def tokens(s):
    return set(norm(s).split())

def near_miss(pred_set, gold_set):
    for p in pred_set:
        for g in gold_set:
            if not p or not g:
                continue
            pt, gt = tokens(p), tokens(g)
            if pt and gt and len(pt & gt) / len(pt | gt) >= 0.5:
                return True
    return False

def main():
    for ds in ("webqsp", "cwq"):
        path = Path(f"results/phase4/test_{ds}_agr.jsonl")
        recs = [json.loads(l) for l in open(path, encoding="utf-8")]

        wrongs, gold_votes = [], defaultdict(Counter)
        for r in recs:
            gold = {norm(g) for g in r["gold"]}
            pred = {norm(a) for a in r.get("answer_entities", [])}
            if pred and not (gold & pred):
                wrongs.append(r)
                for p in pred:
                    gold_votes[r["qid"]][p] += 1

        nm = sum(1 for r in wrongs
                if near_miss({norm(a) for a in r["answer_entities"]},
                            {norm(g) for g in r["gold"]}))
        print(f"{ds}: {len(wrongs)} wrongs total, {nm} ({nm/max(len(wrongs),1):.0%}) "
              f"flagged as surface-form near-misses")

        out = [{"qid": r["qid"], "question": r["question"],
                "gold": r["gold"], "pred": r["answer_entities"],
                "near_miss": near_miss({norm(a) for a in r["answer_entities"]},
                                       {norm(g) for g in r["gold"]})}
               for r in wrongs]
        json.dump(out, open(f"results/phase4/prepass_wrongs_{ds}.json", "w",
                            encoding="utf-8"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
