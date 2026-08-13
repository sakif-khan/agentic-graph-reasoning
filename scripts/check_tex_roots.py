"""Every .tex file in the thesis is either a document or knows which one is.

Most of the .tex files here are fragments: a chapter, a tikzpicture, a tabular,
a preamble. Aimed at directly, a fragment stops at "Missing \\begin{document}"
or "Emergency stop", and an editor's build button aims at whatever file is in
front of you. A `% !TEX root' line on each fragment redirects that build to the
document that \\inputs it.

The repository holds three documents -- the book and two decks -- so a workspace
cannot resolve the root by looking for the one file with a \\documentclass. The
directive is the only thing that disambiguates.

Run: python scripts/check_tex_roots.py
Exits non-zero if any fragment is unrooted, points at a file that is not there,
or points at something that is not a document.
"""
import io
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MODULES = ("thesis_book", "thesis_presentation")
ROOT = re.compile(r"^\s*%\s*!TEX\s+root\s*=\s*(\S+)", re.I | re.M)
HEAD = 5          # the directive has to be near the top to be honoured


COMMENT = re.compile(r"(?<!\\)%.*$", re.M)


def uncomment(text):
    return COMMENT.sub("", text)


def isdocument(path):
    """A document is the file carrying \\begin{document}, not \\documentclass.

    preamble.tex has the \\documentclass and is still not buildable, which is
    exactly the distinction that matters here.

    Comments are stripped first, and not as a nicety: preamble.tex and both
    content files explain in their headers that they have "no
    \\begin{document}", and a plain substring search reads that sentence as
    proof of the opposite and declares all three documents.
    """
    try:
        return "\\begin{document}" in uncomment(io.open(
            path, encoding="utf-8", errors="replace").read())
    except OSError:
        return False


def main():
    bad = []
    docs, frags = [], []
    for mod in MODULES:
        for p in sorted(pathlib.Path(mod).rglob("*.tex")):
            text = io.open(p, encoding="utf-8", errors="replace").read()
            if isdocument(p):
                docs.append(p)
                continue
            frags.append(p)
            head = "\n".join(text.split("\n")[:HEAD])
            m = ROOT.search(head)
            if not m:
                bad.append(f"{p.as_posix()}: fragment with no % !TEX root "
                           f"in its first {HEAD} lines")
                continue
            target = (p.parent / m.group(1)).resolve()
            if not target.exists():
                bad.append(f"{p.as_posix()}: root {m.group(1)} does not exist")
            elif not isdocument(target):
                bad.append(f"{p.as_posix()}: root {m.group(1)} is itself not "
                           f"a document")

    print(f"{len(docs)} document(s), {len(frags)} fragment(s)")
    for d in docs:
        print(f"  [DOC ] {d.as_posix()}")
    if bad:
        print(f"\n{len(bad)} problem(s):")
        for b in bad:
            print("  " + b)
        return 1
    print(f"\nevery one of the {len(frags)} fragments names a document that "
          f"exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
