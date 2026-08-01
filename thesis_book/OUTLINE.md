# Thesis Outline — Table of Contents

**Title:** Agentic Graph Reasoning: Autonomous Knowledge Graph Navigation for Fact
Verification and Hallucination Mitigation in Large Language Models

**Target:** 60–90 pages of body text. Per-chapter page estimates below total ~86 pages
(front matter is roman-numbered and does not count against the budget).

Structural conventions follow `thesis_templates/buetcsepgthesis.pdf` (the approved
UNN thesis): a heavily sub-sectioned Introduction that ends with *Our Contribution* and
*Thesis Organization*, a separate *Preliminaries* chapter for concepts the reader must
have before the technical chapters, and a Conclusion that walks the reader back through
the thesis chapter by chapter before opening the future-work discussion.

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

## 1. Introduction — *~9 pages*

1.1 Hallucination in Large Language Models
&nbsp;&nbsp;&nbsp;&nbsp;1.1.1 Where Hallucination Originates: Training Data, Model, and Prompt
&nbsp;&nbsp;&nbsp;&nbsp;1.1.2 Why Multi-Hop Questions Are the Hard Case

1.2 From Retrieval Augmentation to Graph-Structured Grounding
&nbsp;&nbsp;&nbsp;&nbsp;1.2.1 Vector Retrieval and Its Structural Blind Spot
&nbsp;&nbsp;&nbsp;&nbsp;1.2.2 Knowledge Graphs and Static GraphRAG
&nbsp;&nbsp;&nbsp;&nbsp;1.2.3 Agentic Retrieval: Reasoning as Navigation

1.3 Limitations of Existing Agentic KGQA Systems
&nbsp;&nbsp;&nbsp;&nbsp;1.3.1 No Verification Before the Answer Is Emitted
&nbsp;&nbsp;&nbsp;&nbsp;1.3.2 Unquantified Contribution of Individual Agentic Mechanisms
&nbsp;&nbsp;&nbsp;&nbsp;1.3.3 Accuracy Reported Without Cost

1.4 Problem Statement

1.5 Research Questions
&nbsp;&nbsp;&nbsp;&nbsp;1.5.1 RQ1: Does Agentic Navigation Improve Multi-Hop Factual Accuracy?
&nbsp;&nbsp;&nbsp;&nbsp;1.5.2 RQ2: Does Pre-Generation Structural Verification Reduce Hallucination?
&nbsp;&nbsp;&nbsp;&nbsp;1.5.3 RQ3: Which Components Contribute What, at What Token Cost?

1.6 Our Contribution

1.7 Scope and Delimitations

1.8 Thesis Organization

---

## 2. Background and Preliminaries — *~8 pages*

2.1 Knowledge Graphs
&nbsp;&nbsp;&nbsp;&nbsp;2.1.1 Triples, Entities, and Relations
&nbsp;&nbsp;&nbsp;&nbsp;2.1.2 Freebase: MIDs, Schema, and Mediator (CVT) Nodes
&nbsp;&nbsp;&nbsp;&nbsp;2.1.3 Property Graphs, Neo4j, and Cypher

2.2 Knowledge Graph Question Answering
&nbsp;&nbsp;&nbsp;&nbsp;2.2.1 Multi-Hop Questions and Constraint Satisfaction
&nbsp;&nbsp;&nbsp;&nbsp;2.2.2 Semantic Parsing versus Information Retrieval Approaches
&nbsp;&nbsp;&nbsp;&nbsp;2.2.3 Evaluation Conventions: Hits@1 and F1

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
&nbsp;&nbsp;&nbsp;&nbsp;2.6.1 Bootstrap Confidence Intervals
&nbsp;&nbsp;&nbsp;&nbsp;2.6.2 McNemar's Test for Paired Correctness
&nbsp;&nbsp;&nbsp;&nbsp;2.6.3 Cohen's κ for Annotator Agreement

---

## 3. Related Work — *~9 pages*

3.1 Static Graph-Augmented Generation
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1 GraphRAG and Query-Focused Summarization
&nbsp;&nbsp;&nbsp;&nbsp;3.1.2 HippoRAG and Memory-Structured Retrieval
&nbsp;&nbsp;&nbsp;&nbsp;3.1.3 Temporal Extensions (T-GRAG)

3.2 Path-Retrieval and Semantic-Parsing KGQA
&nbsp;&nbsp;&nbsp;&nbsp;3.2.1 Reasoning-on-Graphs
&nbsp;&nbsp;&nbsp;&nbsp;3.2.2 StructGPT and KG-Agent

3.3 Agentic Graph Exploration
&nbsp;&nbsp;&nbsp;&nbsp;3.3.1 Think-on-Graph
&nbsp;&nbsp;&nbsp;&nbsp;3.3.2 Plan-on-Graph
&nbsp;&nbsp;&nbsp;&nbsp;3.3.3 Generate-on-Graph and Reasoning with Trees

3.4 Verification and Self-Correction in Language Models
&nbsp;&nbsp;&nbsp;&nbsp;3.4.1 Chain-of-Verification
&nbsp;&nbsp;&nbsp;&nbsp;3.4.2 Multi-Agent Debate
&nbsp;&nbsp;&nbsp;&nbsp;3.4.3 Ontology-Guided and Self-Correcting Graph RAG

3.5 Measuring Factuality
&nbsp;&nbsp;&nbsp;&nbsp;3.5.1 Claim-Decomposition Metrics
&nbsp;&nbsp;&nbsp;&nbsp;3.5.2 Factuality Benchmarks and Their Limits

3.6 Comparative Summary of Agentic KGQA Systems
&nbsp;&nbsp;&nbsp;&nbsp;*(the cross-system table: exploration strategy, decomposition, backtracking,
pre-generation verification, datasets, reported Hits@1 — this table also justifies the
baseline selection in Chapter 7)*

3.7 Positioning of This Work

---

## 4. The Knowledge Environment — *~10 pages*

4.1 Design Goals
&nbsp;&nbsp;&nbsp;&nbsp;4.1.1 Decoupling the Graph Source from the Question Sets
&nbsp;&nbsp;&nbsp;&nbsp;4.1.2 Why a Curated Subgraph Rather Than LLM-Extracted Triples

4.2 Source Data
&nbsp;&nbsp;&nbsp;&nbsp;4.2.1 The Freebase Snapshot
&nbsp;&nbsp;&nbsp;&nbsp;4.2.2 WebQSP and ComplexWebQuestions as Question Sets

4.3 Subgraph Extraction
&nbsp;&nbsp;&nbsp;&nbsp;4.3.1 Topic-Entity Seeding and k-Hop Expansion
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

4.7 Environment Validation Gate
&nbsp;&nbsp;&nbsp;&nbsp;4.7.1 Answer-Reachability Protocol
&nbsp;&nbsp;&nbsp;&nbsp;4.7.2 Coverage Results and the Induced Accuracy Ceiling
&nbsp;&nbsp;&nbsp;&nbsp;4.7.3 Analysis of Linking Misses and Gate Failures

---

## 5. The AGR Framework: Architecture and Navigation — *~12 pages*

5.1 Architectural Overview
&nbsp;&nbsp;&nbsp;&nbsp;*(figure: the Planner → Explorer → Evaluator → {Backtrack | Verify} → Answerer
state machine)*

5.2 The Graph Tool API
&nbsp;&nbsp;&nbsp;&nbsp;5.2.1 Rationale: Constrained Tools Instead of Free-Form Cypher Generation
&nbsp;&nbsp;&nbsp;&nbsp;5.2.2 `search_entity`
&nbsp;&nbsp;&nbsp;&nbsp;5.2.3 `get_relations`
&nbsp;&nbsp;&nbsp;&nbsp;5.2.4 `get_neighbors`
&nbsp;&nbsp;&nbsp;&nbsp;5.2.5 `verify_triple`
&nbsp;&nbsp;&nbsp;&nbsp;5.2.6 Determinism, Caching, and Tool-Call Logging

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

6.3 Two-Tier Claim Checking
&nbsp;&nbsp;&nbsp;&nbsp;6.3.1 Tier 1: Structural Grounding Against the Traversed Subgraph
&nbsp;&nbsp;&nbsp;&nbsp;6.3.2 Tier 2: LLM Entailment for Paraphrased Claims
&nbsp;&nbsp;&nbsp;&nbsp;6.3.3 Why Structural Checking Comes First

6.4 Repair Policies for Unsupported Claims
&nbsp;&nbsp;&nbsp;&nbsp;6.4.1 Targeted Re-Exploration Under Remaining Budget
&nbsp;&nbsp;&nbsp;&nbsp;6.4.2 Answer Rewriting and Hedging
&nbsp;&nbsp;&nbsp;&nbsp;6.4.3 Iteration Cap and the Draft-Only Fallback

6.5 Entity Filtering of the Final Answer

6.6 Output Contract: Answer Paired with Supporting Triples

6.7 A Worked Example

6.8 Failure Modes by Construction: False Positives and False Negatives

---

## 7. Experimental Setup — *~10 pages*

7.1 Mapping Experiments to Research Questions

7.2 Test Sets
&nbsp;&nbsp;&nbsp;&nbsp;7.2.1 WebQSP
&nbsp;&nbsp;&nbsp;&nbsp;7.2.2 ComplexWebQuestions
&nbsp;&nbsp;&nbsp;&nbsp;7.2.3 Stratified Sampling, Seeds, and Published Question IDs
&nbsp;&nbsp;&nbsp;&nbsp;7.2.4 Hop-Count Stratification

7.3 Backbone Model Selection and Qualification

7.4 Baseline Systems
&nbsp;&nbsp;&nbsp;&nbsp;7.4.1 No-Retrieval LLM (Parametric-Memory Control)
&nbsp;&nbsp;&nbsp;&nbsp;7.4.2 Vector-RAG over Verbalized Triples
&nbsp;&nbsp;&nbsp;&nbsp;7.4.3 Static GraphRAG
&nbsp;&nbsp;&nbsp;&nbsp;7.4.4 Think-on-Graph (Agentic Baseline)
&nbsp;&nbsp;&nbsp;&nbsp;7.4.5 Variables Held Constant Across All Systems

7.5 Metrics
&nbsp;&nbsp;&nbsp;&nbsp;7.5.1 Answer Accuracy: Hits@1 and F1
&nbsp;&nbsp;&nbsp;&nbsp;7.5.2 Accounting for Hedges and Abstentions
&nbsp;&nbsp;&nbsp;&nbsp;7.5.3 Groundedness and Hallucination Rate
&nbsp;&nbsp;&nbsp;&nbsp;7.5.4 Efficiency: Tokens, LLM Calls, and Wall-Clock Latency

7.6 The Groundedness Judge and Its Validation
&nbsp;&nbsp;&nbsp;&nbsp;7.6.1 Independence of the Judge from the Answering System
&nbsp;&nbsp;&nbsp;&nbsp;7.6.2 Human Annotation Protocol
&nbsp;&nbsp;&nbsp;&nbsp;7.6.3 Agreement Between Judge and Human Annotator

7.7 Gold-Answer Quality Control
&nbsp;&nbsp;&nbsp;&nbsp;7.7.1 The Gold-Noise Problem in WebQSP and CWQ
&nbsp;&nbsp;&nbsp;&nbsp;7.7.2 Consensus Pre-Pass and Per-Item Adjudication
&nbsp;&nbsp;&nbsp;&nbsp;7.7.3 Census-Based Exclusions and the Dual-Reporting Policy

7.8 Ablation Conditions

7.9 Hyperparameter Selection on the Development Set
&nbsp;&nbsp;&nbsp;&nbsp;7.9.1 The α–τ Sweep Protocol
&nbsp;&nbsp;&nbsp;&nbsp;7.9.2 Development Set Construction and Coverage

7.10 Implementation, Environment, and Reproducibility

---

## 8. Results — *~12 pages*

8.1 Development-Set Tuning Outcomes

8.2 Main Results on WebQSP

8.3 Main Results on ComplexWebQuestions

8.4 Accuracy Broken Down by Hop Count

8.5 Groundedness and Hallucination Rate Across Systems

8.6 Efficiency and Cost
&nbsp;&nbsp;&nbsp;&nbsp;8.6.1 Token and Call Budgets per System
&nbsp;&nbsp;&nbsp;&nbsp;8.6.2 The Accuracy–Cost Frontier

8.7 Ablation Study
&nbsp;&nbsp;&nbsp;&nbsp;8.7.1 Without the Planner
&nbsp;&nbsp;&nbsp;&nbsp;8.7.2 Without Backtracking
&nbsp;&nbsp;&nbsp;&nbsp;8.7.3 Without the Verification Layer
&nbsp;&nbsp;&nbsp;&nbsp;8.7.4 Embedding-Only Scoring
&nbsp;&nbsp;&nbsp;&nbsp;8.7.5 Paired Significance Testing

8.8 Findings Against RQ1, RQ2, and RQ3

---

## 9. Error Analysis and Discussion — *~8 pages*

9.1 Annotation Protocol and the Failure Taxonomy

9.2 Distribution of Failure Categories Across Datasets

9.3 Decomposition and Planning Errors

9.4 Relation-Selection and Navigation Errors

9.5 Verifier False Positives and False Negatives

9.6 Knowledge-Graph Gaps: Literals, Temporal Qualifiers, and Ordinals

9.7 The Echo Attractor: Answering with the Topic or an Intermediate Entity

9.8 Benchmark Defects: Gold Noise and Ambiguous Questions

9.9 Discussion
&nbsp;&nbsp;&nbsp;&nbsp;9.9.1 What Agency Buys, and What It Costs
&nbsp;&nbsp;&nbsp;&nbsp;9.9.2 When Verification Helps and When It Over-Hedges
&nbsp;&nbsp;&nbsp;&nbsp;9.9.3 Threats to Validity

---

## 10. Conclusion — *~5 pages*

10.1 Summary of Contributions *(chapter-by-chapter walkthrough, as in the gold standard)*

10.2 Limitations

10.3 Future Work
&nbsp;&nbsp;&nbsp;&nbsp;10.3.1 Path Fidelity Against Gold SPARQL Relation Chains
&nbsp;&nbsp;&nbsp;&nbsp;10.3.2 LLM-Constructed Knowledge Graphs as a Controlled Comparison
&nbsp;&nbsp;&nbsp;&nbsp;10.3.3 Rollout-Based Value Estimation
&nbsp;&nbsp;&nbsp;&nbsp;10.3.4 Temporal and Multi-Source Knowledge Environments
&nbsp;&nbsp;&nbsp;&nbsp;10.3.5 Transfer to High-Stakes Domains

---

## Back Matter

- References
- Index
- Appendix A: Prompt Templates
- Appendix B: Tool API Specification and Cypher Templates
- Appendix C: Sampled Question IDs and Run Manifests
- Appendix D: Annotation Instructions and Label Schema

---

## Page Budget

| Chapter | Pages |
|---|---:|
| 1 Introduction | 9 |
| 2 Background and Preliminaries | 8 |
| 3 Related Work | 9 |
| 4 The Knowledge Environment | 10 |
| 5 The AGR Framework | 12 |
| 6 The Structural Verification Layer | 8 |
| 7 Experimental Setup | 10 |
| 8 Results | 12 |
| 9 Error Analysis and Discussion | 8 |
| 10 Conclusion | 5 |
| **Body total** | **91** |
| References + Index + Appendices | ~10 |

If the count runs long, the two safe compressions are folding Chapter 9 into Chapter 8
as sections 8.9–8.15, and trimming Chapter 2 to only the concepts actually used later.

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
