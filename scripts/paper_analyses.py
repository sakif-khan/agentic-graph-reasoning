"""Derived analyses for the journal paper, computed from committed records.

Nothing here runs a system or reads the database. Every function reads the
run records, tool logs and label files that the thesis committed, and the
RoG distribution's per-question subgraphs where they are checked out
beside the repository. The thesis and its numbers file are the source of
truth for every measurement; this module only reads them a further time.
scripts/check_paper_numbers.py imports it and pins each figure to the
sentence that quotes it.

Run directly to print everything:  python scripts/paper_analyses.py

  gold_path_discards   the agentic baseline's 40-relation cut, read against
                       the relation that continues a shortest path to a gold
                       answer in the question's published subgraph
  gold_in_hand         whether a gold entity was among the entities the
                       baseline retained after pruning, by outcome
  ablation_bootstrap   paired bootstrap intervals for every ablation delta,
                       and the union of the discordant sets
  dev_sweep_hits       the development-set alpha sweep the thesis tabulates
"""
import csv
import glob
import json
import random
import sys
import unicodedata
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P4 = ROOT / "results" / "phase4"
P3 = ROOT / "results" / "phase3"
ROG = ROOT.parent  # RoG-webqsp/ and RoG-cwq/ sit beside the repository

TOG_RELATION_CAP, TOG_NEIGHBOR_CAP = 40, 20   # agr/baselines/tog.py
N_BOOT = 10_000                               # scripts/score_test.py


def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()


def records(name):
    return [json.loads(l) for l in open(P4 / name, encoding="utf-8") if l.strip()]


def hit(rec):
    return bool({norm(g) for g in rec["gold"]}
                & {norm(a) for a in rec.get("answer_entities", [])})


def prf(gold, pred):
    """Identical to scripts/score_test.py."""
    g, p = set(map(norm, gold)), set(map(norm, pred))
    if not p:
        return 0.0, 0.0, 0.0
    tp = len(g & p)
    prec = tp / len(p)
    rec = tp / len(g) if g else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def clipped(rec):
    return any(t.get("budget_exhausted") for t in rec["trace"])


def tool_log(ds, system):
    by_q = defaultdict(list)
    for l in open(P4 / f"test_{ds}_{system}_tools.jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            by_q[r["qid"]].append(r)
    return by_q


# --------------------------------------------------------------------------
def _is_mediator(name):
    return name.startswith("m.") or name.startswith("g.")


def _subgraphs(ds):
    """qid -> (q_entity names, a_entity names, edge list) from the RoG parquet.

    Returns None when the distribution is not checked out beside the repo."""
    import pyarrow.parquet as pq
    files = glob.glob(str(ROG / f"RoG-{ds}" / "data" / "test-*.parquet"))
    if not files:
        return None
    out = {}
    for f in files:
        for row in pq.read_table(f, columns=["id", "q_entity", "a_entity", "graph"]).to_pylist():
            out[row["id"]] = (row["q_entity"], row["a_entity"], row["graph"])
    return out


def _qid_to_rog_id(qid):
    # WebQSP: WebQTest-431 ; CWQ: WebQTrn-1557_25aa6673...  -> RoG id is the
    # full string for both distributions.
    return qid


def _next_hop_relations(q_names, a_names, edges):
    """For every node on a shortest undirected path from a topic entity to a
    gold answer, the (relation, direction) rows that continue such a path
    from that node. Mediator nodes are ordinary nodes here; a path through
    one costs two edges, as it does in the tool layer's neighbour query."""
    adj = defaultdict(list)          # name -> [(neighbour, rel, dir)]
    for h, r, t in edges:
        adj[h].append((t, r, "out"))
        adj[t].append((h, r, "in"))
    starts = [q for q in q_names if q in adj]
    golds = {a for a in a_names if a in adj}
    if not starts or not golds:
        return {}
    dist = {s: 0 for s in starts}
    dq = deque(starts)
    while dq:
        u = dq.popleft()
        for v, _, _ in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    reached = [g for g in golds if g in dist]
    if not reached:
        return {}
    dmin = min(dist[g] for g in reached)
    targets = {g for g in reached if dist[g] == dmin}
    # walk back from the targets along strictly decreasing distance
    on_path = set(targets)
    nxt = defaultdict(set)           # node -> {(rel, dir)} continuing a path
    frontier = set(targets)
    while frontier:
        new = set()
        for v in frontier:
            for u, r, d in adj[v]:   # edge u--v seen from v; from u it is the reverse dir
                if u in dist and dist[u] == dist[v] - 1:
                    nxt[u].add((r, "out" if d == "in" else "in"))
                    if u not in on_path:
                        on_path.add(u)
                        new.add(u)
        frontier = new
    return nxt


def gold_path_discards(ds):
    """The baseline's 40-relation cut against the gold path.

    Unit: a distinct (question, anchor) expansion the baseline made, where
    the returned relation list exceeded the cut (an anchor the baseline
    re-expanded in the same question counts once; its list is identical).
    For the expansions whose anchor lies on a shortest path from a topic
    entity to a gold answer in the question's published subgraph: was the
    (relation, direction) that continues that path among the rows offered
    to the pruning prompt, or among the rows discarded? Per question, the
    outcome of the baseline's run is crossed with whether any such discard
    occurred."""
    subs = _subgraphs(ds)
    if subs is None:
        return None
    logs = tool_log(ds, "tog")
    recs = {r["qid"]: r for r in records(f"test_{ds}_tog.jsonl")}
    # data/id2name.json is the environment's node table (build_id2name.py),
    # so every anchor the baseline expanded resolves to its name.
    id2name = json.load(open(ROOT / "data" / "id2name.json", encoding="utf-8"))
    out = {"expansions_over_cap": 0, "anchor_on_path": 0, "continuing_offered": 0,
           "continuing_discarded": 0, "continuing_absent": 0,
           "questions_over_cap": 0, "questions_with_discard": 0,
           "discard_qids": set(), "discard_by_outcome": {}}
    for qid, rows in logs.items():
        sub = subs.get(_qid_to_rog_id(qid))
        if sub is None:
            continue
        nxt = _next_hop_relations(*sub)
        seen, over, discard = set(), False, False
        for r in rows:
            if r["tool"] != "get_relations":
                continue
            key = r["args"]["id"]
            if key in seen:
                continue
            seen.add(key)
            if len(r["result"]) <= TOG_RELATION_CAP:
                continue
            out["expansions_over_cap"] += 1
            over = True
            name = id2name.get(key)
            if name is None or name not in nxt:
                continue
            out["anchor_on_path"] += 1
            offered = {(x["rel"], x["dir"]) for x in r["result"][:TOG_RELATION_CAP]}
            discarded = {(x["rel"], x["dir"]) for x in r["result"][TOG_RELATION_CAP:]}
            want = nxt[name]
            if want & offered:
                out["continuing_offered"] += 1
            elif want & discarded:
                out["continuing_discarded"] += 1
                discard = True
            else:
                out["continuing_absent"] += 1
        out["questions_over_cap"] += over
        out["questions_with_discard"] += discard
        if discard:
            out["discard_qids"].add(qid)
            rec = recs[qid]
            k = ("clipped" if clipped(rec) else "finished", "hit" if hit(rec) else "miss")
            out["discard_by_outcome"][k] = out["discard_by_outcome"].get(k, 0) + 1
    # the budget split read a second time: (finished|clipped, discard|not)
    # -> (n, baseline Hits@1, AGR Hits@1), plus the hit margins on the
    # discard questions and on the rest
    agrs = {r["qid"]: r for r in records(f"test_{ds}_agr.jsonl")}
    cells, margin = {}, {True: [0, 0, 0], False: [0, 0, 0]}
    for qid, rec in recs.items():
        d = qid in out["discard_qids"]
        k = ("clipped" if clipped(rec) else "finished", d)
        cells.setdefault(k, [0, 0, 0])
        cells[k][0] += 1
        cells[k][1] += hit(rec)
        cells[k][2] += hit(agrs[qid])
        margin[d][0] += 1
        margin[d][1] += hit(rec)
        margin[d][2] += hit(agrs[qid])
    out["split"] = {k: (v[0], v[1] / v[0], v[2] / v[0]) for k, v in cells.items()}
    out["margin_discard"] = tuple(margin[True])      # n, baseline hits, AGR hits
    out["margin_rest"] = tuple(margin[False])
    return out


# --------------------------------------------------------------------------
def gold_in_hand(ds):
    """Was a gold entity among the entities the baseline RETAINED after
    pruning, by outcome? Read from the record's trace, which names the
    first ten retained entities per depth, so this is a lower bound on
    retention. The tool log keeps only the count of neighbours returned,
    not their names, so what the pruning prompt was SHOWN is not
    recoverable."""
    out = {}
    for r in records(f"test_{ds}_tog.jsonl"):
        gold = {norm(g) for g in r["gold"]}
        kept = {norm(n) for t in r["trace"] for n in t.get("frontier", [])}
        key = ("clipped" if clipped(r) else "finished",
               "hit" if hit(r) else ("hedge" if not r["answer_entities"] else "wrong"))
        out.setdefault(key, [0, 0])
        out[key][0] += 1
        out[key][1] += bool(gold & kept)
    return out


# --------------------------------------------------------------------------
def ablation_bootstrap(ds, conditions=("noplanner", "nobacktrack", "noverifier", "embonly")):
    """Paired bootstrap 95% interval on each ablation's mean F1 delta, and
    the union of the four discordant hit sets."""
    ref = {r["qid"]: r for r in records(f"ablations/test_{ds}_half_abl_full.jsonl")}
    qids = sorted(ref)
    out = {"n": len(qids)}
    union = set()
    for cond in conditions:
        cur = {r["qid"]: r for r in records(f"ablations/test_{ds}_half_abl_{cond}.jsonl")}
        d = [prf(cur[q]["gold"], cur[q]["answer_entities"])[2]
             - prf(ref[q]["gold"], ref[q]["answer_entities"])[2] for q in qids]
        random.seed(42)
        pts = sorted(sum(d[random.randrange(len(d))] for _ in range(len(d))) / len(d)
                     for _ in range(N_BOOT))
        out[cond] = {"delta": sum(d) / len(d),
                     "ci95": (pts[int(0.025 * N_BOOT)], pts[int(0.975 * N_BOOT)])}
        union |= {q for q in qids if hit(cur[q]) != hit(ref[q])}
    out["discordant_union"] = len(union)
    return out


# --------------------------------------------------------------------------
def dev_sweep_hits():
    """Hits of 80 at tau = 0.20 for each alpha, from the phase-3 score log
    the thesis's sweep table was built from."""
    out = {}
    for row in csv.DictReader(open(P3 / "score_run.csv", encoding="utf-8")):
        name = Path(row["file"].replace("\\", "/")).name
        if name.startswith("dev80_a") and name.endswith("_t0.2.jsonl"):
            alpha = float(name[len("dev80_a"):name.index("_t")])
            out[alpha] = int(row["hits"])
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for ds in ("webqsp", "cwq"):
        print(f"== {ds}: gold-path discards ==")
        g = gold_path_discards(ds)
        g["discard_qids"] = len(g["discard_qids"])
        print(" ", g)
        print(f"== {ds}: gold in hand ==")
        for k, v in sorted(gold_in_hand(ds).items()):
            print(f"  {k}: {v[1]}/{v[0]}")
        print(f"== {ds}: ablation bootstrap ==")
        print(" ", ablation_bootstrap(ds))
    print("== dev sweep hits at tau=0.20 ==", dev_sweep_hits())
