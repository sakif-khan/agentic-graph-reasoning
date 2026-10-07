# FAQ

Running list of questions about the system, with short answers grounded in
the code. Ordered by the slide each question concerns.

---

## 1. How do beam width 3, max relations 300 and max neighbors 200 come into play? How does the beam search work?

*Slides 6, 10 and 11: guided beam search, AGR, the explorer.*

**None of the three lives in the evaluator.** They act in the explorer
([agr/nodes.py](../agr/nodes.py) `explorer_node`) and in the KG tools it
calls ([agr/kg_tools.py](../agr/kg_tools.py)). The evaluator only reads the
result: the 30 highest-scoring facts gathered so far (`top_facts(k=30)`).

| Setting | Where | What it caps |
| --- | --- | --- |
| `max_relations=300` | `KGTools.get_relations` | relation types listed per anchor, before scoring |
| `beam_width=3` | `BudgetConfig`, used in `explorer_node` | relations expanded per anchor, after scoring |
| `max_fanout=200` | `KGTools.get_neighbors` | neighbour entities returned per expanded relation |
| `max_anchors=5` | `BudgetConfig` | entities carried into the next step |

**One explorer step, for the current sub-objective:**

1. **List.** For each anchor entity, `get_relations` lists every relation
   type touching it, in both directions, with its edge count. Schema
   relations (`common.`, `type.`, `freebase.` and so on) are dropped. The
   rest are sorted by edge count and **the 300 most frequent are kept**.
   This is a safety cap on hub entities, so the scorer never sees an
   unbounded list.
2. **Score.** All candidates from all anchors are scored in one pass. Each
   gets an embedding similarity to the objective. The top 20 by embedding go
   to one batched LLM call that rates each 0 to 1. The final score is
   `alpha * embedding + (1 - alpha) * LLM`.
3. **Prune (the beam).** Per anchor, the **3 best-scoring relations** are
   kept. A relation banned by an earlier backtrack is skipped and does not
   use a slot, so the 4th best moves up. The beam is per anchor, not
   global. With 5 anchors, up to 15 relations are expanded in one step.
4. **Expand.** `get_neighbors` follows each kept relation and returns **at
   most 200 neighbours**. It asks the database for 201, so it can tell the
   list was cut (`truncated`). If a neighbour is a CVT (a Freebase mediator
   node, such as a "marriage" record), it hops through to the real entities
   behind it. The combined list is still cut to 200. Every neighbour becomes
   a traversed triple. Worst case is 5 x 3 x 200 = 3,000 triples per step.
5. **Next frontier.** The neighbours are ranked by the score of the
   relation that reached them and deduplicated. **The top 5 become the
   anchors for the next step.** Depth goes up by one (max 4).

**Then the evaluator** sees the 30 most relevant facts and answers
"answer", "continue" or "backtrack". The router backtracks on any of three
triggers, in order: the step found nothing (dead end), the best score fell
below `tau`, or the evaluator said so. A backtrack restores the
highest-scoring saved frontier and bans the relations just expanded, so the
next attempt takes a different branch.

**So, in one line:** 300 bounds what the scorer has to rank, 3 bounds what
gets followed, 200 bounds what each follow brings back, and 5 bounds what
carries forward.

---

## 2. How do slide 8's systems ("What everyone else does") relate to slide 7's families ("Where existing approaches stop")? And how do both relate to my baselines?

*Slides 7, 8 and 17: related work and the baselines.*

**Slide 7 is the map, slide 8 zooms into one region.** Slide 7 sorts
approaches into four families by *when* retrieval happens. Slide 8 lists
named systems, almost all from the last two families, and scores them on
AGR's four features.

| Slide 7 family | Slide 8 systems | My baseline (slide 17) |
| --- | --- | --- |
| Parametric | — | **No-retrieval** |
| Vector-RAG | — | **Vector-RAG** |
| Static GraphRAG | GraphRAG | **Static GraphRAG** (one hop, own build) |
| Agentic navigation | Think-on-Graph, Plan-on-Graph; RoG near it | **Think-on-Graph** (reimplemented) |

- **One baseline per family.** Each row of slide 7 is one baseline, so the
  comparison runs along the same axis the slide argues: retrieval before
  reasoning, fixed radius, then navigation.
- **Think-on-Graph is the agentic representative**, run on our graph,
  tools, model and budget (Q4).
- **Static GraphRAG is a stand-in, not Microsoft's GraphRAG.** That system
  builds a graph from text. Ours keeps only the idea "fixed neighbourhood,
  no search": one logical hop, reranked, answered with Vector-RAG's exact
  prompt, so the pair differs only in retrieval (`sec:baseline-graphrag`).
- **RoG is not a baseline.** It is fine-tuned and plans relation paths
  before retrieving. It is compared on slide 19 from its released outputs,
  rescored with its own scorer.
- **Plan-on-Graph is not a baseline either**, though it is the closest in
  ambition (decomposition and real backtracking). Its reflection corrects
  the *search*, not the *answer's claims*. That is the gap in slide 8's
  last column. The thesis does not say why it was not run, so expect the
  question.
- **Chain-of-Verification and FActScore** (slide 8's footnote) are a
  different line: they check claims *after* generation, not against
  retrieved triples before answering.

**What ties all three slides together:** none of the families or systems
verifies the answer's claims against what it retrieved *before* answering.
That is the takeaway of both slides 7 and 8, and the gap the
Structural Verification Layer fills (slides 12 to 14).

---

## 3. Entity-pair adjacency is explainable groundedness. Why fall back to one batched model call for entailment? Doesn't that violate the groundedness-checking principle?

*Slides 12 to 14: the Structural Verification Layer.*

**It bends the principle at one point, on purpose, and in one direction
only.** The principle as the book states it (framework chapter, "Why the
Structural Check Runs First") is: *models rank, symbols decide; the model
is consulted only where the graph is silent, and never overrides it.* The
entailment call keeps that rule, but it does give up explainability for
the claims it handles. Code: `verifier_node` in
[agr/nodes.py](../agr/nodes.py).

**Why a fallback is needed at all.** The structural routes cannot run on
every claim:

1. **Untraversed names.** The name-to-ID map is built only from traversed
   triples. A claim naming an entity the agent never walked has no ID, so
   neither adjacency test can run, even if the entity is in the graph.
2. **Non-adjacent pairs.** Both routes test "adjacent directly or through
   one mediator". A true claim whose endpoints are further apart fails
   both.

Without a fallback, every such claim becomes unsupported automatically and
triggers a retry or a hedge, even when the retrieved facts support it.

**What keeps it grounded:**

- **The source is still the graph.** The model judges each claim against
  the same 60 retrieved triples the draft was written from, not its own
  knowledge. The prompt counts "plausible but absent, contradicted, or
  only inferable via outside knowledge" as unsupported.
- **It only sees leftovers.** Claims the graph accepted never reach it, so
  it cannot override a structural verdict.
- **It fails closed.** If the call errors or the budget is spent, every
  pending claim is marked unsupported.
- **Batching is about cost, not principle.** One numbered list, one call,
  one verdict per claim. It asks the same question a separate call per
  claim would, but costs 1 of the 25 calls instead of N. (Claims judged
  side by side could sway each other a little; that was not measured.)

**What it does give up (the thesis states all three):**

- **No evidence.** Only the traversed-adjacency route attaches triples. A
  claim accepted by entailment, or by `verify_connection`, is accepted
  with nothing attached.
- **No per-claim record.** At test scale 2,008 of 2,110 claims were
  accepted, 39 of them by `verify_connection`. How the other 1,969 split
  between adjacency and entailment **was not logged**, so the share that
  rests on a model judgement is unknown (book: `app:route-frequencies`).
- **The fact window is ranked for the question, not the claim.** A claim
  about a side entity may be judged against facts that never mention it.
  This cuts *against* such claims, so it errs toward rejecting.

**The flip side, worth saying:** the structural routes are explainable but
*relation-blind*. A "mother" claim passes on a "child" edge (slide 14).
The entailment check is the only route that reads the relation at all.
Structural gives an auditable "some edge exists"; entailment gives a
semantic but unauditable "these facts say this". Each covers what the
other misses.

**If asked "what would you change":** (a) log each claim's route, which
closes the 1,969 gap; (b) before falling back, resolve untraversed names
with `search_entity` and try `verify_connection`, so more claims settle in
the graph and fewer by the model.

---

## 4. Why re-implement ToG? Couldn't we use the paper's implementation? What relation/neighbour pruning did they use?

*Slides 8 and 17: Think-on-Graph, reimplemented.*

**Why not their code or their numbers:**

- **Published numbers** come from other backbones (ChatGPT, GPT-4), full
  Freebase and other answer matching. ToG's own two variants differ by
  ~1.8 points on CWQ, the size of a typical claimed gain, so a cross-paper
  number can't rank architectures (background chapter).
- **Their code** (github.com/IDEA-FinAI/ToG) queries a full-Freebase
  SPARQL server, defaults to gpt-3.5-turbo at temperature 0.4 for
  exploration, and has no call cap. Running it would vary the graph,
  tools, model and budget along with the algorithm.
- **Reimplementing on our tools** holds all of those fixed, so only the
  search differs (`sec:baseline-tog`). The price: its scores are not
  comparable to the published ones.

**What their released code prunes** (`main_freebase.py`,
`freebase_func.py`, checked 2026-10-07):

| | Original ToG code | Our reimplementation | AGR |
| --- | --- | --- | --- |
| Relations shown to the LLM | **all**, minus schema relations, alphabetical | first 40 by edge count | first 300 by edge count |
| Neighbours shown to the LLM | all; if ≥ 20, a **random 5** | first 20 | first 200 (no LLM) |
| Relations kept | top 3 by LLM score | up to 3 | 3 per anchor |
| Next frontier | top 3 **by score**, across all candidates | **first 3** kept, unscored | top 5 by score |
| Width / depth | 3 / 3 | 3 / 3 | — / 4 |

So the thesis is right that 40/20 are not the paper's. Note the
directions: relations are narrower than the original (40 vs all),
neighbours wider (20 vs a random 5).

**A gap the thesis does not state:** the original ranks entities by
relation score × entity score and keeps the global top 3. Ours keeps the
first 3 entities selected, in visiting order
([agr/baselines/tog.py](../agr/baselines/tog.py), `frontier = nxt[:WIDTH]`),
so the first relation's picks can fill the whole frontier. That makes our
ToG weaker than the original on that point, and it should be disclosed
alongside the 40/20 widths.

---

## 5. How do ToG's 40/20 candidate caps compare with AGR's 300/200? What does "Not held equal" mean?

*Slide 17: making the comparison fair.*

**The 40/20 caps play the same role as AGR's 300/200.** They limit how
much of each tool result the system gets to choose from
([agr/baselines/tog.py](../agr/baselines/tog.py)). Both systems call the
same `get_relations` and `get_neighbors`. ToG then cuts the results more
tightly:

| | ToG | AGR |
| --- | --- | --- |
| Relations shown per entity | first 40 | first 300 |
| Neighbours shown per relation | first 20 | first 200 |
| Who picks relations | LLM, 1 call **per entity**, up to 3 | scorer, 1 batched call **per step**, 3 per anchor |
| Who picks entities | LLM, 1 call **per relation**, up to 3 | no LLM; ranked by relation score, top 5 |
| Frontier / depth | 3 entities, depth 3 | 5 anchors, depth 4 |

`get_relations` sorts by edge count, so ToG's 40-cut drops the relations
with the fewest edges, which are often the specific ones a question needs.
The cut binds on **31.6% of the entities ToG expanded**, against 1 of AGR's
3,097. The neighbour cut binds on 32.8% of ToG's neighbour calls, against
3.3% of AGR's.

**"Not held equal"** means two things on slide 17 differ between the
systems, and the slide says so before anyone else does:

1. **The candidate widths** (40/20 against 300/200). The beam width and
   depth come from the ToG paper. The 40/20 widths do not; they belong to
   this reimplementation.
2. **The prompt.** AGR's drafting prompt carries grounding rules. The
   baselines' prompt is plain.

**Why the widths don't explain the result:** a narrower list makes each
ToG step *cheaper*, so it cannot be why ToG runs out of calls. The catch is
on the questions ToG does finish. There it searched a thinner pool than
AGR, so its score there (0.852 / 0.629) is a **lower bound**. With equal
widths it could be higher. Equalising the widths is the first item of
future work.

---

## 6. What are the Hits@1 and F1 scores?

*Slide 18: main results.*

Both compare the answer entities a system asserts with the gold answer set,
per question, then average over questions
([scripts/score_test.py](../scripts/score_test.py)). Names are matched
exactly after lower-casing and Unicode normalisation.

- **Hits@1:** 1 if *any* asserted entity is a gold answer, else 0. Strictly
  this is set-intersection Hits@1: the answer is a set, not a ranked list,
  so there is no "top 1". A hedge (nothing asserted) scores 0.
- **F1:** the balance of precision (share of asserted entities that are
  gold) and recall (share of gold entities asserted):
  `2·P·R / (P + R)`. A hedge scores 0.

**Example:** gold {A, B}, answer {A, C} → Hits@1 = 1, P = ½, R = ½,
F1 = 0.5. So Hits@1 asks "got one right?", F1 also punishes wrong extras
and missed answers.

---

## 7. Formulas for precision, recall and F1.

*Slide 18: main results.*

Per question, with **G** the gold answer set and **A** the asserted set
(both normalised), from `prf` in
[scripts/score_test.py](../scripts/score_test.py):

- **Precision** = |G ∩ A| / |A|
- **Recall** = |G ∩ A| / |G|
- **F1** = 2 · P · R / (P + R), or 0 if P + R = 0

If A is empty (a hedge), all three are 0. Each is averaged over questions.

---

## 8. McNemar p: does high mean the component makes no difference, and low mean it is more effective?

*Slides 18 and 26: paired McNemar tests.*

**Not quite.** p answers one question: *if removing the component changed
nothing, how likely is a split of disagreements this lopsided?*

- **Low p (< 0.05):** the difference is probably real. It says nothing
  about **direction** or **size**. Direction comes from which way the
  discordant questions split, size from the Δ in Hits@1. Example: the
  planner's p = 0.006 on WebQSP, but the split was 21–6 *for* the version
  without it. The planner was significantly **harmful** there.
- **High p:** **no evidence** of a difference, not evidence of none. It can
  mean the effect is tiny, or that there were too few disagreements to
  tell (the verifier's p = 1.0 rests on one question; see Q10). Hence
  "no detectable effect", never "no effect".

---

## 9. If ToG does better on the questions it finishes within the call budget, with fewer relations and neighbours, doesn't that make AGR worse?

*Slide 21: ToG finished vs clipped.*

**It makes AGR's search no better than ToG's, and the thesis says that.
It does not make AGR the worse system.** The figures are in Table
`tab:tog-split` ([thesis_book/tables/tab_tog_split.tex](../thesis_book/tables/tab_tog_split.tex)).

| | n | ToG | AGR | Δ |
| --- | --- | --- | --- | --- |
| WebQSP, ToG finished | 283 | 0.852 | 0.788 | −0.064 |
| WebQSP, ToG clipped | 117 | 0.197 | 0.675 | +0.478 |
| **WebQSP, all** | 400 | 0.660 | **0.755** | **+0.095** |
| CWQ, ToG finished | 224 | 0.629 | 0.607 | −0.022 |
| CWQ, ToG clipped | 176 | 0.188 | 0.415 | +0.227 |
| **CWQ, all** | 400 | 0.435 | **0.522** | **+0.087** |

**What the thesis concedes:** on finished questions ToG is ahead, and its
score there is a lower bound. So the claim "guided search finds answers
better than beam search" is *not* made (evaluation chapter,
`sec:tog-split`).

**What it claims instead:** beam search cannot afford to finish under a
budget a deployed system would impose. Guided search can. The cap is part
of the task, not a nuisance. Every system got the same 25 calls, fixed in
advance. ToG is clipped on 29% of WebQSP and 44% of CWQ, and on all 400
questions AGR wins on both datasets (McNemar p < 0.004).

**Why ToG gets clipped:** its cost multiplies. Each depth costs up to
3 entities × (1 relation call + 3 entity calls) + 1 sufficiency call = 13
calls. It stops one call early to save the answer call, so it has 24 to
spend. Two depths at full width need 26, so **a question that keeps the
beam full past the first hop runs out**. AGR batches all its scoring into
one call per step and averages 6.2 calls a question on WebQSP, against
ToG's 12.8.

**Why the finished subset favours ToG** (my point, not in the thesis):
the subset is chosen by ToG's own behaviour. A run finishes early when ToG
judges its triples sufficient, and that judgement tends to go with being
right. These are also easier questions in general: AGR scores 0.788 on
them and 0.675 on the rest. A subset selected by one system's success
leans toward that system, so −0.064 is not a clean measure of search
quality either.

**Be ready for:** AGR is not cheaper on every axis. It uses fewer calls
but **more tokens** (4,511 against 3,615 a question on WebQSP; 6,818 on
CWQ). Say "fewer calls under a call cap", not "cheaper".

---

## 10. "Remove it and Hits@1 and F1 do not detectably change, at p = 1.0 on both datasets." What does p = 1.0 mean here?

*Slide 23: what verification does not do.*

**It is the p-value of a McNemar test comparing the full system with the
same system minus the verification layer, question by question.** p = 1.0
is the highest a p-value can be. It means the data give no evidence at all
of a difference, but here mainly because there was almost nothing to test.

**How the test works** (exact-binomial McNemar, evaluation chapter):

1. Pair the two runs on the same questions, scoring each question
   right/wrong (Hits@1).
2. Ignore every question both got right or both got wrong. They say
   nothing about which system is better.
3. Count the **discordant** questions, where one system was right and the
   other wrong. If removing the layer makes no difference, each one is a
   coin flip, so the split should look like heads/tails.
4. p = the chance of a split at least this lopsided from fair coins.

**What happened:** removing the layer changed the result on exactly one
question per dataset (WebQSP 0 vs 1, CWQ 1 vs 0; 2 of 398 in all). With
one discordant question, any outcome is a 1–0 split, and the two-sided
chance of a split that lopsided is 2 × 0.5 = **1.0**. So p = 1.0 was
certain before you looked at which way it went.

**How to say it:** "the test had no information", not "proved no
effect". That is why the slide says *detectably*. The real finding is the
count itself. The layer passes nearly every draft untouched (77 of 80 on
development), so it barely changes which answers come out, and an
accuracy test cannot see it. Its value is the output contract (answers
paired with supporting triples), not accuracy.

**One wording catch on the slide:** McNemar is run on Hits@1 right/wrong
only. **F1 has no p-value.** The book reports F1 moving +0.004 and −0.009
with no test. "Hits@1 and F1 do not detectably change, at p = 1.0" reads
as if both were tested. If asked: "the p is for Hits@1; F1 moved under a
point on both datasets."

---

## 11. What is the "embedding-only scoring" ablation? Explain the component.

*Slide 26: the ablations.*

**The component is the hybrid scorer**
([agr/scorer.py](../agr/scorer.py)), which ranks candidate relations in
each explorer step (Q1, step 2):

- **Embedding term:** cosine similarity between the sub-objective and the
  relation name (MiniLM vectors, relation vectors precomputed). Free, no
  model call.
- **LLM term:** the 20 best by embedding go to one batched model call,
  which rates each 0–1 for "does following this edge from this anchor
  serve the objective". It judges meaning, not word overlap.
- **Blend:** score = α · embedding + (1 − α) · LLM, with **α = 0.7**
  (frozen from the development sweep).

**The ablation sets α = 1.0:** embedding only, no scoring call.

**Result** (evaluation chapter, `sec:abl-embonly`):

| | Hits@1 Δ | F1 Δ | p | Tokens | Calls |
| --- | --- | --- | --- | --- | --- |
| WebQSP | −0.015 | −0.016 | 0.66 | 3,413 vs 4,562 | 4.4 vs 6.2 |
| CWQ | −0.020 | −0.008 | 0.48 | 4,925 vs 7,105 | 5.9 vs 9.1 |

Always slightly worse, never significant, and clearly cheaper. So the LLM
term buys a little accuracy with tokens. The main evidence for α = 0.7 is
the development sweep, where α = 1.0 lost 5 hits of 80; this ablation
only corroborates it.
