"""Auto-verdict the mechanical gold-noise cases,
leaving only genuinely ambiguous ones for manual review.
Idempotent: rows that already have a verdict are left untouched."""
import json, re, unicodedata


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    return re.sub(r"[.,;:'\"()\[\]\-]", "", s)

def main():
    TYPE_WORDS = {"lawyer", "investor", "businessperson", "politician", "pilot",
                  "writer", "scientist", "actor", "singer", "author", "director",
                  "producer", "adventurer", "ethnographer", "cinematographer",
                  "executive officer", "musician", "artist", "athlete"}

    for ds in ("webqsp", "cwq"):
        path = f"results/phase4/prepass_goldnoise_{ds}.json"
        flags = json.load(open(path, encoding="utf-8"))

        for f in flags:
            if f.get("verdict"):
                continue
            cons = norm(f["consensus_answer"])
            qtext = norm(f["question"])            # same normalization both sides
            golds = [norm(g) for g in f["gold"]]
            has_mid = any(re.match(r"^[mg]\.", str(g).strip()) for g in f["gold"])

            if cons and cons in qtext:
                f["verdict"] = "gold_ok"
                f["note"] = "echo: consensus answer appears in question text"
                f["subtype"] = "echo_topic"
            elif len(f["gold"]) > 20 or has_mid:
                f["verdict"] = "gold_wrong"
                f["note"] = (f"malformed gold ({len(f['gold'])} entities, "
                             f"MID leakage={has_mid})")

        json.dump(flags, open(path, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)

        done = sum(1 for f in flags if f.get("verdict"))
        manual = [f for f in flags if not f.get("verdict")]
        mixed = sum(1 for f in manual if f.get("mixed_evidence"))
        print(f"{ds}: auto {done}/{len(flags)} "
              f"({len({f['qid'] for f in flags})} distinct questions); "
              f"manual {len(manual)} ({mixed} mixed-evidence, "
              f"{len(manual) - mixed} graph-only)")

if __name__ == "__main__":
    main()
