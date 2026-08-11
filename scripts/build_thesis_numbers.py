"""Stage F: collect every number the thesis reports into a single file.

Parses the scoring, groundedness and census artifacts and writes
results/phase4/thesis_numbers.json. Each block records the path it was parsed
from, so a figure quoted in the prose can be traced back to the artifact that
produced it, and a rerun that changes a value identifies the claims affected.

The thesis quotes this file rather than transcribing numbers from the logs.

Usage: python scripts/build_thesis_numbers.py
"""
import csv, inspect, json, re, statistics, unicodedata
from pathlib import Path

from agr.baselines.tog import MAX_NEIGHBORS, MAX_RELATIONS
from agr.baselines.graphrag import StaticGraphRAG
from agr.kg_tools import KGTools

P4 = Path("results/phase4")
OUT = P4 / "thesis_numbers.json"


def _default(cls, param):
    """A constructor default, read from the class rather than restated here.

    The caps below are properties of the systems, not of this script, and the
    thesis reports how often each one binds. Restating them made a config change
    a silent edit to the thesis: the numbers would still regenerate, still agree
    with each other, and still be wrong. Importing costs nothing -- none of these
    modules touches the database at import time -- and it means the caps cannot
    disagree with the code that applied them.
    """
    d = inspect.signature(cls.__init__).parameters[param].default
    assert d is not inspect.Parameter.empty, f"{cls.__name__}.{param} has no default"
    return d


# GraphRAG's per-topic fanout cap. The degree blocks below split entities on it,
# so it is the same literal the baseline applied, not a number that matches today.
GRAPHRAG_FANOUT_CAP = _default(StaticGraphRAG, "fanout_cap")

# dataset system  H [lo,hi]  F1 [lo,hi]  P  R  hedge%  tok  calls  secs
ROW = re.compile(
    r"^(webqsp|cwq)\s+(\S+)\s+"
    r"([\d.]+)\s+\[([\d.]+),([\d.]+)\]\s+"
    r"([\d.]+)\s+\[([\d.]+),([\d.]+)\]\s+"
    r"([\d.]+)\s+([\d.]+)\s+([\d.]+)%\s+(\d+)\s+([\d.]+)\s+(\S+)$")

STRATUM = re.compile(r"(h1|h2|h3plus|unreachable):([\d.]+)/([\d.]+)\(n=(\d+)\)")

MCNEMAR = re.compile(
    r"^(webqsp|cwq)\s+(\S+)\s+vs\s+(\S+)\s+"
    r"\S*-only-correct=(\d+)\s+\S*-only-correct=(\d+)\s+p=(\S+)$")

TIER1 = re.compile(
    r"^(test_\S+)\s+(\d+)\s+(\d+)\s+([\d.]+)%\s+(\d+)\s+(\d+)\s+([\d.]+)%$")

TIER2 = re.compile(r"^(test_\S+)\s+(\d+)/(\d+)\s+=\s+([\d.]+)%$")

HIST = re.compile(r"^\s{4}(\w+)\s+(\d+)\s+\((\d+)%\)$")


HOPS = ("h1", "h2", "h3plus")


def hop_trends(strata):
    """The shape of each system's accuracy curve across the hop strata.

    The abstract, the conclusion and two places in the results chapter all make
    the same claim about these curves -- that AGR is the only system that gets
    better as the required chain gets longer. The claim is about the shape of
    five curves, but it was written as prose beside a table of points, and the
    unqualified form of it ("every other system decays") is not what the points
    say: the agentic baseline falls and then partially recovers, so it does not
    decay monotonically even though it does end below where it started.

    Both readings are derived here so a sentence can quote the one it means.
    `monotone_rising` and `monotone_falling` are strict about the middle
    stratum; `ends_below_h1` ignores the middle and asks only about the two
    ends. The unreachable stratum is excluded throughout -- it has no hop count,
    so it is not a point on this curve.
    """
    out = {}
    for key, s in strata.items():
        ds, sysname = key.split("/")
        h = [s[k]["hits_at_1"] for k in HOPS]
        rising = all(b >= a for a, b in zip(h, h[1:])) and h[-1] > h[0]
        falling = all(b <= a for a, b in zip(h, h[1:])) and h[-1] < h[0]
        out.setdefault(ds, {})[sysname] = {
            "hits_at_1": h,
            "f1": [s[k]["f1"] for k in HOPS],
            "net_hits_at_1": round(h[-1] - h[0], 2),
            "monotone_rising": rising,
            "monotone_falling": falling,
            "ends_below_h1": h[-1] < h[0],
        }
    rollups = {"_systems_monotone_rising": "monotone_rising",
               "_systems_monotone_falling": "monotone_falling",
               "_systems_ending_below_h1": "ends_below_h1"}
    for systems in out.values():
        systems.update({name: sorted(k for k, v in systems.items() if v[flag])
                        for name, flag in rollups.items()})
    return out


def parse_scores(path):
    """Main table, per-stratum breakdown, and McNemar block from a score log."""
    rows, strata, mcnemar = {}, {}, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line.strip())
        if m:
            ds, sys_ = m.group(1), m.group(2)
            secs = m.group(14)
            rows[f"{ds}/{sys_}"] = {
                "hits_at_1": float(m.group(3)),
                "hits_at_1_ci95": [float(m.group(4)), float(m.group(5))],
                "f1": float(m.group(6)),
                "f1_ci95": [float(m.group(7)), float(m.group(8))],
                "precision": float(m.group(9)),
                "recall": float(m.group(10)),
                "hedge_pct": float(m.group(11)),
                "mean_tokens": int(m.group(12)),
                "mean_calls": float(m.group(13)),
                "mean_seconds_cold_cache": None if secs == "nan" else float(secs),
            }
            continue
        m = MCNEMAR.match(line.strip())
        if m:
            mcnemar.append({
                "dataset": m.group(1), "system_a": m.group(2),
                "system_b": m.group(3), "a_only_correct": int(m.group(4)),
                "b_only_correct": int(m.group(5)), "p": float(m.group(6)),
            })
            continue
        cells = STRATUM.findall(line)
        if cells:
            head = line.strip().split()[:2]
            if len(head) == 2:
                strata[f"{head[0]}/{head[1]}"] = {
                    s: {"hits_at_1": float(h), "f1": float(f), "n": int(n)}
                    for s, h, f, n in cells}
    return rows, strata, mcnemar


def parse_tier1(path):
    """Tier-1 rates, plus whether the log was written by the corrected query.

    scripts/groundedness.py stamps its semantics into the log. A log without the
    stamp came from the version whose `WITH t, b LIMIT 1` collapsed a question's
    topic set to one arbitrary node, testing something stricter than Sec. 7.5.3
    defines. That inflates baseline ungroundedness and cannot deflate it, so the
    0.0% results stand either way -- but the baseline rates would be quoted from
    a measurement the text does not describe, so the artifact says so instead of
    letting the number pass as though it matched.
    """
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    if "tier1-semantics: any-topic-entity" not in text:
        out["_STALE"] = (
            "This log predates the fix to scripts/groundedness.py and was "
            "produced by a query that collapsed each question's topic set to "
            "one arbitrary node, a stricter test than Sec. 7.5.3 defines. When "
            "that fix was first applied the rerun flipped none of the 6,327 "
            "verdicts in the sidecars, so an unstamped log most likely still "
            "holds the right numbers -- but 'most likely' is not the standard "
            "this file exists to meet. Rerun scripts/groundedness.py against a "
            "live database.")
    for line in text.splitlines():
        m = TIER1.match(line.strip())
        if m:
            out[m.group(1)] = {
                "entities_asserted": int(m.group(2)),
                "entities_ungrounded": int(m.group(3)),
                "entity_ungrounded_pct": float(m.group(4)),
                "questions_answered": int(m.group(5)),
                "questions_any_ungrounded": int(m.group(6)),
                "question_ungrounded_pct": float(m.group(7)),
            }
    # Both-dataset totals per system. These exist because the abstract and the
    # conclusion quoted AGR's both-dataset assertion count against the
    # no-retrieval rate on WebQSP alone -- two different scopes in one sentence.
    # Quoting a computed pair from here makes that mistake harder to repeat.
    for sysname in ("noretrieval", "vectorrag", "graphrag", "tog", "agr"):
        keys = [f"test_{ds}_{sysname}" for ds in ("webqsp", "cwq")]
        if not all(k in out for k in keys):
            continue
        a = sum(out[k]["entities_asserted"] for k in keys)
        u = sum(out[k]["entities_ungrounded"] for k in keys)
        out[f"both_{sysname}"] = {
            "entities_asserted": a,
            "entities_ungrounded": u,
            "entity_ungrounded_pct": round(100 * u / a, 1),
        }
    return out


def parse_tier2(path):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = TIER2.match(line.strip())
        if m:
            out[m.group(1)] = {
                "supported": int(m.group(2)), "sampled": int(m.group(3)),
                "supported_pct": float(m.group(4)),
            }
    return out


def compute_kappa(sheet, key):
    """Cohen's kappa between the blind human labels and the judge.

    scripts/compute_kappa.py implements this a second time and the two are held
    to agree by tests/test_kappa_agreement.py. The point of the duplication is
    that an arithmetic slip in a chance-correction formula produces a plausible
    number rather than an error, so a second reading of the same two files is
    worth more than a shared helper would be. Independence is only worth
    claiming if both readings accept the same inputs, hence the label check
    below -- without it this one silently took labels the other rejects.
    """
    human = []
    for r in csv.DictReader(open(sheet, encoding="utf-8")):
        val = r["your_label(1/0)"].strip()
        assert val in ("0", "1"), f"row {r['idx']} not labeled: {val!r}"
        human.append(int(val))
    judge = [int(bool(r["supported"]))
             for r in json.load(open(key, encoding="utf-8"))]
    assert len(human) == len(judge), "row count mismatch"
    n = len(human)
    a = sum(1 for y, j in zip(human, judge) if y == 1 and j == 1)
    b = sum(1 for y, j in zip(human, judge) if y == 1 and j == 0)
    c = sum(1 for y, j in zip(human, judge) if y == 0 and j == 1)
    d = sum(1 for y, j in zip(human, judge) if y == 0 and j == 0)
    po = (a + d) / n
    pe = (a + b) / n * (a + c) / n + (c + d) / n * (b + d) / n
    return {"n": n, "observed_agreement": round(po, 4),
            "cohens_kappa": round((po - pe) / (1 - pe), 4),
            "human_supported": a + b, "judge_supported": a + c,
            "preregistered_threshold": 0.7}


_TESTSETS = {}


def testset(ds):
    """The questions in a test split, read once per run.

    Two blocks below need these files. Opening them per call made the number of
    reads a property of who calls what, which matters more than the redundant
    I/O: the assertions in this module are only as good as a test that can
    patch every read, and a test that patches one of four reads passes without
    exercising anything. One cache, one point to patch. Callers only read.
    """
    if ds not in _TESTSETS:
        _TESTSETS[ds] = json.load(
            open(P4 / f"test_{ds}.json", encoding="utf-8"))
    return _TESTSETS[ds]


def gold_stats(ds):
    """Shape of the gold answer sets in a test split, and its accuracy ceiling.

    These were being quoted from a one-off calculation rather than from here,
    and the WebQSP median had drifted to 2 in the prose against an actual 1.5.
    The median matters to the argument -- it is what makes the point that
    Hits@1's any-match loophole is wide on WebQSP -- so it is derived.

    reachable_pct is the ceiling that bounds the reported results, and it is not
    the one the validation gate reports: the gate measures the full split and
    this measures the 400 questions actually evaluated, so the two differ by
    sampling. Both are real and neither is a correction of the other, which is
    exactly why each needs a home in this file rather than a figure in prose.
    Reachability is read from n_gold_reachable, the same per-question quantity
    the stratum assignment uses, so the ceiling and the strata cannot disagree.

    Set sizes are counted over DISTINCT answer strings, because that is the
    population every metric acts on: Sec 2.2.2 defines precision and recall over
    sets and scripts/score_test.py scores against set(map(norm, gold)). The raw
    answers list repeats a string on 4 WebQSP and 6 CWQ questions, and those
    repeats sit in the tail: counting them takes the WebQSP mean from 7.15 to
    7.98 and its largest question from 237 to 382, which is the gap that had the
    thesis quoting one quantity in two units. gold_max_scored applies the
    scorer's own NFKC + case folding on top, and is recorded so the residual
    difference between exact-string and matched-form deduplication is visible
    rather than discovered later.
    """
    rows = testset(ds)
    n_gold = [len(dict.fromkeys(r["answers"])) for r in rows]
    scored = [len(set(map(_norm, r["answers"]))) for r in rows]
    assert n_gold == [r["n_gold"] for r in rows], (
        "n_gold in the committed split no longer equals the distinct answer "
        "count, so the split's own metadata and these figures disagree")
    reachable = sum(1 for r in rows if r["n_gold_reachable"] > 0)
    assert reachable == sum(1 for r in rows if r["stratum"] != "unreachable"), (
        "the unreachable stratum and n_gold_reachable disagree, so the ceiling "
        "and the stratum sizes in tab:testsets no longer describe one split")
    return {
        "n_questions": len(n_gold),
        "gold_mean": round(statistics.mean(n_gold), 2),
        "gold_median": statistics.median(n_gold),
        "gold_max": max(n_gold),
        "questions_with_one_gold": sum(1 for n in n_gold if n == 1),
        "gold_mean_raw_with_repeats": round(
            statistics.mean(len(r["answers"]) for r in rows), 2),
        "gold_max_raw_with_repeats": max(len(r["answers"]) for r in rows),
        "gold_mean_scored": round(statistics.mean(scored), 2),
        "gold_max_scored": max(scored),
        "questions_with_repeated_gold": sum(
            1 for r, n in zip(rows, n_gold) if len(r["answers"]) != n),
        "strata": {s: sum(1 for r in rows if r["stratum"] == s)
                   for s in HOPS + ("unreachable",)},
        "any_gold_reachable": reachable,
        "reachable_pct": round(100 * reachable / len(rows), 1),
    }


def _norm(s):
    return unicodedata.normalize("NFKC", s).casefold().strip()


def _read_run(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        pred = set(map(_norm, r.get("answer_entities", [])))
        gold = set(map(_norm, r["gold"]))
        out[r["qid"]] = {
            "hit": bool(gold & pred),
            "n_pred": len(pred),
            "precision": (len(gold & pred) / len(pred)) if pred else None,
            # Reaching the cap is not the same as being cut off by it: a run
            # can spend its last allowed call on the step that finishes it.
            # The trace flag is the authority; llm_calls == 25 is not.
            "clipped": any(s.get("budget_exhausted")
                           for s in r.get("trace", [])),
        }
    return out


def tog_budget_split():
    """AGR against Think-on-Graph, split by whether the shared call cap cut ToG off.

    The headline AGR-over-ToG margin is not evenly distributed. On the questions
    ToG is allowed to finish it is ahead on both datasets; the entire margin
    comes from the questions where the shared budget truncates its beam search.
    That is a sharper finding than the aggregate, and it is only visible split.
    """
    out = {}
    for ds in ("webqsp", "cwq"):
        tog = _read_run(P4 / f"test_{ds}_tog.jsonl")
        agr = _read_run(P4 / f"test_{ds}_agr.jsonl")
        qids = sorted(set(tog) & set(agr))
        block = {}
        for label, sel in (("tog_finished", False), ("tog_clipped", True)):
            sub = [q for q in qids if tog[q]["clipped"] == sel]
            block[label] = {
                "n": len(sub),
                "tog_hits_at_1": round(sum(tog[q]["hit"] for q in sub) / len(sub), 4),
                "agr_hits_at_1": round(sum(agr[q]["hit"] for q in sub) / len(sub), 4),
            }
        block["n_questions"] = len(qids)
        block["tog_clip_rate"] = round(
            sum(tog[q]["clipped"] for q in qids) / len(qids), 4)
        # Assertion breadth over answered questions only. AGR names more
        # entities per answer, which mechanically helps an any-match metric;
        # precision over the same questions is the check on that.
        for name, run in (("agr", agr), ("tog", tog)):
            ans = [v for v in run.values() if v["n_pred"]]
            block[f"{name}_answered"] = {
                "n": len(ans),
                "entities_per_answer": round(
                    sum(v["n_pred"] for v in ans) / len(ans), 2),
                "precision": round(
                    sum(v["precision"] for v in ans) / len(ans), 4),
            }
        out[ds] = block
    return out


def ablation_backtrack_reasons():
    """Backtrack triggers per ablation condition, from the run records.

    Sec 8.8.4 attributed the embedding-only condition's extra backtracks to the
    tau mechanism. Every backtrack stores its trigger, so the increase can be
    decomposed instead of attributed, and the decomposition is what the section
    now reports. low_score is the trigger tau governs.
    """
    out = {}
    for cond in ("full", "noplanner", "nobacktrack", "noverifier", "embonly"):
        for ds in ("webqsp", "cwq"):
            path = (P4 / "ablations" / f"test_{ds}_half_abl_{cond}.jsonl")
            if not path.exists():
                continue
            counts = {"dead_end": 0, "low_score": 0, "evaluator": 0}
            for line in open(path, encoding="utf-8"):
                for b in json.loads(line).get("backtracks", []):
                    r = b.get("reason")
                    if r in counts:
                        counts[r] += 1
            out[f"{ds}/{cond}"] = {**counts, "total": sum(counts.values())}
    return out


def _agr_runs():
    """The two main-matrix AGR records, read once, as (dataset, rows) pairs."""
    for ds in ("webqsp", "cwq"):
        yield ds, [json.loads(l) for l in
                   open(P4 / f"test_{ds}_agr.jsonl", encoding="utf-8")]


def verifier_route():
    """What the verify--repair cycle did on test, in the unit each claim needs.

    Chapter 6 characterises this route on the 80-question development set, where
    it never fired, and generalised that to the thesis. It does fire on test, and
    sec:verifier-errors narrates three of its five wrongly-rejected specimens as
    retries that ran -- so the two chapters contradicted each other and the
    frozen records settle it against Chapter 6.

    Three populations get confused here and each is counted separately:

      verify_iters_ge_1    the verifier ASKED for a repair. It increments the
                           counter before the router decides, so this counts
                           intent, not execution.
      explorer_reentered   exploration actually resumed after the first verdict,
                           read from the node sequence. This is the executed
                           repair, and it is what sec:repair's claim is about.
      cap_reached          two repair iterations, the cap sec:repair says was
                           never reached.

    verifier_invocations is the firing count and exceeds the question count,
    because a repaired question is verified twice. first_verdict_* is the
    per-question unit that runlog.py persists (it stores the FIRST verifier trace
    entry, so verifier_outcome is not the final verdict); final_verdict_* is the
    outcome the answer was actually produced under. sec:verifier-errors quoted
    the firing count against the first-verdict grounded count, which are
    different units over different populations.
    """
    out = {}
    for ds, rows in _agr_runs():
        nodes = [[t.get("node") for t in r["trace"]] for r in rows]
        last = [next((t["outcome"] for t in reversed(r["trace"])
                      if t.get("node") == "verifier"), None) for r in rows]
        first = [r["verifier_outcome"] for r in rows]
        assert all(r["verifier_outcome"] == next(
            (t["outcome"] for t in r["trace"] if t.get("node") == "verifier"),
            None) for r in rows), "verifier_outcome is not the first verdict"
        out[ds] = {
            "n_questions": len(rows),
            "verifier_invocations": sum(n.count("verifier") for n in nodes),
            "verify_iters_ge_1": sum(
                1 for r in rows if r["budget"]["verify_iters"] >= 1),
            "explorer_reentered": sum(
                1 for n in nodes
                if "verifier" in n and "explorer" in n[n.index("verifier") + 1:]),
            "cap_reached": sum(
                1 for r in rows if r["budget"]["verify_iters"] >= 2),
            "first_verdict_unsupported": first.count("unsupported"),
            "first_verdict_grounded": first.count("grounded"),
            "final_verdict_unsupported": last.count("unsupported"),
            "final_verdict_grounded": last.count("grounded"),
            "repaired_to_grounded": sum(
                1 for f, l in zip(first, last)
                if f == "unsupported" and l == "grounded"),
        }
    keys = list(next(iter(out.values())))
    out["total"] = {k: sum(v[k] for v in out.values()) for k in keys}
    t = out["total"]
    assert t["explorer_reentered"] > 0, (
        "Sec 6.4 says the repair route never executed and scopes that to the "
        "development set; if it never executes on test either, that scoping "
        "sentence is now the wrong correction")
    assert (t["final_verdict_grounded"]
            == t["first_verdict_grounded"] + t["repaired_to_grounded"]), (
        "grounded questions do not decompose into first-verdict grounded plus "
        "repaired, so one of the two counts is not the unit it claims to be")
    return out


def backtrack_ban_scope():
    """How far the ban list reaches, against how far the backtracker jumps.

    sec:backtracking describes the backtracker as banning every triple expanded
    since the restored snapshot. It bans state["last_expanded"] -- the single most
    recent explorer pass -- while popping the highest-scoring snapshot, which
    need not be the most recent. Everything expanded in between stays unbanned,
    and the section's own argument for why the ban list exists (a deterministic
    scorer facing an identical frontier repeats itself) is what then fails.

    Two quantities, and they are not equally strong:

      repeat_expansion_passes is EXACT. It counts explorer passes whose
      (anchor, relation) set is identical to a set the same question expanded
      earlier -- the repetition the ban list is supposed to make impossible,
      observed directly, with no reconstruction involved.

      by_reason is EXACT. It decomposes the pops by the trigger the backtracker
      recorded against each one. sec:abl-backtracking quotes the evaluator
      sub-counts, and the provenance rule at the head of ch:setup requires every
      number in Chapters 7 to 9 to be derived by this script rather than
      hand-counted out of the trace, which is why they are computed here.

      pops_below_stack_top is a LOWER BOUND. Identifying the popped snapshot
      needs the scores, which the trace does not carry; depth it does carry, and
      the depth series reconstructs exactly (verified against budget.depth on
      every record). So a pop whose restored depth differs from the top
      snapshot's depth is provably not the most recent one, while a pop that
      restores the same depth from an older snapshot cannot be distinguished and
      is counted as most-recent here. The true figure is at least this.
    """
    out = {}
    for ds, rows in _agr_runs():
        pops = below = repeats = 0
        reasons = {}
        for r in rows:
            stack, depth, seen = [], 0, []
            for t in r["trace"]:
                if t.get("node") == "explorer":
                    stack.append(depth)
                    depth += 1
                    key = frozenset((e["anchor"], e["rel"])
                                    for e in t["expanded"])
                    if key and key in seen:
                        repeats += 1
                    seen.append(key)
                elif t.get("node") == "backtracker":
                    rd = t["restored_depth"]
                    pops += 1
                    reasons[t["reason"]] = reasons.get(t["reason"], 0) + 1
                    if stack:
                        if stack[-1] != rd:
                            below += 1
                        match = [i for i, d in enumerate(stack) if d == rd]
                        stack.pop(match[-1] if match else -1)
                    depth = rd
            assert depth == r["budget"]["depth"], (
                f"the depth series does not reconstruct on {r['qid']}, so the "
                f"stack simulation below it is not trustworthy either")
        out[ds] = {
            "backtracks": sum(r["budget"]["backtracks"] for r in rows),
            "pops_below_stack_top": below,
            "repeat_expansion_passes": repeats,
            "by_reason": dict(sorted(reasons.items())),
        }
        assert out[ds]["backtracks"] == pops, (
            "the backtrack counter and the backtracker trace entries disagree")
        assert sum(reasons.values()) == pops, (
            "the recorded trigger reasons do not account for every pop, so the "
            "decomposition is not of the same population as the total")
    per_ds = list(out.values())
    keys = [k for k, v in per_ds[0].items() if not isinstance(v, dict)]
    out["total"] = {k: sum(v[k] for v in per_ds) for k in keys}
    out["total"]["by_reason"] = {
        reason: sum(v["by_reason"].get(reason, 0) for v in per_ds)
        for reason in sorted({r for v in per_ds for r in v["by_reason"]})}
    return out


# Every agent run in the two phases the thesis reports records into. Phase 2 is
# excluded deliberately: backbone qualification uses its own logger and carries
# no budget snapshot at all, so it is not a population this claim ranges over.
RECORD_GLOBS = ("results/phase3/*.jsonl", "results/phase4/*.jsonl",
                "results/phase4/ablations/*.jsonl")


def run_record_census():
    """Every committed agent run, and the reasoning-token field's value in it.

    The appendix says the cache's failure to replay reasoning_tokens is harmless
    because the field is zero in every record. That was quoted as 6,060, which is
    the phase-4 count and silently drops the development runs Table 8.1 reports
    -- a claim of the form "all N records" cannot be scoped to some of them. The
    population is counted here instead, over both phases, and the zero is checked
    rather than asserted in prose.

    smoke_runs_short reports any phase-4 smoke file holding fewer than the twenty
    questions of the smoke set. One does: the Think-on-Graph run stopped at ten
    where its three baseline siblings hold twenty. It is a partial run, it is left
    partial rather than re-run, and it is surfaced here so that a reader who
    notices the short file in results/ finds it accounted for rather than
    unexplained. Nothing reads those records but this census -- the smoke-set
    discussion of sec:design-validation reads the phase-3 file -- so the count it
    touches is n_records and no other figure in the thesis.
    """
    files = sorted(p for g in RECORD_GLOBS for p in Path().glob(g)
                   if not p.name.endswith("_tools.jsonl"))
    n = nonzero = 0
    per_file = {}
    for p in files:
        rows = 0
        for line in open(p, encoding="utf-8"):
            n += 1
            rows += 1
            if json.loads(line)["budget"].get("reasoning_tokens"):
                nonzero += 1
        per_file[p] = rows
    assert nonzero == 0, (
        f"{nonzero} records carry a non-zero reasoning_tokens, so the cache's "
        f"replay gap is no longer harmless and sec:instrumentation is wrong")
    return {"n_files": len(files), "n_records": n,
            "records_with_nonzero_reasoning_tokens": nonzero,
            "smoke_runs_short": {p.name: c for p, c in sorted(per_file.items())
                                 if p.name.startswith("smoke20_") and c < 20}}


def gold_adjudication(exclusions):
    """Every cell of tab:goldnoise, and the closure the table depends on.

    The table separates two units the surrounding prose says must not be
    conflated -- rows flagged by the consensus pass, questions flagged, and
    questions adjudicated defective -- and every one of its six cells was typed
    from goldnoise_summary.json rather than read from here. The counts were
    right, but a table whose whole point is that two numbers are different units
    is the last place to leave the units unchecked, so they are read from the
    artifact and the exclusion arithmetic is asserted: gold_wrong plus ambiguous
    must equal excluded, and excluded must equal what census_exclusions.json
    actually holds, which is the file the census reads.
    """
    s = json.load(open(P4 / "goldnoise_summary.json", encoding="utf-8"))
    out = {}
    for ds, v in s.items():
        out[ds] = {k: v[k] for k in ("flag_rows", "flagged_questions",
                                     "gold_wrong_questions",
                                     "ambiguous_questions",
                                     "excluded_questions")}
        out[ds]["excluded_pct"] = round(
            100 * v["excluded_questions"] / len(testset(ds)), 1)
        assert (v["gold_wrong_questions"] + v["ambiguous_questions"]
                == v["excluded_questions"]), (
            f"{ds}: exclusions are the union of gold_wrong and ambiguous, and "
            f"that union no longer closes, so tab:goldnoise adds up to a total "
            f"it does not contain")
        assert v["excluded_questions"] == len(exclusions[ds]), (
            f"{ds}: tab:goldnoise reports {v['excluded_questions']} exclusions "
            f"but census_exclusions.json holds {len(exclusions[ds])}, so the "
            f"table and the file the census actually reads disagree")
    return out


DEFECT_CATEGORIES = ("gold_noise", "ambiguous_question")


def benchmark_defects(exclusions):
    """Distinct questions where the benchmark, not the system, needed correcting.

    Two sets carry this: the formal exclusions adjudicated before the census read
    anything, and the rows still sitting in the merged census under a defect
    category. They are nearly disjoint, and the thesis quoted their sum -- but
    one question was promoted from a census row to a formal exclusion mid-project
    and appears in both, so the sum double-counted exactly the question the
    surrounding paragraph singles out as needing care. Counting identifiers
    instead of adding two totals is the only way that stays right, so the union
    is taken here and the overlap is reported rather than assumed to be empty.
    """
    ex = {q if isinstance(q, str) else q["qid"]
          for v in exclusions.values() for q in v}
    rows = {}
    for name in ("labels_webqsp.csv", "labels_cwq.csv", "labels_cwq_dropped.csv",
                 "ablations/noplanner_categories_webqsp.csv",
                 "ablations/noplanner_categories_cwq.csv"):
        path = P4 / name
        if not path.exists():
            continue
        for r in csv.DictReader(open(path, encoding="utf-8")):
            if r["category"] in DEFECT_CATEGORIES:
                rows[r["qid"]] = r["category"]

    both = ex & set(rows)
    return {
        "excluded_before_census": len(ex),
        "census_rows_in_defect_categories": len(rows),
        "counted_in_both": sorted(both),
        "distinct_questions": len(ex | set(rows)),
    }


def parse_census(path):
    """Stage E histogram: {dataset: {wrong|hedge: {category: count}}}."""
    out, ds, kind = {}, None, None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^=== (\w+) ===$", line.strip())
        if m:
            ds = m.group(1); out[ds] = {}; continue
        m = re.match(r"^--\s+(wrong|hedge)\s+\(n=(\d+)\)\s+--$", line.strip())
        if m:
            kind = m.group(1)
            out[ds][kind] = {"_n": int(m.group(2))}; continue
        m = HIST.match(line)
        if m and ds and kind:
            out[ds][kind][m.group(1)] = int(m.group(2))
    return out


def candidate_caps():
    """How often each system's candidate-set caps actually truncated.

    The agentic baseline re-uses AGR's tools and then cuts the result to its own
    beam-search widths, which are narrower than the ones AGR keeps. Both cuts are
    invisible in the accuracy tables, so the rate at which each one binds is
    measured here from the committed tool logs and reported in the baseline
    description rather than left to be read off the source. Every width comes
    from the class that applies it, so the widths reported are the widths run.
    """
    caps = {"tog": {"relations": MAX_RELATIONS, "neighbors": MAX_NEIGHBORS},
            "agr": {"relations": _default(KGTools, "max_relations"),
                    "neighbors": _default(KGTools, "max_fanout")}}
    out = {}
    # Post-blocklist degree of every entity AGR expanded. get_relations returns
    # one row per relation type with its fanout, and the two blocklists are
    # equivalent, so the row sum is the degree the static graph baseline's own
    # LIMIT has to cut into.
    #
    # The static baseline expands topic entities only, and it resolves them by
    # calling resolver(name, 1) on q["gold_q_entities"]. Those same names are
    # resolved by AGR through the logged search_entity tool, so its topic set is
    # recoverable exactly rather than approximated: every gold name resolves at
    # tier 1 to a single hit, which makes the resolution independent of k and
    # free of tie-breaking. The assertion below fails if that ever stops holding,
    # because the whole identification rests on it.
    degree, searches = {}, {}
    for ds in ("webqsp", "cwq"):
        path = P4 / f"test_{ds}_agr_tools.jsonl"
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["tool"] == "get_relations":
                degree[r["args"]["id"]] = sum(row["n"] for row in r["result"])
            elif r["tool"] == "search_entity":
                searches.setdefault(r["args"]["q"], r["result"])

    names, mentions, per_question = set(), 0, []
    for ds in ("webqsp", "cwq"):
        for q in testset(ds):
            names |= set(q["gold_q_entities"])
            mentions += len(q["gold_q_entities"])
            per_question.append(q["gold_q_entities"])

    unresolved = [n for n in names
                  if len(searches.get(n, [])) != 1
                  or searches[n][0]["tier"] != 1]
    assert not unresolved, (
        f"{len(unresolved)} gold topic names do not resolve to a single tier-1 "
        f"hit, so the static baseline's topic set is no longer identifiable "
        f"from the log: {unresolved[:5]}")

    topic_ids = {searches[n][0]["id"] for n in names}
    assert topic_ids <= set(degree), "some topic entity was never expanded"

    def block(ids):
        v = sorted(degree[i] for i in ids)
        over = sum(1 for x in v if x > GRAPHRAG_FANOUT_CAP)
        return {"n_entities": len(v),
                "median": statistics.median(v),
                "p90": v[int(0.9 * len(v))],
                "max": max(v),
                "over_100": over,
                "over_100_pct": round(100 * over / len(v), 1)}

    # Entities and questions are different units -- a question carries 1.29 topic
    # entities on average -- so the share of truncated entities does not give the
    # share of affected questions in either direction. Both question-level shares
    # are measured here so that a sentence about questions can quote one.
    # The tier-1 assertion above only ranges over names that exist, so it says
    # nothing about a question that annotates none. Such a question would satisfy
    # "every topic entity is truncated" vacuously and inflate the all-topics
    # share, which is the one way left for this block to report a population it
    # did not measure. Assert instead of guarding: a question the static baseline
    # cannot seed at all is worth failing on, not silently omitting from a rate.
    empty = [i for i, ents in enumerate(per_question) if not ents]
    assert not empty, (
        f"{len(empty)} test questions annotate no topic entity, so the static "
        f"baseline seeds nothing for them and the question-level truncation "
        f"rates below no longer describe all {len(per_question)} questions")

    # The key names below carry the cap as a literal because the thesis quotes
    # them by name. That is only safe while the cap is what the names say, so a
    # change to the baseline has to come here and rename them rather than quietly
    # relabel a different threshold with the old name.
    assert GRAPHRAG_FANOUT_CAP == 100, (
        f"the static baseline's fanout cap is now {GRAPHRAG_FANOUT_CAP}; the "
        f"over_100 keys below are named for a cap of 100 and must be renamed")

    q_any = q_all = 0
    for ents in per_question:
        degs = [degree[searches[n][0]["id"]] for n in set(ents)]
        over = sum(1 for d in degs if d > GRAPHRAG_FANOUT_CAP)
        q_any += over > 0
        q_all += over == len(degs)

    out["expanded_entity_degree"] = {
        **block(set(degree)),
        "topic_mentions": mentions,
        "topic_entities": block(topic_ids),
        "frontier_entities": block(set(degree) - topic_ids),
        "questions": len(per_question),
        "questions_any_topic_over_100": q_any,
        "questions_any_topic_over_100_pct": round(100 * q_any / len(per_question), 1),
        "questions_all_topics_over_100": q_all,
        "questions_all_topics_over_100_pct": round(100 * q_all / len(per_question), 1),
    }
    for sysname, cap in caps.items():
        rel_n, per_entity, nbr_n = [], {}, []
        for ds in ("webqsp", "cwq"):
            path = P4 / f"test_{ds}_{sysname}_tools.jsonl"
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if r["tool"] == "get_relations":
                    rel_n.append(len(r["result"]))
                    per_entity[r["args"]["id"]] = len(r["result"])
                elif r["tool"] == "get_neighbors":
                    nbr_n.append(r["result"]["n"])
        ent = list(per_entity.values())
        out[sysname] = {
            "relation_cap": cap["relations"],
            "neighbor_cap": cap["neighbors"],
            "get_relations_calls": len(rel_n),
            "entities_expanded": len(ent),
            "entities_at_relation_cap": sum(1 for n in ent
                                            if n >= cap["relations"]),
            "entities_at_relation_cap_pct": round(
                100 * sum(1 for n in ent if n >= cap["relations"]) / len(ent), 1),
            "get_neighbors_calls": len(nbr_n),
            "neighbor_calls_at_cap": sum(1 for n in nbr_n
                                         if n >= cap["neighbors"]),
            "neighbor_calls_at_cap_pct": round(
                100 * sum(1 for n in nbr_n if n >= cap["neighbors"])
                / len(nbr_n), 1),
        }
    return out


def main():
    main_rows, main_strata, main_mcnemar = parse_scores(P4 / "score_test_log.txt")
    abl_rows, abl_strata, abl_mcnemar = parse_scores(
        P4 / "ablations" / "score_test_ablations_log.txt")

    coverage = json.load(open("results/phase1/coverage_report.json",
                              encoding="utf-8"))["stats"]
    exclusions = json.load(open(P4 / "census_exclusions.json", encoding="utf-8"))

    doc = {
        "_README": (
            "Generated by scripts/build_thesis_numbers.py. Every number the "
            "thesis states should come from here. Do not hand-edit; rerun the "
            "script. Each block names the artifact it was parsed from."),
        "environment_coverage": {
            "_source": "results/phase1/coverage_report.json",
            "_note": ("any_reachable / n is the answer-reachability ceiling "
                      "reported in the validation gate. This is the ceiling "
                      "over the FULL splits (n=1628, n=3531). The systems are "
                      "evaluated on 400-question samples, whose ceilings differ "
                      "by sampling and live in test_sets.*.reachable_pct; a "
                      "sentence about the reported results wants that one."),
            **{ds: {**v,
                    "reachable_pct": round(100 * v["any_reachable"] / v["n"], 2)}
               for ds, v in coverage.items()},
        },
        "test_sets": {
            "_source": ("results/phase4/test_webqsp.json + "
                        "results/phase4/test_cwq.json"),
            "_note": ("shape of the gold answer sets in the evaluated splits. "
                      "gold_median is 1.5 on WebQSP: exactly half the questions "
                      "carry a single gold answer, and the mean is dragged up "
                      "by a long tail. reachable_pct is the ceiling over these "
                      "400 questions and is the bound on every Hits@1 reported "
                      "in Chapter 8; environment_coverage carries the full-split "
                      "figure, which is a different population, not a revision."),
            **{ds: gold_stats(ds) for ds in ("webqsp", "cwq")},
        },
        "main_results": {
            "_source": "results/phase4/score_test_log.txt",
            "_note": "secs are cold-cache records only; nan means not measured.",
            "by_system": main_rows,
            "by_hop_stratum": main_strata,
            "_hop_trend_note": (
                "shape of each by_hop_stratum curve over h1/h2/h3plus, so the "
                "claim that AGR is the only system improving with hop count is "
                "quoted rather than read off the table. Note the two readings "
                "differ: on CWQ the agentic baseline is NOT monotone_falling "
                "(it recovers at h3plus) but IS ends_below_h1, so 'every other "
                "system decays' is false and 'every other system ends below "
                "where it started' is true."),
            "hop_trends": hop_trends(main_strata),
            "mcnemar_vs_baselines": main_mcnemar,
        },
        "tog_budget_split": {
            "_source": ("results/phase4/test_{webqsp,cwq}_{tog,agr}.jsonl"),
            "_note": ("AGR vs Think-on-Graph split on whether the shared 25-call "
                      "cap cut ToG off, read from the per-record trace flag "
                      "budget_exhausted (NOT from llm_calls == 25, which "
                      "overcounts CWQ by 3). On the questions ToG finishes it "
                      "is ahead on both datasets; the whole aggregate margin "
                      "comes from the clipped subset."),
            **tog_budget_split(),
        },
        "ablations": {
            "_source": "results/phase4/ablations/score_test_ablations_log.txt",
            "_note": ("half-split: n=200 webqsp, n=198 cwq. Only the planner "
                      "condition reaches significance; the rest are 'no "
                      "detectable effect at this sample size', not confirmed "
                      "nulls."),
            "by_condition": abl_rows,
            "by_hop_stratum": abl_strata,
            "mcnemar_vs_full": abl_mcnemar,
            "backtrack_reasons": ablation_backtrack_reasons(),
            "_backtrack_note": (
                "embonly's extra backtracks are mostly low_score, the trigger "
                "tau governs -- but sigma is computed over a smaller candidate "
                "set when alpha=1 (scorer.py early-returns without setting "
                "last_info), so the rise is confounded. See Sec 8.8.4."),
        },
        "groundedness_tier1_structural": {
            "_source": "results/phase4/tier1_groundedness/groundedness_log.txt",
            "_note": ("structural grounding of asserted entities against the "
                      "graph. AGR and ToG both reach 0.0% -- this is a property "
                      "of graph navigation, NOT of the verification layer."),
            **parse_tier1(P4 / "tier1_groundedness" / "groundedness_log.txt"),
        },
        "groundedness_tier2_judge": {
            "_source": "results/phase4/tier2_judge/judge_support_log.txt",
            "_note": "LLM entailment judgement on a 60-claim sample per run.",
            **parse_tier2(P4 / "tier2_judge" / "judge_support_log.txt"),
        },
        "judge_validation": {
            "_source": ("results/phase4/tier2_judge/kappa_sheet.csv + "
                        "kappa_key.json"),
            "_note": ("scripts/compute_kappa.py recomputes this independently "
                      "from the same two files and must agree."),
            **compute_kappa(P4 / "tier2_judge" / "kappa_sheet.csv",
                            P4 / "tier2_judge" / "kappa_key.json"),
        },
        "census_exclusions": {
            "_source": "results/phase4/census_exclusions.json",
            "_note": "adjudicated gold-defect exclusions, per dataset",
            **{ds: len(v) for ds, v in exclusions.items()},
        },
        "gold_adjudication": {
            "_source": "results/phase4/goldnoise_summary.json",
            "_note": ("Every cell of tab:goldnoise. flag_rows, "
                      "flagged_questions and excluded_questions are three "
                      "different units over the same pass and none implies "
                      "another -- the pass emits one row per consensus answer, "
                      "and most flagged questions are five systems agreeing on "
                      "one wrong answer rather than a bad label. See "
                      "sec:gold-quality, sec:echo."),
            **gold_adjudication(exclusions),
        },
        "benchmark_defects": {
            "_source": ("results/phase4/census_exclusions.json + "
                        "labels_{webqsp,cwq}.csv + labels_cwq_dropped.csv + "
                        "ablations/noplanner_categories_{webqsp,cwq}.csv"),
            "_note": ("Distinct questions where the benchmark needed "
                      "correcting, which is what the abstract and conclusion "
                      "quote. Take distinct_questions, NOT the sum of the two "
                      "component counts: one question sits in both and adding "
                      "them counts it twice. See sec:benchmark-defects."),
            **benchmark_defects(exclusions),
        },
        "verifier_route": {
            "_source": "results/phase4/test_{webqsp,cwq}_agr.jsonl",
            "_note": ("The verify--repair cycle on test. Four different units "
                      "live here and none implies another: firings "
                      "(verifier_invocations), questions asking for a repair "
                      "(verify_iters_ge_1), questions where exploration "
                      "actually resumed (explorer_reentered), and questions by "
                      "verdict. Chapter 6 characterises this route on the "
                      "development set only. See sec:repair, "
                      "sec:verifier-errors."),
            **verifier_route(),
        },
        "backtrack_ban_scope": {
            "_source": "results/phase4/test_{webqsp,cwq}_agr.jsonl",
            "_note": ("The third recorded deviation of sec:backtracking: the ban "
                      "list covers the most recent expansion, the backtracker "
                      "pops the highest-scoring snapshot. "
                      "repeat_expansion_passes and by_reason are exact; "
                      "pops_below_stack_top is a lower bound (see the "
                      "docstring). All three are read from the trace, none "
                      "from a rerun."),
            **backtrack_ban_scope(),
        },
        "run_records": {
            "_source": "results/phase3/*.jsonl + results/phase4/**/*.jsonl",
            "_note": ("Every committed agent run in the two phases the thesis "
                      "reports, tool sidecars excluded. Backs the "
                      "reasoning_tokens claim in sec:instrumentation and "
                      "app:implementation, which was quoted over the phase-4 "
                      "subset while reading as if it covered all of them."),
            **run_record_census(),
        },
        "candidate_caps": {
            "_source": "results/phase4/test_{webqsp,cwq}_{tog,agr}_tools.jsonl",
            "_note": ("How often each system's candidate-set cap truncated, "
                      "both datasets pooled. Relations are sorted by "
                      "descending fanout before the cut, so a binding cut "
                      "discards the low-fanout tail. expanded_entity_degree "
                      "splits AGR's expansion set into the static baseline's "
                      "own topic entities and the rest; the topic block is "
                      "the population its fanout cap acts on. The questions_* "
                      "keys give the same truncation in the question unit, "
                      "which the entity shares do not imply. See "
                      "sec:baseline-tog and sec:baseline-graphrag."),
            **candidate_caps(),
        },
        "failure_histogram": {
            "_source": "results/phase4/synthesize_census_log.txt",
            "_note": ("Stage D + Stage A merged. wrong and hedge are never "
                      "pooled. Regenerate via scripts/synthesize_census.py "
                      "after any relabelling."),
            **parse_census(P4 / "synthesize_census_log.txt"),
        },
    }

    # The multi-hop claim is the one the abstract leads with, and it is the one
    # sentence a reader is most likely to check against the stratum table. It is
    # asserted here so that a rerun which changes the shape of a curve fails the
    # build instead of leaving the claim standing over data that no longer
    # supports it. Both halves are pinned, because the sentence needs both.
    cwq = doc["main_results"]["hop_trends"]["cwq"]
    assert cwq["_systems_monotone_rising"] == ["agr"], (
        f"the abstract and conclusion say AGR is the only CWQ system whose "
        f"accuracy rises with hop count; the rising systems are now "
        f"{cwq['_systems_monotone_rising']}")
    others = sorted(k for k in cwq if not k.startswith("_") and k != "agr")
    assert cwq["_systems_ending_below_h1"] == others, (
        f"the same sentence says every other CWQ system ends below its h1; "
        f"those that do are now {cwq['_systems_ending_below_h1']}, not {others}")

    # The abstract quotes the benchmark-defect total, and it was quoted as the
    # sum of the two component counts, which double-counts the one question that
    # appears in both. Fail here rather than let the sum look like the answer.
    bd = doc["benchmark_defects"]
    assert (bd["distinct_questions"]
            == bd["excluded_before_census"]
            + bd["census_rows_in_defect_categories"]
            - len(bd["counted_in_both"])), "benchmark-defect union does not close"

    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")
    if "_STALE" in doc["groundedness_tier1_structural"]:
        print("\n  *** tier-1 groundedness is STALE ***")
        print("  " + doc["groundedness_tier1_structural"]["_STALE"])
        print()
    print(f"  systems scored      : {len(main_rows)}")
    print(f"  ablation conditions : {len(abl_rows)}")
    print(f"  mcnemar comparisons : {len(main_mcnemar) + len(abl_mcnemar)}")
    print(f"  cohen's kappa       : {doc['judge_validation']['cohens_kappa']}")


if __name__ == "__main__":
    main()
