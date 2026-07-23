"""scripts/pull_noplanner_discordant.py — extract WebQSP/CWQ questions where
noplanner got the hit and full-AGR (with planner) did not, with full trace
comparison for manual reading.
Writes results/phase4/ablations/noplanner_discordant_{webqsp,cwq}.md
"""
import json
import unicodedata
from pathlib import Path

def norm(s):
    return unicodedata.normalize("NFKC", str(s)).strip().lower()

def load(path):
    return {json.loads(l)["qid"]: json.loads(l)
            for l in open(path, encoding="utf-8")}

def is_hit(rec):
    gold = {norm(g) for g in rec["gold"]}
    pred = {norm(a) for a in rec.get("answer_entities", [])}
    return bool(gold & pred)

def plan_summary(rec):
    plan_trace = next((t for t in rec["trace"] if t.get("node") == "planner"),
                      None)
    if not plan_trace:
        return "(no planner trace)"
    subs = plan_trace.get("plan", {}).get("sub_objectives", [])
    ablated = plan_trace.get("ablated", False)
    return f'ablated={ablated}  sub_objectives={subs}'

def backtrack_summary(rec):
    bts = rec.get("backtracks", [])
    if not bts:
        return "0 backtracks"
    reasons = [b["reason"] for b in bts]
    return f'{len(bts)} backtracks: {reasons}'

def main():
    DIR = Path("results/phase4/ablations")

    for ds in ("webqsp", "cwq"):
        full = load(DIR / f"test_{ds}_half_abl_full.jsonl")
        nop = load(DIR / f"test_{ds}_half_abl_noplanner.jsonl")

        discordant = []
        for qid, rf in full.items():
            rn = nop.get(qid)
            if rn is None:
                continue
            if rn and is_hit(rn) and not is_hit(rf):
                discordant.append((qid, rf, rn))

        out_path = DIR / f"noplanner_discordant_{ds}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# noplanner-only-correct: {ds} ({len(discordant)} cases)\n\n")
            for qid, rf, rn in discordant:
                f.write(f"## {qid}\n\n")
                f.write(f"**Question:** {rf['question']}\n\n")
                f.write(f"**Gold:** {rf['gold']}\n\n")
                f.write("| | full (with planner) | noplanner |\n")
                f.write("|---|---|---|\n")
                f.write(f"| answer | {rf['answer']} | {rn['answer']} |\n")
                f.write(f"| entities | {rf['answer_entities']} | "
                        f"{rn['answer_entities']} |\n")
                f.write(f"| plan | {plan_summary(rf)} | {plan_summary(rn)} |\n")
                f.write(f"| backtracks | {backtrack_summary(rf)} | "
                        f"{backtrack_summary(rn)} |\n")
                f.write(f"| verifier | {rf.get('verifier_outcome')} | "
                        f"{rn.get('verifier_outcome')} |\n")
                f.write(f"| calls/tokens | {rf['budget']['llm_calls']}/"
                        f"{rf['budget']['tokens']} | "
                        f"{rn['budget']['llm_calls']}/{rn['budget']['tokens']} |\n")
                f.write(f"\n**category:** _(fill in)_\n\n**note:** _(fill in)_\n\n"
                        f"---\n\n")

        print(f"{ds}: {len(discordant)} discordant cases -> {out_path}")

if __name__ == "__main__":
    main()
