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

Each probe reinstates a defect that actually shipped, verbatim where
possible, runs the relevant checker, and asserts it fails. Then it
restores the file in a `finally` block.

## Running them

```bash
python tests/probes/run_all.py          # all of them
python tests/probes/prove_kappa.py .    # one, repo root as argv[1]
```

Every probe takes the repository root as `sys.argv[1]`.

They are **not** pytest tests and pytest will not collect them — the
filenames do not match `test_*.py`, deliberately. They mutate tracked
files while running, so they are not safe to run concurrently with each
other or with an editor saving over the same paths. If one is interrupted
its `finally` will not run; `git diff` will show what was left behind.

## Reading the output

`ALL CASES CAUGHT` means every reinstated defect was detected. `MISSED`
names a corruption that slipped through, which means the check that was
supposed to cover it is vacuous for that case. A probe that cannot find
its own anchor raises instead — that is a probe bug, not a passing check,
and it is why the anchors are whitespace-tolerant: the `.tex` is
hard-wrapped and its line endings have flipped between LF and CRLF under
git round-trips.
