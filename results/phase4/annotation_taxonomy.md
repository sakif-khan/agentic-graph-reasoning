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
| `gold_noise` / `ambiguous_question` | see [below](#gold_noise--ambiguous_question-subtypes-from-stage-c) | escaped Stage C's net (should be rare now) |
| `other` | — | genuinely new — flag for discussion |

## `gold_noise` / `ambiguous_question` subtypes (from Stage C)

Stage D's own reading pass never produced a `gold_noise`/`ambiguous_question` subtype breakdown
(both categories were rare here — 1-2 cases each, see distribution below). But Stage C's
per-item consensus-vs-gold adjudication (`prepass_goldnoise_{webqsp,cwq}.json`, ~148 flagged
rows across both datasets) went through exactly this judgment call at much higher volume, and
its `family`/`subtype` fields have since been normalized to this table's category vocabulary
(`family` now only takes values from the left column above). The finer `subtype` values it
produced for these two categories are real and worth keeping as the reference subtype list:

| category | subtype | meaning | n (webqsp+cwq) |
|---|---|---|---:|
| `gold_noise` | `wrong_gold` | gold answer is factually incorrect | 16 |
| `gold_noise` | `incomplete_gold` | gold is missing valid answer(s) that systems correctly found | 16 |
| `gold_noise` | `type_mismatch` | gold answers at the wrong entity type/granularity for what was asked (e.g. gives a city when a country was asked), even though the right type is in the graph | 6 |
| `gold_noise` | `malformed_gold` | gold data is structurally corrupted (e.g. absurd entity counts, MID leakage into the answer strings) | 3 |
| `ambiguous_question` | `temporal` | question's time reference doesn't uniquely pick out gold's answer | 9 |
| `ambiguous_question` | `container_vs_member` | question readable as asking about the container or about its members/instances | 3 |
| `ambiguous_question` | `place_vs_lineage` | "where does X come from" answerable as a literal place or as a lineage/ancestry chain; gold picks one, a reasonable system picks the other | 3 |
| `ambiguous_question` | `malformed_question` | question conflates two or more sub-questions into one (e.g. "who voices X? who composed Y?") | 2 |
| `ambiguous_question` | `birthplace_vs_upbringing` | "where is X from" genuinely ambiguous between birthplace and the place X is most associated with | 1 |
| `ambiguous_question` | `variety` | gold picks one defensible variety/register of an entity (e.g. standard vs. vernacular form) over another equally defensible one | 1 |
| `ambiguous_question` | `place_name` | a named place has genuinely competing referents and gold picks one | 1 |
| `ambiguous_question` | `underdetermined` | catch-all: question doesn't have enough information to determine a single correct answer | 1 |

Normalizing `family` also surfaced a handful of rows where the original label didn't match the
row's own note/verdict (e.g. `type_mismatch` cases filed under a generic relation-mismatch
family when the note said the *gold* had the wrong type, not the system; a two-part
"malformed_question" case filed under a gold-defect family when the defect was in the question).
These were re-filed by content, not by blind string substitution — `verdict` (which is what
`census_exclusions.json` is actually derived from) was untouched and re-verified to still match
exactly.

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
