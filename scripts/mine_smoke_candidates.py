"""Mine dev-set candidates from TRAIN splits, classified into exactly one of
five buckets (priority order): unanswerable_env > conjunction > cvt_heavy >
one_hop > two_hop. The sixth bucket (unanswerable_fake) is hand-written,
never mined. Output: scripts/smoke_candidates_v2.json
"""
import json, random, re

from datasets import load_dataset
from agr.runtime import get_driver

SAMPLE_PER_DATASET = 500

# Questions whose gold requires date/founding-year facts. Verified 2026-07-12:
# the graph contains NO date literals, so these are unanswerable-in-environment.
DATE_CONSTRAINT = re.compile(
    r"\b(in \d{4}|born (in|before|after) \d{4}|"
    r"(?:founded|established|opened) (prior to|before|after)|"
    r"founding date|"
    r"(before|after|since|until) \d{4}|\d{4} to \d{4})\b",
    re.IGNORECASE)


def classify_path(session, q_names, a_names):
    """Shortest q->a path in the live graph: (raw_hops, via_cvt) or None."""
    rec = session.run("""
        MATCH (a:Entity) WHERE a.name IN $qs
        MATCH (b:Entity) WHERE b.name IN $ans
        WITH a, b WHERE a <> b
        MATCH p = shortestPath((a)-[*..4]-(b))
        RETURN length(p) AS hops,
               any(n IN nodes(p) WHERE n.is_cvt) AS via_cvt
        ORDER BY hops LIMIT 1""",
        qs=q_names, ans=a_names).single()
    return (rec["hops"], rec["via_cvt"]) if rec else None


def bucket_of(question: str, n_topics: int, hops: int, via_cvt: bool):
    """Priority-ordered, mutually exclusive assignment. Returns None if the
    record fits no bucket we sample (e.g. 3+ hop plain paths)."""
    if DATE_CONSTRAINT.search(question):
        return "unanswerable_env"
    if n_topics >= 2:
        return "conjunction"
    if via_cvt:
        return "cvt_heavy"
    if hops == 1:
        return "one_hop"
    if hops == 2:
        return "two_hop"
    return None


BUCKETS = ["unanswerable_env", "conjunction", "cvt_heavy",
           "one_hop", "two_hop"]


def main():
    random.seed(42)
    driver = get_driver()

    buckets = {bucket: [] for bucket in BUCKETS}

    with driver.session() as session:
        for ds_name in ["webqsp", "cwq"]:
            path = f"../RoG-{ds_name}/data"
            ds = load_dataset("parquet",
                              data_files={"train": f"{path}/train-*.parquet"})
            rows = list(ds["train"])
            for example in random.sample(rows, min(SAMPLE_PER_DATASET, len(rows))):
                q_entity = [str(x).strip() for x in example["q_entity"] if str(x).strip()]
                a_entity = [str(x).strip() for x in example["a_entity"] if str(x).strip()]
                if not q_entity or not a_entity:
                    continue
                res = classify_path(session, q_entity, a_entity)
                if res is None:
                    continue          # gold unreachable within 4 hops: skip
                hops, via_cvt = res
                bucket = bucket_of(example["question"], len(q_entity), hops, via_cvt)
                if bucket is None:
                    continue
                buckets[bucket].append({
                    "qid": str(example.get("id", "")),
                    "dataset": ds_name,
                    "question": example["question"],
                    "gold_q_entities": q_entity,
                    "answers": a_entity,
                    "bucket": bucket,
                    "raw_hops": hops,
                    "via_cvt": via_cvt,
                })

    json.dump(buckets, open("data/smoke_candidates_v2.json", "w",
                            encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"{'bucket':<18} count   examples")
    for bucket in BUCKETS:
        print(f"{bucket:<18} {len(buckets[bucket]):>5}")
        for r in buckets[bucket][:3]:
            print(f"    [{r['dataset']}] {r['question']!r} -> "
                  f"{r['answers'][:2]} (hops={r['raw_hops']}, cvt={r['via_cvt']})")
    driver.close()


if __name__ == "__main__":
    main()
