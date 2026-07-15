from dataclasses import dataclass, asdict
from agr.scorer import HybridScorer
from agr.llm import LLMClient
from agr.env import OPENAI_API_KEY

@dataclass(frozen=True)
class RunConfig:
    use_gold_entities: bool = True   # seed anchors from dataset q_entity
    alpha: float = 0.7               # frozen 2026-07-13, dev80 sweep
    tau: float = 0.20                # frozen 2026-07-13
    verify_claims: bool = True       # False = draft-only ablation: grounded
                                     # drafting, no claim extraction/checking

    def as_dict(self) -> dict:
        return asdict(self)

run_cfg = RunConfig()


BACKBONE = {
    "model": "gpt-5.4-mini-2026-03-17",
    "temperature": 0.0,
    "reasoning_effort": "none",
}

llm = LLMClient(api_key=OPENAI_API_KEY, **BACKBONE)

scorer = HybridScorer("data/relation_embeddings.npy",
                      "data/relation_names.json",
                      llm=llm, alpha=run_cfg.alpha)

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
