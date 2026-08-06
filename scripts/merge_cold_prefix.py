"""Restore cold-run records into the canonical AGR WebQSP file,
with strict verification. Run ONCE, then archive inputs.

SPENT: already run; the .bak input was consumed and removed, and the merged
output was promoted to results/phase4/test_webqsp_agr.jsonl. Kept for the
record -- the absent paths below are expected, not breakage.
"""
import copy, json, sys

COLD, WARM, OUT = ("results/phase4/test_webqsp_agr.jsonl.bak",
                   "results/phase4/test_webqsp_agr.jsonl",
                   "results/phase4/test_webqsp_agr_merged.jsonl")

def load(p):
    return {json.loads(l)["qid"]: json.loads(l)
            for l in open(p, encoding="utf-8")}

def normalized(rec):
    r = copy.deepcopy(rec)
    r["wall_seconds"] = None
    r["budget"]["seconds"] = None
    r["budget"]["cache_hits"] = None
    for t in r["trace"]:
        if "budget" in t:                       # answerer's embedded snapshot
            t["budget"]["seconds"] = None
            t["budget"]["cache_hits"] = None
    return r


def main():
    cold, warm = load(COLD), load(WARM)
    overlap = set(cold) & set(warm)
    print(f"cold={len(cold)} warm={len(warm)} overlap={len(overlap)}")

    for qid in sorted(overlap):
        for k in ("git", "budget_hash", "backbone", "run_config"):
            assert cold[qid][k] == warm[qid][k], f"{qid}: {k} differs -- ABORT"
        if normalized(cold[qid]) != normalized(warm[qid]):
            sys.exit(f"{qid}: records differ beyond timing fields -- ABORT, "
                     "keep the sidecar-filter approach instead")

    order = [json.loads(l)["qid"] for l in open(WARM, encoding="utf-8")]
    with open(OUT, "w", encoding="utf-8") as f:
        for qid in order:
            rec = cold[qid] if qid in overlap else warm[qid]
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"merged {len(order)} records ({len(overlap)} from cold run) -> {OUT}")


if __name__ == "__main__":
    main()
