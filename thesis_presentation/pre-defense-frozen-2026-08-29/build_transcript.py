r"""Generate transcript.tex from transcript.md.

transcript.md is the source of truth for the rehearsal script. The .tex was
a hand-made typeset copy of it, and the header of that file said to
"regenerate by hand after editing the Markdown -- there is no automated
build step from .md to .tex". Three resectionings later the two had drifted
by nine sections, and nothing in the project could see it: every rule reads
the Markdown, so a .tex a whole restructure behind stayed green. This is
that build step.

    python build_transcript.py           # regenerate transcript.tex
    python build_transcript.py --check   # fail if it is out of date

WHAT IS GENERATED AND WHAT IS NOT
The preamble -- documentclass through the title block -- is authored in
transcript.tex and left exactly as found; it carries long comments about
why the `slide` environment is a minipage and why \markright is issued
outside it, and none of that belongs in a generator. Everything after the
BODY sentinel is derived. Running this never touches a line above it.

Wrapped at 76 columns so the generated file reads like the hand-written
one it replaces, and so a diff of two runs is legible.
"""
import io
import pathlib
import re
import sys
import textwrap

HERE = pathlib.Path(__file__).resolve().parent
MD = HERE / "transcript.md"
TEX = HERE / "transcript.tex"

SENTINEL = ("% ===================================================="
            "=================\n"
            "% BODY -- GENERATED FROM transcript.md BY "
            "build_transcript.py.\n"
            "% Do not edit below this line; edit the Markdown and "
            "regenerate.\n"
            "% ===================================================="
            "=================")

RULE = "% " + "=" * 69

# Characters that mean something else to TeX. Backslash first, or the
# replacements introduced for the others get mangled in turn.
ESCAPES = [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
           ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
           ("}", r"\}"), ("^", r"\textasciicircum{}")]

# Typography this document actually uses. Kept short on purpose: a
# generator that silently rewrites characters it was not asked about is
# how a quotation stops being a quotation.
GLYPHS = [("\u2014", "---"), ("\u2013", "--"), ("\u2026", r"\ldots{}"),
          ("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"),
          ("\u2019", "'"), ("\u2248", r"\(\approx\)"),
          ("\u2192", r"\(\to\)"), ("\u00d7", r"\(\times\)"),
          ("\u2605", r"\ensuremath{\bigstar}"), ("\u03ba", r"\(\kappa\)")]


def esc(s):
    """One run of plain text, ready for TeX."""
    # "~35 s" is an approximation, not a tie -- and it is the only ~ in
    # this document. It has to be recognised before ~ is escaped as a
    # character and substituted after, or the backslashes this inserts
    # are escaped in their turn: the first version of this emitted
    # "\{}(\{}sim\{})15~s" and cost two overfull boxes to notice.
    s = re.sub(r"~(\d+)\s*s\b", "\x00\\1\x01", s)
    for a, b in ESCAPES:
        s = s.replace(a, b)
    s = s.replace("~", r"\textasciitilde{}")
    s = s.replace("\x00", r"\(\sim\)").replace("\x01", "~s")
    for a, b in GLYPHS:
        s = s.replace(a, b)
    # Non-breaking spaces where a number and its unit must not part.
    s = re.sub(r"(\d) (wpm|min|s\b)", r"\1~\2", s)
    return s


def inline(s):
    """Markdown inline markup -> TeX, code spans protected first.

    Escaping happens before the markup is turned into commands, so the
    backslashes this function introduces are never escaped in turn.
    """
    out = []
    for i, part in enumerate(re.split(r"(`[^`]*`)", s)):
        if i % 2:
            out.append(r"\texttt{" + esc(part[1:-1]) + "}")
        else:
            t = esc(part)
            t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t, flags=re.S)
            t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\textit{\1}", t,
                       flags=re.S)
            out.append(t)
    return "".join(out)


def wrap(s, indent=""):
    return textwrap.fill(s, width=76, initial_indent=indent,
                         subsequent_indent=indent,
                         break_long_words=False, break_on_hyphens=False)


def paras(text):
    """Blank-line-separated paragraphs, each flattened to one line."""
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", text.strip())
            if p.strip()]


# ---------------------------------------------------------------- parsing
def split_sections(md):
    """(heading, body) for every ## heading, in order."""
    parts = re.split(r"^## ", md, flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(),
             p.split("\n", 1)[1] if "\n" in p else "") for p in parts]


def blocks(body):
    """A section's body as ('speech'|'note', text) in order."""
    out = []
    for chunk in re.split(r"\n\s*\n", body.strip()):
        chunk = chunk.strip()
        if not chunk or chunk == "---":
            continue
        if chunk.startswith(">"):
            kind, text = "speech", "\n".join(
                l[1:].strip() if l.startswith(">") else l
                for l in chunk.splitlines())
        else:
            kind, text = "note", chunk
        if out and out[-1][0] == kind == "speech":
            out[-1] = (kind, out[-1][1] + "\n\n" + text)
        else:
            out.append((kind, text))
    return out


def md_table(text):
    """Rows of the first Markdown table in `text`, header dropped."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


# ---------------------------------------------------------------- emitting
def emit_timing(rows):
    out = [r"\begin{center}", r"\small",
           r"\begin{tabular}{@{}cL{82mm}rr@{}}", r"  \toprule",
           r"  \textbf{\#} & \textbf{Slide} & \textbf{Slide time} "
           r"& \textbf{Cumulative} \\", r"  \midrule"]
    for n, title, t, cum in rows:
        out.append(f"  {n:<3s}& {inline(title)} & {t} & {cum} \\\\")
    out += [r"  \bottomrule", r"\end{tabular}", r"\end{center}"]
    return out


def emit_backup(rows):
    out = [r"\begin{center}", r"\small",
           r"\begin{tabular}{@{}cL{50mm}L{78mm}@{}}", r"  \toprule",
           r"  \textbf{Page} & \textbf{Contents} & "
           r"\textbf{Use when asked} \\", r"  \midrule"]
    for page, what, when in rows:
        out.append(f"  {page} & {inline(what)} &")
        out.append(wrap(inline(when), "    ") + r" \\")
    out += [r"  \bottomrule", r"\end{tabular}", r"\end{center}"]
    return out


def emit_bullets(text):
    items = re.split(r"^- ", text.strip(), flags=re.M)[1:]
    out = [r"\begin{itemize}[leftmargin=*,itemsep=4pt,topsep=2pt]"]
    for it in items:
        out.append(wrap(r"\item " + inline(" ".join(it.split())), "  ")
                   .replace("  \\item", "  \\item", 1))
    out.append(r"\end{itemize}")
    return out


def emit_slide(num, title, time, star, body):
    head = (f"\\begin{{slide}}{'*' if star else ''}{{{num}}}"
            f"{{{inline(title)}}}{{{time}}}")
    out = [RULE, head, ""]
    for kind, text in blocks(body):
        out.append(f"\\begin{{{kind}}}")
        out.append("\n\n".join(wrap(inline(p)) for p in paras(text)))
        out.append(f"\\end{{{kind}}}")
    out += [r"\end{slide}", ""]
    return out


def build():
    md = io.open(MD, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    body = []

    # -- everything before the first "## " heading: intro, table, note --
    front = md.split("\n## ", 1)[0]
    front = front.split("\n", 1)[1]                     # drop the # title
    before, after = re.split(r"^\| # \| Slide \|.*?(?=\n\n)", front,
                             flags=re.M | re.S)[0], None
    tail = front[len(before):]
    body += [wrap(inline(p)) + "\n" for p in paras(before)]
    body += emit_timing(md_table(tail))
    body.append("")
    rest = re.sub(r"^\|.*$", "", tail, flags=re.M).strip()
    body += [wrap(inline(p)) + "\n" for p in paras(rest)]

    # -- the numbered slide sections ----------------------------------
    n_slides = 0
    for head, sec in split_sections(md):
        m = re.match(r"(\d+) — (.*?) \*\((\d+:\d\d)\)\*(\s*\u2605)?$", head)
        if m:
            n_slides += 1
            body += emit_slide(m.group(1), m.group(2), m.group(3),
                               bool(m.group(4)), sec)
            continue
        name = head.split(" — ")[0].strip()
        body += [RULE, f"\\plainhead{{{inline(name)}}}", ""]
        if name == "Backup slides":
            intro = re.split(r"^\|", sec, flags=re.M)[0]
            body += [wrap(inline(p)) + "\n" for p in paras(intro)]
            body += emit_backup(md_table(sec))
            body.append("")
            outro = re.sub(r"^\|.*$", "", sec, flags=re.M)
            outro = "\n".join(outro.splitlines()[len(paras(intro)) and 0:])
            for p in paras(outro):
                if p not in paras(intro):
                    body.append(wrap(inline(p)) + "\n")
        elif "- " in sec:
            pre, lst = sec.split("\n- ", 1)
            body += [wrap(inline(p)) + "\n" for p in paras(pre)]
            body += emit_bullets("- " + lst.split("\n\n")[0])
            body.append("")
            for p in paras("\n\n".join(("- " + lst).split("\n\n")[1:])):
                body.append(wrap(inline(p)) + "\n")
        else:
            body += [wrap(inline(p)) + "\n" for p in paras(sec)]

    body += [r"\end{document}", ""]
    return "\n".join(body), n_slides


def main():
    old = io.open(TEX, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in old else "\n"
    flat = old.replace("\r\n", "\n")
    if SENTINEL in flat:
        head = flat.split(SENTINEL)[0]
    else:
        # First run: the body begins after the title block.
        head = flat.split(r"\vspace{7mm}", 1)[0] + "\\vspace{7mm}\n\n"
    text, n = build()
    new = head + SENTINEL + "\n\n" + text

    if "--check" in sys.argv:
        ok = flat == new
        print(("transcript.tex is up to date" if ok else
               "STALE -- run: python build_transcript.py"), f"({n} slides)")
        return 0 if ok else 1
    io.open(TEX, "w", encoding="utf-8", newline="").write(
        new.replace("\n", eol))
    print(f"  transcript.tex regenerated: {n} slides")
    return 0


sys.exit(main())
