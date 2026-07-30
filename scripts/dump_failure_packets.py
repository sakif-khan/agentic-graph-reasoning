"""Stage D input generator.

Builds the manual-census reading packets for AGR's genuine failures
(wrongs + hedges), excluding: Stage-C gold-noise/ambiguous qids,
Stage-B surface-form near-misses, and Stage-A (noplanner census) qids
already categorized.

Full census for BOTH datasets (no sampling; supersedes the earlier CWQ
stratified sample). Wrongs and hedges remain separate strata -- never
pool them into one histogram.

Idempotent: filled labels in an existing labels_{ds}.csv are carried
forward by qid. New qids get blank rows to read; labels whose qid left
the population (e.g. newly adjudicated gold noise) are saved to
labels_{ds}_dropped.csv, never silently discarded.

Outputs failures_{ds}.md + labels_{ds}.csv + sampling_manifest.json.
"""
import csv, json, unicodedata
from pathlib import Path

DIR = Path("results/phase4")


def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()


def load_labels(path):
    """qid -> previously filled label row (category is non-empty)."""
    if not path.exists():
        return {}
    return {r["qid"]: r for r in csv.DictReader(open(path, encoding="utf-8"))
            if (r.get("category") or "").strip()}


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
    excl = json.load(open(DIR / "census_exclusions.json", encoding="utf-8"))
    skip_a = stage_a_qids()
    manifest = {}

    for ds in ("webqsp", "cwq"):
        lbl_path = DIR / f"labels_{ds}.csv"
        old = load_labels(lbl_path)

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

        s_wrong, s_hedge = sorted(wrongs), sorted(hedges)    # full census
        census = s_wrong + s_hedge

        carried = [q for q in census if q in old]
        to_read = [q for q in census if q not in old]
        dropped = sorted(set(old) - set(census))

        manifest[ds] = {
            "population_wrong": len(wrongs), "population_hedge": len(hedges),
            "n_skipped": len(skip & set(recs)),
            "mode": "full_census",
            "labels_carried": len(carried), "labels_to_read": len(to_read),
            "labels_dropped": len(dropped),
        }
        print(f"{ds}: census {len(wrongs)}W/{len(hedges)}H "
              f"({manifest[ds]['n_skipped']} skipped) "
              f"[labels: {len(carried)} carried, {len(to_read)} to read, "
              f"{len(dropped)} dropped]")

        if dropped:
            drop_path = DIR / f"labels_{ds}_dropped.csv"
            with open(drop_path, "w", newline="", encoding="utf-8") as df:
                w = csv.writer(df)
                w.writerow(["qid", "kind", "category", "subtype", "note"])
                for q in dropped:
                    r = old[q]
                    w.writerow([r["qid"], r["kind"], r["category"],
                                r["subtype"], r["note"]])
            print(f"  dropped (left the population; saved to {drop_path.name}):")
            for q in dropped:
                print(f"    {q}  [{old[q]['category']}]")

        with open(DIR / f"failures_{ds}.md", "w", encoding="utf-8") as f, \
             open(lbl_path, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(["qid", "kind", "category", "subtype", "note"])
            for kind, qids in (("wrong", s_wrong), ("hedge", s_hedge)):
                for qid in qids:
                    write_packet(f, recs[qid], kind)
                    r = old.get(qid)
                    if r and r["kind"] != kind:
                        print(f"  WARNING {qid}: kind changed "
                              f"{r['kind']} -> {kind} (label carried anyway)")
                    w.writerow([qid, kind,
                                r["category"] if r else "",
                                r["subtype"] if r else "",
                                r["note"] if r else ""])

    json.dump(manifest, open(DIR / "sampling_manifest.json", "w"), indent=1)
    print("wrote sampling_manifest.json")


if __name__ == "__main__":
    main()
