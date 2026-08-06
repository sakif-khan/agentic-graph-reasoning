# Stage D — failure taxonomy (annotation reference)

Companion reference for `labels_webqsp.csv` / `labels_cwq.csv`, which label every packet in
`failures_webqsp.md` / `failures_cwq.md`. Each row gets one `category`, an optional `subtype`,
and a one-sentence `note` pinpointing where the trajectory *first* left the correct path
(plan → explored relations → backtracks → verifier) — not the last symptom.

Convention for the verifier categories: the verifier's *positive* class is "claim is
supported". A **false negative** is therefore a claim wrongly **rejected** (hedged a right
one); a **false positive** is a claim wrongly **accepted** (passed a wrong one). This is
the standard convention, and it is the one the Stage D labels use.

| category | subtypes | meaning |
|---|---|---|
| `decomposition_error` | `over_decomposition`, `paraphrase_drift`, `context_stripping`, `extraction_bug` | planner/draft pipeline caused it |
| `relation_selection` | — | scorer picked the wrong edge |
| `composite_claim` | `conjunction_uncovered`, `no_set_intersection` | multi-constraint handled partially |
| `premature_termination` | `budget`, `evaluator` | stopped before the answer |
| `verifier_fn` / `verifier_fp` | `structural_not_semantic` | hedged a right one / passed a wrong claim |
| `kg_gap` | `date_literal`, `numeric_literal`, `temporal_qualifier`, `ordinal`, `data_error` | environment can't express it |
| `answer_selection` | — | correct candidate retrieved, drafter chose another |
| `echo` | `topic`, `intermediate`, `granularity` | the shared-attractor pattern |
| `gold_noise` / `ambiguous_question` | see [below](#gold_noise--ambiguous_question-subtypes-from-stage-c) | a defect in the gold or the question that Stage C did not catch |
| `other` | — | fits none of the categories above |

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
Each of these was re-filed against the content of its own note. The `verdict` field, from which
`census_exclusions.json` is derived, was left unchanged.

One row, `WebQTrn-64_d8e43a02200cfdff82052f8cc5395b27` (cwq), was adjudicated during this
cleanup rather than left as originally filed: Stage C had called it `gold_ok`/`echo` (multiple
systems, including AGR, converged on "Tupac Shakur" and the consensus reasoning treated that as
an echo-of-topic mistake against a fine gold). On review, the question literally asks for "the
actor's name," and gold ("Bishop") is a character name from a *different* role Tupac Shakur
plays in the same film — a `type_mismatch` gold defect, and AGR's answer is correct. Flipped to
`verdict: gold_wrong` / `family: gold_noise` / `subtype: type_mismatch` in
`prepass_goldnoise_cwq.json`, added to `census_exclusions.json`, and the matching row in
`labels_cwq.csv` (found independently during the Stage D reading, also as `gold_noise`) had its
subtype and note tightened to match. This is the case the `gold_noise`/`ambiguous_question` row
of the taxonomy table exists to catch: a gold defect that survived Stage C and was picked up in
the Stage D reading.

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

Both datasets are now full censuses (no sampling): webqsp 43W+22H, cwq 70W+87H (the cwq
population dropped from 71W after `WebQTrn-64_d8e43a...` was adjudicated as gold noise and
excluded). The cwq column below reflects the complete 157-row read, not the earlier 40W+20H
stratified sample.

| category | webqsp | cwq |
|---|---:|---:|
| composite_claim | 1 | 40 |
| relation_selection | 24 | 39 |
| kg_gap | 9 | 30 |
| answer_selection | 2 | 12 |
| ambiguous_question | 2 | 8 |
| decomposition_error | 10 | 7 |
| echo | 7 | 6 |
| other | 1 | 5 |
| gold_noise | 1 | 4 |
| verifier_fn | 3 | 3 |
| premature_termination | 5 | 3 |
| **total** | **65** | **157** |

The shape flipped sharply once cwq went to full coverage: `composite_claim` and `kg_gap` are now
cwq's dominant categories (both barely present in webqsp), consistent with cwq's questions being
multi-hop/multi-constraint by construction — `composite_claim` catches the dropped-constraint
failures, `kg_gap` catches the internal numeric IDs (netflix_id, tvrage_id, thetvdb_id, ISO
codes) and superlatives ("smallest", "latest", "earliest") that recur constantly in cwq's
question templates but rarely in webqsp's.
