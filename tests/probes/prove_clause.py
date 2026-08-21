"""The abstract's verification rule must fire on overclaims, and only those.

Scored against two earlier versions of the rule, so the output shows what
each change bought rather than asserting it:

  window   the original: a +-120-character window around each mention of
           verification. Measures distance; the rule is about grammatical
           subject. The real abstract cleared it by five characters.
  clause   split on clause boundaries, require both in one clause. Fixes
           the false alarms but loses a subject to its own appositive.
  +elide   drop parentheticals first, rejoining subject to verb.

Reads the rule's own regexes from tests/test_paper_abstract.py rather than
restating them, so a change there is scored here instead of drifting.
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
spec = importlib.util.spec_from_file_location(
    "t", ROOT / "tests" / "test_paper_abstract.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

REAL = " ".join(t.words()).lower()


def window(text):
    for m in re.finditer(r"verification|verify|claim check", text):
        w = text[max(0, m.start() - 120):m.end() + 120]
        if re.search(r"improv\w*\s+accuracy|rais\w*\s+accuracy"
                     r"|accuracy\s+gain", w):
            return True
    return False


def clause(text, elide=False):
    src = t.elide_parentheticals(text) if elide else text
    for c in t.CLAUSE.split(src):
        if not t.VERIFY.search(c):
            continue
        g = t.GAIN.search(c)
        if not g:
            continue
        if t.NEGATED.search(c[:g.start()]):
            continue
        return True
    return False


FLAG = {
    "appositive between subject and verb":
        "claim verification, which checks each claim against the traversed "
        "triples, improves accuracy",
    "short appositive":
        "claim verification, applied before emission, improves accuracy on "
        "both benchmarks",
    "plain subject-verb": "claim verification improves accuracy measurably",
    "the layer spelled out":
        "the structural verification layer raises accuracy on both benchmarks",
    "reversed construction":
        "we observe an accuracy gain from claim verification",
    "boosts": "claim verification boosts accuracy by four points",
}
OK = {
    "the real abstract": REAL,
    "real, planner clause trimmed":
        REAL.replace("while cutting tokens by 31", "cutting tokens 31"),
    "real, em dashes written as commas":
        REAL.replace("components including claim verification show",
                     "components, including claim verification, show"),
    "null stated plainly": "claim verification does not improve accuracy",
    "null, other phrasing":
        "we find no accuracy gain from claim verification",
    "gain belongs to another component, verification in an aside":
        "removing the planner, our decomposition step, improves accuracy "
        "while claim verification shows no detectable accuracy effect",
    "gain belongs to another component, verification negated":
        "the explorer improves accuracy, and claim verification, which runs "
        "after it, does not",
}

RULES = [("window", lambda s: window(s)),
         ("clause", lambda s: clause(s, elide=False)),
         ("+elide", lambda s: clause(s, elide=True))]

errs = {n: 0 for n, _ in RULES}
print(f"  {'case':58s} {'want':5s} " + " ".join(f"{n:7s}" for n, _ in RULES))
for name, s in list(FLAG.items()) + list(OK.items()):
    want = name in FLAG
    cells = []
    for n, f in RULES:
        got = f(s)
        errs[n] += got != want
        cells.append(("FLAG" if got else "ok") + ("*" if got != want else ""))
    print(f"  {name:58s} {'FLAG' if want else 'ok':5s} "
          + " ".join(f"{c:7s}" for c in cells))
print(f"\n  {'errors':58s} {'':5s} "
      + " ".join(f"{errs[n]:<7d}" for n, _ in RULES))
print("  * = wrong answer")

live = errs["+elide"]
print(f"\nThe rule as shipped in tests/test_paper_abstract.py is '+elide'.")
print("CLAUSE RULE IS SOUND" if live == 0
      else f"CLAUSE RULE IS WRONG on {live} case(s)")
sys.exit(1 if live else 0)
