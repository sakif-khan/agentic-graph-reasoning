class MockLLM:
    """Scripted stand-in for LLMClient; same call signature."""

    def __init__(self, script):
        self.script, self.i = script, 0

    def __call__(self, state, prompt, schema_hint):
        state["budget"].llm_calls += 1
        out = self.script[min(self.i, len(self.script) - 1)]
        self.i += 1
        return out
