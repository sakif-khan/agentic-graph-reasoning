"""The manuscript's build log must be clean, fresh, and complete.

thesis_paper/README.md sets the bar as "0 overfull, 0 underfull, 0 warnings
of any class", and that last phrase is the whole point of this script. The
bar was breached without anyone noticing: adding \\corref to designate the
corresponding author put elsarticle markup into the string hyperref builds
for the PDF's /Author field, and every build after that printed four
"Token not allowed in a PDF string" warnings. They survived because the
check was a grep for "LaTeX Warning" and "Overfull", and these say
"Package hyperref Warning". A checker that has to be told each warning's
wording only ever catches the ones already known about.

So this looks for the word itself, and refuses three ways of passing that
are not the same as being clean:

  * a log that is not there -- an unbuilt document is not a quiet one;
  * a log built from sources that have since been edited, which reports
    the previous draft;
  * a log that stops before the run finished, which reports part of one.

Run, after latexmk:  python scripts/check_paper_log.py
Optionally on another log:  python scripts/check_paper_log.py path/to.log
Exits non-zero if the log is missing, stale, truncated, or carries a
diagnostic of any kind.
"""
import hashlib
import io
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAPER = ROOT / "thesis_paper"
DEFAULT_LOG = PAPER / "agr-paper.log"

# Sources the log is measured against, for the fallback below. Only what
# TeX actually reads: highlights.txt is submitted separately and compiles
# nowhere, so a change to it does not make a log stale.
SOURCES = ("*.tex", "sections/*.tex", "figures/*.tex", "*.bib")

# latexmk's own record of what it read and what it hashed to:
#   "sections/setup.tex" 1787308041 9659 fae4d53c...4f0 ""
# Preferred over comparing modification times, and not for tidiness. The
# first version of this script compared mtimes, and a scratch script that
# rewrote preamble.tex with identical contents deadlocked it: the file
# looked newer, so this demanded a rebuild, and latexmk -- which decides
# by hash -- had nothing to do and would not perform one. Content is the
# question actually being asked.
#
# The digest is of the file with CRLF normalised to LF, because latexmk
# reads in text mode: on this repository, where agr-paper.tex and the
# sections flip line endings across a stash or a checkout, hashing the raw
# bytes disagreed with latexmk about five files whose recorded size it
# matched exactly. Normalising is also the answer to the right question --
# a line-ending flip changes no character TeX sets.
FDB = re.compile(r'^\s+"([^"]+)" \d+ \d+ ([0-9a-f]{32}) ')
FDB_SOURCE = (".tex", ".bib")

# A log line carries a diagnostic if it names one. Kept deliberately broad
# -- "warning" in any case, anywhere on the line -- because the class of
# thing being looked for is "wording nobody predicted".
DIAGNOSTIC = [
    ("error", re.compile(r"^! ")),
    ("warning", re.compile(r"\bwarnings?\b", re.I)),
    ("box", re.compile(r"^(?:Over|Under)full \\[hv]box\b")),
    ("glyph", re.compile(r"^Missing character:")),
]

# Package identification banners are not diagnostics, and two of them name
# themselves after the messages they provide: "Package: infwarerr ...
# Providing info/warning/error messages". Every such line begins with one
# of these labels, and no real warning does -- "Class elsarticle Warning:"
# is not "Class: ".
BANNER = re.compile(r"^(?:Package|File|Class|Document Class|Language|"
                    r"LaTeX2e|LaTeX Info|LaTeX Font Info):")

# pdftex prints this last and only on a completed run.
WRITTEN = re.compile(r"^Output written on .*\((\d+) pages?, \d+ bytes\)")

# TeX hard-wraps the log at max_print_line, which is 79 by default, with no
# continuation marker: a line of exactly that length is the first half of
# something. It is not a nicety. "Output written on <path>/agr-paper.pdf"
# runs past 79 as soon as the output directory is anywhere but here, so the
# summary above splits mid-word -- which is how the first version of this
# script declared every out-of-tree build incomplete. The same break can
# fall inside a warning.
#
# Joining is the conservative direction for a search: a genuine 79-column
# line merged with its neighbour still contains everything either of them
# said, at the cost of the two being reported as one.
WRAP = 79


def newest_source():
    newest, where = 0.0, None
    for pattern in SOURCES:
        for p in PAPER.glob(pattern):
            if p.stat().st_mtime > newest:
                newest, where = p.stat().st_mtime, p
    return newest, where


def stale_sources(fdb):
    """Sources whose contents no longer match what the build hashed.

    Absolute paths are TeX Live's own files and are skipped; so is
    everything that is not a .tex or .bib, because the .aux and .bbl the
    run reads are rewritten by the run itself and would always disagree.
    """
    changed = []
    for line in io.open(fdb, encoding="utf-8", errors="replace"):
        m = FDB.match(line)
        if not m:
            continue
        name, digest = m.group(1), m.group(2)
        if pathlib.PurePath(name).is_absolute() or name[1:2] == ":":
            continue
        if not name.lower().endswith(FDB_SOURCE):
            continue
        p = (PAPER / name).resolve()
        if not p.exists():
            changed.append(f"{name} (read by the build, now missing)")
        elif hashlib.md5(p.read_bytes().replace(b"\r\n", b"\n")) \
                .hexdigest() != digest:
            changed.append(name)
    return changed


def unwrap(text):
    """The log as logical lines, each with the line number it starts on."""
    out, buf, start = [], "", 1
    for n, line in enumerate(text.splitlines(), 1):
        if not buf:
            start = n
        buf += line
        if len(line) != WRAP:
            out.append((start, buf))
            buf = ""
    if buf:
        out.append((start, buf))
    return out


def scan(lines):
    """Every logical line that reports something, with its number and kind."""
    found = []
    for n, line in lines:
        if BANNER.match(line):
            continue
        for kind, pattern in DIAGNOSTIC:
            if pattern.search(line):
                found.append((n, kind, line.strip()))
                break
    return found


def main(argv):
    log = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_LOG

    if not log.exists():
        print(f"no log at {log}")
        print("  Build it first: cd thesis_paper && latexmk -pdf agr-paper.tex")
        print("  A missing log is not a clean one.")
        return 1

    fdb = log.with_suffix(".fdb_latexmk")
    if fdb.exists():
        changed = stale_sources(fdb)
        if changed:
            print(f"{log.name} was built from different sources:")
            for c in changed:
                print(f"  {c}")
            print("  It describes the previous draft. Rebuild, then re-run "
                  "this.")
            return 1
    else:
        # No latexmk record -- a bare pdflatex run. Modification time is
        # all that is left, and it over-reports: a file rewritten with
        # identical contents reads as an edit.
        newest, where = newest_source()
        if where is not None and log.stat().st_mtime < newest:
            print(f"{log.name} is older than "
                  f"{where.relative_to(ROOT).as_posix()}, and there is no "
                  f"{fdb.name} to check contents against")
            print("  It may describe the previous draft. Rebuild with "
                  "latexmk, then re-run this.")
            return 1

    lines = unwrap(io.open(log, encoding="utf-8", errors="replace").read())

    m = next((WRITTEN.match(l) for _, l in lines if WRITTEN.match(l)), None)
    if not m:
        print(f"{log.name} records no completed run "
              f"(no 'Output written on' line)")
        print("  The build stopped early; whatever it did not reach is "
              "unchecked.")
        return 1
    pages = int(m.group(1))

    found = scan(lines)
    if found:
        print(f"{len(found)} diagnostic(s) in {log.name}:\n")
        for n, kind, line in found:
            print(f"  {log.name}:{n}  [{kind}] {line}")
        print("\nthesis_paper/README.md asks for none of any class.")
        return 1

    print(f"{log.name}: {pages} pages, no errors, no warnings of any class, "
          f"no over/underfull boxes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
