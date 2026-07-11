from dataclasses import dataclass, field, asdict
import hashlib, json, time


class BudgetExhausted(Exception):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(f"budget exhausted: {resource}")


@dataclass(frozen=True)
class BudgetConfig:
    max_depth: int = 4
    beam_width: int = 3
    max_backtracks: int = 3
    max_llm_calls: int = 20
    max_verify_iters: int = 2
    max_seconds: float = 300.0
    max_anchors: int = 5

    def config_hash(self) -> str:
        return hashlib.md5(
            json.dumps(asdict(self), sort_keys=True).encode()
        ).hexdigest()[:8]


@dataclass
class BudgetMeter:
    cfg: BudgetConfig
    t0: float = field(default_factory=time.time)
    llm_calls: int = 0
    depth: int = 0
    backtracks: int = 0
    verify_iters: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    cache_hits: int = 0
    exhausted: list = field(default_factory=list)

    def can(self, resource: str) -> bool:
        ok = {
            "llm": self.llm_calls < self.cfg.max_llm_calls,
            "depth": self.depth < self.cfg.max_depth,
            "backtrack": self.backtracks < self.cfg.max_backtracks,
            "verify": self.verify_iters < self.cfg.max_verify_iters,
            "time": time.time() - self.t0 < self.cfg.max_seconds,
        }[resource]
        if not ok and resource not in self.exhausted:
            self.exhausted.append(resource)
        return ok

    def snapshot(self) -> dict:
        return {
            "llm_calls": self.llm_calls, "depth": self.depth,
            "backtracks": self.backtracks, "verify_iters": self.verify_iters,
            "tokens": self.prompt_tokens + self.completion_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "seconds": round(time.time() - self.t0, 1),
            "exhausted": self.exhausted, "cache_hits": self.cache_hits,
        }
