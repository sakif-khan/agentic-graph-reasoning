"""Indentation a mis-anchored patch left behind.

The cause is mechanical and has produced nine instances across five
commits: a patch anchored on a line's first non-whitespace character
keeps that line's existing indent and prepends the replacement's own, so
four spaces plus four makes eight, and eleven plus eleven makes
twenty-two. The result parses, so nothing objected; every one of the
nine was found by a person reading a diff.

The drift takes two shapes and needs two rules, because neither shape is
visible to the other's:

  A standalone comment one indent step deeper than the code on both
  sides. Four of these -- check_slides.py:1515 and :1544, then :1618,
  then :1647 -- one per round, always inside the block being edited.

  An element of a bracketed literal at exactly twice its siblings'
  column. Five of these: units() in test_output_contract_claims.py, two
  CASES entries in prove_residuals.py, one in prove_lists.py, and
  TARGETS in run_all.py. Invisible to the comment rule twice over, being
  code rather than a comment and sitting inside brackets, where that
  rule deliberately stops looking. Two of the five survived six commits.

Both bounds are narrow on purpose -- exactly one step, exactly twice --
and narrowness is what lets these run over every Python file in the
repository without a single suppression. Comments aligned to a
continuation sit further in than one step; a dict value wrapped onto its
own line sits one step past its key, not at twice it. Both are correct
code and both stay outside the rules rather than being silenced inside
them. A rule that has to be silenced in ordinary code is a rule that
gets silenced everywhere.
"""
import collections
import io
import pathlib
import tokenize

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
STEP = 4
SKIP = ("__pycache__", ".git", "thesis_templates", ".venv", "venv")

IGNORE = (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
          tokenize.ENDMARKER, tokenize.ENCODING, tokenize.COMMENT)
OPEN, CLOSE = "([{", ")]}"


def sources():
    return sorted(p for p in ROOT.rglob("*.py")
                  if not any(s in p.parts for s in SKIP))


def where(path):
    """Repo-relative if it is in the repo, bare name otherwise.

    Not a nicety: checking a rule against past versions of a file means
    running it on a tree extracted to a temporary directory, and
    relative_to raises on anything outside ROOT.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def read(path):
    with io.open(path, "rb") as f:
        try:
            return list(tokenize.tokenize(f.readline))
        except (tokenize.TokenError, SyntaxError, IndentationError):
            return []


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
    SKIPPED = (tokenize.NL, tokenize.INDENT, tokenize.DEDENT,
               tokenize.ENDMARKER, tokenize.ENCODING)
    code, comments, fresh, depth = {}, [], True, 0
    for t in read(path):
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
            if t.type == tokenize.OP and t.string in OPEN:
                depth += 1
            elif t.type == tokenize.OP and t.string in CLOSE:
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


def doublings(path):
    """Elements of a bracketed literal at twice their siblings' column.

    Siblings are per bracket instance, not per depth. Pooling by depth
    puts two unrelated calls' continuation lines in one group, and the
    modal column of that mixture means nothing.

    A line counts as an element only if the last token before it opened
    the bracket or was a comma directly inside it. Everything else on a
    fresh line continues the element above -- a dict value under its key,
    a second string in an implicit concatenation -- and is indented
    relative to that element, not to the list. Without this distinction
    the rule reports the wrapped-value shape, which is correct code and
    common: prove_clause.py alone writes it six times.

    The modal column must be held by at least two lines. One sibling
    apiece is not a convention to depart from, and calling the smaller of
    two columns the norm would flag whichever happened to be larger.
    """
    groups = collections.defaultdict(list)
    stack, prev, nth, seen = [], None, 0, None
    for t in read(path):
        if t.type in IGNORE:
            continue
        row, col = t.start
        closing = t.type == tokenize.OP and t.string in CLOSE
        # A closing delimiter dedents to its statement and is not an
        # element of the literal it ends.
        if row != seen and stack and not closing:
            if prev in (("open", stack[-1]), ("comma", stack[-1])):
                groups[stack[-1]].append((row, col))
        seen = row
        if t.type == tokenize.OP and t.string in OPEN:
            nth += 1
            stack.append(nth)
            prev = ("open", nth)
        elif closing:
            if stack:
                stack.pop()
            prev = ("token", None)
        elif t.type == tokenize.OP and t.string == "," and stack:
            prev = ("comma", stack[-1])
        else:
            prev = ("token", None)

    out = []
    for items in groups.values():
        counts = collections.Counter(col for _, col in items)
        modal, held = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if held < 2 or modal == 0:
            continue
        for row, col in items:
            if col == 2 * modal:
                out.append(f"{where(path)}:{row}: "
                           f"col {col} = 2 x {modal}")
    return sorted(out)


@pytest.mark.parametrize("path", sources(), ids=lambda p: p.name)
def test_no_comment_is_indented_past_its_neighbours(path):
    bad = strays(path)
    assert not bad, (
        "these comments sit one indent step deeper than the code on both "
        "sides, which is what a mis-anchored patch leaves behind:\n  "
        + "\n  ".join(bad))


@pytest.mark.parametrize("path", sources(), ids=lambda p: p.name)
def test_no_element_sits_at_twice_its_siblings_indent(path):
    bad = doublings(path)
    assert not bad, (
        "these lines sit at exactly twice the column of the other elements "
        "in the same literal, which is a patch's indent added to the one "
        "already there:\n  " + "\n  ".join(bad))
