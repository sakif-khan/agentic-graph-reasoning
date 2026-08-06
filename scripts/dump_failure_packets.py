"""Stage D input generator.

Builds the manual-census reading packets for AGR's genuine failures, both
wrong answers and hedges. Excluded are the Stage C gold-noise and ambiguous
question IDs, the Stage B surface-form near-misses, and the Stage A no-planner
question IDs that have already been categorized.

Both datasets are read in full rather than sampled. Wrong answers and hedges
are kept as separate strata throughout, because they describe different failure
classes and pooling them into one histogram would conflate the two.

Re-runnable: labels already filled in an existing labels_{ds}.csv are carried
forward by question ID, so hand edits survive. New question IDs are added as
blank rows. Labels whose question ID has left the population, for example after
a case is adjudicated as gold noise, are written to labels_{ds}_dropped.csv
rather than dropped.

Outputs failures_{ds}.md, labels_{ds}.csv and sampling_manifest.json.
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


def render_packet(r, kind):
    """One failure packet as markdown, with no leading or trailing blank lines.

    Returned rather than written so that main can join packets with a single
    separator between them. Writing the separator after each packet instead
    would leave the file ending on a dangling rule and a blank line.
    """
    out = [f"## {r['qid']} ({kind})", "",
           f"**Q:** {r['question']}", "",
           f"**gold:** {r['gold']}", "",
           f"**answer:** {r['answer']}", "",
           f"**entities:** {r['answer_entities']}", ""]
    for t in r["trace"]:
        n = t.get("node")
        if n == "planner":
            out.append(f"- plan: {t['plan'].get('sub_objectives')}"
                       f"{'  [FALLBACK]' if t.get('fallback') else ''}"
                       f"{'  [ABLATED]' if t.get('ablated') else ''}")
        elif n == "explorer":
            out.append(f"- explored: {[e['rel'] for e in t['expanded']][:6]} "
                       f"(max_score {t.get('max_score')})")
        elif n == "backtracker":
            out.append(f"- backtrack: {t['reason']}")
        elif n == "evaluator":
            o = t.get("out", {})
            out.append(f"- eval: {o.get('decision')} "
                       f"resolved={o.get('resolved', [])[:4]}")
        elif n == "verifier":
            out.append(f"- verifier: {t.get('outcome')} "
                       f"unsupported={t.get('unsupported', [])[:2]}")
    return "\n".join(out).rstrip()


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

        packets = []
        with open(lbl_path, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            w.writerow(["qid", "kind", "category", "subtype", "note"])
            for kind, qids in (("wrong", s_wrong), ("hedge", s_hedge)):
                for qid in qids:
                    packets.append(render_packet(recs[qid], kind))
                    r = old.get(qid)
                    if r and r["kind"] != kind:
                        print(f"  WARNING {qid}: kind changed "
                              f"{r['kind']} -> {kind} (label carried anyway)")
                    w.writerow([qid, kind,
                                r["category"] if r else "",
                                r["subtype"] if r else "",
                                r["note"] if r else ""])

        with open(DIR / f"failures_{ds}.md", "w", encoding="utf-8") as f:
            f.write(f"# Stage D failure packets: {ds}\n\n"
                    f"Generated by `scripts/dump_failure_packets.py`. "
                    f"Labels are read into `labels_{ds}.csv`.\n\n")
            f.write("\n\n---\n\n".join(packets) + "\n")

    json.dump(manifest, open(DIR / "sampling_manifest.json", "w"), indent=1)
    print("wrote sampling_manifest.json")


if __name__ == "__main__":
    main()
