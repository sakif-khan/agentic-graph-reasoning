# Pre-defense transcript

Rehearsal script for **`pre-defense-0421052099.pdf`** — 22 pages: a title,
twenty body slides, a closing slide.

The four backup slides are a **separate file**,
`pre-defense-0421052099-backup.pdf`. You do not present them. Open it alongside
the main deck and jump to a slide when a question calls for one; the table near
the end of this file maps each to its question.

**Budget: 22 min 30 s of speaking against a 25-minute limit.** The 2.5-minute
margin is deliberate. Nobody has ever finished a defense talk faster than they
rehearsed it.

Times below are *cumulative at the end of that slide*. If you are more than
40 seconds past a marker, use the recovery notes at the bottom.

| # | Slide | Slide time | Cumulative |
| --- | --- | ---: | ---: |
| 1 | Title | 0:15 | 0:15 |
| 2 | The problem | 1:00 | 1:15 |
| 3 | Where existing approaches stop | 1:00 | 2:15 |
| 4 | Research questions | 0:45 | 3:00 |
| 5 | AGR: an explicit state machine | 1:20 | 4:20 |
| 6 | Constrained tools | 0:50 | 5:10 |
| 7 | The Structural Verification Layer | 1:20 | 6:30 |
| 8 | One claim, three routes | 0:55 | 7:25 |
| 9 | Environment and question sets | 0:55 | 8:20 |
| 10 | Making the comparison fair | 1:00 | 9:20 |
| 11 | **Main results** | 1:30 | 10:50 |
| 12 | Accuracy against cost | 1:05 | 11:55 |
| 13 | **RQ1: hop count** | 1:15 | 13:10 |
| 14 | The caveat I want to raise myself | 1:10 | 14:20 |
| 15 | RQ2: groundedness | 1:10 | 15:30 |
| 16 | RQ2: what verification contributes | 1:05 | 16:35 |
| 17 | **RQ3: ablation** | 1:20 | 17:55 |
| 18 | The result I did not expect | 1:10 | 19:05 |
| 19 | The echo attractor | 1:15 | 20:20 |
| 20 | The benchmark was wrong 57 times | 0:50 | 21:10 |
| 21 | Contributions and limitations | 1:05 | 22:15 |
| 22 | Thank you | 0:15 | 22:30 |

The four **bold** slides are the ones the committee will actually interrogate.
If you are running long, take time from 3, 6, and 8 — never from 11, 13, 17.

---

## 1 — Title *(0:15)*

> Good morning. I'm Sakif Khan. This is my pre-defense on Agentic Graph
> Reasoning — knowledge graph navigation with verification before the answer is
> emitted. My supervisor is Dr. Sadia Sharmin.

*Don't read the title aloud. It's on the screen.*

---

## 2 — The problem *(1:00)*

> Language models answer factual questions fluently. The difficulty is that they
> answer just as fluently when they do not hold the fact.
>
> That isn't a rhetorical claim — it's measured here. In my own no-retrieval
> control on WebQSP, the model asserted 661 entities. 179 of them do not exist
> anywhere in the knowledge graph. That's 27.1 percent, and every one was stated
> without a hedge.
>
> The reason this is hard to defend against is that fluency and factuality come
> out of the same mechanism. The output carries no signal about which one you
> just got.

**Beat after "27.1 percent."** It is the number that sets up the whole talk.

---

## 3 — Where existing approaches stop *(1:00)*

> Four families of approach, and each stops somewhere specific.
>
> Parametric answering uses no external evidence at all. Vector RAG retrieves
> once and then reasons — so retrieval happens *before* reasoning begins, and a
> multi-hop question has to be answered from whatever that single query returned.
> Static GraphRAG fixes a neighbourhood radius before the question is even
> understood. Agentic navigation does interleave retrieval and reasoning, which
> is the right move.
>
> But all four share one gap. Whatever the final generation call produces is what
> gets emitted. Nothing checks what the answer *asserts* before it is delivered.

*Walk the table left to right with the pointer. Don't read the cells verbatim.*

---

## 4 — Research questions *(0:45)*

> Three questions.
>
> RQ1: does agentic navigation actually improve multi-hop accuracy — and does the
> advantage grow with the number of hops?
>
> RQ2: given a system that already navigates the graph, what does a claim-level
> check against the traversed triples contribute?
>
> RQ3: which components earn their cost, in accuracy and in tokens?
>
> One framing note. RQ2 asks what verification *contributes*, not whether it
> reduces hallucination. That's deliberate. The answer has several parts, and a
> yes-or-no question would have hidden most of them.

---

## 5 — AGR: an explicit state machine *(1:20)*

> AGR is an explicit state machine — not a prompt loop. Six nodes.
>
> The planner decomposes the question into ordered sub-objectives. The explorer
> scores candidate edges and expands the frontier. The evaluator decides whether
> the current sub-objective has been met. The backtracker undoes a bad expansion
> and bans the edge that caused it, so the agent can't re-take the same wrong
> turn. The verifier is the contribution and I'll come back to it. The answerer
> emits only what survived.
>
> There are exactly two cycles — explorer-to-evaluator, and verifier back to
> explorer. Both are bounded by explicit budgets rather than by model behaviour.
> That gives a termination guarantee that doesn't depend on the model
> cooperating: every cycle passes through a router that checks a monotone
> counter.

**If asked about budgets, go to Backup 1.**

---

## 6 — Constrained tools *(0:50)*

> The agent never writes a graph query. It gets four operations with fixed
> signatures and hard caps — relations, neighbours, an adjacency check, and
> entity linking.
>
> This matters for more than safety. Because every operation is deterministic and
> logged with its arguments and result, the traversal is a record. And that record
> is what the verification layer checks against. Without deterministic tools there
> would be nothing to verify *against*.

---

## 7 — The Structural Verification Layer *(1:20)*

> This is the contribution.
>
> Before anything is emitted, the draft answer is split into atomic claims. Each
> claim is checked against the triples the agent actually traversed. Claims that
> are supported keep their supporting triples and are returned with the answer.
> Claims that can't be grounded either trigger targeted re-exploration, or are
> dropped.
>
> The consequence is that the system hedges rather than asserts, and every answer
> comes back with its evidence attached.
>
> Two things I want to be precise about. First, why *structural* — the check is
> against the graph the agent walked, not against the model's own opinion of its
> own output. A model grading itself is not an independent check. Second, the
> honest limit: a claim can be perfectly true and still be the wrong answer.
> Structural grounding cannot catch that. I'll show you exactly that failure in a
> few minutes.

**The last sentence is a promise. Slide 19 pays it off.**

---

## 8 — One claim, three routes *(0:55)*

> This is the path a single claim takes. Three routes to being called supported.
>
> First, are both endpoint names things we saw during traversal. Second, are they
> adjacent in the traversal record. Third — and only if the first two fail — an
> entailment check.
>
> The point of the ordering is cost. Only the third route spends a model call.
> The first two are pure lookups against a record we already have.

---

## 9 — The environment and the question sets *(0:55)*

> The environment is a Freebase-derived graph: 2.6 million entities, 8.3 million
> triples, seven thousand distinct relations. It imports in 36 seconds, which
> matters only because it means the whole thing is reproducible on one machine.
>
> Questions: 400 each from WebQSP and ComplexWebQuestions. The important column
> is reachability — for every question I verified whether the gold answer is
> actually reachable in this graph. 97 percent on WebQSP, 99.2 on CWQ.
>
> That number is the *ceiling* on every accuracy figure I'm about to show. It
> means when a system misses, the miss belongs to the system and not to the
> environment.

---

## 10 — Making the comparison fair *(1:00)*

> Five systems: a parametric control, vector RAG, static GraphRAG,
> Think-on-Graph as the agentic comparison, and AGR.
>
> All five run on one frozen backbone, at temperature zero, under the same
> 25-call budget, on the same questions, against the same graph.
>
> That's what lets me attribute differences to architecture rather than to model
> capacity or to somebody getting a bigger retrieval budget.
>
> The parametric control deserves a word. These benchmarks predate current
> models and may be partly memorised. Without a no-retrieval control I couldn't
> separate what retrieval contributes from what the model already knew.

---

## 11 — Main results *(1:30)* ★

> Here is the comparison.
>
> AGR reaches 0.755 Hits@1 and 0.642 F1 on WebQSP, and 0.522 and 0.469 on
> ComplexWebQuestions. That's ahead of every baseline on both datasets.
>
> Two things I'd draw your attention to beyond the top line.
>
> First, look at vector RAG and GraphRAG on ComplexWebQuestions — 0.203 and
> 0.205, *below* the no-retrieval control at 0.307. On genuinely multi-hop
> questions, single-shot retrieval is worse than not retrieving at all. It fills
> the context with plausible but wrong material.
>
> Second, the cost columns. AGR spends 4,511 tokens and 6.2 calls against
> Think-on-Graph's 3,615 and 12.8. More tokens, but half the calls. I'll come
> back to why calls are the number that matters.

**Slow down here. This is the slide they read while you talk.**

---

## 12 — Accuracy against cost *(1:05)*

> Plotted, the frontier depends on which cost you charge, and the two costs I
> record disagree.
>
> On tokens — the axis here — Think-on-Graph is *not* dominated. It buys lower
> accuracy at a genuinely lower token price, and any honest reading has to say
> so. The interior point on WebQSP is static GraphRAG, which the parametric
> control beats on both axes at once.
>
> On calls, which is what the budget actually meters, Think-on-Graph is dominated
> on both datasets.
>
> I'm showing both because stating it on one axis alone would overclaim.

---

## 13 — RQ1: accuracy against hop count *(1:15)* ★

> This is the direct answer to RQ1, and it's a shape rather than a difference of
> means.
>
> Look at ComplexWebQuestions on the right. AGR goes 0.46, 0.55, 0.57 as
> questions get harder — one hop, two hops, three or more. It is the only system
> on that dataset that ends above where it started.
>
> Three of the other four decay monotonically. Think-on-Graph is the exception to
> the monotonicity but not to the direction — it falls and partially recovers,
> still 0.08 below its own one-hop score.
>
> I want to be careful about the left panel. On WebQSP the three-or-more stratum
> has n equals 4. I don't draw a conclusion from four questions, and the thesis
> doesn't either.

**Volunteering the n=4 weakness pre-empts the obvious attack.**

---

## 14 — The caveat I want to raise myself *(1:10)*

> I want to raise this before you do.
>
> If you split the questions by whether Think-on-Graph finished inside the shared
> 25-call cap, then on the questions it *finishes*, Think-on-Graph is ahead of
> AGR. 0.852 against 0.788 on WebQSP. 0.629 against 0.607 on CWQ.
>
> The entire aggregate margin comes from the questions it cannot finish — where
> it drops to 0.197 and 0.188, because it is cut off mid-search. It gets clipped
> on 29 percent of WebQSP and 44 percent of CWQ.
>
> So the honest claim is not that AGR reasons better per step. It's that AGR
> completes its reasoning inside a fixed budget, and Think-on-Graph frequently
> does not. That's an efficiency claim, and it's the one I'm making.

**Deliver this as a strength. It is the most defensible slide in the deck.**

---

## 15 — RQ2: does anything ungrounded get asserted? *(1:10)*

> RQ2. Does anything ungrounded get asserted?
>
> Pooling both datasets: AGR asserts 1,709 entities and zero of them are absent
> from the graph. The parametric control asserts 1,001 and 22.1 percent of them
> don't exist.
>
> That looks like a headline result for the verification layer. It isn't — and
> this is the finding I think matters most.
>
> Think-on-Graph also reaches 0.0 percent. It has no verification layer at all.
>
> So zero ungrounded assertion is a property of *navigating a graph* — if you can
> only name entities you actually visited, you can't invent one. It is not a
> property of my verification layer, and I don't claim it as one.

---

## 16 — RQ2: so what does verification actually contribute? *(1:05)*

> Which leaves the real question.
>
> What it does not do: removing it changes accuracy by an amount I cannot detect.
> p equals 1.0 on both datasets. It does not earn its place on Hits@1 or F1, and
> I report that as a negative result.
>
> What it does do: it converts silent error into an explicit hedge — AGR hedges
> on 8.2 percent of WebQSP where the parametric control is simply wrong on more
> than that. It attaches supporting triples to every claim it does assert. And it
> gives an auditable output contract — you can check the system's work.
>
> The layer's case rests on auditability, not accuracy. The thesis says that
> plainly rather than claiming a benefit the measurement doesn't support.

---

## 17 — RQ3: what each component earns *(1:20)* ★

> RQ3, and this is a four-condition ablation with paired McNemar tests against
> the full system on stratified halves.
>
> Read the p-value columns. Backtracking: 0.727 and 1.0. Verification: 1.0 and
> 1.0. Learned scoring versus embedding-only: 0.664 and 0.481. For three of the
> four components I detect no accuracy effect at this sample size.
>
> I want to be careful with that phrasing — that is "no detectable effect at
> n equals 200," not "confirmed no effect." These are underpowered for small
> differences and I say so.
>
> One row is different. Removing the planner, on WebQSP, p equals 0.006.

**Pause on the 0.006. Then turn the slide.**

---

## 18 — The result I did not expect *(1:10)*

> Removing the planner *improves* WebQSP. Plus 0.083 F1, at p equals 0.006, while
> cutting tokens 31 percent and calls from 6.2 to 4.0. Better, cheaper, and
> faster, by deleting a component I built.
>
> On ComplexWebQuestions it trends the other way — minus 0.047 F1 at p equals
> 0.088. Not significant, but the opposite sign, and that's the useful part.
>
> The explanation is that WebQSP is predominantly one hop. Decomposing a one-hop
> question invents a second sub-objective that sends the frontier away from the
> answer it already had.
>
> So the conclusion is that decomposition should be gated on question structure
> rather than applied unconditionally. That's a design conclusion the measurement
> forced on me, not one it confirmed.

**Own this. A negative result you can explain is stronger than a positive one
you can't.**

---

## 19 — Every failure, read: the echo attractor *(1:15)*

> I read all 259 remaining failures and labelled them against a ten-category
> scheme. Here are the top categories pooled.
>
> The one I want to name is sixth on that list, with 13 cases, and it is the one
> that matters conceptually.
>
> The characteristic error of a graph navigator is not invention. It's what I
> call the **echo attractor** — the system returns a real, grounded entity that
> sits one hop from the correct answer. Ask for a director and get the film. Ask
> for a capital and get the country.
>
> Here's why it matters, and this is the promise I made on slide seven: any
> grounding check *passes* it. The entity is real, it was traversed, the triple
> exists. It is true and it is wrong. Verification cannot catch this by
> construction.
>
> It appears across systems, so it's a property of the task rather than of AGR.
> Naming it is what lets future work target it.

**The full 12-category histogram is Backup 4 if anyone wants it.**

---

## 20 — The benchmark was wrong 57 times *(0:50)*

> One more thing came out of reading every failure.
>
> 57 distinct questions where the *benchmark* was wrong, not the system —
> 41 caught before the census and 17 inside it, with one question in both, so 57
> distinct.
>
> Published defect rates for these two standard benchmarks are rare and usually
> anecdotal. This is a counted rate, with a documented adjudication procedure and
> per-question provenance, so anyone can check it.
>
> That's a contribution that outlives this particular system.

---

## 21 — Contributions, and what I would not claim *(1:05)*

> To summarise. Six contributions: the framework, the verification layer and its
> output contract, the controlled five-system comparison, the hop-count result
> for RQ1, the echo attractor as a named failure mode, and the benchmark-defect
> rate.
>
> And the limitations, which I'd rather state than be asked.
>
> Verification earns no detectable accuracy gain. Zero ungrounded assertion comes
> from navigation, not from my layer. Think-on-Graph leads on the questions it
> finishes. And everything here runs on one backbone — these are architectural
> results, not universal ones.

---

## 22 — Thank you *(0:15)*

> Thank you. I'm happy to take questions.

---

## Backup slides — `pre-defense-0421052099-backup.pdf`

A separate document. Open it before you start, minimised or on a second screen.
Page numbers below are that file's own.

| Page | Contents | Use when asked |
| --- | --- | --- |
| 2 | Budget configuration and enforcement sites | "How do you guarantee termination?" |
| 3 | Which budgets actually bind | "Is the 25-call cap fair to Think-on-Graph?" |
| 4 | Full 12-category failure histogram | "What were the other failure modes?" |
| 5 | Hedging rates, all five systems | "Doesn't it just refuse more often?" |

**Page 3 is the important one.** It shows AGR never reaches the call cap —
0.0 percent on both datasets — which is precisely what makes the comparison
against a clipped Think-on-Graph legitimate rather than an artefact of a cap
chosen to suit AGR.

---

## Anticipated questions

**"Isn't the 25-call cap arbitrary, and doesn't it favour AGR?"**
It's the cap Think-on-Graph's own paper operates under. And AGR never reaches it
— zero percent on both datasets (B2). If I raised the cap, AGR's numbers would
not move; Think-on-Graph's would. I say that in the thesis rather than leaving it
for someone to find.

**"If verification doesn't improve accuracy, why keep it?"**
Because accuracy was never the only claim. It converts silent error into an
explicit hedge and attaches evidence to every assertion. If you want a system
whose answers can be *checked*, that is the deliverable. I report the null on
accuracy rather than hiding it.

**"Your planner result says your own design is wrong."**
It says the planner is wrong *for one-hop questions*, and WebQSP is mostly
one-hop. On ComplexWebQuestions the effect reverses in sign. The conclusion is
that decomposition should be gated on question structure — which is a finding,
and one I'd have missed without the ablation.

**"n=4 in the three-hop WebQSP stratum is meaningless."**
Agreed, and I don't draw a conclusion from it. The hop-count claim rests on
ComplexWebQuestions, where the strata are 137, 211, and 49.

**"How do you know the gold answers are reachable?"**
Verified per question against the graph before scoring — 97.0 percent on WebQSP,
99.2 on CWQ. It's the ceiling on every Hits@1 I report, and it's stated as such.

**"Is this reproducible?"**
Every number in the thesis is generated from frozen run records by a script;
none is transcribed. Same for the three data figures in this deck — they are
pulled directly from the thesis's own generated sources.

---

## Recovery notes

If you hit **11:55 (slide 12) more than 40 seconds late**, compress as follows.

- Slide 16 — cut to: *"It doesn't improve accuracy. It converts silent error
  into an explicit hedge and attaches evidence. The case is auditability."*
  Saves ~35 s.
- Slide 20 — cut to: *"Reading every failure also found 57 questions where the
  benchmark was wrong, with documented provenance."* Saves ~25 s.
- Slide 3 — name only the fourth row and the gap. Saves ~30 s.

Never compress 11, 13, 14, 17, or 18. Slide 14 in particular: skipping it means
a committee member raises the clipping issue instead of you, and it lands very
differently that way.

## Delivery

- **Say the number, then what it means.** Not the reverse. "Twenty-seven percent
  of asserted entities don't exist — the model is confidently inventing."
- **Three slides are negative results** (16, 17, 18). Deliver them at normal
  pace, not apologetically. A student who reports a clean null is more credible
  than one who reports only wins.
- The word is **hedge**, not "refuse." A hedge is a calibrated non-assertion.
- If you lose your place, the takeaway bar at the bottom of the data slides is
  your prompt — read it aloud and continue.
