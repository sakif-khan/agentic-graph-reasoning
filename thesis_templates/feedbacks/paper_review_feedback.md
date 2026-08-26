# Supervisor review — status of the eight critical issues

**Date:** 27 August 2026 · **Context:** pre-defense on 29 August; no
experimental changes in that window, so every remedy below is
documentation, disclosure or placement rather than a new measurement.

Read each entry as three separate things, because they carry different
weight: what the thesis already said before this review, what changed in
response to it, and what remains unfixed together with the reason. Where
an issue could only be removed by running something, that is stated as
such rather than dressed up.

**Every citation here was resolved against the built PDFs, not from
memory.** Section numbers come from each document's own outline and page
numbers are the printed page labels — so `§6.8, p. 66` means the sentence
is on the page numbered 66, which for the book is not the 66th page of
the file, because the front matter is roman. Where a section begins on
one page and the sentence lands on the next, the page given is the
**sentence's**, because that is the page you turn to when asked. Six
citations in the first version of this note were wrong; they are listed
at the end.

The eight issues were a table until this revision. They are prose now
because the cells had grown past 1,800 characters and a Markdown table
row cannot be wrapped, so the table could not be held to 80 columns
without losing what the cells said.

---

## 1. The verifier does not verify the asserted relationship

**Addressed as disclosure; not fixed in code.**

Already stated before this round. **Book §6.3.1** *The Structural Check*,
**pp. 56–57** says both graph routes are relation-agnostic and why: the
claim's *r* is free text with no Freebase predicate — "X played for Y"
runs through a roster mediator naming nothing about playing. **Book
§6.8** *Failure Modes by Construction*, **p. 66** calls it "the layer's
principal acceptance risk" and uses the mother/child example.

**What was missing was scale, and that is new.** A `claim_routes` block
now measures it from the frozen records: at test scale 2,110 claims over
828 verifier firings, 2,008 accepted; `verify_connection` consulted on
100 of them (4.7%) and accepting 39. The log cannot split the remaining
1,969 between traversed adjacency and entailment, so the relation-blind
share is reported as the interval **[39, 2,008]** — two orders of
magnitude wide — rather than as a point.

That interval appears in **book §6.3.1 (pp. 56–57)**, **§6.8 (p. 66)**,
**§9.5.4** *A Rate for One Polarity, and a Blank for the Other*
**(p. 117)**, and **paper §8.1** *What Bounds the Contribution*
**(p. 39)**.

Also new: a bounding sentence at first use of the layer's name, in **book
§1.6.1** *The AGR Framework and Its Verification Layer* **(p. 6)** and
**paper §1** *Introduction* **(p. 4)**. And the limit now reaches the
**deck and transcript, where it was entirely absent** — **deck slide 14**
*What structural means — and what it does not* states it, **transcript
§14** speaks it, and the anticipated-question entry answers the
supervisor's wording verbatim ("Your verifier doesn't verify the
relationship — any edge between the two entities passes").

Not fixed: the verifier still doesn't test the relation.

## 2. The claimed evidence contract is not externally auditable

**Disclosed, ranked first, and machine-enforced — not fixed.**

The thesis already calls this its most serious limitation. **Book §6.6**
*Output Contract: Answer Paired with Supporting Triples*, **p. 62**
carries both bounds on one page: "Only one of the three routes records
evidence", and `RunLogger` writes `n_supporting_triples` and "drops the
list, so no committed artifact in this work contains a single supporting
triple".

It is **limitation 1 of 8 in book §10.2** *Limitations*, **p. 127** —
"Wrongful acceptance is unmeasured, and the evidence is not persisted" —
that is, ranked first by severity rather than buried.

The 112,901-run-record verification lives in the test suite
(`tests/test_output_contract_claims.py`), not in the prose. That suite
refuses any document claiming the contract without stating both bounds,
route and record, enforced **per document** — so the deck and transcript
each carry both rather than relying on a section the audience never
reads. The transcript answers "Show me one supporting triple, then" as a
limitation rather than an evasion.

Not fixed because the fix is persisting triples and re-running, which is
an experiment: excluded by the window, and it would separate the code
from results already frozen against it.

## 3. Verification produces no measurable accuracy improvement

**Reframing now complete in all four documents; titles deliberately
unchanged.**

The paper already did this. Its **abstract, p. 2** says "three of four
components — including claim verification — show no detectable accuracy
effect", and **paper §1**, **p. 4** states the contribution is the output
contract "rather than an accuracy gain".

**The thesis abstract was the gap and is fixed.** It previously said only
"an effect in only one component", leaving the reader to work out which
three were null; the **book abstract, p. xvi** now names claim
verification explicitly. Underpowering is stated separately as
**limitation 2 in book §10.2, p. 127** — "Three of four ablations are
underpowered" — so "not detected" is never presented as "none".

On the title: the paper's already scopes the mechanism — *Claim-Level
Structural Verification* — with a source comment recording the choice not
to say "fact verification". The thesis title is the CASR-registered one,
fixed at registration and not revisable; the run-in paragraph **"How to
read the title" in book §1.7** *Scope and Delimitations*, **p. 8** walks
all three over-broad terms (*hallucination mitigation*, *autonomous*,
*fact verification*) and states what the measurements support instead.
That is the whole available remedy and it is in place.

## 4. The main baseline comparison is not fully controlled

**Disclosed with measured numbers; not re-run.**

Nothing needed changing this round — it was already the most thoroughly
handled of the eight. **Book §7.4.4** *Think-on-Graph (Agentic
Baseline)*, **p. 78** defines the widths and gives the asymmetry measured
from the committed tool logs: ToG's 40-relation cut binds on 31.6% of the
1,651 entities it expanded and the 20-neighbour cut on 32.8% of its 7,992
neighbour calls, against AGR's relation cap binding once in 3,097
expansions and its neighbour cap on 3.3%.

The split table is **Table 8.4**, in **book §8.4** *Where the Margin Over
the Agentic Baseline Comes From*, **p. 92**; in the paper it is **Table
3, p. 24**, discussed in **§5.3, p. 25**.

It is **limitation 5 in book §10.2, p. 128** — "The agentic baseline
prunes from a narrower candidate set" — and restated in **book §9.9.3**
*Threats to Validity*, **p. 122** and **paper §8.2** *What Bounds the
Comparisons*, **p. 40**. The paper defines the widths in **§4.2, p. 17**.
In the deck it is **slide 19** *What is not held equal* (`40/20 vs
300/200`), a slide of its own, plus the limitations bullet on **slide
30**.

It also carries the argument for the room: a narrower candidate set makes
each step *cheaper*, so it cannot explain why ToG runs out of calls —
width cannot rescue the budget reading. The residual gap on questions ToG
finishes is stated as a **lower bound** on what it could resolve at equal
width, not an estimate.

Re-running at 300/200 is real API cost and prompt changes miss the cache;
it is already the first item in future work.

## 5. Only one run per system

**Disclosed; deliberately not attempted, for a reason worth knowing.**

**Book §7.3.1** *Trajectory Stability Under Temperature-Zero Decoding*,
**p. 73** measures the frozen backbone at 8 of 12 probes reproducing,
≈67% — roughly one trajectory in three differs. **Book §9.9.3, p. 123**
tells the reader to treat that figure as unquantified rather than as
evidence, and it is part of **limitation 4 in §10.2, p. 128**
("single-environment, single-backbone, single-annotator"). The paper
states it in **§8.2, p. 39**. Unchanged this round.

The reason it isn't a quick win is set out in **book §7.3.2** *Response
Caching as the Reproducibility Backstop*, **p. 74**: **a same-config
re-run would measure nothing.** The response cache keys on model,
temperature, reasoning effort and the full prompt, so an identical rerun
is 100% cache hits and reproduces the run exactly, budget snapshots
included. Genuine variance requires bypassing the cache at full price — a
new experiment, not a re-execution.

## 6. Evaluation uses only 400 questions per benchmark

**Disclosed as a stated bound; not expanded.**

The supervisor grants this is defensible. The 400 is a **pre-registered**
scoping decision, not a post-hoc one: **book §7.1.1** *Pre-Registration
and the No-Tuning Policy*, **p. 69** lists sample size among the
quantities fixed in advance, and **book §7.2.2** *Stratified Sampling,
Seeds, and Published Question IDs*, **p. 71** gives the construction and
publishes the question IDs.

**Note honestly:** there is no limitation entry in §10.2 that names 400
as such. The nearest is limitation 2, "Three of four ablations are
underpowered" (**p. 127**), which states the consequence at *n* ≈ 200 per
split rather than the sample size itself. If asked, that is the right
place to point.

Unchanged this round; full test splits are roughly $45–55 of API spend
plus hours of runtime, which is an experiment and outside the window.
Worth saying plainly in the room: the 400 per benchmark are *certified*
questions, and every comparison is within-environment and paired, so the
sample size costs power, not validity.

## 7. The environment is easier than full Freebase

**Closed, for documentation purposes.**

**Book §9.9.3** *Threats to Validity*, **p. 122** already said it about as
strongly as it can be said: the environment is the union of per-question
subgraphs the RoG distribution pre-extracted *so as to contain their own
answer*; reachability is certified at 97.3% / 99.7%; "accuracies measured
on this environment are therefore *not* comparable to evaluations over
full Freebase"; only the **relative** ordering is sound, and every claim
in the findings section is relative for that reason.

It is also stated in **book §1.7, p. 7** and, for the paper, in **§4.2,
p. 17** ("friendlier than full Freebase") and **§8.3, p. 41** ("a more
forgiving substrate").

The gap was placement — the warning lived thirty pages after the numbers
it qualifies. **The caption of Table 8.2 (book p. 90) now carries it and
points to §9.9.3**, so a reader who reads only the main results table
gets the caveat with the numbers.

## 8. Semantic groundedness is weakly validated

**Disclosed, including the unflattering half; not re-run.**

κ = 0.6995 against a pre-registered 0.70 is reported as a **miss**, with
the arithmetic shown, in **book §7.6.3** *Agreement Between Judge and
Human Annotator*, **p. 83**. It is repeated in **§8.6.2** *Tier 2: A
Narrow Band and an Underpowered Comparison*, **p. 97**; in **§9.9.3,
p. 124** ("The judge fell short of its pre-registered bar"); in **§10.2,
p. 128**; in the future-work item **§10.3.4** *Semantic-Level
Verification*, **p. 130**; and in **Appendix D.1** *Judge Instructions*,
**p. 158**. In the paper it is **§4.3** *Metrics and Protocol*, **p. 20**
and **§8.3** *What Bounds the Measurements*, **p. 42**.

The thesis also names and rejects the tempting alternative — tightening
the judge prompt and re-judging a fresh sample until the bar was met —
and says why.

The model-family point has its own subsection rather than being buried:
**book §7.6.1** *Independence of the Judge from the Answering System*,
**p. 82** states the judge "runs on the same backbone as the systems it
judges, which is a limitation stated in §9.9.3 rather than a claim of
independence from the model family", and it repeats in threats at
**p. 124**.

Tier 2 is treated as corroborating rather than decisive and no conclusion
rests on it alone — the headline groundedness result is Tier 1,
structural (**§8.6.1, p. 96**), and needs no judge at all. Unchanged this
round; a different judge family is a new experiment.

---

## Lookup table — every disclosure site, in page order

Use this when a question lands and you need the page, not the argument.

| # | Doc | Section | Page | What is there |
|---|---|---|---:|---|
| 3 | Book | Abstract | xvi | Names verification a null (new) |
| 1 | Book | §1.6.1 AGR and Its Layer | 6 | Bounding sentence (new) |
| 7 | Book | §1.7 Scope | 7 | Not comparable to Freebase |
| 3 | Book | §1.7 "How to read the title" | 8 | Three title terms scoped |
| 1 | Book | §6.3.1 Structural Check | 56 | Routes relation-blind; counts |
| 2 | Book | §6.6 Output Contract | 62 | Both bounds, one page |
| 1 | Book | §6.8 Failure Modes | 66 | Principal risk; the interval |
| 6 | Book | §7.1.1 Pre-Registration | 69 | Sample size fixed in advance |
| 6 | Book | §7.2.2 Stratified Sampling | 71 | The 400 per dataset |
| 5 | Book | §7.3.1 Trajectory Stability | 73 | 8 of 12 probes, ≈67% |
| 5 | Book | §7.3.2 Response Caching | 74 | Why a re-run measures nothing |
| 4 | Book | §7.4.4 Think-on-Graph | 78 | 40/20 vs 300/200; binding |
| 8 | Book | §7.6.1 Judge Independence | 82 | Judge shares the family |
| 8 | Book | §7.6.3 Judge vs Annotator | 83 | κ = 0.6995, arithmetic shown |
| 7 | Book | Table 8.2 caption | 90 | Caveat beside the numbers (new) |
| 4 | Book | §8.4 Where the Margin Comes From | 92 | Table 8.4, clipped split |
| 8 | Book | §8.6.1 Tier 1 | 96 | The headline, judge-free |
| 8 | Book | §8.6.2 Tier 2 | 97 | Narrow band, underpowered |
| 1 | Book | §9.5.4 A Rate for One Polarity | 117 | The interval, in ch. 9 |
| 7 | Book | §9.9.3 Threats | 122 | Ceilings; "not comparable" |
| 4, 5 | Book | §9.9.3 Threats | 123 | Widths; ≈67% as unquantified |
| 8 | Book | §9.9.3 Threats | 124 | Judge missed bar; same family |
| 2, 3 | Book | §10.2 Limitations 1–2 | 127 | Evidence not persisted; power |
| 4, 5, 8 | Book | §10.2 Limitations 4–5 | 128 | Single-everything; widths |
| 8 | Book | §10.3.4 Semantic Verification | 130 | κ as future work |
| 8 | Book | Appendix D.1 | 158 | The judge prompt, verbatim |
| 3 | Paper | Abstract | 2 | "including claim verification" |
| 1, 3 | Paper | §1 Introduction | 4 | Bounding sentence; not a gain |
| 4, 7 | Paper | §4.2 Benchmarks, Baselines | 17 | Widths; "friendlier" |
| 8 | Paper | §4.3 Metrics and Protocol | 20 | κ misses the 0.70 bar |
| 4 | Paper | §5.3 Accuracy by Hop Depth | 25 | Binding rates; Table 3 |
| 1 | Paper | §8.1 Bounds the Contribution | 39 | The interval |
| 4, 5 | Paper | §8.2 Bounds the Comparisons | 40 | Widths; stability |
| 7, 8 | Paper | §8.3 Bounds the Measurements | 41 | Substrate; κ (p. 42) |
| 1 | Deck | Slide 14 *structural* means | — | Adjacency, either way (new) |
| 4 | Deck | Slide 19 What is *not* held equal | — | 40/20 vs 300/200 |
| 2, 4 | Deck | Slide 30 Contributions | — | Evidence; candidate set |
| 1, 2 | Script | §14; anticipated Qs | — | Verbatim answer; "one triple" |

## Six citations in the first version of this note were wrong

Corrected above. Listed because you may have quoted them already.

| Said | Actually |
|---|---|
| §1.5 "How to read the title" | **§1.7**, p. 8 — §1.5 is *Research Qs* |
| §1.4 for the bounding sentence | **§1.6.1**, p. 6 — §1.4 is *Problem* |
| Paper "§7 and §8" for κ | **§4.3** (p. 20) and **§8.3** (p. 42) |
| "§sec:backbone" — a raw label | **§7.3.1**, p. 73 and **§7.3.2**, p. 74 |
| Deck "frame 6 / slide 7" (issue 1) | **Slide 14 / transcript §14** |
| Deck "frame 20" (issue 4) | **Slide 19**, plus the bullet on slide 30 |

`§9.5.4` was **right** and has been kept — two of my own checks
disagreed with it before a third confirmed it, so do not let anyone talk
you out of that one.

## Short version for the two days

Four of the eight (1, 2, 4, 8) are limitations the thesis already
documented well and that only an experiment could actually remove. Those
are argued, not fixed, and the arguments are now in the deck and
transcript rather than only in the book. Two (3, 7) had genuine
documentation gaps and both are closed. Two (5, 6) are scope statements
to be defended verbally, and for 5 the cache argument is the strongest
thing available.

The one asymmetry worth knowing before walking in: on issue 1 the deck
previously stated only the *relevance* limit ("a claim can be true and
still be the wrong answer") and never the relation limit. If the
committee had asked, the honest answer wasn't on any slide. It is now —
slide 14, and the transcript speaks it.

## What was deferred, and what each would cost

These are the four experiment-dependent items, held back because the
pre-defense is on 29 August 2026 and the frozen results must not move
before it.

| | Item | Cost / obstacle |
|---|---|---|
| **C1** | Persist triples, re-run | Closes 2. Splits code from results. |
| **C2** | ToG at 300/200 | Closes 4. Real spend; the cache misses. |
| **C3** | Repeated runs | Closes 5. Same config = 100% cache hits. |
| **C4** | Full test splits | Closes 6. ~$45–55 plus hours of runtime. |
