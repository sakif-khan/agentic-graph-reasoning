# Defense transcript

Rehearsal script for **`thesis_defense_0421052099.pdf`** — 38 pages: a title,
thirty-six body slides, a closing slide.

You present slides 1 to 31. The seven after the closing slide are **backup**:
you reach them by paging past "Thank you" when a question calls for one, not
by switching to a second file. They are timed 0:00 below because none of them
is spoken; the table near the end of this file maps each to its question.

**Budget: 22 min 38 s of speaking against a 25-minute
limit.** Every row below is set to what its own words take at 93 wpm, rounded
up to the second, so the margin under the limit is the only slack there is.

This round (October 2026) rebuilt the talk against the book. The six
background slides became three, the results now start 11:35 in rather than
16:04, and three things the deck never said are said: the answers to the three
questions (slide 28), what comes next (slide 30), and the six contributions
as a preview (slide 8). The talk had run 52 s over; it now fits with the
margin below.

**A margin is not a cushion.** If you need more time than the margin, it has
to come out of what is said: about 60 words buys 40 seconds, and the recovery
notes below name the slides that can give it up.

Times below are *cumulative at the end of that slide*. If you are more than
40 seconds past a marker, use the recovery notes at the bottom.

| # | Slide | Slide time | Cumulative |
| --- | --- | ---: | ---: |
| 1 | Title | 0:21 | 0:21 |
| 2 | The problem | 0:40 | 1:01 |
| 3 | Where it comes from, and what we can change | 0:35 | 1:36 |
| 4 | Knowledge graphs, and why multi-hop is hard | 0:49 | 2:25 |
| 5 | Where existing approaches stop | 0:41 | 3:06 |
| 6 | What guided beam search is | 0:46 | 3:52 |
| 7 | What everyone else does | 0:43 | 4:35 |
| 8 | Research questions | 0:34 | 5:09 |
| 9 | AGR: An explicit state machine | 0:53 | 6:02 |
| 10 | Constrained tools, not free-form queries | 0:33 | 6:35 |
| 11 | The Structural Verification Layer | 0:37 | 7:12 |
| 12 | What *structural* means, and what it does not | 0:58 | 8:10 |
| 13 | One claim, three routes | 0:45 | 8:55 |
| 14 | One question, end to end | 0:44 | 9:39 |
| 15 | The environment and the question sets | 0:48 | 10:27 |
| 16 | Making the comparison fair | 1:08 | 11:35 |
| 17 | **Main results** | 1:21 | 12:56 |
| 18 | **RQ1: Does agentic navigation improve multi-hop factual accuracy?** | 0:56 | 13:52 |
| 19 | The caveat I want to raise myself | 1:01 | 14:53 |
| 20 | RQ2: What does pre-generation verification contribute beyond graph navigation? | 0:50 | 15:43 |
| 21 | RQ2: What verification does *not* do | 0:50 | 16:33 |
| 22 | RQ2: So what does it do? | 0:41 | 17:14 |
| 23 | Does it just refuse more often? | 0:31 | 17:45 |
| 24 | **RQ3: Which components contribute what, at what token cost?** | 0:24 | 18:09 |
| 25 | **RQ3: One effect, and its sign is backwards** | 0:57 | 19:06 |
| 26 | Every failure, read and labelled | 0:20 | 19:26 |
| 27 | The echo attractor | 1:01 | 20:27 |
| 28 | The three answers | 0:39 | 21:06 |
| 29 | Contributions | 0:58 | 22:04 |
| 30 | What comes next | 0:29 | 22:33 |
| 31 | Thank you | 0:05 | 22:38 |
| 32 | *Backup:* budget configuration | 0:00 | 22:38 |
| 33 | *Backup:* which budgets actually bind | 0:00 | 22:38 |
| 34 | *Backup:* the full failure census | 0:00 | 22:38 |
| 35 | *Backup:* accuracy against cost | 0:00 | 22:38 |
| 36 | *Backup:* the benchmark was wrong 57 times | 0:00 | 22:38 |
| 37 | *Backup:* AGR against RoG | 0:00 | 22:38 |
| 38 | *Backup:* what changed from the proposal | 0:00 | 22:38 |

The four **bold** slides are the ones the committee will actually
interrogate. If you are running long, take time from 9, 13 and 14 —
never from 17, 18, 19, 24 or 25. That is the same list the recovery notes
protect, and 19 is on it for a different reason: skipping it hands the
clipping issue to them.

---

## 1 — Title *(0:21)*

> Good afternoon. I'm Sakif Khan. This is my thesis defense on Agentic Graph
> Reasoning, which is knowledge graph navigation with verification before the
> answer is emitted. My supervisor is Dr. Sadia Sharmin.

*Don't read the title aloud. It's on the screen. It is the title registered
at the proposal stage, and three of its terms are broader than the claims.
Slide 29 names them, so do not defend them here.*

---

## 2 — The problem *(0:40)*

> Language models answer factual questions just as fluently when they do not
> hold the fact. A hallucination is output with no source the model can
> point to.
>
> Two kinds, separated by what it takes to catch them. A factually wrong
> answer needs the true answer already. An unsupported one needs only what
> was retrieved, and we have that. I claim the second.

*The last sentence is a scope limit, not modesty. Say it at normal pace.*

---

## 3 — Where it comes from, and what we can change *(0:35)*

> It is not a bug that escaped testing. It comes from how these models are
> built, so the response has to be architectural.
>
> Three origins. The training data, the model itself, and the prompt. Only
> the prompt is ours to change. So control what goes in, and check what
> comes out against it.

*Name the three, don't read them. The slide carries the wording.*

---

## 4 — Knowledge graphs, and why multi-hop is hard *(0:49)*

> A knowledge graph stores facts as triples, so every fact has an address
> and a claim can be checked by looking for an edge. A question that chains
> two facts is multi-hop, and a wrong first hop is never revisited.
>
> One complication. Freebase stores a fact with more than two participants
> as an unnamed node, and nearly two thirds of this graph's nodes are that
> kind. So nothing here is called "plays". Hold onto that.

*The last line is a setup. The worked example on slide 14 pays it off, and so
does the verification layer's limit on slide 12.*

---

## 5 — Where existing approaches stop *(0:41)*

> Four families, and each stops somewhere specific. The first three fix their
> evidence before reasoning begins. Agentic navigation interleaves the two,
> which is the right move, and it already names only what it traversed.
>
> So its problem is precision. A real, traversed entity can still be the
> wrong answer, and none of the four checks what the answer asserts before it
> goes out.

*This is the book's turn from fabrication to precision. It is what makes
slide 20's zero for both navigating systems a result rather than a
surprise.*

---

## 6 — What guided beam search is *(0:46)*

> You hold a set of current nodes, the frontier. List every edge out of it,
> score each, keep the best few, expand those, and repeat to a depth cap.
> The number you keep is the beam width.
>
> Guided means the score is a judgement, here a model call. So the width is
> the cost, and it multiplies with every hop. And whatever falls outside the
> beam is gone for good.

*The multiplication is what slide 19 cashes: it is why Think-on-Graph runs out
of calls and AGR does not.*

---

## 7 — What everyone else does *(0:43)*

> Four prior systems, and the column that matters is the last one. They
> differ in how they explore, some decompose, and Plan-on-Graph backtracks.
> None checks its answer's claims against what it retrieved, before
> answering. RoG comes closest, since its answers are grounded by
> construction, but nothing examines them. Post-hoc checkers such as
> Chain-of-Verification check after generation.
>
> Their published accuracies are higher than mine and not comparable.

*Plan-on-Graph in full, always. Paths-over-Graph is also cited as "PoG" and
reports higher numbers. The note on the slide gives the three reasons the
published figures are not comparable; read them only if asked.*

---

## 8 — Research questions *(0:34)*

> Three questions. RQ1: does agentic navigation improve multi-hop accuracy,
> and does the advantage grow with hop count? RQ2: what does pre-generation
> verification contribute beyond graph navigation? RQ3: which components
> contribute what, at what token cost?
>
> On the right are the six contributions the thesis claims. I return to them
> at the end.

*RQ2 asks what verification contributes, not whether it reduces
hallucination. The slide says so; say it only if asked why.*

---

## 9 — AGR: An explicit state machine *(0:53)*

> AGR is an explicit state machine, not a prompt loop. Six nodes. The planner
> writes sub-objectives. The explorer scores candidate edges and keeps the
> best three per anchor. The evaluator decides whether an objective is met.
> The backtracker returns to the best-scoring earlier frontier and bans the
> edges that failed. The verifier checks the draft's claims, and the answerer
> emits what survived.
>
> Three cycles, the three arrows back to the explorer, and all three are
> bounded by budgets checked in code.

**Do not say "exactly two cycles."** The diagram has three arrows returning to
the Explorer and the audience is looking at it while you speak. Naming them
after the edge labels — continue, backtrack, retry — means counting the
arrows confirms the sentence.

**Do not call the backtracker an undo.** It restores the highest-scoring
earlier snapshot, not the most recent one, and the thesis says outright that
popping the most recent one "would make backtracking a simple undo". If
pressed, the implementation bans the latest pass while restoring an older
frontier, and the thesis records that misalignment rather than hiding it.

**If asked about budgets, go to backup slide 32.**

---

## 10 — Constrained tools, not free-form queries *(0:33)*

> One agent, six nodes, and only three touch the graph. The planner resolves
> entity mentions, the explorer asks for relations and neighbours, and the
> verifier checks adjacency. Four operations, never Cypher. Every call is
> logged, so the traversal is a record, and that record is what the
> verification layer checks against.

*Say "one agent" out loud. The previous slide draws six named boxes, and
"the agent" on its own invites the question of how many there are.*

---

## 11 — The Structural Verification Layer *(0:37)*

> This is the part I set out to contribute. Before anything is emitted, the
> draft is split into atomic claims, each checked against the graph, the
> traversed triples first. What cannot be grounded is re-explored or
> dropped. So where it cannot ground a claim, the system hedges rather than
> asserts. Measured, it buys auditability rather than accuracy.

---

## 12 — What *structural* means, and what it does not *(0:58)*

> Now the bound. The graph decides. The model is consulted only where the
> graph is silent, and it never overrides the graph.
>
> Structural does not mean it can read the relation. The first two routes
> test adjacency, in either direction, so a mother claim survives on a child
> edge. That is the mediator problem as a limitation.
>
> "Its evidence" is narrower too. Only the walked-graph check attaches
> triples, and the log keeps a count, not the triples. And a claim can be
> true and still be the wrong answer.

**The last sentence is a promise. Slide 27 pays it off.**

---

## 13 — One claim, three routes *(0:45)*

> This is the inside of the verifier. One model call drafts the answer and
> splits it into claims. Each claim leaves at the first test that settles
> it, left to right. Traversed adjacency comes first, and it is the only
> route that adds evidence. Then verify connection, on the full graph. Only
> the third route, entailment, spends a model call. With no unsupported
> claim the answer goes out grounded.

*Say the first sentence before anything else. This is the one slide that is a
zoom rather than a new subject. A claim whose endpoints were never traversed
skips both structural routes; point at the lower lane if asked.*

---

## 14 — One question, end to end *(0:44)*

> One real question, from the committed records. "Who plays Dwight in The
> Office." The dataset gives the mention The Office, and the planner resolves
> it and splits the question. The explorer keeps three relations and the
> evaluator resolves Dwight Schrute. Second hop, and it resolves Rainn
> Wilson and answers. The verifier finds two claims, both supported.
>
> Six model calls, depth two, and at most eighteen supporting triples.

**If "at most" is questioned.** The counter counts matches rather than
distinct triples, so the thesis reads it as an upper bound (section on the
output contract), and so does the slide.

**If the relation names are challenged.** They read backwards until you say
the walk is two edges. `tv.tv_program.regular_cast` has 42 direct edges out of
The Office and `get_neighbors` returned 200, because every one of them lands on
an unnamed appearance record the tool expands one edge further
(`kg_tools.py:68`). That expansion reaches the actor *and* the character, which
is how hop 1 resolves Dwight Schrute. Hop 2 is the same shape: 1 direct edge
into Dwight, 12 returned, the actor among them. Both counts are in the
committed tool log.

*If you are behind, cut everything after "both supported."*

---

## 15 — The environment and the question sets *(0:48)*

> The environment is the union of RoG's per-question subgraphs, 2.6 million
> entities and 8.3 million triples. Each subgraph was cut to contain its own
> answer, so this is friendlier than full Freebase.
>
> 400 questions each from WebQSP and ComplexWebQuestions, unmodified. Every
> question's gold answer is certified reachable, 97 percent and 99.2. That
> is the ceiling on every accuracy figure, for entity answers only. Dates,
> quantities and superlatives this graph cannot express at all.

*Both disclosures are the book's: the friendliness is threat 1 in the threats
to validity, and the inexpressible class is defined in the environment
chapter. Say them rather than have them raised.*

---

## 16 — Making the comparison fair *(1:08)*

> Five systems on one frozen backbone, under the same 25-call budget, on the
> same questions and graph. That is what lets me attribute differences to
> architecture rather than to model capacity. Think-on-Graph is my
> reimplementation, and the graph systems all start from the datasets'
> topic entities.
>
> Two things are not equal, and I would rather say them than have them
> found. Think-on-Graph prunes from a narrower candidate set. That cuts
> against it, since a thinner set is cheaper, so it cannot explain the
> clipping, but it makes its score a lower bound. And AGR's drafting prompt
> carries grounding rules the baselines' plain prompt does not.

**Say the width line, don't skip it.** The Think-on-Graph baseline section
names the widths as the one place a reader should look first for a confound,
and the threats to validity rank it limitation 2. The numbers are on the
slide and in the answer below — you do not have to recite 40/20/300/200 here.

---

## 17 — Main results *(1:21)* ★

> Here is the comparison.
>
> AGR reaches 0.755 Hits@1 and 0.642 F1 on WebQSP, and 0.522 and 0.469 on
> ComplexWebQuestions, ahead of every baseline on both. All eight paired
> tests reject.
>
> First, vector RAG on ComplexWebQuestions: 0.203, *below* the no-retrieval
> control at 0.307. One verbalised triple cannot contain a chain, so
> single-shot retrieval is worse there than not retrieving at all. GraphRAG
> sits beside it at 0.205, but its one-hop radius confounds the paradigm, so
> the claim rests on vector RAG.
>
> On WebQSP the control even beats GraphRAG on raw hits, by guessing. It is
> right on 51.6 percent of what it asserts, GraphRAG on 76.8.
>
> And cost: about a quarter more tokens than Think-on-Graph, at half the
> calls, and calls are what the budget meters.

**Slow down here. This is the slide they read while you talk.**

**Do not pool the two retrieval baselines.** The table puts 0.203 and 0.205 side
by side and the pooled version of this point is the one that gets walked back:
the CWQ results section calls GraphRAG the weaker evidence of the two and says
the claim rests on vector RAG. If they press on GraphRAG, the answer below has
the strata.

---

## 18 — RQ1: Does agentic navigation improve multi-hop factual accuracy? *(0:56)* ★

> The answer to RQ1 is yes, and the evidence is a shape.
>
> ComplexWebQuestions, on the right. AGR goes 0.46, 0.55, 0.57 as questions
> get harder. It is the only system on that dataset that ends above where it
> started. Three of the other four decay monotonically, and Think-on-Graph
> falls and partially recovers, still 0.08 below its own one-hop score. It
> does beat AGR at one hop, 0.53 against 0.46, where decomposition is not
> needed.
>
> The left panel is dashed because its three-hop stratum is four questions.

**Volunteering the n=4 weakness pre-empts the obvious attack.** The one-hop
loss is the book's own boundary on this answer; say it before it is found.

---

## 19 — The caveat I want to raise myself *(1:01)*

> I want to raise this before you do.
>
> Split the questions by whether Think-on-Graph finished inside the shared
> 25-call cap. On the ones it finishes, it is ahead of AGR, 0.852 against
> 0.788 on WebQSP and 0.629 against 0.607 on CWQ.
>
> The entire margin comes from the questions it cannot finish, 29 percent
> of WebQSP and 44 percent of CWQ. Beam search pays width times depth in
> calls, and AGR's plan does not multiply.
>
> So the claim is not that AGR reasons better per step. It is that AGR
> finishes inside a fixed budget.

**Deliver this as a strength. It is the most defensible slide in the deck.**

---

## 20 — RQ2: What does pre-generation verification contribute beyond graph navigation? *(0:50)*

> RQ2, in its narrowest form. Does anything ungrounded get asserted?
>
> Across both datasets, AGR asserts 1,709 entities and zero are ungrounded.
> The parametric control asserts 1,001 and 22.1 percent are ungrounded.
>
> That looks like a headline for the verification layer. It isn't.
> Think-on-Graph also reaches zero, with no verification layer at all. So
> this is a property of navigating a graph. And a stricter semantic check
> still fails a third to a half of every system's answers.

---

## 21 — RQ2: What verification does *not* do *(0:50)*

> Removing the layer changes accuracy by nothing I can detect, p equals 1.0
> on both datasets. On test it changed two answers, one each way.
>
> Nor does it explain the precision lead. On CWQ, AGR is right on 67.9
> percent of what it asserts, Think-on-Graph on 56.1, and removing the layer
> barely moves AGR's. The lead belongs to the architecture, and perhaps the
> prompt.
>
> And its evidence ends with the run. The log keeps a count.

*The slide's foot answers the objection that this retracts slide 17: that
was AGR against four baselines, this is AGR against itself. Say it if the
room looks puzzled.*

---

## 22 — RQ2: So what does it do? *(0:41)*

> What it does is withhold what it cannot ground. Without it, CWQ hedging
> falls from 23.2 to 20.2 percent. Those six answers were all wrong. On
> WebQSP it withheld one, and that one was right.
>
> Its clearest catch was a draft claiming Marlon Brando was in Joy. The
> verifier rejected it. Not right more often, but right for a reason it can
> show.

*The six and the one are the paired records, not a difference of rates. The
anticipated questions below have the full answer if it is pressed.*

---

## 23 — Does it just refuse more often? *(0:31)*

> The obvious objection, and the answer is no. AGR hedges least of the five
> on WebQSP, where it is also the most accurate. On CWQ it is within half a
> point of Think-on-Graph, and nearly nine points more accurate. A hedge
> scores zero, like a wrong answer.

**Do not overstate CWQ.** 23.0 against Think-on-Graph's 22.5 is half a point
*more*, not less. What holds on both datasets is the pairing: it hedges no
more than the agentic baseline and scores above it.

---

## 24 — RQ3: Which components contribute what, at what token cost? *(0:24)* ★

> RQ3: which components earn their cost. Four ablations, each a paired test
> against the full system on the same halves. Three change nothing I can
> detect: backtracking, the verifier, and the learned half of the scorer.

**"Full system" is the main run restricted to the same half-samples.** That is
why its WebQSP F1 reads 0.659 here and 0.642 on slide 17. The p-values are
uncorrected, as the thesis reports them, and read as descriptive.

**What the p column is, if you are asked.** McNemar throws away every question
both systems get right and every question both get wrong, and reads only the
ones they disagree on. On WebQSP no-planner that is 27 questions: 21 the
ablation got and the full system missed, 6 the other way. Under "no difference"
that split is a coin toss, and 21–6 gives p = 0.006.

**The verifier rows are the ones to understand before you are asked.** p = 1.000
there rests on **one** discordant question on each dataset. That is "the test had
no information", not "there is no effect" — which is exactly why slides 21 and
24 say *detectable* rather than *none*.

---

## 25 — RQ3: One effect, and its sign is backwards *(0:57)* ★

> The one that does is the planner, and the sign is backwards. Removing it
> improves WebQSP by 0.083 F1 at p equals 0.006, and cuts tokens by 31
> percent. On ComplexWebQuestions it trends the other way, and its two-hop
> stratum falls from 0.48 to 0.34.
>
> The mechanism is context-stripping. Asked for the 33rd president who led
> during WW2, the planner split the question, WW2 was never used, and the run
> answered Woodrow Wilson. Undecomposed, it found Truman in three calls. So
> decomposition should be gated on question structure.

**Do not compress this one.** It is the only place a component's cost is priced.

---

## 26 — Every failure, read and labelled *(0:20)*

> Two hundred and fifty-six failures, read and labelled by hand. The largest
> category is relation selection, the agent taking the wrong edge, not
> inventing one. That shape is the finding.

**The table is pooled, and the slide says so.** Wrong and hedge are never
pooled in the thesis — sec:taxonomy: "a pooled percentage would describe
neither" — and pooling also hides the shape flip: `composite_claim` is 1 on
WebQSP against 46 on CWQ. The block on the slide carries both facts, so the
split census is something you offer rather than something you are corrected
with. The last row closes the column to 256; the six smaller categories are
backup slide 34 if anyone wants them.

---

## 27 — The echo attractor *(1:01)*

> The one to name is sixth, with 13 cases: the echo attractor, a real,
> grounded entity one hop from the answer. Asked who plays Lex Luthor on
> Smallville, AGR named the actor who plays his father.
>
> Any grounding check passes it. It is real, it was traversed, the triple
> exists. True, and wrong. That is the promise from slide 12.
>
> Different systems fall into it together, so no evaluation treating them as
> independent can see it. Rescore whenever a majority agrees, and this
> becomes apparent correctness. The contribution is the mechanism, not the
> count.

**Do not say "it appears across systems, so it is a property of the task rather
than of AGR."** That is defensive where the thesis is substantive, and nothing
on the slide blames AGR for it. The claim is about evaluation: sec:echo calls
the attractor "invisible to any evaluation treating systems as independent",
and section 1.6 says the contribution is the mechanism "and what it means for
consensus-based evaluation rather than the frequency". Backup slide 36 is the same finding
seen from the other side.

---

## 28 — The three answers *(0:39)*

> So, the three answers. RQ1: yes, though the margin over Think-on-Graph lies
> in the budget. RQ2: navigation, not verification, removes structural
> hallucination, and the layer buys auditability. RQ3: only the planner
> matters detectably, and its sign depends on the stratum.
>
> Navigation is where the accuracy comes from. Verification is where the
> auditability comes from. And decomposition is sometimes harmful.

*The last three sentences are the book's discussion chapter, closing its
answer to the three questions. Say them slowly.*

---

## 29 — Contributions *(0:58)*

> Six contributions, the six the thesis claims. The one I'd underline is
> stratum-dependent decomposition. The literature treats it as plainly
> beneficial, and it is not. The protocol fixed four decisions in advance,
> and I missed one: the judge reached a kappa of 0.6995 against 0.7.
>
> The limitations. The most serious is that the verifier persists only what
> it rejects, so wrongful acceptance has no rate. Then one environment, one
> backbone, one run, and the narrower candidate set. And the title is
> broader than my claims, as the thesis says.

*The title's three terms, if asked: hallucination mitigation happens, but
navigation does it, not the layer; "autonomous" names a design the thesis
argues against, since the program drives the loop; and "fact verification" is
structural adjacency, not the relation and never relevance. The book's scope
section reads the title the same way.*

---

## 30 — What comes next *(0:29)*

> Next, three cheap repairs the census earned, and three operators the
> failures specify, from decomposition gating to set intersection.
>
> The thesis closes on this. Fact verification against a knowledge graph
> turns out to be the easier half. Relevance verification is the half still
> open.

---

## 31 — Thank you *(0:05)*

> Thank you. I'm happy to take questions.

---


## Backup slides — the tail of the same deck

They are slides 32 to 38 of `thesis_defense_0421052099.pdf`, after the closing
slide. **Everything in this script refers to a backup slide by its number in
that deck**, which is what this table lists — the same numbering the footer
prints, so there is nothing to convert under pressure. Page forward from
"Thank you"; there is no second file to open.

| Slide | Contents | Use when asked |
| --- | --- | --- |
| 32 | Budget configuration and enforcement sites | "How do you guarantee termination?" |
| 33 | Which budgets actually bind | "Is the 25-call cap fair to Think-on-Graph?" |
| 34 | Full 12-category failure histogram | "What were the other failure modes?" |
| 35 | Accuracy against cost, both metrics | "Is it cheaper, or just better?" |
| 36 | The benchmark was wrong 57 times | "How good is the gold?" |
| 37 | AGR against RoG, side by side | "How does this compare to RoG?" |
| 38 | What changed from the proposal | "Your proposal said MCTS. What happened?" |

**Slide 33 is the important one.** It shows AGR never reaches the call cap —
0.0 percent on both datasets — which is precisely what makes the comparison
against a clipped Think-on-Graph legitimate rather than an artefact of a cap
chosen to suit AGR.

---

## Anticipated questions

**"How do you know models actually do this? Where is your evidence?"**
From this work's own no-retrieval baseline, which is the parametric control
in the five-system comparison. On WebQSP it asserted 661 entities and 179 of
them have no basis in the knowledge graph. That is 27.1 percent, every one
stated without a hedge. Slide 20 gives the same measurement over both
datasets pooled: 1,001 asserted, 221 ungrounded, 22.1 percent. The WebQSP
slice runs higher because CWQ questions are longer and the model hedges more
on them; the pooled row is the one I quote, and the one the thesis's abstract
and conclusion use.

**"Isn't the 25-call cap arbitrary, and doesn't it favour AGR?"**
It is AGR's own budget, applied identically to every system. And AGR never
reaches it — zero percent on both datasets (backup slide 33). If I raised the
cap, AGR's numbers would not move; Think-on-Graph's would. I say that in the thesis rather than leaving it
for someone to find.

**"Do the categories look the same on both datasets?"** *(Slide 26 is pooled.)*
No, and that is the more interesting answer. The census is reported split in the
thesis and never pooled, because wrong and hedge describe different failure
semantics and the proportions differ sharply by dataset. The clearest case is
`composite_claim`: 1 on WebQSP against 46 on CWQ. WebQSP questions mostly are
not compound, so the category barely exists there; on ComplexWebQuestions it is
the largest single failure mode. A pooled percentage would describe neither
dataset. The full split is backup slide 34.

**"Doesn't GraphRAG show the same thing?"** *(Slide 17 puts 0.203 and 0.205
side by side. Do not pool them.)*
No, and the thesis says so rather than letting the two numbers be read together.
GraphRAG retrieves a one-logical-hop neighbourhood, so its fall on CWQ confounds
static retrieval with a radius I chose in advance. The evidence that it is the
radius is in the strata: GraphRAG scores 0.44 on WebQSP's two-hop questions,
which are largely mediator paths a one-hop expansion does reach, against 0.16 on
the CWQ two-hop stratum, where the chains are genuine compositions it cannot
reach at all. A retriever failing uniformly on depth would not show that gap.
There is a second bound on it: it takes at most 100 edges per topic entity with
no ordering imposed, and on 72.5 percent of questions at least one topic entity
exceeds that degree, so on those it answers from an arbitrary sample. Vector RAG
carries the paradigm claim, because one verbalised triple cannot contain a chain
at any radius.

**"Why does the no-retrieval control beat GraphRAG on WebQSP?"** *(Slide 17.
Said in passing there; this is the long form.)*
Because it guesses and GraphRAG abstains. The retrieval baselines are told to
answer only from the facts given and to return nothing otherwise, so when
retrieval misses they hedge; the control has no such rule and answers from
memory, which pays on a benchmark this old. Count only the questions each one
commits on and the picture inverts: the control asserts on 351 of 400 and is
right on 51.6 percent of them, GraphRAG asserts on 177 and is right on 76.8
percent. A grounded system scoring below an ungrounded one on raw hits while
asserting far fewer falsehoods is the contamination the control was there to
expose.

**"What exactly does that p-value test?"** *(Slide 24 prints five of
them. Expect it from anyone who reads tables.)*
An exact paired McNemar test on per-question correctness, full system against
one ablation, over the same questions. It uses only the discordant pairs — the
questions the two disagree on — because a question they both get right or both
get wrong says nothing about a difference between them. Under the null each
discordant question is a coin flip, so the p is the exact two-sided binomial
tail: how often chance alone would split them at least this unevenly. Exact
binomial rather than the chi-square approximation, because most of these counts
are single digits. The planner condition on WebQSP splits 21–6 out of 27 and
gives 0.006; the verifier splits 0–1 and 1–0, one discordant question on each
dataset, which is why its p is 1.000 and why I report it as no *detected*
effect rather than no effect. The power limit is arithmetic: at n around 200 a
component that moves five questions in a hundred produces roughly ten discordant
pairs, and ten pairs cannot reject at conventional levels. Doubling the
half-samples is the remedy, and the threats to validity list the ablations as
underpowered.

**"Did both systems see the same candidate sets?"** *(The sharper form of the
cap question. Slide 16 raises it deliberately — answer it, don't deflect.)*
No, and it is the one thing I do not hold constant. Think-on-Graph keeps 40
relations per entity and 20 neighbours per relation — the pruning widths of the
algorithm as published — where AGR keeps 300 and 200. Measured over the
committed tool logs, the 40-relation cut binds on 31.6 percent of the 1,651
entities it expanded and the 20-neighbour cut on 32.8 percent of its neighbour
calls; AGR's relation cap binds once in 3,097 expansions and its neighbour cap
on 3.3 percent of calls. So the cut is real and it is asymmetric. What it cannot
do is rescue the budget argument: a narrower candidate set makes each step
*cheaper*, so it cannot explain why Think-on-Graph runs out of calls. What it
does mean is that the residual gap on the questions it *finishes* is measured
against a system searching a thinner pool, so that figure is a lower bound on
what it could resolve at equal width — not an estimate of it. Re-running it at
300 and 200 is the first of two baseline bounds my future work calls cheap to
lift, and it is limitation 2 in the threats to validity.

**"Your verifier doesn't verify the relationship — any edge between the two
entities passes."**
Correct, and I would rather name it than defend it: it is the layer's principal
acceptance risk, and section 4.15 lists it first among the mechanisms of wrongful
acceptance. Both structural routes ignore the relation and the direction, so a
claim that X is Y's mother is certified by an edge recording that X is Y's child.
It is a deliberate consequence of one design choice. The claim's relation is free
text and Freebase predicates are not — "X played for Y" is realised through a
roster mediator carrying no predicate named for playing — so matching on it would
reject true claims wholesale. The division of labour is that the structural
routes buy recall for "some supporting edge exists" and the third route, the
entailment check, buys the semantic precision. What I will not do is state the
exposure at the smaller of the two scales available. The population at risk is
not the rare `verify_connection` route but every claim those two routes accept
between them, and the log does not separate them: on test, of 2,008 accepted
claims, somewhere between 39 and all 2,008 were certified without any test of the
asserted relation. That is an interval two orders of magnitude wide and I report
it as one rather than choose a point inside it. Narrowing it needs the logging
change — persist accepted claims with the triples that matched them — which is
the future-work item the supporting-triple answer below names, and it is what
would let the relation be checked where the mediator schema makes that possible.

**"If verification doesn't improve accuracy, why keep it?"**
Because accuracy was never the only claim. It converts silent error into an
explicit hedge, and it pairs the answer with the triples that ground it at the
point of emission. I report the null on accuracy rather than hiding it — and I
report the bounds on the auditability too, which is the next question.

**"Show me one supporting triple, then."** *(Expect this. Slide 22 invites it.)*
I can't, from the committed record, and that is a limitation rather than an
evasion. `RunLogger` writes `n_supporting_triples` — an integer — and discards
the list, so no committed artifact in this work contains a single supporting
triple; every statistic I quote about them comes from that counter. What I can
show is the traversal record each answer was produced against. Two things follow
and I state both: the pairing is real inside the run and unavailable afterwards,
and one polarity of the verifier's error is therefore unmeasured. Persisting
accepted claims with their matching triples is one logging change, and my
future work ranks it the highest-value change for its cost. I did not make it
late because it would separate the code from results already frozen against it.

**"Why isn't the five-system comparison one of your contributions?"**
Because the thesis does not count it as one, and slide 29 is the thesis's list —
the six section 1.6 claims, in its order. The comparison and the hop-count shape
are results the contributions rest on; they get slides 17 and 18, which is where
the weight belongs. An earlier version of that slide promoted both to
contributions and dropped the ablation, the decomposition finding and the
protocol to make room — still saying "six". The thesis had already been audited
for exactly that mismatch: its conclusion itemises four and says where the
other two are.

**"How many questions is that hedge difference, and is it significant?"**
Six, on CWQ: 23.2 percent of 198 against 20.2. The sets nest — there is no
question the ablated run hedged on that the full system asserted on — so those
are exactly the six the ablated run answered and the layer declined to. None of
the six came back correct: all six were assertions that would have been wrong,
which is the mechanism, seen at the only place the design isolates it.

On WebQSP it is one question, and there the ablated run got it right. So across
the 398 paired questions correctness moved twice, once each way. I would rather
say that than be shown it. No, it is not significance-tested; the ablation's
McNemar test is on correctness, not on the hedge column, and I claim the
direction and nothing more.
*Do not* offer the no-retrieval contrast here. Its 12.2 percent is a hedge rate,
not an error rate — slide 23, a table of hedge rates, has it under WebQSP —
and AGR hedges *less* than it does, 8.2 against 12.2, so that comparison argues
the opposite of what it looks like. No-retrieval's actual error rate is 170 wrong
out of the 351 questions it asserts on.

**"Does every accepted claim get evidence attached?"**
No — one route of three does. Traversed adjacency attaches every traversed
triple joining the pair; `verify_connection` and the entailment fallback accept
with nothing attached. On the 80-question development set, 13 answers carry no
supporting triples: ten are hedges that asserted nothing, one had every claim
rejected, and two asserted a single claim certified by the route that records no
evidence. Median across all 80 is 3, mean 4.1, maximum 16 — read from the
counter, since the triples are exactly what the log does not keep.

**"Your planner result says your own design is wrong."**
It says something narrower: the thesis's finding is neither "the planner
helps" nor "the planner hurts". Without it, WebQSP rises at one hop *and* at
two — most of its questions need no composing. On ComplexWebQuestions the sign
reverses and the two-hop stratum collapses without it, though at p = 0.088
that is a direction, not an effect. The conclusion is that decomposition should
be gated on question structure — which is a finding, and one I'd have missed
without the ablation.

**"n=4 in the three-hop WebQSP stratum is meaningless."**
Agreed, and I don't draw a conclusion from it. The hop-count claim rests on
ComplexWebQuestions, where the strata are 137, 211, and 49.

**"How do you know the gold answers are reachable?"**
Verified per question against the graph before scoring — 97.0 percent on WebQSP,
99.2 on CWQ. It's the ceiling on every Hits@1 I report, and it's stated as such.
It covers answers that are entities. A gold answer that is a date, a quantity or
a superlative selection is in a class the environment chapter defines as
unanswerable here, and slide 15 says so.

**"Your CWQ Hits@1 is 209 out of 400. Isn't that 0.523, not 0.522?"**
By hand, rounding half up, yes. The scoring script formats floats, and 0.5225 is
stored a hair below itself, so it prints 0.522; the clip rate of 117 in 400 is
the same case, 29.25 percent printed as 29.2. The thesis and the deck both carry
the script's figure, so they agree with each other and with the JSON. Neither
rounding moves a comparison.

**"Where do the topic entities come from — doesn't the system have to find
them first?"**
They are given by the datasets. `use_gold_entities` is on for every run I
report, so the question's annotated mentions go to `search_entity`, which
resolves each one to a graph node through the three-stage resolver. Mention
*detection* is assumed; mention-to-node resolution is not — that part the
system does. It is limitation 7 in the threats to validity: the accuracies
I report presume a linking step a deployed system would have to perform,
and I do not
measure that step. What it is not is a between-system confound. The three
systems that touch the graph — AGR, Think-on-Graph and GraphRAG — all seed
from the same annotated mentions, and neither the parametric control nor Vector-RAG ever sees them.

**"Nine of your failures are one bug. Isn't the census measuring your
implementation?"**
In part, and I would rather say which part. Nine of the 38
`decomposition_error` cases carry the subtype `extraction_bug`, and they share
one mechanism: the evaluator resolves every gold value, the drafted sentence
names them verbatim, and `answer_entities` then collapses to the sentence's
grammatical subject. WebQTest-1215 drafts all six of Stephen Covey's
professions and scores `['Stephen Covey']`. The reasoning was complete and the
verifier certified it; what failed is the step that reads entities back out of
the draft. That is limitation 10, and the direction is the part worth saying:
it depresses my *own* reported accuracy, so on that question shape the
headline numbers are a floor rather than an estimate. The fix is an
instruction to the claim decomposer, not an architecture change, and it is the
first of the three repairs the census earned. The category split is backup
slide 34.

**"Is that a standard dataset, or one you built yourself?"**
*(Asked at the pre-defense. Section 3.1.3 of the thesis is “Source Datasets”.)*
Standard, and public. WebQSP and ComplexWebQuestions, both unmodified, taken
from the per-question subgraph distribution the Reasoning-on-Graphs paper
released — rmanluo/RoG-webqsp and rmanluo/RoG-cwq on HuggingFace. I collected
nothing and annotated nothing, which is also why every system on slide 17 is
measured on the questions those benchmarks define. What I did build is the
knowledge environment derived from them: the union of every per-question
subgraph into one graph, plus its store and its vector index. That union is
deliberate — a per-question subgraph in isolation is a near-oracle, extracted
to contain its own answer, so merging all of them back together is what
restores the distractors. Section 3.1.3 gives the provenance, section 5.2.2
gives the sampling: 400 per dataset, stratified at seed 42, every question ID
listed in the appendix.

**"You used RoG’s data. How does AGR compare to RoG itself?"**
*(Asked at the pre-defense. Backup slide 37 has the table — put it up.)*
Directly, and RoG is ahead: 85.7 and 70.8 on WebQSP, 62.6 and 56.2 on CWQ,
against my 75.5 and 64.2, and 52.2 and 46.9. The gap is outside my confidence
intervals, so it is real and not sampling. The reason is not subtle. RoG
fine-tunes LLaMA2-Chat-7B on the training splits of both benchmarks — 2,826
WebQSP and 27,639 CWQ questions — for three epochs. AGR does no training at
all: the backbone is frozen and has seen no question from either benchmark
before it is evaluated. So it is a supervised system against a zero-shot one on
the same data, which is a difference in kind. I could not hold the backbone
constant against RoG the way I do across my five systems, because RoG’s
contribution *is* its fine-tuned weights — that is the same objection my
Chapter 2 table already makes against every fine-tuned entry in the literature.
What I would not do is claim parity. Section 5.9 of the thesis states the
numbers, states that RoG leads, and separates what the comparison settles from
what it cannot. The verification layer, the ablation and the failure census
have no counterpart in RoG’s evaluation, and closing that accuracy gap would
not settle any of them.

**"Your proposal promised MCTS and FactBench. What happened?"**
*(Backup slide 38.)* Both were withdrawn before any test run, and the thesis
says why where each would have appeared. The search has no rollouts and no
value backpropagation, so calling it MCTS-inspired would invite comparison with
machinery it does not have; it is guided best-first search with a bounded beam
and backtracking. FactBench was dropped because an evaluator whose facts sit
inside the graph the system retrieves from makes a low hallucination rate
automatic. Path fidelity, the proposal's third criterion, needs gold SPARQL
relation chains the RoG distribution does not carry, so it is future work.

**"Is this reproducible?"**
Every number in the thesis is generated from frozen run records by a script;
none is transcribed. Same for the three data figures in this deck — they are
pulled directly from the thesis's own generated sources.

---

## Recovery notes

If you hit **12:56 (the end of slide 17) more than 40 seconds late**, compress
as follows.

- Slides 21 and 22 — take them as one: *"It doesn't improve accuracy or explain
  the precision lead. It withholds what it cannot ground and attaches evidence.
  The case is auditability."* Saves ~40 s.
- Slide 7 — say the first two sentences and the last; skip RoG and the
  post-hoc checkers. Saves ~15 s.
- Slide 14 — stop at "both supported." Saves ~5 s.

Never compress 17, 18, 19, 24, or 25. Slide 19 in particular: skipping it
means a committee member raises the clipping issue instead of you, and it
lands very differently that way.

## Delivery

- **Say the number, then what it means.** Not the reverse. "Twenty-two percent
  of what the parametric model asserts has no basis in the graph. It has no
  source to point to."
- **Four slides are negative results** (19, 20, 21, 22). Deliver them at normal
  pace, not apologetically. A student who reports a clean null is more credible
  than one who reports only wins.
- The word is **hedge**, not "refuse." A hedge is an explicit non-assertion,
  and it scores as a miss.
- If you lose your place, the takeaway bar at the bottom of the data slides is
  your prompt — read it aloud and continue.
