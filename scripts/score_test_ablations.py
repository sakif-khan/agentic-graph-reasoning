"""Phase 4 metrics over RunLogger JSONLs.
Usage: python scripts/score_test.py results/phase4/test_webqsp_*.jsonl results/phase4/test_cwq_*.jsonl
(excludes *_tools.jsonl automatically)"""
import json, random, unicodedata
from collections import defaultdict

random.seed(42)
N_BOOT = 10_000

def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()

def prf(gold, pred):
    g, p = set(map(norm, gold)), set(map(norm, pred))
    if not p:
        return 0.0, 0.0, 0.0
    tp = len(g & p)
    prec = tp / len(p)
    rec = tp / len(g) if g else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1

def load(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        pred = r.get("answer_entities", [])
        p, rc, f1 = prf(r["gold"], pred)
        g = set(map(norm, r["gold"]))
        rows.append({
            "qid": r["qid"],
            "hit": bool(g & set(map(norm, pred))),
            "hedge": not pred,
            "precision": p, "recall": rc, "f1": f1,
            "tokens": r["budget"]["tokens"],
            "calls": r["budget"]["llm_calls"],
            "warm": r["budget"].get("cache_hits", 0) >= r["budget"]["llm_calls"] > 0,
            "secs": r["wall_seconds"],
            "verifier": r.get("verifier_outcome"),
        })
    return rows

def stratum_map(test_file):
    return {q["qid"]: q["stratum"]
            for q in json.load(open(test_file, encoding="utf-8"))}

def boot_ci(vals, stat=lambda v: sum(v) / len(v)):
    pts = []
    for _ in range(N_BOOT):
        pts.append(stat([vals[random.randrange(len(vals))]
                         for _ in range(len(vals))]))
    pts.sort()
    return pts[int(0.025 * N_BOOT)], pts[int(0.975 * N_BOOT)]

def mcnemar(a_rows, b_rows):
    """Exact binomial McNemar on per-question hit; rows keyed by qid."""
    b_by = {r["qid"]: r for r in b_rows}
    b01 = b10 = 0
    for ra in a_rows:
        rb = b_by.get(ra["qid"])
        if not rb:
            continue
        if ra["hit"] and not rb["hit"]:
            b10 += 1
        elif rb["hit"] and not ra["hit"]:
            b01 += 1
    n = b01 + b10
    if n == 0:
        return 1.0, b10, b01
    from math import comb
    k = min(b01, b10)
    p = sum(comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(p, 1.0), b10, b01

def main():
    files = [
        "logs/test_webqsp_half_abl_full.jsonl",
        "logs/test_cwq_half_abl_full.jsonl",
        "logs/test_webqsp_half_abl_noplanner.jsonl",
        "logs/test_cwq_half_abl_noplanner.jsonl",
        "logs/test_webqsp_half_abl_nobacktrack.jsonl",
        "logs/test_cwq_half_abl_nobacktrack.jsonl",
        "logs/test_webqsp_half_abl_noverifier.jsonl",
        "logs/test_cwq_half_abl_noverifier.jsonl",
        "logs/test_webqsp_half_abl_embonly.jsonl",
        "logs/test_cwq_half_abl_embonly.jsonl",
    ]
    strata = {"webqsp": stratum_map("results/phase4/test_webqsp_half.json"),
              "cwq": stratum_map("results/phase4/test_cwq_half.json")}
    runs = {}                                   # (dataset, system) -> rows
    for p in files:
        parts = p.replace("\\", "/").split("/")[-1].replace(".jsonl", "").split("_")
        dataset, system = parts[1], "_".join(parts[2:])
        runs[(dataset, system)] = load(p)

    print(f"{'dataset':<8}{'system':<21}{'Hits@1':<21}{'F1':<21}"
          f"{'P':<7}{'R':<7}{'hedge%':<8}{'tok':<7}{'calls':<7}{'secs*':<7}")
    for (ds, sysname), rows in runs.items():
        n = len(rows)
        hits = [r["hit"] for r in rows]
        f1s = [r["f1"] for r in rows]
        lo, hi = boot_ci([1.0 if h else 0.0 for h in hits])
        flo, fhi = boot_ci(f1s)
        cold = [r["secs"] for r in rows if not r["warm"]]
        print(f"{ds:<8}{sysname:<21}"
              f"{sum(hits)/n:.3f} [{lo:.3f},{hi:.3f}]  "
              f"{sum(f1s)/n:.3f} [{flo:.3f},{fhi:.3f}]  "
              f"{sum(r['precision'] for r in rows)/n:<7.3f}"
              f"{sum(r['recall'] for r in rows)/n:<7.3f}"
              f"{sum(r['hedge'] for r in rows)/n:<8.1%}"
              f"{sum(r['tokens'] for r in rows)//n:<7}"
              f"{sum(r['calls'] for r in rows)/n:<7.1f}"
              f"{(sum(cold)/len(cold)) if cold else float('nan'):<7.1f}")

    # per-stratum Hits@1 and F1
    print("\nPer-stratum Hits@1 / F1:")
    for (ds, sysname), rows in runs.items():
        by = defaultdict(list)
        for r in rows:
            by[strata[ds].get(r["qid"], "?")].append(r)
        cells = "  ".join(
            f"{st}:{sum(x['hit'] for x in v)/len(v):.2f}/{sum(x['f1'] for x in v)/len(v):.2f}(n={len(v)})".ljust(22)
            for st, v in sorted(by.items()))
        print(f"  {ds:<8}{sysname:<21}{cells}")

    # McNemar: AGR vs each baseline, per dataset
    print("\nMcNemar (AGR vs baseline, per-question hit):")
    for ds in ("webqsp", "cwq"):
        agr_abl_full = runs.get((ds, "half_abl_full"))
        for (d2, sysname), rows in runs.items():
            if d2 != ds or sysname == "half_abl_full":
                continue
            p, agr_only, base_only = mcnemar(agr_abl_full, rows)

            sys_string = f"{sysname}-only-correct={base_only:<4} "
            print(f"  {ds:<8}half_abl_full vs {sysname:<21} "
                  f"half_abl_full-only-correct={agr_only:<4} "
                  f"{sys_string:<39} "
                  f"p={p:.2e}")
                  
if __name__ == "__main__":
    main()
