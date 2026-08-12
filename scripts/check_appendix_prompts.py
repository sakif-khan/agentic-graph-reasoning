"""Assert that Appendix A still reproduces the prompts the code actually sends.

The appendix quotes each template verbatim. Nothing in the build catches a
divergence: LaTeX cannot know what agr/ contains, and the response cache keys on
prompt text, so an edit to a prompt that is not mirrored in the appendix leaves
the thesis describing a system that no longer exists.

Run after any prompt edit. Exits non-zero on the first mismatch.

Usage: python scripts/check_appendix_prompts.py
"""
import re
import sys
from pathlib import Path

APPENDIX = Path("thesis_book/appendices/prompts.tex")

# constant name -> module it lives in
PROMPTS = {
    "PLANNER_PROMPT": "agr/planner.py",
    "SCORE_PROMPT":   "agr/scorer.py",
    "EVAL_PROMPT":    "agr/nodes.py",
    "DRAFT_PROMPT":   "agr/nodes.py",
    "ENTAIL_PROMPT":  "agr/nodes.py",
    "REWRITE_PROMPT": "agr/nodes.py",
    "ANSWER_PROMPT":  "agr/nodes.py",
    "PROMPT@noretrieval": "agr/baselines/noretrieval.py",
    "PROMPT@vectorrag":   "agr/baselines/vectorrag.py",
    # The agentic baseline's four. These were omitted originally, which made the
    # checker's pass a statement about AGR's prompts only while the appendix
    # claimed to reproduce every prompt in the system. Sec 7.4.4 rests the
    # central comparison on this reimplementation, so these are the prompts a
    # sceptical reader most needs to be able to audit.
    "REL_PRUNE@tog":  "agr/baselines/tog.py",
    "ENT_PRUNE@tog":  "agr/baselines/tog.py",
    "SUFFICIENT@tog": "agr/baselines/tog.py",
    "ANSWER@tog":     "agr/baselines/tog.py",
}


def extract(module, name):
    """Pull one triple-quoted prompt constant out of a source file."""
    src = Path(module).read_text(encoding="utf-8")
    bare = name.split("@")[0]
    m = re.search(rf'^{bare}\s*=\s*"""(.*?)"""', src, re.S | re.M)
    if not m:
        return None
    body = m.group(1)
    # a trailing backslash continues the line in the source but is not sent
    return re.sub(r"\\\n", "", body)


def normalise(text):
    """Compare on content, not on how a line happened to be wrapped."""
    return " ".join(text.split())


# The appendix opens by asserting two properties of the whole set, and a new
# template can falsify either one without changing any template this checker
# already compares -- so verbatim reproduction is not enough to keep that
# paragraph true. Both are checked over every template above.
#
#   1. No template carries a configuration constant. This is what lets one
#      cached response be shared across every condition of the alpha--tau sweep.
#   2. Exactly one template carries a budget figure, and it is EVAL_PROMPT,
#      whose remaining depth and backtracks are substituted at send time. The
#      appendix names it as the sole exception and says why a model that ignores
#      the figures changes nothing.
CONFIG_CONSTANT = re.compile(r"\balpha\b|\btau\b|\{alpha\}|\{tau\}", re.I)
BUDGET_FIGURE = re.compile(
    r"budget|d_left|b_left|max_depth|max_backtracks|max_llm_calls", re.I)
BUDGET_EXCEPTION = "EVAL_PROMPT"


def check_set_properties(bodies):
    """The two set-level claims Appendix A's opening paragraph makes."""
    problems = []
    named = sorted(n for n, b in bodies.items() if CONFIG_CONSTANT.search(b))
    if named:
        problems.append(
            f"a template names a configuration constant: {', '.join(named)}. "
            f"Appendix A's first property, and the cache argument resting on "
            f"it, no longer hold.")
    carriers = sorted(n for n, b in bodies.items() if BUDGET_FIGURE.search(b))
    if carriers != [BUDGET_EXCEPTION]:
        problems.append(
            f"templates carrying a budget figure: {carriers or 'none'}; "
            f"Appendix A says exactly one does and names {BUDGET_EXCEPTION}.")
    return problems


def main():
    tex = normalise(APPENDIX.read_text(encoding="utf-8"))
    missing, ok, bodies = [], 0, {}

    for name, module in PROMPTS.items():
        body = extract(module, name)
        if body is None:
            missing.append(f"{name}: not found in {module}")
            continue
        bodies[name.split("@")[0]] = body
        if normalise(body) in tex:
            ok += 1
        else:
            head = " ".join(body.split())[:70]
            missing.append(f"{name} ({module}) is not reproduced in the "
                           f"appendix\n      starts: {head}...")

    problems = check_set_properties(bodies)

    print(f"prompt templates checked : {len(PROMPTS)}")
    print(f"reproduced verbatim      : {ok}")
    print(f"set properties checked   : 2 (no config constant; one budget "
          f"carrier, {BUDGET_EXCEPTION})")
    for m in missing:
        print(f"  MISMATCH {m}")
    for p in problems:
        print(f"  PROPERTY {p}")
    if missing or problems:
        print("\nAppendix A is out of date with agr/. Update it before building.")
        return 1
    print("Appendix A matches the source, and its two set properties hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
