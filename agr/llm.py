import json, re
from openai import OpenAI

from agr.budget import BudgetExhausted


def strip_fences(text: str) -> str:
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


class LLMClient:
    def __init__(self, model: str, api_key: str, temperature: float = 0.0):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def _chat(self, meter, content: str) -> str:
        if not meter.can("llm"):
            raise BudgetExhausted("llm")
        meter.llm_calls += 1
        resp = self.client.chat.completions.create(
            model=self.model, temperature=self.temperature,
            messages=[{"role": "user", "content": content}])
        meter.prompt_tokens += resp.usage.prompt_tokens
        meter.completion_tokens += resp.usage.completion_tokens
        return resp.choices[0].message.content

    def __call__(self, state: dict, prompt: str, schema_hint: str) -> dict:
        meter = state["budget"]
        raw = strip_fences(self._chat(
            meter, prompt + "\n\nRespond ONLY with JSON matching: "
            + schema_hint))
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            fixed = strip_fences(self._chat(
                meter, "Fix this into valid JSON only, no prose:\n" + raw))
            return json.loads(fixed)
