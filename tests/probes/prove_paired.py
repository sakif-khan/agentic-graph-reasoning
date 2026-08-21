"""Prove the hedge-difference answer is held to the paired records.

Case 1 reinstates the shipped sentence: "Correctness moved on exactly one
of the 398 paired questions, so at least five of those six were assertions
that would have been wrong." Two errors and an omission. Correctness moved
on two of 398, one per dataset -- "one" is the CWQ-only figure set against
the pooled denominator. None of the six came back correct, not five, so
the available claim was stronger than the written one. And the omission
that mattered: on WebQSP the single question the layer hedged on is one
the ablated run got right, which is the counter-example to the whole
answer and went unmentioned.

The anticipated-questions section was the one part of this material bound
to nothing, which is where the error was written and why it survived.

Cases 2-6 remove each half of the corrected answer in turn. Case 7 moves
the records under it: a question the ablated run hedged and the full
system asserted breaks the nesting the answer claims as a fact.

The transcript and one ablation record file are restored in a finally
block.
"""
import io
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
ABL = ROOT / "results" / "phase4" / "ablations" / "test_cwq_half_abl_noverifier.jsonl"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

if not ABL.exists():
    print("ablation records absent")
    sys.exit(0)

FILES = (SCRIPT, ABL)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0][:88] if fail else "")


def edit(path, old, new):
    def go():
        pattern = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


CURRENT = (
    "The sets nest — there is no question the ablated run hedged on that the "
    "full system asserted on — so those are exactly the six the ablated run "
    "answered and the layer declined to. None of the six came back correct: "
    "all six were assertions that would have been wrong, which is the "
    "mechanism, seen at the only place the design isolates it. On WebQSP it "
    "is one question, and there the ablated run got it right. So across the "
    "398 paired questions correctness moved twice, once each way.")
SHIPPED = (
    "so the layer declined to assert on six questions the ablated system "
    "answered. Correctness moved on exactly one of the 398 paired questions, "
    "so at least five of those six were assertions that would have been "
    "wrong — which is the mechanism, seen at the only place the design "
    "isolates it.")


def unhedge_one():
    """Make the ablated run hedge where the full system asserts.

    Blanks one answer that the full run also answers, which creates a
    question in the other direction and breaks the nesting.
    """
    def go():
        lines = orig[ABL].splitlines(keepends=True)
        out, done = [], False
        for line in lines:
            if not done and line.strip():
                rec = json.loads(line)
                if rec.get("answer_entities"):
                    rec["answer_entities"] = []
                    line = json.dumps(rec) + "\n"
                    done = True
            out.append(line)
        assert done, "no asserted record to blank"
        io.open(ABL, "w", encoding="utf-8", newline="").write("".join(out))
    return go


CASES = [
    ("shipped: one of 398, and at least five of six", edit(SCRIPT, CURRENT,
                                                          SHIPPED)),
    ("the nesting claim is dropped",
     edit(SCRIPT, "The sets nest — there is no question the ablated run "
                  "hedged on that the full system asserted on — so those",
          "Those")),
    ("'none of the six came back correct' is softened",
     edit(SCRIPT, "None of the six came back correct:",
          "Most of the six came back wrong:")),
    ("the WebQSP counter-example is dropped",
     edit(SCRIPT, "On WebQSP it is one question, and there the ablated run "
                  "got it right.", "")),
    ("the pooled denominator is wrong",
     edit(SCRIPT, "across the 398 paired questions", "across the 400 paired "
                                                     "questions")),
    ("correctness 'moved twice' becomes 'moved once'",
     edit(SCRIPT, "correctness moved twice", "correctness moved once")),
    ("the records stop nesting and the answer does not follow",
     unhedge_one()),
]

rc, first = run()
assert rc == 0, f"not clean before the probe: {first}"

out = []
try:
    for name, mutate in CASES:
        mutate()
        rc, first = run()
        out.append((name, rc, first))
        restore()
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{first[:96]}")

rc, first = run()
print(f"\nrestored -> rc={rc}  ({first[:70]})")
passed = all(rc for _, rc, _ in out) and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
