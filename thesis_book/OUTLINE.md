# Thesis Outline — Table of Contents

**Title:** Agentic Graph Reasoning: Autonomous Knowledge Graph Navigation for Fact
Verification and Hallucination Mitigation in Large Language Models

**Target:** 60–90 pages of body text. The per-chapter estimates below total **87 pages**
(front matter is roman-numbered and does not count against the budget).

> **Status: planning record, not a specification.** This file was the plan the book was
> written against, and the framing directives in it are still the reason many sections are
> shaped the way they are — which is why it is kept. It is **no longer authoritative on
> structure**: the book has moved past it in several places (§3.3.4 on KBQA-o1 and §8.4 on
> the clipped/unclipped split are new; §5.5, §5.6 and §7.2 were restructured; §9.3, §9.5
> and §10.3 renumbered; `premature_termination`'s subtypes went from "all 8 evaluator" to
> 5 + 3). **Where this file and the built PDF disagree, the PDF is correct.** The Page
> Budget section at the end *is* maintained against each build and is the one part to
> trust for numbers.

Structural conventions follow `thesis_templates/buetcsepgthesis.pdf` (the approved
UNN thesis): a heavily sub-sectioned Introduction that ends with *Our Contribution* and
*Thesis Organization*, a separate *Preliminaries* chapter for concepts the reader must
have before the technical chapters, and a Conclusion that walks the reader back through
the thesis chapter by chapter before opening the future-work discussion.

## Numbers

Every figure Chapters 7–9 state comes from `results/phase4/thesis_numbers.json`, generated
by `scripts/build_thesis_numbers.py` from the scoring, groundedness, judge, and census
artifacts. Numbers are not transcribed from the logs by hand, and that file is regenerated
rather than edited. Each block records the artifact it was parsed from, so a rerun that
changes a value identifies the sentences depending on it.

Chapters 5 and 6 are development-set chapters and sit outside that scope: they quote the
archived dev-set run and the smoke run directly, and §5.10 is the one section in the book
with no committed artifact behind its before-state — which the section now says in the
text rather than leaving to be found. Where those two chapters state a **test-set** figure
they go through `thesis_numbers.json` like everything else: §5.6.3 reads
`backtrack_ban_scope` and §6.4 reads `verifier_route`.

## Terminology discipline

The word **"tier"** is reserved for **one** concept in this thesis: the two-tier
groundedness *metric* (§7.5.3, §8.5). Two other cascades in the system must therefore be
named differently wherever they appear:

- The verification layer's two checks (§6.3) are the **structural check** and the
  **entailment check** — never "Tier 1 / Tier 2".
- The entity resolver's three-stage cascade (§4.6) is **exact / lexical / vector**
  matching — never "Tier 1 / Tier 2 / Tier 3", despite the `tier` identifier used in
  `agr/resolver.py` and surfaced to the agent through `agr/kg_tools.py`
  (`scripts/entity_resolver.py` carries the same name in the analysis script).
  Appendix B declares the collision; this note is about the prose.

Verifier errors are described as **wrongly rejected** / **wrongly accepted** throughout
(§6.8, §9.5), never as `verifier_fn` / `verifier_fp`.

Under the standard convention — the verifier's positive class is *"claim is supported"* —
a **false positive is a wrongly accepted claim** and a **false negative is a wrongly
rejected one**. Define this once in §9.5.1 and use plain English thereafter, because with
`supported`/`unsupported` outputs a reader has no reliable way to infer which class is
"positive".

Three source corrections underlie that convention, recorded here so the provenance carries
into Appendix D. The gloss in `annotation_taxonomy.md` originally paired the names in the
reverse order and has been corrected, with the convention now stated above the table.
Stage D's labels followed the standard convention throughout and were left untouched. Two
rows did not and were relabelled: the De Niro case (§9.3.1, → `answer_selection`) and the
MacFarlane case (§9.5.3, → `verifier_fp`, Stage A having used the reversed convention).
`results/phase4/synthesize_census_log.txt` was regenerated afterwards.

---

## Front Matter (template-generated, roman numerals)

- Candidate's Declaration
- Board of Examiners
- Acknowledgement
- Contents
- List of Figures
- List of Tables
- List of Algorithms
- Abstract

---

## 1. Introduction — *~8 pages*

1.1 Hallucination in Large Language Models
&nbsp;&nbsp;&nbsp;&nbsp;1.1.1 Where Hallucination Originates: Training Data, Model, and Prompt
&nbsp;&nbsp;&nbsp;&nbsp;1.1.2 Why Multi-Hop Questions Are the Hard Case

1.2 From Retrieval Augmentation to Graph-Structured Grounding
&nbsp;&nbsp;&nbsp;&nbsp;1.2.1 Vector Retrieval and Its Structural Blind Spot
&nbsp;&nbsp;&nbsp;&nbsp;1.2.2 Knowledge Graphs and Static GraphRAG
&nbsp;&nbsp;&nbsp;&nbsp;1.2.3 Agentic Retrieval: Reasoning as Navigation

1.3 Limitations of Existing Agentic KGQA Systems
&nbsp;&nbsp;&nbsp;&nbsp;1.3.1 No Check on What the Final Answer Asserts
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Motivate this as a* precision *deficit, not
a groundedness one. Prior agentic systems emit whatever the final LLM call produces from
the traversed context, with no check that each asserted entity is supported* as an answer
*— which surfaces as over-assertion on multi-answer questions and as grounded-but-wrong
answers. Point forward to the precision gap in §8.2. Do not claim prior systems
hallucinate structurally: §8.5 shows they do not.)*
&nbsp;&nbsp;&nbsp;&nbsp;1.3.2 Unquantified Contribution of Individual Agentic Mechanisms
&nbsp;&nbsp;&nbsp;&nbsp;1.3.3 Accuracy Reported Without Cost

1.4 Problem Statement

1.5 Research Questions
&nbsp;&nbsp;&nbsp;&nbsp;1.5.1 RQ1: Does Agentic Navigation Improve Multi-Hop Factual Accuracy?
&nbsp;&nbsp;&nbsp;&nbsp;1.5.2 RQ2: What Does Pre-Generation Verification Contribute Beyond Graph Navigation?
&nbsp;&nbsp;&nbsp;&nbsp;1.5.3 RQ3: Which Components Contribute What, at What Token Cost?

1.6 Our Contribution
&nbsp;&nbsp;&nbsp;&nbsp;1.6.1 The AGR Framework and Its Verification Layer
&nbsp;&nbsp;&nbsp;&nbsp;1.6.2 A Component-Level Ablation of Agentic Mechanisms
&nbsp;&nbsp;&nbsp;&nbsp;1.6.3 Stratum-Dependent Decomposition: When Planning Hurts
&nbsp;&nbsp;&nbsp;&nbsp;1.6.4 The Echo Attractor as a Named Failure Mode
&nbsp;&nbsp;&nbsp;&nbsp;1.6.5 Quantified Benchmark Defect Rates for WebQSP and CWQ
&nbsp;&nbsp;&nbsp;&nbsp;1.6.6 An Evaluation Protocol with Pre-Registered Thresholds

1.7 Scope and Delimitations

1.8 Thesis Organization

---

## 2. Background and Preliminaries — *~5 pages*

2.1 Knowledge Graphs
&nbsp;&nbsp;&nbsp;&nbsp;2.1.1 Triples, Entities, and Relations
&nbsp;&nbsp;&nbsp;&nbsp;2.1.2 Freebase: MIDs, Schema, and Mediator (CVT) Nodes
&nbsp;&nbsp;&nbsp;&nbsp;2.1.3 Property Graphs, Neo4j, and Cypher

2.2 Knowledge Graph Question Answering
&nbsp;&nbsp;&nbsp;&nbsp;2.2.1 Multi-Hop Questions and Constraint Satisfaction
&nbsp;&nbsp;&nbsp;&nbsp;2.2.2 Evaluation Conventions: Hits@1 and F1
&nbsp;&nbsp;&nbsp;&nbsp;*(semantic parsing vs. information retrieval: one paragraph inside 2.2.1)*

2.3 Large Language Models as Reasoning Engines
&nbsp;&nbsp;&nbsp;&nbsp;2.3.1 In-Context Learning and Chain-of-Thought Prompting
&nbsp;&nbsp;&nbsp;&nbsp;2.3.2 Tool Use and the ReAct Loop
&nbsp;&nbsp;&nbsp;&nbsp;2.3.3 A Working Definition of Hallucination for This Thesis

2.4 Retrieval-Augmented Generation
&nbsp;&nbsp;&nbsp;&nbsp;2.4.1 Dense Retrieval and Sentence Embeddings
&nbsp;&nbsp;&nbsp;&nbsp;2.4.2 Graph-Based Retrieval

2.5 Search over Graphs
&nbsp;&nbsp;&nbsp;&nbsp;2.5.1 Best-First and Beam Search
&nbsp;&nbsp;&nbsp;&nbsp;2.5.2 Backtracking and Dead-End Detection
&nbsp;&nbsp;&nbsp;&nbsp;2.5.3 Relation to Monte Carlo Tree Search: A Terminological Clarification

2.6 Statistical Tools Used in This Thesis
&nbsp;&nbsp;&nbsp;&nbsp;*(one page: bootstrap confidence intervals, McNemar's test for paired
correctness, Cohen's κ — definitions and the reason each was chosen, no derivations)*

---

## 3. Related Work — *~7 pages*

3.1 Static Graph-Augmented Generation
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1 GraphRAG and Query-Focused Summarization
&nbsp;&nbsp;&nbsp;&nbsp;3.1.2 HippoRAG and Memory-Structured Retrieval

3.2 Path-Retrieval and Semantic-Parsing KGQA
&nbsp;&nbsp;&nbsp;&nbsp;3.2.1 Reasoning-on-Graphs
&nbsp;&nbsp;&nbsp;&nbsp;3.2.2 StructGPT and KG-Agent

3.3 Agentic Graph Exploration
&nbsp;&nbsp;&nbsp;&nbsp;3.3.1 Think-on-Graph
&nbsp;&nbsp;&nbsp;&nbsp;3.3.2 Plan-on-Graph
&nbsp;&nbsp;&nbsp;&nbsp;3.3.3 Generate-on-Graph and Reasoning with Trees

3.4 Verification and Self-Correction in Language Models
&nbsp;&nbsp;&nbsp;&nbsp;3.4.1 Chain-of-Verification
&nbsp;&nbsp;&nbsp;&nbsp;3.4.2 Ontology-Guided and Self-Correcting Graph RAG

3.5 Measuring Factuality
&nbsp;&nbsp;&nbsp;&nbsp;3.5.1 Claim-Decomposition Metrics
&nbsp;&nbsp;&nbsp;&nbsp;3.5.2 Factuality Benchmarks and Their Limits

3.6 Comparative Summary of Agentic KGQA Systems
&nbsp;&nbsp;&nbsp;&nbsp;*(the cross-system table: exploration strategy, decomposition, backtracking,
pre-generation verification, datasets, reported Hits@1 — this table also justifies the
baseline selection in §7.4)*

3.7 Positioning of This Work

---

## 4. The Knowledge Environment — *~10 pages*

4.1 Design Goals
&nbsp;&nbsp;&nbsp;&nbsp;4.1.1 Decoupling the Graph Source from the Question Sets
&nbsp;&nbsp;&nbsp;&nbsp;4.1.2 Why a Curated Subgraph Rather Than LLM-Extracted Triples

4.2 Source Data
&nbsp;&nbsp;&nbsp;&nbsp;4.2.1 The Freebase Snapshot
&nbsp;&nbsp;&nbsp;&nbsp;4.2.2 WebQSP and ComplexWebQuestions as Question Sets

4.3 Graph Construction
&nbsp;&nbsp;&nbsp;&nbsp;4.3.1 Union of Per-Question Subgraphs from the RoG Distribution
&nbsp;&nbsp;&nbsp;&nbsp;4.3.2 Relation Filtering and Noise Removal
&nbsp;&nbsp;&nbsp;&nbsp;4.3.3 Treatment of Mediator Nodes and Its Effect on Hop Counts

4.4 Graph Store Construction
&nbsp;&nbsp;&nbsp;&nbsp;4.4.1 Property-Graph Schema
&nbsp;&nbsp;&nbsp;&nbsp;4.4.2 Bulk Import into Neo4j
&nbsp;&nbsp;&nbsp;&nbsp;4.4.3 Graph Statistics

4.5 The Vector Index
&nbsp;&nbsp;&nbsp;&nbsp;4.5.1 Entity Embeddings
&nbsp;&nbsp;&nbsp;&nbsp;4.5.2 Relation-Vocabulary Embeddings
&nbsp;&nbsp;&nbsp;&nbsp;4.5.3 Scope: Linking and Candidate Ranking, Never Ground Truth

4.6 Entity Resolution and Surface-Form Linking
&nbsp;&nbsp;&nbsp;&nbsp;4.6.1 The Exact, Lexical, and Vector Cascade
&nbsp;&nbsp;&nbsp;&nbsp;4.6.2 Threshold Selection on Development Data

4.7 Environment Validation Gate
&nbsp;&nbsp;&nbsp;&nbsp;4.7.1 Answer-Reachability Protocol
&nbsp;&nbsp;&nbsp;&nbsp;4.7.2 Coverage Results and the Induced Accuracy Ceiling
&nbsp;&nbsp;&nbsp;&nbsp;4.7.3 Analysis of Linking Misses and Gate Failures
&nbsp;&nbsp;&nbsp;&nbsp;4.7.4 What the Environment Cannot Express
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(no date literals, no numeric literals, no ordinal
encodings — all three verified; defines the* unanswerable-in-environment *question class
that §9.6 later invokes rather than introduces)*

---

## 5. The AGR Framework: Architecture and Navigation — *~11 pages*

5.1 Architectural Overview
&nbsp;&nbsp;&nbsp;&nbsp;*(figure: the Planner → Explorer → Evaluator → {Backtrack | Verify} → Answerer
state machine)*

5.2 The Graph Tool API
&nbsp;&nbsp;&nbsp;&nbsp;5.2.1 Rationale: Constrained Tools Instead of Free-Form Cypher Generation
&nbsp;&nbsp;&nbsp;&nbsp;5.2.2 The Five Operations
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(table + prose: `search_entity`, `get_relations`,
`get_neighbors`, `verify_triple`, `verify_connection`)*
&nbsp;&nbsp;&nbsp;&nbsp;5.2.3 Relation-Agnostic Adjacency and Traversal Through Mediators
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(`verify_connection` — what the structural check
in §6.3.1 actually calls, and why endpoint adjacency rather than exact-triple matching)*
&nbsp;&nbsp;&nbsp;&nbsp;5.2.4 Determinism, Caching, and Tool-Call Logging

5.3 Agent State Representation

5.4 The Planner
&nbsp;&nbsp;&nbsp;&nbsp;5.4.1 Decomposition into Ordered Sub-Objectives
&nbsp;&nbsp;&nbsp;&nbsp;5.4.2 Plan Validation and Degenerate-Plan Handling

5.5 The Explorer
&nbsp;&nbsp;&nbsp;&nbsp;5.5.1 Frontier Construction
&nbsp;&nbsp;&nbsp;&nbsp;5.5.2 The Hybrid Scoring Function
&nbsp;&nbsp;&nbsp;&nbsp;5.5.3 Embedding Pre-Filtering and Batched LLM Scoring
&nbsp;&nbsp;&nbsp;&nbsp;5.5.4 Beam Selection and Expansion

5.6 The Evaluator and Routing Policy
&nbsp;&nbsp;&nbsp;&nbsp;5.6.1 Sub-Objective Completion Judgment
&nbsp;&nbsp;&nbsp;&nbsp;5.6.2 Backtracking Triggers: Score Threshold, Dead Ends, Evaluator Veto
&nbsp;&nbsp;&nbsp;&nbsp;5.6.3 The Backtrack Stack and Branch Invalidation

5.7 The Answerer

5.8 Budgets and Termination Guarantees

5.9 Instrumentation: What Every Run Records

5.10 The Complete Navigation Algorithm

---

## 6. The Structural Verification Layer — *~8 pages*

6.1 Motivation: Verifying Before Emitting, Not After

6.2 Claim Decomposition of the Draft Answer

6.3 Two-Stage Claim Checking
&nbsp;&nbsp;&nbsp;&nbsp;6.3.1 The Structural Check
&nbsp;&nbsp;&nbsp;&nbsp;6.3.2 The Entailment Check
&nbsp;&nbsp;&nbsp;&nbsp;6.3.3 Why the Structural Check Runs First

6.4 Repair Policies for Unsupported Claims
&nbsp;&nbsp;&nbsp;&nbsp;6.4.1 Targeted Re-Exploration Under Remaining Budget
&nbsp;&nbsp;&nbsp;&nbsp;6.4.2 Answer Rewriting and Hedging
&nbsp;&nbsp;&nbsp;&nbsp;6.4.3 Iteration Cap and the Draft-Only Fallback

6.5 Entity Filtering of the Final Answer

6.6 Output Contract: Answer Paired with Supporting Triples

6.7 A Worked Example

6.8 Failure Modes by Construction: Wrongful Rejection and Wrongful Acceptance
&nbsp;&nbsp;&nbsp;&nbsp;*(Analytical, derived from the design rather than the data — but
§9.5 now has empirical specimens for both polarities, so this section should name the
mechanism each one instantiates and forward-reference them. Use the same polarity
vocabulary §9.5.1 fixes; do not use fn/fp here.)*

---

## 7. Experimental Setup — *~11 pages*

7.1 Mapping Experiments to Research Questions
&nbsp;&nbsp;&nbsp;&nbsp;7.1.1 Pre-Registration and the No-Tuning Policy
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(no tuning after test data is touched; κ ≥ 0.7,
the 15% baseline-certification diagnostic, and the α/τ freeze all fixed before
measurement)*
&nbsp;&nbsp;&nbsp;&nbsp;7.1.2 Metrics Proposed but Not Run
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(One short paragraph accounting for path
fidelity, which the approved proposal named as its third evaluation criterion. State the
reason once: it requires gold SPARQL relation chains, and the RoG distribution's
name-keyed triples do not carry them, so reconstructing the chains fell outside the
budget. §10.3.1 then picks it up as future work without relitigating. Two mentions, one
reason, no defensiveness.)*

7.2 Test Sets
&nbsp;&nbsp;&nbsp;&nbsp;7.2.1 WebQSP
&nbsp;&nbsp;&nbsp;&nbsp;7.2.2 ComplexWebQuestions
&nbsp;&nbsp;&nbsp;&nbsp;7.2.3 Stratified Sampling, Seeds, and Published Question IDs
&nbsp;&nbsp;&nbsp;&nbsp;7.2.4 Hop-Count Stratification

7.3 Backbone Model Selection and Qualification
&nbsp;&nbsp;&nbsp;&nbsp;**The frozen backbone is `gpt-5.4-mini-2026-03-17`, temperature 0.0,
`reasoning_effort="none"`, response cache on** — stamped on all 4,000 test-matrix records and
on every ablation record. The selection story is a *reversal* and must be told as one, because
it is the strongest methodology anecdote the project has. Round one of `qualify_backbone.py`
(20 smoke questions × 2 candidates, 3 repeat probes) reported determinism 3/3 for
`gpt-4.1-mini-2025-04-14` against 1/3 for `gpt-5.4-mini-2026-03-17`, and 4.1-mini was chosen
on that basis. A rerun with the cache disabled reversed it: 2/3 against 3/3. Diagnosis, and
this is §7.3.1's content: temperature-0 decoding on a hosted API is *greedy*, not
deterministic, and a sequential agent is a divergence amplifier — one flipped token in a
planner or evaluator call changes a sub-objective's wording, hence the embedding, hence the
beam. With n=3 the estimator was pure noise. A tiebreaker was pre-registered before rounds 3
and 4 (*within 3 matches → take 5.4-mini on longevity*); pooled over all four runs the score
is **9/12 vs 8/12** — one match apart, **not** a tie, but inside the pre-registered
three-match band — so the rule fired and 5.4-mini was frozen on 2026-07-12.
&nbsp;&nbsp;&nbsp;&nbsp;*Provenance to state honestly: only round one survives as per-question
artifacts (`results/phase2/qualify_*_full.jsonl`, 20 records each, written in `"w"` mode and
therefore overwritten by later rounds) plus `qualify-backbone-log.txt`, which holds round
one's table only. The tool logs did accumulate across all four rounds (append mode; 649 and
858 records over 20 distinct qids). Rounds 2–4 exist as console tables in the project record,
not as artifacts. Report the pooled 9/12 vs 8/12 with that limitation named.*
&nbsp;&nbsp;&nbsp;&nbsp;7.3.1 Trajectory Stability Under Temperature-Zero Decoding
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(hosted APIs are only approximately
deterministic at temperature 0; sequential agents amplify per-call divergence; report the
**frozen model's** rate, which is 8/12 ≈ 67% — the 9/12 ≈ 75% is 4.1-mini's, the candidate
that was *not* frozen, and quoting it here reports the runner-up's stability as the
system's. Pooled across both candidates it is 17/24 ≈ 71%. That number, not a claim of
determinism, is what the thesis reports.)*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**The load-bearing observation, and it belongs
in §1.1 as well as here:** across four runs, *both* candidates produced ungrounded answers
stochastically, each with one sticky failure — 4.1-mini's Salcedo→"United States Dollar" in
2 of 4 runs and Barroso in 1 of 4; 5.4-mini's Beckham→"Harper Seven Beckham" in 4 of 4 and
Van Rompuy in 1 of 4. Same question, same graph, same budget, and the answer moves between
grounded-correct and ungrounded-wrong with the sampling weather. That is a *measured*
statement of the thesis's premise: **hallucination mitigation cannot be delegated to backbone
selection; it requires an architectural mechanism.**
&nbsp;&nbsp;&nbsp;&nbsp;7.3.2 Response Caching as the Reproducibility Backstop
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Reproducibility rests on the cache, not on
model determinism: one recorded run per condition, replayed byte-identically because the cache
also replays the original token counts into the meter, so a cached rerun reproduces the budget
snapshot exactly. Fresh-run variance is handled the standard way — bootstrap CIs over
questions and paired McNemar. Cross-reference §7.10's cache-identity verification technique.)*

7.4 Baseline Systems
&nbsp;&nbsp;&nbsp;&nbsp;7.4.1 No-Retrieval LLM (Parametric-Memory Control)
&nbsp;&nbsp;&nbsp;&nbsp;7.4.2 Vector-RAG over Verbalized Triples
&nbsp;&nbsp;&nbsp;&nbsp;7.4.3 Static GraphRAG
&nbsp;&nbsp;&nbsp;&nbsp;7.4.4 Think-on-Graph (Agentic Baseline)
&nbsp;&nbsp;&nbsp;&nbsp;7.4.5 Variables Held Constant Across All Systems
&nbsp;&nbsp;&nbsp;&nbsp;7.4.6 Baseline Certification Protocol
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(the pre-registered gold-visible-while-hedged
diagnostic, dev-only debugging of all four baselines, and the ToG budget-clip rates)*

7.5 Metrics
&nbsp;&nbsp;&nbsp;&nbsp;7.5.1 Answer Accuracy: Hits@1 and F1
&nbsp;&nbsp;&nbsp;&nbsp;7.5.2 Accounting for Hedges and Abstentions
&nbsp;&nbsp;&nbsp;&nbsp;7.5.3 Two-Tier Groundedness and Hallucination Rate
&nbsp;&nbsp;&nbsp;&nbsp;7.5.4 Efficiency: Tokens, LLM Calls, and Wall-Clock Latency
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(latency is computed over cold-cache records
only — state this wherever wall-clock is reported)*

7.6 The Groundedness Judge and Its Validation
&nbsp;&nbsp;&nbsp;&nbsp;7.6.1 Independence of the Judge from the Answering System
&nbsp;&nbsp;&nbsp;&nbsp;7.6.2 Human Annotation Protocol
&nbsp;&nbsp;&nbsp;&nbsp;7.6.3 Agreement Between Judge and Human Annotator
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**State the exact value, not the rounded
one.** Cohen's κ is **0.6995** on n = 100 (85% observed agreement), against a
pre-registered threshold of κ ≥ 0.7. Rounded to three decimals it reads 0.700 and appears
to clear; it does not. Report it as *marginally below* the threshold, say what that means
for how much weight the Tier-2 numbers can carry, and do not silently round up — a
pre-registered threshold reported as met when it was missed by 0.0005 is exactly the kind
of thing that destroys a viva. The honest framing is that agreement is substantial by any
conventional reading of κ, and that the pre-registered bar was set marginally above what
was achieved.

7.7 Gold-Answer Quality Control
&nbsp;&nbsp;&nbsp;&nbsp;7.7.1 The Gold-Noise Problem in WebQSP and CWQ
&nbsp;&nbsp;&nbsp;&nbsp;7.7.2 Consensus Pre-Pass and Per-Item Adjudication
&nbsp;&nbsp;&nbsp;&nbsp;7.7.3 Two Evidence Signatures of Label Error
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Label errors come in two kinds with
opposite signatures, and separating them is what makes the adjudication reproducible
rather than ad hoc. World-fact errors require* mixed *consensus — parametric and
graph-based systems agreeing against the label. Annotation-pipeline errors show up as*
graph-only *consensus, where every graph-grounded system finds the answer the label
contradicts. Give the diagnostic and one specimen of each. The San Antonio City Council
item (`WebQTest-634…`, `mixed_evidence: true`, four systems converging on Bexar County
against a Comal County gold) is the worked mixed-evidence specimen — and see §9.8 for
where that particular label came from.)*
&nbsp;&nbsp;&nbsp;&nbsp;7.7.4 Census-Based Exclusions and the Dual-Reporting Policy
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Verified numbers, from
`results/phase4/make_goldnoise_exclusions_log.txt`, `goldnoise_summary.json` and
`results/phase4/census_exclusions_agr_log.txt` — quote these, not the intermediate figures that appear
in the project record. The pass emits one row per (qid, consensus answer) pair, so rows and
questions must be reported as separate units:* **WebQSP 89 rows over 58 distinct questions**
*→ 36 `gold_ok`, 12 `gold_wrong`, 10 `ambiguous_question` → **22 excluded (5.5%)**;*
**CWQ 59 rows over 47 questions** *→ 28 / 17 / 2 → **19 excluded (4.8%)**. Auto-triage cleared
15/89 and 2/59; the rest were adjudicated by hand. Of the excluded questions, **12 of 22
(WebQSP) and 15 of 19 (CWQ) were AGR failures** — those are the numbers that shrink the census
pool; the remainder were questions AGR "got right" against a label now judged broken, which is
the honest symmetry the footnote needs:* label errors cut both ways, *and a small number of
scored hits rest on the same defective labels. No rescoring — Table 1 stands as reported, with
the footnote.)*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Two scope statements belong here because they
are limits on the method, not on the finding: the auto rule that assigned `gold_wrong` on
gold-list length is a heuristic, not proof; and the adjudication covered all mixed-evidence
flags plus every graph-only flag that was not a topic echo — a scope that had to be widened
mid-pass when the Michael Bublé case (`WebQTest-55_54e856…`, `mixed_evidence: false`) turned
out to be a genuine label error. That widening is §7.7.3's two-signature argument in action
and should be narrated as such.*

7.8 Ablation Conditions

7.9 Hyperparameter Selection on the Development Set
&nbsp;&nbsp;&nbsp;&nbsp;7.9.1 The α–τ Sweep Protocol
&nbsp;&nbsp;&nbsp;&nbsp;7.9.2 Development Set Construction and Coverage

7.10 Implementation, Environment, and Reproducibility

---

## 8. Results — *~12 pages*

8.1 Development-Set Tuning Outcomes
&nbsp;&nbsp;&nbsp;&nbsp;*(Report the α = 0.5 non-monotonicity rather than smoothing the
sweep into a clean curve, and say in one sentence why: the data show it, and a presented
curve that hides a known irregularity is the kind of thing a defense finds.)*

8.2 Main Results on WebQSP

8.3 Main Results on ComplexWebQuestions

8.4 Accuracy Broken Down by Hop Count

8.5 Groundedness and Hallucination Rate Across Systems
&nbsp;&nbsp;&nbsp;&nbsp;*(headline: structural groundedness is a property of the navigation
paradigm, not of the verifier — AGR and ToG both reach it. Frame accordingly; do not
attribute it to the verification layer.)*

8.6 Efficiency and Cost
&nbsp;&nbsp;&nbsp;&nbsp;8.6.1 Token and Call Budgets per System
&nbsp;&nbsp;&nbsp;&nbsp;8.6.2 The Accuracy–Cost Frontier

8.7 Ablation Study
&nbsp;&nbsp;&nbsp;&nbsp;8.7.1 Without the Planner: A Stratum-Dependent Effect
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(removal helps WebQSP and trends toward
hurting CWQ — the asymmetry is the finding, not the pooled average)*
&nbsp;&nbsp;&nbsp;&nbsp;8.7.2 Without Backtracking
&nbsp;&nbsp;&nbsp;&nbsp;8.7.3 Without the Verification Layer
&nbsp;&nbsp;&nbsp;&nbsp;8.7.4 Embedding-Only Scoring
&nbsp;&nbsp;&nbsp;&nbsp;8.7.5 Paired Significance Testing and Statistical Power
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(open by stating that only the planner
condition reached significance at n ≈ 200; the other three are reported as "no detectable
effect at this sample size," never as confirmed nulls)*

8.8 Findings Against RQ1, RQ2, and RQ3
&nbsp;&nbsp;&nbsp;&nbsp;*(RQ2's answer is three-part: navigation eliminates structural
hallucination; verification contributes precision and F1; verification shows no
measurable Hits@1 effect in ablation)*

---

## 9. Error Analysis and Discussion — *~10 pages*

9.1 Annotation Protocol and the Failure Taxonomy
&nbsp;&nbsp;&nbsp;&nbsp;9.1.1 Category and Subtype Schema
&nbsp;&nbsp;&nbsp;&nbsp;9.1.2 Population, Not Sample: Both Datasets Read to Completion
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Corrected against
`results/phase4/sampling_manifest.json`, which records `mode: "full_census"` for *both*
datasets** (WebQSP 43 wrong + 22 hedge = 65; CWQ 70 + 87 = 157). An earlier plan drew a
stratified 40W+20H sample from CWQ; the census was subsequently read to completion instead,
and `synthesis.md` §1 states it explicitly. So there is **no sampling asymmetry to caveat** —
say so plainly, since it is a strictly stronger claim than a sample. Wrong and hedge are still
reported separately and never pooled, but for a *semantic* reason, not a sampling one: a wrong
answer is a reasoning error, a hedge is usually a coverage gap that never produced a committal
answer. The three populations merged into the histogram are Stage D (65 / 157), the one Stage D
row later promoted to a formal Stage C exclusion (0 / 1), and Stage A's ablation-discordance
census (21 / 15) — 86 and 173, 259 failures in total.

9.2 Distribution of Failure Categories Across Datasets
&nbsp;&nbsp;&nbsp;&nbsp;*(Source: the Stage E merged histogram,
`results/phase4/synthesize_census_log.txt` and `results/phase4/synthesis.md` §2 — Stage D + Stage A,
86 WebQSP and 173 CWQ rows, wrong and hedge kept separate throughout. The headline is the*
shape flip *between datasets — but state it the way `synthesis.md` does, because the obvious
phrasing is wrong.* `relation_selection` *is the largest category in* **both** *datasets (26
WebQSP, 39 CWQ), so it is not what distinguishes them. What distinguishes them is*
`composite_claim` *and* `kg_gap`: *1 and 12 of WebQSP's 86, against 46 and 32 of CWQ's 173.
WebQSP's other top category is* `decomposition_error` *(26, tied with relation_selection —
together nearly 60% of its total). That is not noise; it follows from CWQ's questions being
multi-constraint by construction, with* `composite_claim` *catching dropped constraints and*
`kg_gap` *catching the internal numeric IDs and superlatives its templates keep producing.
Second observation worth its own sentence:* `kg_gap` *skews three-to-one toward* hedges *on
CWQ (24 hedge vs 8 wrong) and the other way on WebQSP (4 vs 8) — when CWQ's literals are
unreachable AGR much more often abstains than asserts, which is a* good *property and should
be reported as one rather than only as a deficiency. The log is current as of the three label
corrections recorded in §9.3.1 and §9.5 — regenerate it if any further relabelling happens,
since totals are unaffected but three CWQ hedge rows move.*
&nbsp;&nbsp;&nbsp;&nbsp;*Do not leave the structural explanation asserted — it is
demonstrable from data already in hand, and two citations in the same paragraph turn it
into a shown result. First, the stratum distribution: WebQSP is 64% one-hop (256/400) with
a four-question h3plus tail, whereas CWQ is majority h2 (211/400) with a real h3plus tail
of 49. Second, the `kg_gap` cases trace to the specific expressiveness limits verified in
§4.7.4 — no date literals, no numeric literals, no ordinals — which CWQ's templates invoke
constantly and WebQSP's rarely.)*

9.3 Decomposition, Drafting, and Answer-Selection Errors
&nbsp;&nbsp;&nbsp;&nbsp;*(including the context-stripping mechanism. This section now
carries three families in the space originally budgeted for one, so give context-stripping
the full worked treatment — it is the strongest mechanism finding here — and let the
extraction-bug cases share a single worked example with the De Niro case below. They are the
same family: the drafter or extractor selecting the wrong entity out of correct prose.)*
&nbsp;&nbsp;&nbsp;&nbsp;*Corrected counts from `synthesis.md`:* `context_stripping` *has*
**three** *instances, not two — `WebQTest-1367` (Glastonbury England → the Connecticut town,
from Stage D) joins `WebQTrn-2615` (Fela!) and `WebQTrn-2570_d63877a…` (33rd president /
WW2) from Stage A.* `extraction_bug` *has* **nine**, *not three, and is the single most
actionable finding in the census: on profession- and "what did X do"-shaped questions the
evaluator resolves every correct gold value and states them verbatim in the answer text,
and then* `answer_entities` *collapses to the sentence's grammatical subject. Use the
three-row table from `synthesis.md` §2 verbatim (`WebQTest-1215` Stephen R. Covey,
`WebQTest-704` Thor Heyerdahl, `WebQTrn-124_0782789f…` Angelina Jolie) — correct prose,
subject-only entity list. Because scoring reads* `answer_entities`, *this bug depresses
measured accuracy on a whole question shape independently of any reasoning defect, and that
has to be said as a limitation on the headline numbers, not just as a bug.*
&nbsp;&nbsp;&nbsp;&nbsp;*One further drafting bug the earlier outline missed, filed under*
`other` *(6 cases): the evaluator resolves the exact gold value,* `verifier_outcome` *is*
`grounded`, *and the drafted text hedges anyway — no rejection is involved, so it is not a
verifier error. `WebQTest-689` (Spanish/Spain), `WebQTest-989_4b6636a0…` (Dunkirk) and
`WebQTrn-1392_d372995c…` (Eleanor Roosevelt's two schools) are the clean instances. Contrast
it explicitly with the extraction bug: there the text is right and the entities wrong; here
the text contradicts a fact it has just stated.*
&nbsp;&nbsp;&nbsp;&nbsp;9.3.1 Right Candidate Retrieved, Wrong One Drafted
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(The De Niro case,
`WebQTrn-1294_a4b2006a…`, relabelled. The census filed it as `verifier_fn` on the theory
that the verifier checked a claim about a different candidate than the one the evaluator
resolved. The run record refutes that: the* draft itself *reads "Marlon Brando also played
in Joy", and the verifier rejected exactly what the drafter asserted. Brando did not
appear in* Joy; *De Niro did. The verifier was correct and the error is upstream, in the
answerer — the taxonomy's own `answer_selection` category, to which the label has been
corrected.)*

9.4 Relation-Selection and Navigation Errors
&nbsp;&nbsp;&nbsp;&nbsp;*(`relation_selection` is the largest category in both datasets — 65
combined, and no subtypes, because the mechanism is uniform. Two exhibits carry it. First,
the* **Beyoncé triplet** *(`WebQTrn-1770_540abec8…`, `…_6325ee89…`, `…_6a7c160a…`): three
differently-phrased CWQ questions all resolve Beyoncé correctly and all three never once try*
`people.person.children`, *the one relation that answers them; all three hedge. Three
independent entry points hitting the identical dead end is the cleanest evidence in the corpus
that a relation gap is systemic rather than an artefact of phrasing. Second, the* **government
triplet** *(`WebQTrn-1758_477d7040…`, `WebQTest-1226`, `WebQTest-314`) all reach for*
`government.governmental_jurisdiction.government` *— the organisation — instead of*
`government.form_of_government.countries` *— the type labels the question asks for.)*
&nbsp;&nbsp;&nbsp;&nbsp;*Give `premature_termination` its own paragraph here rather than
scattering it: all 8 instances carry the* `evaluator` *subtype and all 8 are the* same
*pattern — the correct relation is explored with a solid score and the evaluator backtracks
away from it and never returns.* `WebQTest-1226` *(0.451),* `WebQTest-314` *(0.731),*
`WebQTrn-710_e3d40457…` *(0.702). Eight identical shapes across unrelated domains reads as an
evaluator-threshold or backtracking-policy defect, not as eight reasoning failures, and it is
one of the most directly fixable findings in the census (see §10.3).*

9.5 Verifier Rejection and Acceptance Errors
&nbsp;&nbsp;&nbsp;&nbsp;**Stands as a section, but the two polarities are very unevenly
evidenced — and that imbalance is itself the finding.** Verified inventory across the full
Stage E census:
&nbsp;&nbsp;&nbsp;&nbsp;• *Wrongly rejected* — **five** cases: WebQTest-1133, -38, -725
(WebQSP, hedge), WebQTest-1348 (CWQ, wrong), WebQTrn-568 (CWQ, hedge).
&nbsp;&nbsp;&nbsp;&nbsp;• *Wrongly accepted* — **one** clean case: WebQTrn-1597
(MacFarlane), from Stage A, whose note already records "not grounded in any real edge
despite `verifier_outcome: grounded`". The direct Cypher query confirms no MacFarlane
edge to Lion-O or ThunderCats exists.
&nbsp;&nbsp;&nbsp;&nbsp;• *Two instructive boundary cases that are **not** verifier
defects:* De Niro (relabelled `answer_selection`, §9.3.1) and Wilson / WebQTest-1620
(labelled `kg_gap` / `date_literal` — see §9.5.3).
&nbsp;&nbsp;&nbsp;&nbsp;*Open the section by cross-referencing §9.3.1: the verifier's
correct rejections are not merely the background population of the 52 firings, one of them
is narrated there as a positive demonstration of the layer doing its job.*
&nbsp;&nbsp;&nbsp;&nbsp;9.5.1 Defining the Error Polarities
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Open with an explicit convention and use
it consistently thereafter.** State that the verifier's positive class is "claim is
supported", so a false positive is a wrongly accepted claim and a false negative a wrongly
rejected one — then name the polarities in prose (*wrongly rejected* / *wrongly accepted*)
and avoid fn/fp for the rest of the thesis, since the verifier's output is `supported` /
`unsupported` and "positive" has no stable referent for a reader. The label sources now
follow this convention consistently; see the terminology note at the head of this outline
for what was corrected to get there.
&nbsp;&nbsp;&nbsp;&nbsp;9.5.2 Wrongly Rejected: Semantically Correct, Structurally Unmatched
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(The five genuine census cases —
W. H. Smith, the four campaign entities, California/Nevada, Houston Oilers, Mecklenburg
County. All share one mechanism: the claim is true and the answer correct, but no single
triple states it in the drafted phrasing, so a transitively-true or differently-anchored
fact is rejected and the retry loses the answer. This is a single, cleanly-argued failure
mode — resist the urge to subdivide it.)*
&nbsp;&nbsp;&nbsp;&nbsp;9.5.3 Wrongly Accepted: Unsupported Claims Passed as Grounded
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(MacFarlane is the only clean specimen:
no edge exists, yet the claim passed as `grounded`. Use Wilson (WebQTest-1620) as the
contrasting boundary case rather than a second defect — there the asserted inauguration
entities* do *exist and the edges* are *real, so the structural check passed correctly;
the answer is nonetheless wrong because the environment holds no date literal. That
contrast is the section's most useful point, and it is the same argument §1.3.1 makes:
structural grounding is a claim about edge existence, not about answer adequacy.)*
&nbsp;&nbsp;&nbsp;&nbsp;9.5.4 Rate for One Polarity, and a Blank for the Other
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Aggregate counts are the
`verifier.grounded` / `verifier.unsupported` columns of `score_run_phase4.csv`; per-record
outcomes are the `verifier_outcome` field of `results/phase4/test_{ds}_agr.jsonl` — which
holds the* first *verdict, not the final one, so a repaired question reads* unsupported
*there. Take the units from `thesis_numbers.json → verifier_route`, which separates all
four: 828 firings, 52 questions whose first verdict was* unsupported *(16/400 WebQSP,
36/400 CWQ), 13 of those repaired to* grounded*, and 761 questions answered under a
grounded verdict. The wrongly-rejected specimens are drawn from the 52 questions, so that
polarity has a denominator in the question unit. Wrongly-accepted cases have* no logged
population at all *— they sit undifferentiated inside the 761, because accepted claims are
never persisted (§9.9.3). Report a rate for rejection and an explicit blank for
acceptance; do not average them into a single "verifier error rate".)*

9.6 Knowledge-Graph Gaps: Literals, Temporal Qualifiers, and Ordinals
&nbsp;&nbsp;&nbsp;&nbsp;*(invokes the unanswerable-in-environment class defined in §4.7.4)*

9.7 The Echo Attractor: Answering with the Topic or an Intermediate Entity

9.8 Benchmark Defects: Gold Noise and Ambiguous Questions
&nbsp;&nbsp;&nbsp;&nbsp;*(Open by separating two numbers that are easy to conflate: the
share of questions the consensus pass* flagged, *and the much smaller share adjudication
confirmed as genuine label defects. Most flagged items were not label errors — they were
all five systems converging on the same wrong answer. That phenomenon is §9.7's; point
there for it and keep this section to the defects proper.)*
&nbsp;&nbsp;&nbsp;&nbsp;*The headline total:* **57 questions across
both datasets where the benchmark, not AGR, was the thing that needed correcting** — 41
excluded by Stage C before the census read anything (22 + 19), plus 17 still sitting in
the merged census as `gold_noise`/`ambiguous_question` rows (3 WebQSP + 14 CWQ). The two
counts are **not** disjoint, which is why the total is 57 and not the 58 an addition gives.
`WebQTrn-64_d8e43a02…` began as a Stage D finding and was promoted to a formal Stage C
exclusion mid-project; it is inside the 41 (`census_exclusions.json`, CWQ list) *and* inside
the 17, because `labels_cwq_dropped.csv` is merged into the census histogram — that is what
keeps the histogram totals whole, and it is exactly what makes the sum wrong. Count identifiers,
not totals: `thesis_numbers.json → benchmark_defects.distinct_questions` takes the union and the
generator asserts it closes. (`synthesis.md` §4 says 59 and is wrong here.) *Two exhibits earn their space:* `WebQTest-958`
*("what are some famous people from el salvador") with* **116 gold entities** *and raw
Freebase MIDs leaked into the answer strings — a "list some famous X" template ballooning gold
past any reachable match; and the* **Vicksburg pair**, *two sibling questions with the same
gold string and opposite diagnoses —* `WebQTest-1797_5a1c66f…` *("who was president during the
battle of Vicksburg", gold `Ulysses S. Grant`, who took office six years later) where the full
pipeline's verifier* correctly *rejected the claim and hedged while the no-planner ablation
asserted it and scored a "hit"; and* `WebQTest-1797_dece4dd…` *("what Government position
holder fought in the battle of Vicksburg"), coherent as asked, where AGR genuinely dropped the
qualifier and answered with the Confederate commander. Same battle, same gold, one question
unanswerable and one a real AGR failure. That pair is the argument for reading each case
individually instead of trusting question similarity, and it is also a second exhibit for
§9.9.2's over-hedging discussion.*
&nbsp;&nbsp;&nbsp;&nbsp;*One process finding worth a sentence:* `WebQTrn-64_d8e43a…` *was
adjudicated `gold_ok`/echo by Stage C and the opposite way by Stage D's independent read of
the same evidence; the second reading held, and the row was promoted to a formal exclusion.
Two adjudication passes can legitimately disagree, and the taxonomy keeping a `gold_noise`
category open is what let that be resolved rather than settled by whichever ran first.*
&nbsp;&nbsp;&nbsp;&nbsp;9.8.1 Where Bad Gold Comes From: Flattened Multi-Valued Relations
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(A short, concrete provenance argument
built on the San Antonio case. The graph does carry
`San Antonio —location.location.containedby→ Comal County`, alongside two HUD
county-place edges. That edge is not fabricated: San Antonio's city limits genuinely
extend into Comal and Medina counties, though the city and its council sit overwhelmingly
in Bexar. The defect is therefore neither a pure label error nor a pure graph error but a*
multi-valued containment relation flattened to a single value, *with the annotation
pipeline then selecting the marginal value. Framing it this way is both more accurate and
more useful than calling it a data error, and it explains why the consensus diagnostic
caught it.)*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Provenance discipline for this subsection.**
*What the artifacts actually record is: Stage C's verdict* `gold_wrong` / `wrong_gold` *with
the note "san antonio and its city council are in bexar county; gold gives comal county, a
neighbouring county" (`prepass_goldnoise_cwq.json` — still uncorrected, and the "neighbouring"
wording understates the overlap), and Stage A's census label* `kg_gap` *with the note
"containment ambiguity in the source data (annexed territory, or Freebase simply having
imprecise/multiple containment edges)". Write the flattened-multi-valued-relation argument on*
that *evidence. Do* not *state a specific edge inventory (e.g. "the graph carries exactly these
three containment edges") unless the Cypher is re-run and its output archived — it is not in
any committed artifact.*

9.9 Discussion
&nbsp;&nbsp;&nbsp;&nbsp;9.9.1 What Agency Buys, and What It Costs
&nbsp;&nbsp;&nbsp;&nbsp;9.9.2 When Verification Helps and When It Over-Hedges
&nbsp;&nbsp;&nbsp;&nbsp;9.9.3 Threats to Validity
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Include the verifier instrumentation
gap: `verifier_node` logs only* unsupported *claims, never the accepted ones with their
matched triples. Wrongful-acceptance cases are therefore not self-diagnosing from the logs
— both specimens in §9.5.3 required manual trace reconstruction. That polarity is
consequently reported anecdotally while wrongful rejection is reported at census scale,
and the asymmetry must be stated rather than left for a reader to infer.)*

---

## 10. Conclusion — *~5 pages*

10.1 Summary of Contributions *(chapter-by-chapter walkthrough, as in the gold standard)*

10.2 Limitations

10.3 Future Work
&nbsp;&nbsp;&nbsp;&nbsp;**Structure this in two tiers, as `synthesis.md` §5 does, because the
census supports different confidence levels.** *Tier one —* **defects with a clean repeated
pattern behind them, not a hypothesis**: *(a) the entity-extraction bug (9 instances; stop
defaulting to the sentence's grammatical subject); (b) the evaluator abandoning a
solidly-scored relation and never returning (8 instances, scores up to 0.73); (c) the drafter
hedging on a fact it has just stated with* `verifier_outcome: grounded` *(6 instances). Each is
a named, counted failure mass, and each is small enough to fix. Tier two — architectural, each
now* earned *by a labelled mass rather than asserted: adaptive decomposition gating,
semantic-level verification, an explicit set-intersection operator for compound questions, and
ordinal/literal support. The last of these was not in the original plan and belongs there on
the numbers alone —* `kg_gap` *is the third-largest category overall at 44 and CWQ's single
largest hedge category at 24.*
&nbsp;&nbsp;&nbsp;&nbsp;10.3.1 Path Fidelity Against Gold SPARQL Relation Chains
&nbsp;&nbsp;&nbsp;&nbsp;10.3.2 Logging Accepted Claims to Make Wrongful Acceptance Measurable
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(the fix for the §9.9.3 instrumentation
gap: persist each accepted claim with the triples that matched it, converting the
wrongful-acceptance class from anecdote to rate)*
&nbsp;&nbsp;&nbsp;&nbsp;10.3.3 LLM-Constructed Knowledge Graphs as a Controlled Comparison
&nbsp;&nbsp;&nbsp;&nbsp;10.3.4 Rollout-Based Value Estimation
&nbsp;&nbsp;&nbsp;&nbsp;10.3.5 Temporal and Multi-Source Knowledge Environments
&nbsp;&nbsp;&nbsp;&nbsp;10.3.6 Transfer to High-Stakes Domains

---

## Back Matter

- References
- Index
- Appendix A: Prompt Templates
- Appendix B: Tool API Specification and Cypher Templates
- Appendix C: Sampled Question IDs and Run Manifests
- Appendix D: Annotation Instructions and Label Schema
- Appendix E: Implementation Notes *(~2 pages: LangGraph `config` parameter injection,
  the routers-read / nodes-write state discipline, the partial-edit hazard, and the
  cache-identity verification pattern — proving a code change did not perturb the frozen
  path by confirming 100% cache replay. The last of these is a reproducibility technique
  rather than a bug story, and carries the most weight with a methods-minded examiner.
  Also record the verifier logging gap from §9.9.3 here, as a worked example of an
  instrumentation decision that constrained what could later be measured. §7.10 points
  here.)*

---

## Page Budget

| Chapter | Budget | Round 1 | Current |
| --- | ---: | ---: | ---: |
| 1 Introduction | 8 | 7 | 8 |
| 2 Background and Preliminaries | 5 | 6 | 6 |
| 3 Related Work | 7 | 8 | 8 |
| 4 The Knowledge Environment | 10 | 9 | 10 |
| 5 The AGR Framework | 11 | 13 | 18 |
| 6 The Structural Verification Layer | 8 | 13 | 15 |
| 7 Experimental Setup | 11 | 15 | 20 |
| 8 Results | 12 | 12 | 18 |
| 9 Error Analysis and Discussion | 10 | 15 | 19 |
| 10 Conclusion | 5 | 6 | 8 |
| **Body total** | **87** | **104** | **130** |
| References + Index + Appendices | ~12 | 6 + appendices | 6 + 29 |

**The body is 130 pages against a 60–90 target — 44% over the 90 ceiling.** Body runs pages 1–130;
References begin on 131, the index on 136; the document is 182 pages including front
matter and five appendices.

The decision to cross the ceiling was taken at 104 pages and recorded so it would not
be revisited by accident: *cross the ceiling if needed.* That decision was made
against a smaller number. The 26 pages added since fall in Chapter 5 (+5), Chapter 7
(+5), Chapters 8 and 9 (+6 and +4), Chapters 6 and 10 (+2 each), and one page each in
1 and 4 — corrections, scoping notes and disclosure statements added in review, not
new material. **Re-confirm before submission whether the department enforces a hard
cap.** If it does, the compression targets are unchanged: Chapters 2 and 3 first,
never Chapter 9.

Where the 43 pages over budget went, and why each is defensible if questioned.
The `r1` column is the round-1 overrun measured at 104 pages; `now` is measured at
130. The difference between the two columns is review work — corrections, scoping
notes, and baseline-configuration disclosures — not new material.

| Chapter | r1 | now | Reason |
| --- | ---: | ---: | --- |
| 9 Error Analysis | +5 | **+9** | The census is a population of 259, not a sample; three named mechanism findings, three counted defect families, the benchmark-defect provenance argument. Grew by the union-of-subgraphs and name-keying threats, the Phoenician case, the corrected 57-question exclusion arithmetic, and the verifier-unit restatement in §9.5.4. |
| 7 Setup | +4 | **+9** | Ten sections averaging 1.5 pages, all pre-registered method or verified numbers. Grew by the GraphRAG one-hop scoping note, the hedge-counting convention, the two baseline candidate-width disclosures (§7.4.3 fanout cap, §7.4.4 relation/neighbour caps), and the reconciliation of the sample ceiling against the validation gate's population ceiling (§7.2.3). |
| 6 Verification | +5 | **+7** | Algorithm, attribution-census table, worked example, by-construction failure analysis. Grew by Figure 6.1, the post-hoc-verification positioning, the supporting-triples persistence gap, and the test-set correction to the repair-route claim. |
| 8 Results | +0 | **+6** | Grew entirely in review: §8.4, the clipped/unclipped split of the agentic-baseline margin, the per-stratum radius qualification, the token-vs-call frontier correction, and the withdrawal of the verifier's precision attribution — precision and recall columns in Table 8.8 plus the multiple-comparison policy in §8.8.5. |
| 5 Framework | +2 | **+7** | τ signal-maximum derivation and the design-validation table. Grew by the state-machine figure, `verify_triple`'s real status, the three implementation deviations (two σ, one ban-list), §5.10's provenance disclosure, and the corrected account of which budgets are enforced where. |
| 10 Conclusion | +1 | **+3** | Future work is two-tiered (earned repairs vs. architectural), which the census made possible; plus the equal-width and two-hop baseline experiments and two added limitations. |
| 2, 3 | +1, +1 | **+1, +1** | Unchanged since round 1. |
| 1, 4 | −1, −1 | **+0, +0** | Each gained a page in review — §1.7's environment scoping and §4.3.3's two hop conventions — bringing both back to budget. |

**If a page cut is ever forced**, the order is unchanged: §2.6, §3.1, §3.4 first
(background the committee already has), then Chapter 7's §7.4 and §7.6 enumerations
into the appendices. **Chapters 6 and 9 stay off the table** — the verification
specification and the error census are what distinguish this from a system report.

**Chapter 9 is not a compression target** — decided deliberately, not under page
pressure. It now carries three families in §9.3, four subsections in §9.5, and a
provenance subsection in §9.8, which does not fit in eight pages. It is budgeted at **10**,
with the two pages taken from Chapters 2 and 3, where the material is background the
committee already has. The error analysis and benchmark-defect work are what distinguish
this thesis from a system report; if the count still runs long, cut §2.6, §3.1, and §3.4
further before touching Chapter 9.

---

## Proposed Source-File Mapping

| Chapter | File |
| --- | --- |
| 1 | `chapters/introduction.tex` |
| 2 | `chapters/preliminaries.tex` |
| 3 | `chapters/relatedwork.tex` |
| 4 | `chapters/environment.tex` |
| 5 | `chapters/framework.tex` |
| 6 | `chapters/verification.tex` |
| 7 | `chapters/setup.tex` |
| 8 | `chapters/results.tex` |
| 9 | `chapters/erroranalysis.tex` |
| 10 | `chapters/conclusion.tex` |
| Appendices | `appendices/*.tex` |
