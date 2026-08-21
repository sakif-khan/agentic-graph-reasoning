"""Prove the limitations roster fires on every entry.

Deletes each limitation's paragraph in turn and asserts the checker fails.
A roster that cannot detect a deletion is a list, not a contract.
discussion.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
D = ROOT / "thesis_paper" / "sections" / "discussion.tex"

# One distinctive phrase per limitation, mutilated in place.
PHRASES = [
    "questions per dataset", "one backbone", "trajectory stability",
    "reachability", "no effect detected", "English factoid",
    "Wrongful acceptance is unmeasured", "cannot be audited",
    "identical access", "radius-bounded", "given, not linked",
    "homonyms merge", "unmeasured floor", "0.6995",
    "single-annotator", "after its outcome was known",
]

orig = io.open(D, encoding="utf-8").read()
out = []
try:
    for ph in PHRASES:
        # Whitespace-tolerant: the .tex is hard-wrapped, so "after its
        # outcome was known" straddles a newline and a literal search
        # misses it -- the same hazard the checker collapses whitespace for.
        # IGNORECASE to match the checker, which lowercases both sides.
        # Without it the probe left "One backbone." standing while removing
        # "one backbone", and reported a miss that was the probe's own.
        pat = re.compile(re.escape(ph).replace(r"\ ", r"\s+"), re.IGNORECASE)
        # EVERY non-comment occurrence, not just the first. "one backbone"
        # and "single-annotator" each appear twice, so blanking one left the
        # other standing and the probe reported a miss that was its own.
        spans = []
        for m in pat.finditer(orig):
            line_start = orig.rfind("\n", 0, m.start()) + 1
            if not orig[line_start:m.start()].lstrip().startswith("%"):
                spans.append(m.span())
        assert spans, f"{ph!r} not found outside a comment"
        cur, shift = orig, 0
        for a, b in spans:
            cur = cur[:a + shift] + "XXREMOVEDXX" + cur[b + shift:]
            shift += len("XXREMOVEDXX") - (b - a)
        io.open(D, "w", encoding="utf-8").write(cur)
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((ph, r.returncode))
finally:
    io.open(D, "w", encoding="utf-8").write(orig)

for ph, rc in out:
    print(f"  {'CAUGHT' if rc else 'MISSED':7s} removing {ph!r}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
passed = all(rc for _, rc in out) and r.returncode == 0
print("ALL LIMITATIONS ENFORCED" if passed else "SOME LIMITATION NOT ENFORCED")
sys.exit(0 if passed else 1)
