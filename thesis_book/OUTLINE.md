# Thesis Outline — Table of Contents

**Title:** Agentic Graph Reasoning: Autonomous Knowledge Graph Navigation for Fact
Verification and Hallucination Mitigation in Large Language Models

**Target:** 60–90 pages of body text. The per-chapter estimates below total **87 pages**
(front matter is roman-numbered and does not count against the budget).

Structural conventions follow `thesis_templates/buetcsepgthesis.pdf` (the approved
UNN thesis): a heavily sub-sectioned Introduction that ends with *Our Contribution* and
*Thesis Organization*, a separate *Preliminaries* chapter for concepts the reader must
have before the technical chapters, and a Conclusion that walks the reader back through
the thesis chapter by chapter before opening the future-work discussion.

### Terminology discipline

The word **"tier"** is reserved for **one** concept in this thesis: the two-tier
groundedness *metric* (§7.5.3, §8.5). Two other cascades in the system must therefore be
named differently wherever they appear:

- The verification layer's two checks (§6.3) are the **structural check** and the
  **entailment check** — never "Tier 1 / Tier 2".
- The entity resolver's three-stage cascade (§4.6) is **exact / lexical / vector**
  matching — never "Tier 1 / Tier 2 / Tier 3", despite the identifiers used in
  `scripts/entity_resolver.py`.

Verifier errors are described as **wrongly rejected** / **wrongly accepted** throughout
(§6.8, §9.5). Do not use `verifier_fn` / `verifier_fp` in the thesis text: the two sources
disagree about what those names mean. `annotation_taxonomy.md:14` glosses the pair as
"passed a wrong claim / hedged a right one", but all six labelled rows in
`labels_{webqsp,cwq}.csv` use `verifier_fn` for *hedged a right one*, and the annotator's
own note at `annotation_taxonomy.md:80` ("forced into `verifier_fn` since no verifier
rejection is involved") confirms that usage is deliberate. **The labels are internally
consistent; the table's gloss is reversed and should be corrected at source** before either
is quoted.

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

## 2. Background and Preliminaries — *~6 pages*

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

## 3. Related Work — *~8 pages*

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
&nbsp;&nbsp;&nbsp;&nbsp;4.6.1 The Exact / Lexical / Vector Cascade
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
&nbsp;&nbsp;&nbsp;&nbsp;7.3.1 Trajectory Stability Under Temperature-Zero Decoding
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(hosted APIs are only approximately
deterministic at temperature 0; sequential agents amplify per-call divergence; measured
trajectory stability across the qualification runs)*
&nbsp;&nbsp;&nbsp;&nbsp;7.3.2 Response Caching as the Reproducibility Backstop

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

## 9. Error Analysis and Discussion — *~8 pages*

9.1 Annotation Protocol and the Failure Taxonomy
&nbsp;&nbsp;&nbsp;&nbsp;9.1.1 Category and Subtype Schema
&nbsp;&nbsp;&nbsp;&nbsp;9.1.2 Sampling Asymmetry: Census versus Stratified Sample
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(WebQSP is a full census of remaining
failures; CWQ is a stratified sample of wrongs and hedges — so wrong-answer and hedge
histograms are reported separately and never pooled)*

9.2 Distribution of Failure Categories Across Datasets

9.3 Decomposition and Planning Errors
&nbsp;&nbsp;&nbsp;&nbsp;*(including the context-stripping mechanism)*

9.4 Relation-Selection and Navigation Errors

9.5 Verifier Rejection and Acceptance Errors
&nbsp;&nbsp;&nbsp;&nbsp;**Confirmed as a standalone section — eight specimens, both
polarities.** Inventory: six census cases labelled `verifier_fn` /
`structural_not_semantic` (3 WebQSP + 3 CWQ), all of them the verifier *rejecting a
correct claim*; plus the Wilson and Seth MacFarlane cases, both the verifier *accepting an
unsupported one*.
&nbsp;&nbsp;&nbsp;&nbsp;9.5.1 Defining the Error Polarities
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Open with an explicit convention and use
it consistently thereafter.** The annotation labels and the taxonomy table in
`results/phase4/annotation_taxonomy.md` disagree about which polarity `verifier_fn` names
(see the note below); the thesis must not inherit that ambiguity. Recommended: name the
polarities in prose — *wrongly rejected* and *wrongly accepted* — and avoid fn/fp
entirely, since the verifier's output is `supported` / `unsupported` and "positive" has no
stable referent.
&nbsp;&nbsp;&nbsp;&nbsp;9.5.2 Wrongly Rejected: Semantically Correct, Structurally Unmatched
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(The six census cases. All share one
mechanism — the claim is true and the answer correct, but no single triple states it in
the drafted phrasing, so a transitively-true or differently-anchored fact is rejected and
the retry loses the answer. The De Niro case is distinct and worth separating: the
rejection message references a different candidate entirely, suggesting a claim/candidate
pairing bug rather than a structural mismatch.)*
&nbsp;&nbsp;&nbsp;&nbsp;9.5.3 Wrongly Accepted: Unsupported Claims Passed as Grounded
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(Wilson, plus MacFarlane — the graph
contains no edge from Seth MacFarlane to Lion-O or ThunderCats, confirmed by direct query,
yet the claim passed as `grounded`.)*
&nbsp;&nbsp;&nbsp;&nbsp;9.5.4 Rates Across the Test Matrix
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(the `unsupported` firings in
`score_run_phase4.csv` are the population these specimens are drawn from)*

9.6 Knowledge-Graph Gaps: Literals, Temporal Qualifiers, and Ordinals
&nbsp;&nbsp;&nbsp;&nbsp;*(invokes the unanswerable-in-environment class defined in §4.7.4)*

9.7 The Echo Attractor: Answering with the Topic or an Intermediate Entity

9.8 Benchmark Defects: Gold Noise and Ambiguous Questions
&nbsp;&nbsp;&nbsp;&nbsp;*(Open by separating two numbers that are easy to conflate: the
share of questions the consensus pass* flagged, *and the much smaller share adjudication
confirmed as genuine label defects. Most flagged items were not label errors — they were
all five systems converging on the same wrong answer. That phenomenon is §9.7's; point
there for it and keep this section to the defects proper.)*
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
caught it. Note also that the adjudication note in `prepass_goldnoise_cwq.json` calls Comal
"a neighbouring county," which understates the overlap — worth correcting there before it
is quoted in the thesis.)*

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

| Chapter | Pages |
|---|---:|
| 1 Introduction | 8 |
| 2 Background and Preliminaries | 6 |
| 3 Related Work | 8 |
| 4 The Knowledge Environment | 10 |
| 5 The AGR Framework | 11 |
| 6 The Structural Verification Layer | 8 |
| 7 Experimental Setup | 11 |
| 8 Results | 12 |
| 9 Error Analysis and Discussion | 8 |
| 10 Conclusion | 5 |
| **Body total** | **87** |
| References + Index + Appendices | ~12 |

**Chapter 9 is not a compression target.** The error analysis and the benchmark-defect
work are what distinguish this thesis from a system report. If the count runs long, cut
further from §2.6, §3.1, and §3.4 — the material there is background the committee
already has.

---

## Proposed Source-File Mapping

| Chapter | File |
|---|---|
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
