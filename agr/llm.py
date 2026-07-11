import json, re
from openai import OpenAI

from agr.budget import BudgetExhausted


def strip_fences(text: str) -> str:
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


class LLMClient:
    def __init__(self, model: str, api_key: str,
                 temperature: float | None = 0.0,
                 reasoning_effort: str | None = None):
        """
        temperature=None      -> parameter omitted (for models that reject it)
        reasoning_effort=None -> parameter omitted (for non-reasoning models
                                 like gpt-4.1-mini, which reject it)
        For gpt-5.4-mini use reasoning_effort="none" EXPLICITLY -- never rely
        on the server-side default staying "none".
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort

    def describe(self) -> dict:
        return {"model": self.model, "temperature": self.temperature,
                "reasoning_effort": self.reasoning_effort}

    def _chat(self, meter, content: str) -> str:
        if not meter.can("llm"):
            raise BudgetExhausted("llm")
        meter.llm_calls += 1

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
