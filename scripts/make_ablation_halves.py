import json, random
from collections import defaultdict

def main():
    random.seed(42)
    for ds in ("webqsp", "cwq"):
        qs = json.load(open(f"results/phase4/test_{ds}.json", encoding="utf-8"))
        by = defaultdict(list)
        for q in qs:
            by[q["stratum"]].append(q)
        half = []
        for _, rows in sorted(by.items()):
            half.extend(random.sample(rows, len(rows) // 2))
        json.dump(half, open(f"data/test_{ds}_half.json", "w",
                             encoding="utf-8"), indent=1, ensure_ascii=False)
        print(ds, len(half))

if __name__ == "__main__":
    main()
