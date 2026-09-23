"""Prove the exclusion-sensitivity checks fire.

Cases 1-2 reinstate the retracted claims verbatim; 3-4 corrupt the measured
range. error-analysis.tex is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
E = ROOT / "journal" / "sections" / "error-analysis.tex"
# The exclusion-SENSITIVITY paragraph moved to Appendix D on 2026-09-23
# (\label{app:sensitivity}) when the manuscript went on a hard page budget,
# while the exclusion and census COUNTS stayed in the body. So this probe
# now spans two files and each case names its own. Nothing about which
# defect a case reinstates changed -- only where the sentence lives.
A = ROOT / "journal" / "sections" / "appendix-measurements.tex"


def sub_once(text, find, repl):
    """Replace `find` even where the 72-column fill broke it across lines.

    Same fix as prove_power.py and prove_abstract.py carry: a literal
    anchor is hostage to the wrap, and the 2026-09-23 shortening moved
    breaks into several of the anchors below.

    NOTE: two anchors here are stale for a different reason and this does
    not rescue them. The census correction of September 2026 changed the
    count of defects the hand-read found beyond the pre-pass from 17 to
    16, and its CWQ share from 14 to 13, so the cases keyed on "$17$ more"
    and "and $14$ on ComplexWebQuestions" no longer match the paper. They
    have been failing since that correction. Re-point them at 16 and 13
    only after checking which defect each case is meant to reinstate.
    """
    pat = r"\s+".join(map(re.escape, find.split()))
    m = re.search(pat, text)
    assert m, f"anchor not found: {find!r}"
    return text[:m.start()] + repl + text[m.end():]

CASES = [
    (A, "reinstate 'roughly the defect rate'",
     "moves each system by between",
     "raises every system by roughly the defect rate and moves each by between"),
    (A, "reinstate the label-defect floor claim",
     "which is a fact",
     "The samples carry a label-defect floor of five per cent. This is a fact"),
    (A, "sensitivity top of range 0.020 -> 0.055 (the defect rate)",
     "and $+0.020$", "and $+0.055$"),
    (A, "sensitivity bottom of range 0.001 -> 0.010",
     "between $+0.001$", "between $+0.010$"),
    # The 57 decomposition: 41 + 17 - 1.
    (E, "reinstate '57 as 22 and 19 reconciled'",
     "All $41$ were removed",
     "and $57$ distinct questions once the one question appearing in both "
     "counts is resolved. All $41$ were removed"),
    (E, "drop the 17 census-found defects",
     "found $17$ more that the pre-pass had missed --- $3$",
     "found some more that the pre-pass had missed --- $3$"),
    (E, "census-defect split 14 -> 15",
     "and $14$ on ComplexWebQuestions", "and $15$ on ComplexWebQuestions"),
    (E, "exclusion total 41 -> 40",
     "All $41$ were removed", "All $40$ were removed"),
]

orig = {p: io.open(p, encoding="utf-8").read() for p in (E, A)}
out = []
try:
    for path, name, find, repl in CASES:
        io.open(path, "w", encoding="utf-8").write(
            sub_once(orig[path], find, repl))
        r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                           cwd=ROOT, capture_output=True, text=True)
        out.append((name, r.returncode,
                    [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]))
        # Restore BOTH between cases, not just the one just written: the
        # cases now span two files, and leaving the previous one corrupted
        # would test a combination no case describes.
        for p, s in orig.items():
            io.open(p, "w", encoding="utf-8").write(s)
finally:
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8").write(s)

for name, rc, fails in out:
    print(f"{'CAUGHT' if rc else 'MISSED'}  {name}")
    for f in fails:
        print(f"          {f}")

r = subprocess.run([sys.executable, "scripts/check_paper_numbers.py"],
                   cwd=ROOT, capture_output=True, text=True)
print(f"\nrestored -> rc={r.returncode}")
passed = all(rc for _, rc, _ in out) and r.returncode == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
