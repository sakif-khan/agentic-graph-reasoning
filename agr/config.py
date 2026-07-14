from dataclasses import dataclass, asdict
from agr.scorer import HybridScorer
from agr.llm import LLMClient
from agr.env import OPENAI_API_KEY

@dataclass(frozen=True)
class RunConfig:
    use_gold_entities: bool = True   # seed anchors from dataset q_entity
    alpha: float = 0.7               # embedding weight in the hybrid scorer;
                                     # 1.0 = embedding-only (Phase 2 behavior / ablation)
    tau: float = 0.20                # low-score backtrack threshold;
                                     # 0.0 = trigger disabled (Phase 2 behavior)
    verify_claims: bool = True       # False = draft-only ablation: grounded
                                     # drafting, no claim extraction/checking

    def as_dict(self) -> dict:
        return asdict(self)


BACKBONE = {
    "model": "gpt-5.4-mini-2026-03-17",
    "temperature": 0.0,
    "reasoning_effort": "none",
}

run_cfg = RunConfig(alpha=0.7, tau=0.2)
llm = LLMClient(api_key=OPENAI_API_KEY, **BACKBONE)
scorer = HybridScorer("data/relation_embeddings.npy",
                      "data/relation_names.json",
                      llm=llm, alpha=run_cfg.alpha)
