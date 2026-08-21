"""Run every probe and summarise.

Each probe reinstates a defect that shipped, asserts the relevant checker
catches it, and restores the file. See README.md in this directory.

Exits non-zero if any probe reports a miss, raises, or leaves the working
tree dirty in a file it touched -- the last because an interrupted probe
skips its `finally` and quietly leaves a corruption behind.
"""
import io
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]

PASS = re.compile(r"ALL CASES CAUGHT|ALL CAUGHT|ALL LIMITATIONS ENFORCED"
                  r"|PROBE PASSED|RULE IS SOUND")


def tracked_dirty():
    r = subprocess.run(["git", "status", "--porcelain"],
                       cwd=ROOT, capture_output=True, text=True)
    return {l[3:].strip() for l in r.stdout.splitlines() if l.strip()}


# What the probes mutate. Dirt here before a run is worth saying out loud:
# a probe reads the current contents as its pristine state and restores
# exactly that, so an existing corruption gets preserved rather than
# reverted, and every later run bakes it in further.
TARGETS = ("thesis_paper/", "scripts/check_paper_numbers.py",
           "tests/test_paper_", "thesis_presentation/content-main.tex",
           "thesis_presentation/transcript.md",
           "thesis_book/chapters/introduction.tex",
           "thesis_book/chapters/conclusion.tex",
           "thesis_book/chapters/results.tex",
           "thesis_book/figures/fig_hop_strata.tex",
           "agr/baselines/tog.py", "agr/baselines/graphrag.py",
           "results/phase4/thesis_numbers.json")


def main():
    before = tracked_dirty()
    at_risk = sorted(f for f in before if f.startswith(TARGETS))
    if at_risk:
        print("NOTE: these are already modified, and the probes will treat")
        print("their current contents as the state to restore:")
        for f in at_risk:
            print(f"  {f}")
        print("If any of that is a leftover corruption rather than your own")
        print("edit, revert it first -- otherwise it becomes permanent.\n")

    probes = sorted(HERE.glob("prove_*.py"))
    if not probes:
        print("no probes found")
        return 1

    results = []
    for p in probes:
        r = subprocess.run([sys.executable, str(p), str(ROOT)],
                           cwd=ROOT, capture_output=True, text=True)
        tail = [l for l in r.stdout.splitlines() if l.strip()]
        verdict = tail[-1].strip() if tail else "(no output)"
        ok = r.returncode == 0 and bool(PASS.search(verdict))
        if r.returncode != 0:
            verdict = (r.stderr.strip().splitlines() or ["failed"])[-1][:90]
        results.append((p.name, ok, verdict))
        print(f"  [{'OK  ' if ok else 'FAIL'}] {p.name:24s} {verdict}")

    after = tracked_dirty()
    leaked = after - before
    if leaked:
        print("\nprobes left these modified -- a probe did not restore:")
        for f in sorted(leaked):
            print(f"  {f}")

    bad = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} probes pass")
    return 1 if bad or leaked else 0


if __name__ == "__main__":
    sys.exit(main())
