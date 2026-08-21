# Probes: proof that the checks can fail

`scripts/check_paper_numbers.py` and `tests/test_paper_*.py` assert things
about the manuscript. A check that cannot fail is indistinguishable from a
clean document, and several of these could not, at first:

- the line-number detector reported `0` on a document that *had* line
  numbers, because the numbers outvoted the prose when it computed the
  margin from all spans
- the GraphRAG check went vacuous the moment `41` acquired a second home
  elsewhere in the paper
- the highlights check passed a bullet quoting `44%` as a token cut,
  because `44%` is a real clip rate somewhere else
- `prove_abstract` itself reconstructed its "shipped state" by reading
  `HEAD`, so it stopped corrupting anything the moment the fix landed —
  and went on reporting `CAUGHT`
- the build log was declared clean for several rounds while carrying four
  `Package hyperref Warning` lines, because the check was a grep for
  `LaTeX Warning` and `Overfull`

Each probe reinstates a defect that actually shipped, verbatim where
possible, runs the relevant checker, and asserts it fails. Then it
restores the file in a `finally` block.

## Running them

```bash
python tests/probes/run_all.py          # all of them
python tests/probes/prove_kappa.py .    # one, repo root as argv[1]
```

Every probe takes the repository root as `sys.argv[1]` and exits non-zero
if any corruption slipped through, so `&&` and CI both work. `run_all.py`
additionally fails if a probe leaked a modification.

**Four of the probes shell out to `pytest`, which needs a `.env`.**
`tests/conftest.py` imports `agr.runtime` at module scope and `agr/env.py`
raises at import time if any of the four variables is missing, so on a
fresh clone `prove_abstract`, `prove_declarations`, `prove_highlights` and
`prove_selfcontained` die with `IndexError: list index out of range`
before testing anything. `cp .env.example .env` and fill it in; the other
twelve probes run without it.

**`prove_log` needs a LaTeX toolchain**, because three of its cases are
only visible in a build: it reinstates the defect in `preamble.tex` and
runs `latexmk` for each, into a temporary directory so the tracked
`agr-paper.pdf` is never touched. That is about thirty seconds of
`run_all.py`'s six and a half minutes. It also needs the manuscript to have
been built already, since two more cases age and truncate the real log.

They are **not** pytest tests and pytest will not collect them — the
filenames do not match `test_*.py`, deliberately.

## Do not run them against a dirty tree

A probe reads the file it is about to corrupt, mutates it, checks that the
checker fails, and writes back **what it read**. If what it read was
already corrupt — because an earlier probe was interrupted, or because
something else was mid-edit — then the corruption is what gets restored,
and it survives every later run. `run_all.py` prints a warning when a file
the probes touch is already modified, and lists anything left behind
afterwards, but `git diff` is the authority. They are likewise not safe to
run concurrently with each other or with an editor saving over the same
paths.

## Reading the output

`ALL CASES CAUGHT` means every reinstated defect was detected. `MISSED`
names a corruption that slipped through, which means the check that was
supposed to cover it is vacuous for that case. A probe that cannot find
its own anchor raises instead — that is a probe bug, not a passing check,
and it is why the anchors are whitespace-tolerant: the `.tex` is
hard-wrapped and its line endings have flipped between LF and CRLF under
git round-trips.
