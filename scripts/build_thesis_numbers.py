"""Stage F: single source of truth for every number the thesis states.

Parses the scoring/groundedness/census artifacts and emits
`results/phase4/thesis_numbers.json`. Each block records its own source path so
a claim in the prose can be traced back to the file that produced it, and so a
rerun that moves a number tells you exactly which sentences to revisit.

Cite this file from the thesis; never re-transcribe a number by hand.

Usage: python scripts/build_thesis_numbers.py
"""
import csv, json, re
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
    your = [int(r["your_label(1/0)"].strip())
            for r in csv.DictReader(open(sheet, encoding="utf-8"))]
    judge = [int(bool(r["supported"]))
             for r in json.load(open(key, encoding="utf-8"))]
    assert len(your) == len(judge), "row count mismatch"
    n = len(your)
    a = sum(1 for y, j in zip(your, judge) if y == 1 and j == 1)
    b = sum(1 for y, j in zip(your, judge) if y == 1 and j == 0)
    c = sum(1 for y, j in zip(your, judge) if y == 0 and j == 1)
    d = sum(1 for y, j in zip(your, judge) if y == 0 and j == 0)
    po = (a + d) / n
    pe = (a + b) / n * (a + c) / n + (c + d) / n * (b + d) / n
    return {"n": n, "observed_agreement": round(po, 4),
            "cohens_kappa": round((po - pe) / (1 - pe), 4),
            "human_supported": a + b, "judge_supported": a + c,
            "preregistered_threshold": 0.7}


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
        "main_results": {
            "_source": "results/phase4/score_test_log.txt",
            "_note": "secs are cold-cache records only; nan means not measured.",
            "by_system": main_rows,
            "by_hop_stratum": main_strata,
            "mcnemar_vs_baselines": main_mcnemar,
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
            "_note": ("NOTE: scripts/compute_kappa.py still reads data/"
                      "kappa_sheet.csv and data/kappa_key.json, which do not "
                      "exist -- the artifacts live under results/phase4/"
                      "tier2_judge/. Fix those paths before rerunning it."),
            **compute_kappa(P4 / "tier2_judge" / "kappa_sheet.csv",
                            P4 / "tier2_judge" / "kappa_key.json"),
        },
        "census_exclusions": {
            "_source": "results/phase4/census_exclusions.json",
            "_note": "adjudicated gold-defect exclusions, per dataset",
            **{ds: len(v) for ds, v in exclusions.items()},
        },
        "failure_histogram": {
            "_source": "logs/synthesize_census_log.txt",
            "_note": ("Stage D + Stage A merged. wrong and hedge are never "
                      "pooled. Regenerate via scripts/synthesize_census.py "
                      "after any relabelling."),
            **parse_census("logs/synthesize_census_log.txt"),
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
