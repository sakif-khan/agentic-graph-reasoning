"""Stage D input generator.

Builds the manual-census reading packets for AGR's genuine failures
(wrongs + hedges), excluding: Stage-C gold-noise/ambiguous qids,
Stage-B surface-form near-misses, and Stage-A (noplanner census) qids
already categorized.

WebQSP: full census (all remaining failures).
CWQ: stratified sample (wrongs over-represented 2:1 by design; report
wrongs and hedges separately -- never pool into one histogram).

Outputs failures_{ds}.md + labels_{ds}.csv.
Refuses to overwrite a labels CSV that already contains filled categories.
"""
import csv, json, random, sys, unicodedata
from pathlib import Path

DIR = Path("results/phase4")
SEED = 42
CWQ_N_WRONG, CWQ_N_HEDGE = 40, 20


def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()


def guard_labels(path):
    """Abort if a labels file with human work in it already exists."""
    if not path.exists():
        return
    filled = sum(1 for r in csv.DictReader(open(path, encoding="utf-8"))
                 if (r.get("category") or "").strip())
    if filled:
        sys.exit(f"REFUSING to overwrite {path}: {filled} rows already "
                 f"labeled. Move or delete it manually to resample.")


def stage_a_qids():
    qids = set()
    for ds in ("webqsp", "cwq"):
        p = DIR / "ablations" / f"noplanner_discordant_{ds}.md"
        if p.exists():
            for line in open(p, encoding="utf-8"):
                if line.startswith("## "):
                    qids.add(line[3:].strip())
    return qids


def write_packet(f, r, kind):
    f.write(f"## {r['qid']} ({kind})\n\n**Q:** {r['question']}\n\n"
            f"**gold:** {r['gold']}\n\n**answer:** {r['answer']}\n\n"
            f"**entities:** {r['answer_entities']}\n\n")
    for t in r["trace"]:
        n = t.get("node")
        if n == "planner":
            f.write(f"- plan: {t['plan'].get('sub_objectives')}"
                    f"{'  [FALLBACK]' if t.get('fallback') else ''}"
                    f"{'  [ABLATED]' if t.get('ablated') else ''}\n")
        elif n == "explorer":
            f.write(f"- explored: {[e['rel'] for e in t['expanded']][:6]} "
                    f"(max_score {t.get('max_score')})\n")
        elif n == "backtracker":
            f.write(f"- backtrack: {t['reason']}\n")
        elif n == "evaluator":
            o = t.get("out", {})
            f.write(f"- eval: {o.get('decision')} "
                    f"resolved={o.get('resolved', [])[:4]}\n")
        elif n == "verifier":
            f.write(f"- verifier: {t.get('outcome')} "
                    f"unsupported={t.get('unsupported', [])[:2]}\n")
    f.write("\n---\n\n")


def main():
    random.seed(SEED)
    excl = json.load(open(DIR / "census_exclusions.json", encoding="utf-8"))
    skip_a = stage_a_qids()
    manifest = {}

    for ds in ("webqsp", "cwq"):
        lbl_path = DIR / f"labels_{ds}.csv"
        guard_labels(lbl_path)

        recs = {r["qid"]: r for r in
                (json.loads(l) for l in
                 open(DIR / f"test_{ds}_agr.jsonl", encoding="utf-8"))}
        near_miss = {r["qid"] for r in
                     json.load(open(DIR / f"prepass_wrongs_{ds}.json",
                                    encoding="utf-8")) if r["near_miss"]}
        skip = set(excl.get(ds, [])) | near_miss | skip_a

        wrongs, hedges = [], []
        for qid, r in recs.items():
            if qid in skip:
                continue
            gold = {norm(g) for g in r["gold"]}
            pred = {norm(a) for a in r.get("answer_entities", [])}
            if pred and not (gold & pred):
                wrongs.append(qid)
            elif not pred and gold:
                hedges.append(qid)

        if ds == "webqsp":                       # full census
            s_wrong, s_hedge = sorted(wrongs), sorted(hedges)
        else:                                    # stratified sample
            s_wrong = random.sample(wrongs, min(CWQ_N_WRONG, len(wrongs)))
            s_hedge = random.sample(hedges, min(CWQ_N_HEDGE, len(hedges)))

        manifest[ds] = {
            "population_wrong": len(wrongs), "population_hedge": len(hedges),
            "sampled_wrong": len(s_wrong), "sampled_hedge": len(s_hedge),
            "rate_wrong": round(len(s_wrong) / max(len(wrongs), 1), 3),
            "rate_hedge": round(len(s_hedge) / max(len(hedges), 1), 3),
            "n_skipped": len(skip & set(recs)),
            "mode": "full_census" if ds == "webqsp" else "stratified_sample",
            "seed": SEED,
        }
        print(f"{ds}: population {len(wrongs)}W/{len(hedges)}H "
              f"({manifest[ds]['n_skipped']} skipped) -> "
              f"{len(s_wrong)}W+{len(s_hedge)}H "
              f"[{manifest[ds]['mode']}; rates "
              f"W={manifest[ds]['rate_wrong']:.0%} "
              f"H={manifest[ds]['rate_hedge']:.0%}]")

        with open(DIR / f"failures_{ds}.md", "w", encoding="utf-8") as f, \
             open(lbl_path, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(["qid", "kind", "category", "subtype", "note"])
            for qid in s_wrong:
                write_packet(f, recs[qid], "wrong")
                w.writerow([qid, "wrong", "", "", ""])
            for qid in s_hedge:
                write_packet(f, recs[qid], "hedge")
                w.writerow([qid, "hedge", "", "", ""])

    json.dump(manifest, open(DIR / "sampling_manifest.json", "w"), indent=1)
    print("wrote sampling_manifest.json")


if __name__ == "__main__":
    main()
