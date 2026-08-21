"""Prove scripts/check_paper_log.py fires.

Three cases are shipped defects reinstated verbatim, each rebuilt for real:

  1. the \\corref markup reaching hyperref's PDF-string builder -- four
     "Package hyperref Warning: Token not allowed in a PDF string", which
     is the miss this checker exists because of;
  2. \\url without xurl -- the unbreakable repository URL that
     thesis_paper's README records as a 0.68pt overfull box surviving at
     any document length. It reproduces, but as an *underfull* box of
     badness 2564: \\emergencystretch=1em was added to the preamble after
     that note was written, and it now stretches the line rather than
     letting it overrun. Same defect, opposite diagnostic, which is
     itself the argument for matching the checker's own [box] label here
     rather than a remembered wording;
  3. \\affiliation without lmodern -- the "Font shape ... size <>"
     warnings the same README records.

Between them they cover the three shapes a narrower grep gets wrong:
"Package ... Warning", an over/underfull box, "LaTeX Font Warning".

The other four cases are the ways a log can be clean and still say
nothing: absent, describing sources that have since changed, dated before
its sources with no latexmk record to check contents against, truncated.

Every build goes to a temporary directory, so thesis_paper/agr-paper.pdf
and its log are never touched. The two tracked files this mutates,
preamble.tex and sections/setup.tex, are restored in a finally -- their
modification times along with their contents, for the reason given below.
"""
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
PAPER = ROOT / "thesis_paper"
PRE = PAPER / "preamble.tex"
SETUP = PAPER / "sections" / "setup.tex"
CHECK = ROOT / "scripts" / "check_paper_log.py"
LOG = PAPER / "agr-paper.log"

if not LOG.exists():
    print(f"no log at {LOG} -- build the manuscript first, since half of "
          f"what this probe does is age and truncate it")
    print("SOME CASE MISSED")
    sys.exit(1)

orig = io.open(PRE, encoding="utf-8", newline="").read()

# Rewriting a file updates its modification time, and this probe rewrites
# preamble.tex three times and setup.tex once. The checker compares
# contents where it can, so the times matter only on the fallback path --
# but they matter there, and leaving them bumped would fail that path for
# the rest of the session on a defect this probe invented. Both are put
# back with the contents.
stamps = {p: (p.stat().st_atime, p.stat().st_mtime) for p in (PRE, SETUP)}


def restore():
    io.open(PRE, "w", encoding="utf-8", newline="").write(orig)
    for p, t in stamps.items():
        os.utime(p, t)

# Tolerant of either line ending: this file has been through enough
# stash/checkout round-trips for a literal multi-line anchor to be a
# liability.
HOOK = re.compile(r"\\pdfstringdefDisableCommands\{%.*?\r?\n\}\r?\n", re.S)


def check(log_path):
    r = subprocess.run([sys.executable, str(CHECK), str(log_path)],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def build_with(mutate):
    """Apply a mutation to preamble.tex, build out of tree, check that log."""
    def go():
        text = mutate(orig)
        assert text != orig, "mutation changed nothing -- anchor missed"
        io.open(PRE, "w", encoding="utf-8", newline="").write(text)
        out = tempfile.mkdtemp(prefix="agr-probe-log-")
        try:
            subprocess.run(["latexmk", "-pdf", "-f", "-outdir=" + out,
                            "agr-paper.tex"], cwd=PAPER,
                           capture_output=True, text=True)
            return check(pathlib.Path(out) / "agr-paper.log")
        finally:
            restore()
            shutil.rmtree(out, ignore_errors=True)
    return go


def absent():
    return check(PAPER / "no-such-file.log")


def stale():
    """Edit a source without rebuilding -- the log now describes a draft
    that no longer exists.

    A real content change, not a touched timestamp: the checker compares
    the sources against the digests latexmk recorded, so a file rewritten
    with identical bytes is correctly not stale and moving a timestamp
    proves nothing.
    """
    text = io.open(SETUP, encoding="utf-8", newline="").read()
    io.open(SETUP, "w", encoding="utf-8", newline="").write(
        text + "% a sentence added after the build\n")
    try:
        return check(LOG)
    finally:
        io.open(SETUP, "w", encoding="utf-8", newline="").write(text)
        os.utime(SETUP, stamps[SETUP])


def no_record():
    """The modification-time fallback, for a log with no latexmk record.

    A bare pdflatex run leaves no .fdb_latexmk, so contents cannot be
    compared and age is all there is. The log is copied somewhere without
    one and dated to the epoch.
    """
    out = tempfile.mkdtemp(prefix="agr-probe-norec-")
    try:
        copy = pathlib.Path(out) / "agr-paper.log"
        shutil.copyfile(LOG, copy)
        os.utime(copy, (0, 0))
        return check(copy)
    finally:
        shutil.rmtree(out, ignore_errors=True)


def truncated():
    """A log that stops before pdftex writes its last line.

    Built from the real one so it is a genuine prefix rather than a
    plausible-looking fake, and cut at the first page so nothing after it
    can supply the missing summary.
    """
    text = io.open(LOG, encoding="utf-8", errors="replace").read()
    cut = text.index("\n[1") if "\n[1" in text else len(text) // 2
    fd, path = tempfile.mkstemp(suffix=".log", prefix="agr-probe-cut-")
    os.close(fd)
    try:
        io.open(path, "w", encoding="utf-8").write(text[:cut])
        return check(pathlib.Path(path))
    finally:
        os.unlink(path)


CASES = [
    ("shipped: \\corref markup reaches the PDF string", "hyperref",
     build_with(lambda s: HOOK.sub("", s))),
    ("shipped: the repository URL without xurl", "[box]",
     build_with(lambda s: s.replace(r"\usepackage{xurl}",
                                    r"%\usepackage{xurl}", 1))),
    ("shipped: \\affiliation without a scalable family", "Font",
     build_with(lambda s: s.replace(r"\usepackage{lmodern}",
                                    r"%\usepackage{lmodern}", 1))),
    ("no log at all", "no log at", absent),
    ("a source edited since the build", "built from different sources",
     stale),
    ("no latexmk record, and the log predates the sources", "older than",
     no_record),
    ("log cut off before the run finished", "no completed run", truncated),
]

out = []
try:
    for name, want, run in CASES:
        rc, text = run()
        right = want.lower() in text.lower()
        out.append((name, rc, right, want,
                    next((l.strip() for l in text.splitlines()
                          if want.lower() in l.lower()),
                         (text.strip().splitlines() or ["(silent)"])[0])))
finally:
    restore()

for name, rc, right, want, line in out:
    verdict = "CAUGHT" if rc and right else "MISSED"
    print(f"{verdict:7s}  {name}")
    print(f"{'':9s}rc={rc}  names {want!r}: {'yes' if right else 'NO'}")
    print(f"{'':9s}{line[:96]}")

back_rc, back_text = check(LOG)
print(f"\nrestored -> rc={back_rc}  ({back_text.strip().splitlines()[0]})")
passed = all(rc and right for _, rc, right, _, _ in out) and back_rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
