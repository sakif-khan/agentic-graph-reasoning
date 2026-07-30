"""Stage E prerequisite.

Transcribes Stage A's inline **category:**/**subtype:**/**note:** fields
(already normalized to the project's closed category vocabulary) out of
results/phase4/ablations/noplanner_discordant_{webqsp,cwq}.md into a
machine-readable CSV with the same qid,kind,category,subtype,note schema
as labels_{ds}.csv -- so synthesize_census.py can merge Stage A into the
histogram without hand transcription.

`kind` (wrong/hedge) is derived from the full-pipeline (with-planner)
column's own entities cell: empty -> hedge, non-empty -> wrong. Stage A's
own framing is "noplanner succeeded, full pipeline did not" -- the full
pipeline's failure is what we're categorizing, same as Stage D.

Writes: results/phase4/ablations/noplanner_categories_{webqsp,cwq}.csv
"""
import csv, re
from pathlib import Path

DIR = Path("results/phase4/ablations")

VALID_CATEGORIES = {
    "decomposition_error", "relation_selection", "composite_claim",
    "premature_termination", "verifier_fn", "verifier_fp", "kg_gap",
    "answer_selection", "echo", "gold_noise", "ambiguous_question", "other",
}


def kind_of(block):
    """wrong vs hedge, from the full (with-planner) column's entities cell
    -- the first data column in the comparison table, not noplanner's."""
    m = re.search(r"\|\s*entities\s*\|\s*(.*?)\s*\|", block)
    if not m:
        return ""
    full_entities = m.group(1).strip()
    return "hedge" if full_entities in ("[]", "") else "wrong"


def main():
    for ds in ("webqsp", "cwq"):
        src = DIR / f"noplanner_discordant_{ds}.md"
        out = DIR / f"noplanner_categories_{ds}.csv"
        blocks = re.split(r"(?=^## )", src.read_text(encoding="utf-8"), flags=re.M)[1:]

        rows = []
        for b in blocks:
            qid = b.split("\n", 1)[0][3:].strip()
            cat_m = re.search(r"\*\*category:\*\*\s*(.+)", b)
            sub_m = re.search(r"\*\*subtype:\*\*\s*(.+)", b)
            note_m = re.search(r"\*\*note:\*\*\s*(.+)", b)
            category = cat_m.group(1).strip() if cat_m else ""
            subtype = sub_m.group(1).strip() if sub_m else ""
            note = note_m.group(1).strip() if note_m else ""
            if category not in VALID_CATEGORIES:
                raise ValueError(f"{ds}/{qid}: unrecognised category {category!r} "
                                  "-- re-check noplanner_discordant_{ds}.md by hand")
            rows.append([qid, kind_of(b), category, subtype, note])

        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["qid", "kind", "category", "subtype", "note"])
            w.writerows(rows)

        n_wrong = sum(1 for r in rows if r[1] == "wrong")
        n_hedge = sum(1 for r in rows if r[1] == "hedge")
        print(f"{ds}: {len(rows)} rows ({n_wrong} wrong, {n_hedge} hedge) -> {out}")


if __name__ == "__main__":
    main()
