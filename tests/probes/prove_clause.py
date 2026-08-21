"""The abstract's verification rule must fire on overclaims, and only those.

Calls tests/test_paper_abstract.verification_credited_with_gain directly --
the same function the test asserts on, elide call and all. An earlier
version of this probe imported the regexes and rebuilt the composition
itself, so the line that invokes the elide was never exercised: deleting
it from the test left this probe still reporting a sound rule.

Cases are scored in two shapes, because the bug that mattered only
appeared in one of them. A bare sentence has two commas; the abstract's
sentence has three, and the extra one is a coordinate ", and that ..."
that an earlier elide consumed before reaching the real appositive.
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
spec = importlib.util.spec_from_file_location(
    "t", ROOT / "tests" / "test_paper_abstract.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

REAL = " ".join(t.words()).lower()
# The clause the real abstract uses to talk about verification. Replacing
# it puts a case inside the genuine sentence, with its real comma count.
SLOT = ("and that three of four components including claim verification "
        "show no detectable accuracy effect")
assert SLOT in REAL, "the abstract's verification clause moved; update SLOT"


def in_abstract(fragment):
    return REAL.replace(SLOT, fragment)


FLAG = {
    "appositive between subject and verb":
        "claim verification, which checks each claim against the traversed "
        "triples, improves accuracy",
    "short appositive":
        "claim verification, applied before emission, improves accuracy",
    "noun appositive":
        "claim verification, our checking step, improves accuracy",
    "plain subject-verb": "claim verification improves accuracy measurably",
    "the layer spelled out":
        "the structural verification layer raises accuracy on both benchmarks",
    "reversed construction":
        "we observe an accuracy gain from claim verification",
    "boosts": "claim verification boosts accuracy by four points",
}
OK = {
    "the real abstract, untouched": None,
    "null stated plainly": "claim verification does not improve accuracy",
    "null, other phrasing":
        "we find no accuracy gain from claim verification",
    "gain belongs to another component":
        "the explorer improves accuracy, and claim verification, which runs "
        "after it, does not",
    "verification in a kept aside":
        "removing the planner, which claim verification supports, improves "
        "accuracy",
    "components list, as the abstract writes it":
        "three of four components, including claim verification, show no "
        "detectable accuracy effect",
}

rows, errs = [], 0
print(f"  {'case':52s} {'want':5s} {'bare':6s} {'in abstract':11s}")
for name, frag in list(FLAG.items()) + list(OK.items()):
    want = name in FLAG
    if frag is None:
        got = (t.verification_credited_with_gain(REAL) is not None,) * 2
    else:
        got = (t.verification_credited_with_gain(frag) is not None,
               t.verification_credited_with_gain(in_abstract(frag)) is not None)
    cells = [("FLAG" if g else "ok") + ("*" if g != want else "") for g in got]
    errs += sum(g != want for g in got)
    print(f"  {name:52s} {'FLAG' if want else 'ok':5s} "
          f"{cells[0]:6s} {cells[1]:11s}")

print(f"\n  {'errors':52s} {'':5s} {errs}")
print("  * = wrong answer;  'in abstract' substitutes the case into the "
      "paper's own sentence")

print("\nCLAUSE RULE IS SOUND" if errs == 0
      else f"\nCLAUSE RULE IS WRONG on {errs} case(s)")
sys.exit(1 if errs else 0)
