from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class RunConfig:
    use_gold_entities: bool = True   # seed anchors from dataset q_entity
    alpha: float = 0.7               # frozen 2026-07-13, dev80 sweep
    tau: float = 0.20                # frozen 2026-07-13
    verify_claims: bool = True       # False = draft-only ablation: grounded
                                     # drafting, no claim extraction/checking
    use_planner: bool = True

    def as_dict(self) -> dict:
        return asdict(self)

run_cfg = RunConfig()


BACKBONE = {
    "model": "gpt-5.4-mini-2026-03-17",
    "temperature": 0.0,
    "reasoning_effort": "none",
}
