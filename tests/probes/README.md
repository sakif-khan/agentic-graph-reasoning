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
- a rule spelled `below the no-retrieval` never matched the sentence it
  was written for, which reads `*below* the no-retrieval` — markdown
  emphasis sits inside the phrase. The probe reported CAUGHT anyway,
  because a different check in the same block failed on that corruption
- the candidate widths were checked against the whole deck, so once they
  had a second home the check passed a slide that had dropped them — the
  same shape as the GraphRAG and highlights failures above, on its ninth
  recurrence. Values with more than one home are checked per block now

- the new limitation-order rule ranked the deck's bullets against
  `heads`, a name the transcript-timing block rebinds further down the
  same file to a slide-to-seconds dict. It searched section times for
  "wrongful acceptance" and reported that the thesis ranks nothing. This
  one failed loudly; a rebinding to a *compatible* value would not have
- a `ck` was pulled one level too deep by a careless re-indent and ended
  up inside the `if` that detects the defect, so on a clean document it
  never ran at all. It still failed when a row was short, so every probe
  stayed green; the only signal was the total check count dropping by one
- the token guard `(?![\d.])`, added so that `0.0` stops matching inside
  `40.0`, also rejects a number that ends a sentence — and the strata
  are spoken as "137, 211, and 49." Guarding against a period is not the
  same as guarding against a decimal point, which is `(?!\.\d)`

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

**Five of the probes shell out to `pytest`, which needs a `.env`.**
`tests/conftest.py` imports `agr.runtime` at module scope and `agr/env.py`
raises at import time if any of the four variables is missing, so on a
fresh clone `prove_abstract`, `prove_contract`, `prove_declarations`,
`prove_highlights` and `prove_selfcontained` die with `IndexError: list
index out of range` before testing anything. `cp .env.example .env` and
fill it in; the other twenty-four probes run without it.

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

Whitespace tolerance is not enough for `transcript.md`. It is quoted
speech, so every wrapped line begins with a `>` marker, and `\s+` stops
there.
An anchor that matches today breaks the moment an unrelated edit to the
same paragraph moves the wrap by a few words — which happened to
`prove_contract` and turned it from `CAUGHT` into a raise. Anchors into
the transcript need the marker in the gap: `\s+(?:>\s*)?`.

Nor is whitespace tolerance enough when the anchor **contains a value the
document derives**. `prove_lists` anchored a timing row verbatim,
cumulative column included, and raised the first time an unrelated slide
grew by ten seconds. The corruption a probe applies has to be computed
from the file it is about to corrupt, not written down beside it.

It then happened again in the same file. A second case anchored a section
heading verbatim, `*(1:45)*` included, and raised the moment slide 21 was
re-timed. Both are now self-locating: read the value, then change it.

## What these checks do not catch

**Presence is not order.** Each of the deck's five limitations was
checked to be present and only the first was checked to be in position,
so items 4 and 5 sat swapped against the thesis's severity order — the
order the slide's own comment claimed to follow. A rule about a list has
to rank it, not look each item up.

**A bound satisfied somewhere is not a bound satisfied everywhere.** The
output-contract rule is presence-scoped per document: it asks whether the
document states the bound, and a document that states it in one sentence
and contradicts it in the next still passes. That is the design — where
the bounds live inside an artifact is an editorial matter, and the defect
that shipped was omission, which this does catch. It is not a defence
against a document arguing with itself.
