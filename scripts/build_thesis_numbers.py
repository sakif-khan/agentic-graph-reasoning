"""Stage F: collect every number the thesis reports into a single file.

Parses the scoring, groundedness and census artifacts and writes
results/phase4/thesis_numbers.json. Each block records the path it was parsed
from, so a figure quoted in the prose can be traced back to the artifact that
produced it, and a rerun that changes a value identifies the claims affected.

The thesis quotes this file rather than transcribing numbers from the logs.

Usage: python scripts/build_thesis_numbers.py
"""
import csv, json, re, statistics, unicodedata
from pathlib import Path

P4 = Path("results/phase4")
OUT = P4 / "thesis_numbers.json"

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
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
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
    human = [int(r["your_label(1/0)"].strip())
             for r in csv.DictReader(open(sheet, encoding="utf-8"))]
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
    """Shape of the gold answer sets in a test split.

    These were being quoted from a one-off calculation rather than from here,
    and the WebQSP median had drifted to 2 in the prose against an actual 1.5.
    The median matters to the argument -- it is what makes the point that
    Hits@1's any-match loophole is wide on WebQSP -- so it is derived.
    """
    n_gold = [len(r["answers"]) for r in testset(ds)]
    return {
        "n_questions": len(n_gold),
        "gold_mean": round(statistics.mean(n_gold), 2),
        "gold_median": statistics.median(n_gold),
        "gold_max": max(n_gold),
        "questions_with_one_gold": sum(1 for n in n_gold if n == 1),
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

    Sec 8.7.4 attributed the embedding-only condition's extra backtracks to the
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

    The agentic baseline re-uses AGR's tools and then cuts the result to its
    own beam-search widths (40 relations, 20 neighbours); AGR keeps 300 and
    200. Both cuts are invisible in the accuracy tables, so the rate at which
    each one binds is measured here from the committed tool logs and reported
    in the baseline description rather than left to be read off the source.
    """
    caps = {"tog": {"relations": 40, "neighbors": 20},
            "agr": {"relations": 300, "neighbors": 200}}
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
        over = sum(1 for x in v if x > 100)
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

    q_any = q_all = 0
    for ents in per_question:
        degs = [degree[searches[n][0]["id"]] for n in set(ents)]
        over = sum(1 for d in degs if d > 100)
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
                      "reported in the validation gate."),
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
                      "by a long tail."),
            **{ds: gold_stats(ds) for ds in ("webqsp", "cwq")},
        },
        "main_results": {
            "_source": "results/phase4/score_test_log.txt",
            "_note": "secs are cold-cache records only; nan means not measured.",
            "by_system": main_rows,
            "by_hop_stratum": main_strata,
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
                "last_info), so the rise is confounded. See Sec 8.7.4."),
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

    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  systems scored      : {len(main_rows)}")
    print(f"  ablation conditions : {len(abl_rows)}")
    print(f"  mcnemar comparisons : {len(main_mcnemar) + len(abl_mcnemar)}")
    print(f"  cohen's kappa       : {doc['judge_validation']['cohens_kappa']}")


if __name__ == "__main__":
    main()
