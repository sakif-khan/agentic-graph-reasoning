r"""Generate transcript-min.tex, the speaking copy: the spoken lines of
transcript.md and nothing else.

transcript.md is the working document. It carries the delivery notes, the
timing table, the backup map and the anticipated questions. This is the copy
held while speaking. For each slide it gives the number, the title and the
time, then the words said. No notes, no tables, no Q&A.

    python build_min.py            # regenerate transcript-min.tex
    python build_min.py --check    # fail if it is out of date
    latexmk -pdf transcript-min.tex
    python build_min.py --pages    # after a build, fail if any slide's
                                   # speech runs across two pages
    python build_min.py --digest   # print the digest the PDF should carry

No slide's speech is split across pages. A section that will not fit in
what is left of a page starts on the next one. The document sets each
section in a box and measures it before placing it, so this holds for any
wording rather than for the wording it was checked against. --pages reads
the page each section starts and ends on from the labels the build wrote.

The .tex carries a digest of itself into the PDF's keywords, so whether the
PDF was built from the current script is a question about content, not
about file dates. Dates answered it wrongly both ways here: a probe that
edits transcript.md and restores it leaves the script newer than a PDF that
is still current, and a fresh clone writes the PDF before the script.
check_slides.py runs --check, --pages and --digest.

The pre-defense speaking copy came from pre-defense-frozen-2026-08-29/,
whose build_min.py borrowed its parser from the build_transcript.py beside
it. Both are frozen with the pre-defense, so this builder carries its own.
"""
import hashlib
import io
import pathlib
import re
import sys
import textwrap

HERE = pathlib.Path(__file__).resolve().parent
MD = HERE / "transcript.md"
OUT = HERE / "transcript-min.tex"
AUX = HERE / "transcript-min.aux"

# A numbered section's heading: "## 17 — Main results *(1:21)* ★".
HEAD = re.compile(r"(\d+) \u2014 (.*?) \*\((\d+:\d\d)\)\*(?:\s*\u2605)?$")

# Characters that mean something else to TeX, replaced in one pass so that
# no replacement is itself escaped by a later one.
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
           "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
           "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}

# The non-ASCII characters this script is known to use, or plausibly will.
# Anything else stops the build, rather than reaching the PDF as a missing
# glyph that nobody sees until it is read aloud.
GLYPHS = {"\u2014": "---", "\u2013": "--", "\u2026": r"\ldots{}",
          "\u201c": "``", "\u201d": "''", "\u2018": "`", "\u2019": "'",
          "\u00a0": "~", "\u2192": r"\(\to\)", "\u00d7": r"\(\times\)",
          "\u2248": r"\(\approx\)", "\u2264": r"\(\leq\)",
          "\u2265": r"\(\geq\)", "\u03ba": r"\(\kappa\)"}


def tex(s):
    """One run of Markdown text, ready for TeX."""
    s = re.sub(r"[\\&%$#_{}~^]", lambda m: SPECIAL[m.group()], s)
    for a, b in GLYPHS.items():
        s = s.replace(a, b)
    odd = sorted({c for c in s if ord(c) > 127})
    if odd:
        sys.exit(f"build_min.py: no rendering for {odd!r} in: {s[:60]!r}")
    # A single quote with no letter before it opens a quotation; one after
    # a letter is an apostrophe, which TeX already sets correctly. This has
    # to run before the double quotes below become `` and '', or the first
    # half of every closing '' after a full stop would turn into an opener.
    s = re.sub(r"(?<![A-Za-z0-9])'", "`", s)
    # Straight double quotes open and close in turn within a paragraph.
    parts = s.split('"')
    if len(parts) % 2 == 0:
        sys.exit(f"build_min.py: unbalanced quotes in: {s[:60]!r}")
    s = "".join(p + ("``" if i % 2 == 0 else "''")
                for i, p in enumerate(parts[:-1])) + parts[-1]
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\emph{\1}", s)
    return s


def sections(md):
    """(number, title, time, paragraphs) for every numbered section.

    The speech is the section's quoted lines. A bare ">" separates its
    paragraphs, and any unquoted line is a delivery note and is dropped.
    """
    out = []
    for part in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = part.partition("\n")
        m = HEAD.match(head.strip())
        if not m:
            continue            # backup map, questions, recovery, delivery
        paras, cur = [], []
        for line in body.splitlines() + [""]:
            text = line[1:].strip() if line.startswith(">") else None
            if text:
                cur.append(text)
            elif cur:
                paras.append(" ".join(cur))
                cur = []
        out.append((m.group(1), m.group(2), m.group(3), paras))
    return out


def tied(s):
    """The last two words tied, so the line they end cannot hold one word."""
    return re.sub(r" (\S+)$", r"~\1", s)


def paragraph(p):
    """One spoken paragraph, ready for TeX and wrapped for a legible diff."""
    return textwrap.fill(tied(tex(" ".join(p.split()))), width=76,
                         break_long_words=False, break_on_hyphens=False)


PREAMBLE = r"""% !TEX root = transcript-min.tex
% =====================================================================
% GENERATED by build_min.py from transcript.md. Do not edit: run
%   python build_min.py
% The speaking copy: each slide's number, title and time, then the words
% said. Everything else in transcript.md is left out.
%
% Build:
%   latexmk -pdf transcript-min.tex
% =====================================================================
\documentclass[12pt,a4paper]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=25mm,headheight=15pt]{geometry}
\usepackage{xcolor}
\usepackage{needspace}
\usepackage{microtype}
\usepackage{fancyhdr}
% The keywords carry a digest of this file. check_slides.py compares it
% with the digest build_min.py would write now, and the PDF is current when
% the two agree.
\usepackage[hidelinks,pdftitle={Defense speaking copy},%
  pdfauthor={Md. Sakif Khan},pdfkeywords={speech digest @DIGEST@}]{hyperref}
% ...and so does the .aux, so build_min.py --pages knows that the page
% labels it reads were written by a build of this file.
\makeatletter
\AtBeginDocument{\immediate\write\@mainaux{\@percentchar\space speech
  digest @DIGEST@}}
\makeatother

\definecolor{agrdark}{RGB}{28,54,78}
\definecolor{agrgrey}{RGB}{110,110,110}

% Read aloud, a word broken across a line is a word said in two halves, so
% nothing hyphenates. A justified line then has only its spaces to give,
% and \emergencystretch lets the odd tight one loosen rather than run into
% the margin.
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=3em

\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\raggedbottom
\clubpenalty=10000
\widowpenalty=10000

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\lhead{\small\color{agrgrey}Defense speaking copy}
\rhead{\small\color{agrgrey}\thepage}

% A slide's heading: its number and title, its time, and a rule. A title
% too long for one line wraps ragged rather than justified, and its last
% two words are tied, so the RQ titles neither stretch across the measure
% nor leave one word on a line. The time stays flush right on the line the
% title ends on: fill glue outranks the fil of \raggedright and takes all
% of that line's slack.
\newcommand{\slidehead}[3]{%
  {\raggedright\color{agrdark}\bfseries\large #1.\ #2%
   \hskip 0pt plus 1fill\relax{\color{agrgrey}\normalfont\small #3}\par}%
  \vspace{-2mm}{\color{agrgrey}\rule{\linewidth}{0.4pt}}\par
  \vspace{1mm}}

% One slide's speech, never split across pages. The section, heading and
% all, is set in a box and measured first. If what is left of the page is
% shorter than the box, \Needspace ends the page and the section starts on
% the next one. The box is then unpacked rather than placed whole, so a
% section longer than a page would still start at the top of one and then
% break there. The space above a heading is inside the box, so it is
% measured too, and it is dropped at the top of a page like any glue.
% The two labels are what build_min.py --pages reads back.
\newcommand{\speech}[4]{%
  \par
  \setbox0=\vbox{\vspace{6mm}\label{s-#1}\slidehead{#1}{#2}{#3}%
    #4\par\label{e-#1}}%
  \Needspace{\dimexpr\ht0+\dp0\relax}%
  \unvbox0\par}

\begin{document}
\thispagestyle{fancy}
{\color{agrdark}\huge\bfseries Defense speaking copy}\par
"""


def build():
    md = io.open(MD, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    secs = sections(md)
    out = [PREAMBLE]
    for n, title, time, paras in secs:
        if not paras:
            sys.exit(f"build_min.py: section {n} has no spoken lines")
        out.append(f"\\speech{{{n}}}{{{tied(tex(title))}}}{{{time}}}{{%")
        out.append("\n\n".join(paragraph(p) for p in paras))
        out.append("}\n")
    out.append(r"\end{document}")
    out.append("")
    text = "\n".join(out)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return text.replace("@DIGEST@", digest), len(secs), digest


def pages(digest):
    """Each section's first and last page, from the labels the build wrote."""
    if not AUX.exists():
        return None, "no transcript-min.aux: build the PDF first"
    aux = AUX.read_text(encoding="utf-8")
    if f"% speech digest {digest}" not in aux:
        return None, "transcript-min.aux is from another version: rebuild"
    found = {}
    for kind, n, page in re.findall(
            r"\\newlabel\{([se])-(\d+)\}\{\{[^{}]*\}\{(\d+)\}", aux):
        found[(kind, int(n))] = int(page)
    return found, ""


def main():
    text, n, digest = build()
    old = io.open(OUT, encoding="utf-8", newline="").read() \
        if OUT.exists() else ""
    if "--digest" in sys.argv:
        print(digest)
        return 0
    if "--pages" in sys.argv:
        found, why = pages(digest)
        if found is None:
            print(why)
            return 1
        nums = sorted({k for _, k in found})
        missing = [k for k in range(1, n + 1)
                   if ("s", k) not in found or ("e", k) not in found]
        split = [(k, found[("s", k)], found[("e", k)]) for k in nums
                 if ("s", k) in found and ("e", k) in found
                 and found[("s", k)] != found[("e", k)]]
        for k, a, b in split:
            print(f"slide {k}'s speech runs from page {a} to page {b}")
        if missing:
            print(f"no page labels for slides {missing}: rebuild")
        last = max(found.values()) if found else 0
        print(("SPLIT -- " if split or missing else "") +
              f"{n - len(split) - len(missing)} of {n} slides' speech each "
              f"on one page ({last} pages)")
        return 1 if split or missing else 0
    eol = "\r\n" if "\r\n" in old else "\n"
    current = old.replace("\r\n", "\n") == text
    if "--check" in sys.argv:
        print(("transcript-min.tex is up to date" if current else
               "STALE -- run: python build_min.py"), f"({n} slides)")
        return 0 if current else 1
    if current:
        print(f"  transcript-min.tex unchanged: {n} slides")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="").write(
        text.replace("\n", eol))
    print(f"  transcript-min.tex regenerated: {n} slides; rebuild the PDF")
    return 0


sys.exit(main())
