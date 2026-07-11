import hashlib
import json
import re
from pathlib import Path

from openai import OpenAI

from agr.budget import BudgetExhausted


def strip_fences(text: str) -> str:
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


class LLMClient:
    def __init__(self, model: str, api_key: str,
                 temperature: float | None = 0.0,
                 reasoning_effort: str | None = None,
                 cache_dir: str | None = "cache"):
        """cache_dir=None disables caching (e.g. for the qualification
        script, where you want genuinely live calls)."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def describe(self) -> dict:
        return {"model": self.model, "temperature": self.temperature,
                "reasoning_effort": self.reasoning_effort,
                "cache": str(self.cache_dir) if self.cache_dir else None}

    # ---------------- cache internals ----------------
    def _cache_key(self, content: str) -> str:
        blob = json.dumps({
            "model": self.model,
            "temperature": self.temperature,
            "reasoning_effort": self.reasoning_effort,
            "content": content,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def _cache_read(self, key: str) -> dict | None:
        if not self.cache_dir:
            return None
        p = self.cache_dir / f"{key}.json"
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None          # corrupt entry -> treat as miss

    def _cache_write(self, key: str, record: dict) -> None:
        if not self.cache_dir:
            return
        p = self.cache_dir / f"{key}.json"
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(record, ensure_ascii=False),
                       encoding="utf-8")
        tmp.replace(p)           # atomic-ish on Windows too

    # ---------------- the single chokepoint ----------------
    def _chat(self, meter, content: str) -> str:
        if not meter.can("llm"):
            raise BudgetExhausted("llm")
        meter.llm_calls += 1

        key = self._cache_key(content)
        hit = self._cache_read(key)
        if hit is not None:
            meter.prompt_tokens += hit["usage"]["prompt_tokens"]
            meter.completion_tokens += hit["usage"]["completion_tokens"]
            meter.cache_hits += 1
            return hit["text"]

        kwargs = dict(model=self.model,
                      messages=[{"role": "user", "content": content}])
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort

        resp = self.client.chat.completions.create(**kwargs)
        u = resp.usage
        meter.prompt_tokens += u.prompt_tokens
        meter.completion_tokens += u.completion_tokens

        # hidden-token alarm: contaminates cost metric if ever nonzero
        details = getattr(u, "completion_tokens_details", None)
        rtok = getattr(details, "reasoning_tokens", 0) or 0
        meter.reasoning_tokens += rtok

        text = resp.choices[0].message.content
        self._cache_write(key, {
            "text": text,
            "usage": {"prompt_tokens": u.prompt_tokens,
                      "completion_tokens": u.completion_tokens,
                      "reasoning_tokens": rtok},
            "model": resp.model,           # resolved snapshot, for the record
        })
        return text

    def __call__(self, state: dict, prompt: str, schema_hint: str) -> dict:
        meter = state["budget"]
        full = prompt + "\n\nRespond ONLY with JSON matching: " + schema_hint
        raw = strip_fences(self._chat(meter, full))
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            fixed = strip_fences(self._chat(
                meter, "Fix this into valid JSON only, no prose:\n" + raw))
            return json.loads(fixed)
