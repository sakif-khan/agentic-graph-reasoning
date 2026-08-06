"""Flag questions where multiple independent systems converge on the
same non-gold answer, which makes the gold itself a candidate error.
Agreement between a parametric system and a graph-based one is stronger
evidence than agreement among graph systems alone, since those share a
knowledge source and can be wrong together."""
import json, re, unicodedata
from collections import defaultdict
from pathlib import Path

def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    return re.sub(r"[.,;:'\"()\[\]]", "", s)

def main():
    SYSTEMS = ["noretrieval", "vectorrag", "graphrag", "tog", "agr"]
    PARAMETRIC = {"noretrieval"}          # does not read the graph
    MIN_AGREE = 3
    DIR = Path("results/phase4")

    for ds in ("webqsp", "cwq"):
        per_q = defaultdict(dict)          # qid -> {system: [entities]}
        meta = {}
        for system in SYSTEMS:
            path = DIR / f"test_{ds}_{system}.jsonl"
            if not path.exists():
                print(f"MISSING: {path}")
                continue
            for line in open(path, encoding="utf-8"):
                r = json.loads(line)
                per_q[r["qid"]][system] = [norm(a) for a in
                                           r.get("answer_entities", [])]
                meta.setdefault(r["qid"], {"question": r["question"],
                                           "gold": r["gold"]})

        flagged = []
        for qid, by_system in per_q.items():
            gold = {norm(g) for g in meta[qid]["gold"]}
            votes = defaultdict(set)                    # entity -> {systems}
            for system, ents in by_system.items():
                for e in ents:
                    if e and e not in gold:
                        votes[e].add(system)
            for ent, systems in votes.items():
                if len(systems) >= MIN_AGREE:
                    agr_agrees = "agr" in systems
                    mixed = bool(systems & PARAMETRIC) and bool(systems - PARAMETRIC)
                    flagged.append({
                        "qid": qid,
                        "question": meta[qid]["question"],
                        "gold": meta[qid]["gold"],
                        "consensus_answer": ent,
                        "n_systems": len(systems),
                        "systems": sorted(systems),
                        "includes_agr": agr_agrees,
                        "mixed_evidence": mixed,   # parametric AND graph agree
                        "verdict": "",             # fill: gold_wrong / gold_ok / ambiguous
                        "note": "",
                    })

        flagged.sort(key=lambda f: (-f["mixed_evidence"], -f["n_systems"]))
        out = DIR / f"prepass_goldnoise_{ds}.json"
        json.dump(flagged, open(out, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)

        strong = sum(1 for f in flagged if f["mixed_evidence"])
        print(f"{ds}: {len(flagged)} consensus-vs-gold cases "
              f"({strong} with mixed parametric+graph evidence) -> {out}")
        for f in flagged[:10]:
            print(f'  [{f["qid"][:24]:<26}] {f["n_systems"]} systems say '
                  f'{f["consensus_answer"]!r} vs gold {f["gold"]} '
                  f'{"[MIXED]" if f["mixed_evidence"] else ""}')

if __name__ == "__main__":
    main()
