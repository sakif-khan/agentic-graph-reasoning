"""
Step 1.2: Union graph construction + answer coverage gate + CSV export.
"""

import csv, gzip, json, re
from collections import deque
from datasets import load_dataset

HOP_CAP = 4          # raw hops; covers 2 logical hops through CVT mediators
MID_RE = re.compile(r"^[mg]\.[0-9a-zA-Z_]+$")   # unnamed CVT/MID-style nodes

# ---------- interning tables ----------
ent_to_id, rel_to_id = {}, {}
entities, rels = [], []

def entity_id(name: str) -> int:
    i = ent_to_id.get(name)
    if i is None:
        i = len(entities); ent_to_id[name] = i; entities.append(name)
    return i

def rel_id(name: str) -> int:
    i = rel_to_id.get(name)
    if i is None:
        i = len(rels); rel_to_id[name] = i; rels.append(name)
    return i

# ---------- pass 1: union all triples ----------
triples = set()              # {(h_id, r_id, t_id)}
test_questions = []          # dicts for the coverage gate

# ---------- pass 1: union all triples ----------
for ds_name in ["webqsp", "cwq"]:
    path = f"../RoG-{ds_name}/data"
    ds = load_dataset(
        "parquet",
        data_files={
            "train":      f"{path}/train-*.parquet",
            "validation": f"{path}/validation-*.parquet",
            "test":       f"{path}/test-*.parquet",
        },
    )
    
    for split in ds:
        for ex in ds[split]:
            for triplet in ex["graph"]:
                if not triplet or len(triplet) != 3:
                    continue
                head, relation, tail = (str(x).strip() for x in triplet)
                if head and relation and tail:
                    triples.add((entity_id(head), rel_id(relation), entity_id(tail)))

            if split == "test":
                test_questions.append({
                    "dataset": ds_name,
                    "id": ex.get("id", ""),
                    "q_entity": [str(x).strip() for x in ex["q_entity"] if str(x).strip()],
                    "a_entity": [str(x).strip() for x in ex["a_entity"] if str(x).strip()],
                })
            
    print(f"{ds_name} done. cumulative unique triples: {len(triples):,}, "
          f"entities: {len(entities):,}")

# ---------- pass 2: undirected adjacency for reachability ----------
adj = [[] for _ in range(len(entities))]
for head, _, tail in triples:
    adj[head].append(tail)
    adj[tail].append(head)
adj = [list(set(neighbors)) for neighbors in adj]   # dedupe parallel edges

def reachable(sources, targets, max_depth):
    """BFS from all sources at once; True if any target seen within max_depth hops."""
    targets = set(targets)
    if targets & set(sources):
        return True
    seen = set(sources)
    dq = deque((s, 0) for s in sources)
    while dq:
        node, depth = dq.popleft()
        if depth == max_depth:
            continue
        for neighbor in adj[node]:
            if neighbor in targets:
                return True
            if neighbor not in seen:
                seen.add(neighbor)
                dq.append((neighbor, depth + 1))
    return False

# ---------- coverage gate ----------
stats = {}
per_question = []
for question in test_questions:
    dataset = question["dataset"]
    stat = stats.setdefault(dataset, {"n": 0, "all_exist": 0, "any_exist": 0,
                                      "any_reachable": 0, "no_topic": 0})
    stat["n"] += 1
    a_ids = [ent_to_id[a_entity] for a_entity in question["a_entity"] if a_entity in ent_to_id]
    q_ids = [ent_to_id[q_entity] for q_entity in question["q_entity"] if q_entity in ent_to_id]
    all_exist = bool(question["a_entity"]) and len(a_ids) == len(question["a_entity"])
    any_exist = bool(a_ids)
    if not q_ids:
        stat["no_topic"] += 1
    reach = bool(q_ids) and any_exist and reachable(q_ids, a_ids, HOP_CAP)
    stat["all_exist"] += all_exist
    stat["any_exist"] += any_exist
    stat["any_reachable"] += reach
    per_question.append({**question, "all_exist": all_exist,
                         "any_exist": any_exist, "reachable": reach})

for dataset, stat in stats.items():
    n = stat["n"]
    print(f"\n[{dataset}]  test questions: {n}")
    print(f"  all answers exist as nodes : {stat['all_exist']/n:.1%}")
    print(f"  >=1 answer exists          : {stat['any_exist']/n:.1%}")
    print(f"  >=1 answer reachable <= {HOP_CAP} hops (Hits@1 ceiling): "
          f"{stat['any_reachable']/n:.1%}")
    print(f"  questions with no topic entity in graph: {stat['no_topic']}")

with open("coverage_report.json", "w", encoding="utf-8") as f:
    json.dump({"stats": stats, "hop_cap": HOP_CAP,
               "per_question": per_question}, f, ensure_ascii=False, indent=1)

# ---------- CSV export for neo4j-admin import ----------
def sanitize(rel: str) -> str:              # Cypher-legal relationship type
    return re.sub(r"[^0-9a-zA-Z_]", "_", rel)

with gzip.open("nodes.csv.gz", "wt", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id:ID", "name", "is_cvt:boolean", ":LABEL"])
    for i, name in enumerate(entities):
        w.writerow([i, name, str(bool(MID_RE.match(name))).lower(), "Entity"])

with gzip.open("rels.csv.gz", "wt", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([":START_ID", ":END_ID", ":TYPE", "fb_name"])
    for h, r, t in triples:
        w.writerow([h, t, sanitize(rels[r]), rels[r]])

print(f"\nWrote nodes.csv.gz ({len(entities):,} nodes) and "
      f"rels.csv.gz ({len(triples):,} rels).")