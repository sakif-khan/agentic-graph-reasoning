# Stage D — failure taxonomy (annotation reference)

Companion reference for `labels_webqsp.csv` / `labels_cwq.csv`, which label every packet in
`failures_webqsp.md` / `failures_cwq.md`. Each row gets one `category`, an optional `subtype`,
and a one-sentence `note` pinpointing where the trajectory *first* left the correct path
(plan → explored relations → backtracks → verifier) — not the last symptom.

| category | subtypes | meaning |
|---|---|---|
| `decomposition_error` | `over_decomposition`, `paraphrase_drift`, `context_stripping`, `extraction_bug` | planner/draft pipeline caused it |
| `relation_selection` | — | scorer picked the wrong edge |
| `composite_claim` | `conjunction_uncovered`, `no_set_intersection` | multi-constraint handled partially |
| `premature_termination` | `budget`, `evaluator` | stopped before the answer |
| `verifier_fn` / `verifier_fp` | `structural_not_semantic` | passed a wrong claim / hedged a right one |
| `kg_gap` | `date_literal`, `numeric_literal`, `temporal_qualifier`, `ordinal`, `data_error` | environment can't express it |
| `answer_selection` | — | correct candidate retrieved, drafter chose another |
| `echo` | `topic`, `intermediate`, `granularity` | the shared-attractor pattern |
| `gold_noise` / `ambiguous_question` | — | escaped Stage C's net (should be rare now) |
| `other` | — | genuinely new — flag for discussion |

## Notes from this reading pass

- `decomposition_error/extraction_bug` showed up repeatedly on "who is X" / "what is X known
  for" profession-style questions: the evaluator resolved the correct gold values verbatim in
  the answer *text*, but `answer_entities` collapsed to the subject entity itself. Worth a
  dedicated look at the answer/entity-extraction stage.
- A recurring `premature_termination/evaluator` pattern: the correct relation is explored with
  a solid score (0.4–0.7) and the evaluator backtracks away from it anyway, never returning
  before the run hedges. Seen across unrelated questions (government-form-of-X, draft years,
  mascot lookups, conlang types) — looks systemic rather than per-question bad luck.
- A handful of hedges (`other`) show a fully grounded, correct single-hop resolution that the
  drafter still verbally negates ("could not be determined") and zeroes out of
  `answer_entities`. Doesn't fit any existing subtype; flagged for discussion rather than
  forced into `verifier_fn` since no verifier rejection is involved.
- A few `gold_noise`/`ambiguous_question` cases are CWQ template-composition artifacts (garbled
  or self-contradictory question text) rather than classic gold-label noise — distinct enough
  from the WebQSP gold-noise cases to be worth calling out separately if this taxonomy is
  revisited.

## Distribution (this pass)

| category | webqsp | cwq |
|---|---:|---:|
| relation_selection | 24 | 16 |
| composite_claim | 1 | 13 |
| decomposition_error | 10 | 3 |
| kg_gap | 9 | 9 |
| echo | 7 | 2 |
| premature_termination | 5 | 3 |
| answer_selection | 2 | 5 |
| verifier_fn | 3 | 2 |
| ambiguous_question | 2 | 4 |
| gold_noise | 1 | 1 |
| other | 1 | 2 |
| **total** | **65** | **60** |
