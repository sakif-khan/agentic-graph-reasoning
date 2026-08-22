"""A standalone comment sits at the indent of the code around it.

Four times in three rounds a comment landed one step deeper than its
neighbours -- always inside the block being edited, and always found by
someone reading the diff rather than by anything running. The cause is
mechanical: a patch anchored on a line's first non-whitespace character
keeps that line's existing indent and prepends the replacement's own, so
four spaces plus four spaces makes eight. It parses, so nothing objected.

The bound is deliberately narrow: exactly one indent step deeper than the
code on both sides. Comments aligned to a continuation -- under a `def`'s
wrapped signature, or inside a bracketed literal -- sit further in than
that on purpose, and stay outside the rule rather than needing a
suppression comment. A rule that has to be silenced in ordinary code is a
rule that gets silenced everywhere.
"""
import io
import pathlib
import tokenize

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
STEP = 4
SKIP = ("__pycache__", ".git", "thesis_templates", ".venv", "venv")


def sources():
    return sorted(p for p in ROOT.rglob("*.py")
                  if not any(s in p.parts for s in SKIP))


def where(path):
    """Repo-relative if it is in the repo, bare name otherwise.

    Not a nicety: checking the rule against past versions of a file means
    running it on a blob written to a temporary directory, and
    relative_to raises on anything outside ROOT.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def strays(path):
    """Standalone comments one step deeper than the code either side.

    `code` holds the indent of every line that STARTS a logical one, so
    the neighbours are looked up by line number. Continuation lines are
    not indentation and must not be measured against: the first version
    recorded them, so a comment sitting under a wrapped call was compared
    to that call's hanging indent and the real drift went unflagged.

    A comment run between two code lines is measured against those two,
    not against the comments beside it -- otherwise a whole block that
    drifted together would agree with itself and pass.
    """
    with io.open(path, "rb") as f:
        try:
            toks = list(tokenize.tokenize(f.readline))
        except (tokenize.TokenError, SyntaxError, IndentationError):
            return []

    SKIPPED = (tokenize.NL, tokenize.INDENT, tokenize.DEDENT,
               tokenize.ENDMARKER, tokenize.ENCODING)
    code, comments, fresh, depth = {}, [], True, 0
    for t in toks:
        row, col = t.start
        if t.type == tokenize.NEWLINE:
            fresh = True
        elif t.type == tokenize.COMMENT:
            # Inside brackets a comment annotates an element of the
            # literal it sits in, and one step past the statement that
            # opens the bracket is exactly where it belongs. Every
            # annotated CASES list in tests/probes/ looks like that, so
            # without this the rule reports about sixty of them.
            if depth == 0 and not t.line[:col].strip():
                comments.append((row, col, t.string))
        elif t.type not in SKIPPED:
            if t.type == tokenize.OP and t.string in "([{":
                depth += 1
            elif t.type == tokenize.OP and t.string in ")]}":
                depth = max(0, depth - 1)
            if fresh:
                code[row] = col
                fresh = False

    rows = sorted(code)
    out = []
    for row, col, text in comments:
        before = [r for r in rows if r < row]
        after = [r for r in rows if r > row]
        if not before or not after:
            continue
        neighbour = max(code[before[-1]], code[after[0]])
        if col - neighbour == STEP:
            out.append(f"{where(path)}:{row}: "
                       f"col {col} against {neighbour} -- {text[:56]}")
    return out


@pytest.mark.parametrize("path", sources(), ids=lambda p: p.name)
def test_no_comment_is_indented_past_its_neighbours(path):
    bad = strays(path)
    assert not bad, (
        "these comments sit one indent step deeper than the code on both "
        "sides, which is what a mis-anchored patch leaves behind:\n  "
        + "\n  ".join(bad))
