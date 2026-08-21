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


def main():
    before = tracked_dirty()
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
