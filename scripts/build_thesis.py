"""Build the thesis and its appendix volume, and prove they agree.

The two documents reference each other through xr, which reads the
other document's .aux. That makes the build circular: the book cannot
print "Appendix E.3" until the appendix volume has been built, and the
appendix volume cannot print "Section 5.3" until the book has been.
latexmk settles each document against the other's *previous* state, so
one pass over the pair is not enough and no single latexmk invocation
can know that.

So this builds the pair repeatedly until the labels each document
exports stop changing, which is the actual fixed point -- not a fixed
number of rounds, which would be a guess that happens to work. Two
rounds is the normal answer; a structural change to one volume can
need three.

A reference printing as "??" in a finished PDF means this was not run,
or was interrupted: latexmk alone will build each file happily and
leave the cross-volume references stale.

Run: python scripts/build_thesis.py [--rounds N]
Exits non-zero if a build fails, if the pair has not settled, or if
either document ends with a warning that the book is held to zero of:
undefined or multiply-defined references, undefined citations, overfull
or underfull boxes, and missing hyperlink destinations.
"""
import argparse
import io
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOOK = pathlib.Path("thesis_book")
JOBS = ("thesis_book_0421052099", "thesis_book_0421052099_appendices")
MAX_ROUNDS = 4

# What a clean build means here. Each is counted, and any of them
# non-zero fails the run.
WARNINGS = (
    ("undefined reference", re.compile(r"LaTeX Warning: Reference")),
    ("undefined citation", re.compile(r"Citation .* undefined")),
    ("multiply-defined label", re.compile(r"multiply defined")),
    ("overfull box", re.compile(r"^Overfull", re.M)),
    ("underfull box", re.compile(r"^Underfull", re.M)),
    ("missing destination",
     re.compile(r"has been referenced but does not exist")),
)

NEWLABEL = re.compile(r"^\\newlabel\{([^}]*)\}\{\{([^{}]*)\}", re.M)


def exported(job):
    """The label-to-number table the other document will read."""
    aux = BOOK / f"{job}.aux"
    if not aux.exists():
        return None
    text = io.open(aux, encoding="utf-8", errors="replace").read()
    return dict(NEWLABEL.findall(text))


def build(job):
    proc = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
         f"{job}.tex"],
        cwd=BOOK, capture_output=True, text=True, errors="replace")
    return proc.returncode


def report(job):
    """Page count and warning tally from the last pass's .log."""
    log = io.open(BOOK / f"{job}.log", encoding="utf-8",
                  errors="replace").read()
    m = re.search(r"Output written on \S+ \((\d+) pages", log)
    pages = int(m.group(1)) if m else 0
    found = [(name, len(rx.findall(log))) for name, rx in WARNINGS]
    return pages, [(n, c) for n, c in found if c]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=MAX_ROUNDS,
                    help=f"give up after this many rounds (default "
                         f"{MAX_ROUNDS})")
    args = ap.parse_args()

    if not BOOK.is_dir():
        print(f"run from the repository root: {BOOK} is not here")
        return 1

    before = {job: exported(job) for job in JOBS}
    for round_no in range(1, args.rounds + 1):
        for job in JOBS:
            code = build(job)
            if code:
                print(f"round {round_no}: {job} FAILED (latexmk exit {code})")
                print(f"  see {BOOK / (job + '.log')}")
                return 1
            print(f"round {round_no}: {job} built")

        after = {job: exported(job) for job in JOBS}
        moved = {job: sum(1 for k, v in after[job].items()
                          if before[job] is None or before[job].get(k) != v)
                 for job in JOBS}
        if not any(moved.values()):
            print(f"settled after {round_no} round(s): neither document's "
                  f"labels moved")
            break
        print("  labels still moving: "
              + ", ".join(f"{job.split('_')[-1]}={n}"
                          for job, n in moved.items()))
        before = after
    else:
        print(f"NOT SETTLED after {args.rounds} rounds -- the cross-volume "
              f"numbers may be stale")
        return 1

    print()
    bad = 0
    for job in JOBS:
        pages, warnings = report(job)
        note = ("clean" if not warnings else
                ", ".join(f"{c} {n}{'s' if c > 1 else ''}"
                          for n, c in warnings))
        print(f"{job:38s} {pages:4d} pages  {note}")
        bad += sum(c for _, c in warnings)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
