import json, subprocess, time
from pathlib import Path


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


class RunLogger:
    def __init__(self, path: str, backbone: dict, budget_cfg,
                 run_config: dict | None = None):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.f = open(path, "a", encoding="utf-8")
        self.meta = {"backbone": backbone,
                     "budget_hash": budget_cfg.config_hash(),
                     "run_config": run_config or {},
                     "git": git_commit()}

    def write(self, qid, question, gold, final, wall_seconds):
        backtracks = [t for t in final["trace"]
                      if t.get("node") == "backtracker"]
        verifier = next((t for t in final["trace"]
                         if t.get("node") == "verifier"), {})
        rec = {
            "qid": qid, "question": question, "gold": gold,
            "answer": final["answer"],
            "answer_entities": final.get("answer_entities", []),
            "draft": final.get("draft"),
            "unsupported_claims": final.get("unsupported_claims", []),
            "n_supporting_triples": len(final.get("supporting_triples") or []),
            "verifier_outcome": verifier.get("outcome"),
            "backtracks": [{"reason": b.get("reason"),
                            "to_depth": b.get("restored_depth")}
                           for b in backtracks],
            "budget": final["budget"].snapshot(),
            "wall_seconds": round(wall_seconds, 1),
            "trace": final["trace"],
            **self.meta,
        }
        self.f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.f.flush()
