"""Prove check_slides.py catches a hedge rate sold as an error rate.

Case 1 reinstates slide 15 exactly as it shipped:

    AGR hedges on $8.2\\%$ of WebQSP against no-retrieval's $12.2\\%$ error
    rate

12.2 is no-retrieval's hedge_pct -- backup slide 5 prints it under "WebQSP
hedge %" -- and its error rate is 170 wrong out of the 351 questions it
asserts on. The deck's existing check asked only whether "12.2" appears
somewhere, which it does, on the backup slide, correctly labelled. So the
mislabel rode along behind a check that was passing for a different
occurrence of the same string. That is the presence-matching failure this
repository keeps meeting, and case 1 is the proof it is now closed.

The remaining cases attack the replacement. It quotes four values that are
also cells in the ablation table on another slide, so a check that merely
looked for them would pass with the sentence deleted, the datasets swapped,
or the arrow reversed -- each of which is a different claim. All four are
reinstated as separate defects.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
DECK = ROOT / "thesis_presentation" / "content-main.tex"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

orig = io.open(DECK, encoding="utf-8", newline="").read()

# The shipped bullet, and its replacement, whitespace-tolerantly: the deck
# is hard-wrapped and rewrapping it must not silently turn a probe into a
# no-op.
BULLET = re.compile(
    r"\\item\s+Withholds[^\\]*?(?:\\alert\{hedge\}|hedge)[^\n]*"
    r"(?:\n(?!\s*\\item|\s*\\end)[^\n]*)*")


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0] if fail else r.stdout.strip()[-90:])


def replace_bullet(new):
    def go():
        assert BULLET.search(orig), "the verifier hedge bullet moved"
        io.open(DECK, "w", encoding="utf-8", newline="").write(
            BULLET.sub(lambda _: new, orig, count=1))
    return go


SHIPPED = (r"\item Turns silent error into a \alert{hedge}: AGR hedges on"
           "\n            $8.2\\%$ of WebQSP against no-retrieval's "
           r"$12.2\%$ error rate")

REPLACEMENT = (r"\item Withholds what it cannot ground, as a \alert{hedge}:"
               "\n            removing the layer drops hedging "
               r"$23.2\% \to 20.2\%$ on CWQ,"
               "\n            $8.5\\% \\to 8.0\\%$ on WebQSP")

CASES = [
    ("shipped: 12.2% hedge rate sold as an error rate",
     replace_bullet(SHIPPED)),
    ("the isolating comparison deleted entirely",
     replace_bullet(r"\item Withholds what it cannot ground, as a "
                    r"\alert{hedge}")),
    ("datasets swapped: CWQ's delta attributed to WebQSP",
     replace_bullet(REPLACEMENT.replace("on CWQ,", "on WebQSP,")
                    .replace("on WebQSP\n", "on CWQ\n")
                    .replace(r"$8.5\% \to 8.0\%$ on WebQSP",
                             r"$8.5\% \to 8.0\%$ on CWQ"))),
    ("arrow reversed: removing the layer made it hedge more",
     replace_bullet(REPLACEMENT.replace(r"$23.2\% \to 20.2\%$",
                                        r"$20.2\% \to 23.2\%$"))),
    ("a value quietly wrong: 20.2 becomes 20.5",
     replace_bullet(REPLACEMENT.replace("20.2", "20.5"))),
]

out = []
try:
    for name, mutate in CASES:
        mutate()
        rc, first = run()
        out.append((name, rc, first))
        io.open(DECK, "w", encoding="utf-8", newline="").write(orig)
finally:
    io.open(DECK, "w", encoding="utf-8", newline="").write(orig)

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{first[:96]}")

rc, first = run()
print(f"\nrestored -> rc={rc}  ({first[:70]})")
passed = all(rc for _, rc, _ in out) and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
