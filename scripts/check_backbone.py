"""One-shot backbone sanity check: params accepted? hidden tokens zero?"""
from openai import OpenAI
from agr.env import OPENAI_API_KEY

CANDIDATES = [
    # (model, temperature, reasoning_effort)
    ("gpt-4.1-mini", 0.0, None),
    ("gpt-5.4-mini", 0.0, "none"),
]

client = OpenAI(api_key=OPENAI_API_KEY)
for model, temp, effort in CANDIDATES:
    kwargs = dict(model=model,
                  messages=[{"role": "user",
                             "content": "Reply with the JSON {\"ok\": true}"}])
    if temp is not None:
        kwargs["temperature"] = temp
    if effort is not None:
        kwargs["reasoning_effort"] = effort
    try:
        resp = client.chat.completions.create(**kwargs)
        u = resp.usage
        details = getattr(u, "completion_tokens_details", None)
        rtok = getattr(details, "reasoning_tokens", None)
        print(f"[{model}] OK  resolved_model={resp.model}  "
              f"prompt={u.prompt_tokens} completion={u.completion_tokens} "
              f"reasoning_tokens={rtok}")
    except Exception as e:
        print(f"[{model}] FAILED: {e!r}")

for m in client.models.list():
    if "5.4-mini" in m.id or "4.1-mini" in m.id:
        print(m.id)
