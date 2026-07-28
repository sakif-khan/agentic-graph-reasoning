import json, unicodedata

def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()

def main():
    excl = json.load(open("results/phase4/census_exclusions.json", encoding="utf-8"))
    for ds in ("webqsp", "cwq"):
        n = 0
        for line in open(f"results/phase4/test_{ds}_agr.jsonl", encoding="utf-8"):
            r = json.loads(line)
            if r["qid"] not in excl[ds]:
                continue
            gold = {norm(g) for g in r["gold"]}
            pred = {norm(a) for a in r.get("answer_entities", [])}
            if not pred or not (gold & pred):      # hedge or wrong
                n += 1
        print(f"{ds}: {n} of {len(excl[ds])} excluded questions were AGR failures")

if __name__ == "__main__":
    main()
