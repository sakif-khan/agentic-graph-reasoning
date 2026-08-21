"""Prove the highlights tests fire.

Case 1 restores the shipped bullet verbatim -- the unscoped planner claim
that stood while nothing checked this file. The rest exercise the format
rules and the two content rules.

highlights.txt is restored in a finally block.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
HL = ROOT / "thesis_paper" / "highlights.txt"
orig = io.open(HL, encoding="utf-8", newline="").read()

SCOPED = ("- Removing the planner improves accuracy on the shallower "
          "benchmark, cutting tokens 31%")

CASES = [
    ("shipped: planner claim with no dataset scope",
     lambda s: s.replace(
         SCOPED,
         "- Ablation: removing the planner improves accuracy and cuts "
         "tokens by 31%", 1)),
    ("scope dropped, everything else kept",
     lambda s: s.replace("on the shallower benchmark, ", "", 1)),
    ("a bullet over 85 characters",
     lambda s: s.replace(
         SCOPED,
         SCOPED + " on both benchmarks and at lower cost throughout", 1)),
    ("a sixth bullet",
     lambda s: s.replace(
         SCOPED, SCOPED + "\n- One more claim that pushes past five", 1)),
    ("down to two bullets",
     lambda s: "\n".join(
         l for l in s.splitlines()
         if not l.startswith("- ") or l.startswith("- Agentic")
         or l.startswith("- Matches")) + "\n"),
    ("a bullet claiming verification raises accuracy",
     lambda s: s.replace(
         "- Three of four agentic components show no detectable accuracy effect",
         "- Claim-level verification improves answer accuracy measurably", 1)),
    # 44% is deliberate: it IS in the paper, as a clip rate. Presence
    # matching passes it, which is why the token cut is bound to the
    # records instead.
    ("a real percentage from an unrelated claim (44% is a clip rate)",
     lambda s: s.replace("cutting tokens 31%", "cutting tokens 44%", 1)),
    ("the other benchmark's token cut",
     lambda s: s.replace("cutting tokens 31%", "cutting tokens 21%", 1)),
    ("a percentage appearing nowhere in the paper",
     lambda s: s.replace("cutting tokens 31%", "cutting tokens 77%", 1)),
]

out = []
try:
    for name, mutate in CASES:
        txt = mutate(orig)
        assert txt != orig, f"corruption was a no-op: {name}"
        io.open(HL, "w", encoding="utf-8", newline="").write(txt)
        r = subprocess.run([sys.executable, "-m", "pytest",
                            "tests/test_paper_highlights.py", "-q"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode))
        io.open(HL, "w", encoding="utf-8", newline="").write(orig)
finally:
    io.open(HL, "w", encoding="utf-8", newline="").write(orig)

for name, rc in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")

r = subprocess.run([sys.executable, "-m", "pytest",
                    "tests/test_paper_highlights.py", "-q"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}  ({r.stdout.strip().splitlines()[-1]})")
passed = all(rc for _, rc in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
