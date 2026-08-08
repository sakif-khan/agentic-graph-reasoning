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


def main():
    tex = normalise(APPENDIX.read_text(encoding="utf-8"))
    missing, ok = [], 0

    for name, module in PROMPTS.items():
        body = extract(module, name)
        if body is None:
            missing.append(f"{name}: not found in {module}")
            continue
        if normalise(body) in tex:
            ok += 1
        else:
            head = " ".join(body.split())[:70]
            missing.append(f"{name} ({module}) is not reproduced in the "
                           f"appendix\n      starts: {head}...")

    print(f"prompt templates checked : {len(PROMPTS)}")
    print(f"reproduced verbatim      : {ok}")
    for m in missing:
        print(f"  MISMATCH {m}")
    if missing:
        print("\nAppendix A is out of date with agr/. Update it before building.")
        return 1
    print("Appendix A matches the source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
