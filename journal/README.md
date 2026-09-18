# journal

Journal manuscript drawn from `thesis_book/`. Target: Elsevier —
*Knowledge-Based Systems* or *Information Processing & Management*.

| File | What it is |
| --- | --- |
| `journal_0421052099.tex` | **The document.** `elsarticle`, `preprint,review,12pt` |
| `preamble.tex` | Fonts, figure toolchain, palette, system-name macros |
| `sections/*.tex` | Nine sections. Undrafted ones carry their source chapter and word budget as comments |
| `figures/` | Generated. Do not edit |
| `highlights.txt` | Elsevier highlights, submitted as a separate file |
| `supplement.tex` + `supplement/` | Supplementary material: the thirteen prompts, generated from the code. Build with `latexmk -pdf supplement.tex` |

## Build

```bash
cd journal
latexmk -pdf journal_0421052099.tex
python ../scripts/check_paper_log.py
```

`review` gives the 1.5-spaced single column Elsevier wants for peer
review — all the option does is set the baseline stretch.

**The second line is part of building, not an extra.** The bar below is
"0 warnings of any class", and reading a 900-line log by eye does not
enforce it: four `Package hyperref Warning` lines rode through several
rounds of *zero warnings* because the check was a grep for `LaTeX
Warning` and `Overfull`. `check_paper_log.py` looks for the word rather
than for remembered phrasings, and refuses a log that is missing, that
was built from sources since edited, or that stops before the run
finished — none of which is the same as a quiet one.

**No line numbers, deliberately** — and as of August 2026 this is
settled rather than merely unverified. Elsevier's generic guide for
authors states that at initial submission "there are no strict
formatting requirements", and mentions line numbering nowhere. So the
absence is consistent with Elsevier's stated position, and the original
justification for adding them — "Elsevier's own guidance asks for
numbered lines at submission" — was simply false.

Two caveats, because this is guidance about guidance:

- The **KBS** guide for authors specifically is still unread. It returns
  403 to an automated fetch by every route tried: `sciencedirect.com`
  directly, and `elsevier.com`, which 301s there. Re-tried in September
  2026 through a rendering proxy as well: the page serves a CAPTCHA. What
  a search engine's summary of the page reports is an abstract of at
  most 250 words, 1 to 7 keywords, and 3 to 5 highlights of at most 85
  characters each; the manuscript is inside all three, but a summary is
  not the page. A journal may add its own requirement. If you can open
  that page in a browser, check it and replace this paragraph with what
  it says.
- An earlier version of this note claimed Editorial Manager builds the
  reviewer PDF itself. That may well be true, but it was never verified
  either, so it is gone rather than repeated.

If a checklist does ask for line numbers, it is two lines:
`\usepackage{lineno}` in `preamble.tex`, and `\linenumbers` *after*
`\end{frontmatter}` in `journal_0421052099.tex` — never in the preamble, which
numbers the title block on its own inconsistent count before the body
starts.

**One column is correct for submission** — the
two-column look is the publisher's typesetting at proof stage, not
yours. Swap the class options for other purposes:

| Options | Use |
| --- | --- |
| `preprint,review,12pt` | what you submit |
| `preprint,12pt` | single-spaced copy to circulate or post to arXiv |
| `final,5p,times,twocolumn` | preview the proof; expect figure geometry to need revisiting |

**The measure is widened in `preamble.tex`** (September 2026): under
`preprint` elsarticle leaves the 12pt article default, a 131 × 220 mm
text block with 39 mm side margins, and the 1.5-spaced build ran to 72
pages. `\usepackage[textwidth=468pt, textheight=660pt,
centering]{geometry}` sets the class's own 3p width with 25 mm side
margins and about 30 mm top and bottom; the same content is 51 pages,
with zero box warnings. Elsevier places no layout requirement on an
initial submission. The remaining lever is the `review` option's 1.5
line spacing: dropping it (`preprint,12pt`) gives 36 pages, but 1.5
spacing is the form reviewers expect and the class provides for that
reason. Remove the geometry line before switching to
`1p`/`3p`/`5p`, which load geometry themselves.

Only `journal_0421052099.tex` is a document. `preamble.tex`, the nine sections
and the figures are fragments and stop with *Missing `\begin{document}`*
if built directly; each carries a `% !TEX root` line, checked by
`python scripts/check_tex_roots.py`.

## Numbers and figures

Nothing is transcribed. The three data figures in `figures/` are emitted
by

```bash
python scripts/build_figures.py --target paper
```

from `results/phase4/thesis_numbers.json` — the same file the thesis and
the slides read. `paper` is a third target beside `thesis` and
`presentation`, so a re-run of the experiments propagates to all three
documents at once. No figure that carries a number is re-drawn by hand,
so if the numbers ever are regenerated, the figures follow without
anyone remembering to update them. The fourth file in `figures/`,
`fig_claim_path.tex`, carries no numbers: it is hand-drawn, has no
generator, and is a copy — see below.

## The directory has to build on its own

What gets uploaded is `journal/` and nothing above it, so the
manuscript must build with no parent directory present. It did not,
until this was fixed: `\bibliography` and one `\input` reached into
`../thesis_book/`, which resolved perfectly here and would have failed
at the publisher. Both are now local copies:

| file | copied from | differs by |
| --- | --- | --- |
| `journal.bib` | `thesis_book/buetcsepgthesis.bib` | nothing |
| `figures/fig_claim_path.tex` | `thesis_book/figures/fig_claim_path.tex` | its `% !TEX root` line |

A copy is a thing that drifts, which is the same hazard the two
bibliographies already have a test for. `tests/test_paper_self_contained.py`
pins both against their originals, fails if any source names a path
outside `journal/`, and fails if an `\input` names a file that is
not there.

**The thesis is still the source of truth for references.** Add to
`thesis_book/buetcsepgthesis.bib` — with `agr.bib` as its annotated
mirror, kept in step by `tests/test_citation_convention.py` — then
re-copy it here. The test tells you when you have forgotten.

## The numbers are the thesis's numbers

**This paper reports exactly what the thesis reports.** No re-run, no new
measurements. The submission exists so that the work is on record and
under review during the pre-defense and defense; reviewer requests get
answered in revision, when they arrive and are specific.

That decision is fine, and it has one condition attached: the limits have
to be stated by the paper rather than discovered by the reviewer. Three
of them, all already recorded in the thesis:

- **400 questions per dataset**, not the full splits — a pre-specified
  fallback adopted when full-split cost was projected at \$45–55 against
  a \$15–20 ceiling. Give the bootstrap interval (roughly ±5 points on
  Hits@1) in the results section rather than leaving the sample size to
  be noticed in a table caption.
- **One backbone**, `gpt-5.4-mini`, frozen and closed. The paper
  establishes how these architectures compare on one backbone, not how
  they scale across backbones.
- **Nondeterminism.** Trajectory stability is ≈67%, so one run per system
  is a sample of one. Say so plainly; do not let a reader assume seeds
  were averaged.

Write **"pre-specified"**, never "pre-registered". The protocol was fixed
and documented before the test sets were built, which is the true and
defensible claim; nothing was filed with a registry. A reviewer who
catches that overclaim discounts every other rigour claim in the paper,
and this paper has several worth keeping.

If a revision request does ask for more evidence, the full splits are the
cheapest answer available — the whole benchmark cost \$11.13, so the run
that removes the objection is roughly fifty dollars.

## The framing (September 2026)

The manuscript was reframed after a reviewer-style pass found the
original framing indefensible: it led with the system and its
verification layer, and the paper's own measurements show the layer
changes the answer on one question per dataset, that zero ungrounded
assertions belong to navigation, and that the output contract is not
persisted. All three facts were already in the paper. The title is now
*Component Attribution in Agentic Knowledge Graph Question Answering: A
Controlled Ablation, Budget Analysis, and Failure Census*; the system is
the instrument and the attribution study is the contribution. What that
changed, beyond the front matter:

- **Section 3 specifies the loop** (Algorithm 1, the embedding model,
  τ, what the evaluator sees, how the backtracker picks a snapshot, how
  each ablation flag is implemented, a worked example). A reviewer could
  not reimplement AGR from the earlier version.
- **Section 5.3 reads the budget split within hop strata** (Table 4)
  and states the per-depth call arithmetic that makes the 25-call cap
  forbid the baseline's third expansion. The split conditions on the
  baseline's own outcome, and the paper now says so and shows what that
  costs on each dataset.
- **Section 7.2 reports which systems converge** on the cleared
  consensus rows (Table 8). The earlier claim that the echo attractor is
  "a property of the graph's neighbourhood structure rather than of any
  one search policy" did not survive the breakdown: on CWQ the
  no-retrieval control is among the agreeing systems on 25 of 31 rows.
- **Six references added** (GNN-RAG, SubgraphRAG, ToG 2.0, GCR,
  Self-RAG, CRAG), each checked against its arXiv record.
- **Wall-clock, zero-triple answers, and the one-at-a-time caveat** are
  reported; the outlook names the four experiments the reframe makes
  necessary (equal-width baseline under a cap sweep, replication plus a
  joint-removal condition, full splits, the logging change).

**Derived analyses, September 2026 (`scripts/paper_analyses.py`).** After
the reframe, the reviewer issues that prose could not answer were
answered from the committed records instead of new runs. The paper
reports the ones that stay inside the thesis's readings:

- **Computed but not reported: the candidate-width cut read against
  the gold path** (`gold_path_discards`). The baseline's tool log keeps
  the full relation list before its own 40-row cut, and the RoG parquet
  gives each question's subgraph, so for every truncated expansion at
  an anchor on a shortest path to a gold answer the function asks
  whether the continuing relation was offered or discarded. It was
  discarded on 89 WebQSP and 51 CWQ questions; on the questions where
  neither the cap nor the cut binds, the baseline is ahead on both
  datasets (0.896 vs 0.784, 0.670 vs 0.612), and 65 of the 117 WebQSP
  clips had a discard. That contradicts the thesis's §5.3 sentence that
  a thinner pool cannot explain running out of calls. The paper carried
  this as a table and a rewritten §5.3 for one revision (e081568) and
  then dropped it on 2026-09-18 at the author's decision that the paper
  keeps the thesis's reading; §5.3, §8.2, the abstract and the
  conclusion are back to the wording of 3537b3a, and
  `check_paper_numbers.py` now checks that the table is absent. The
  function stays in the module, and `python scripts/paper_analyses.py`
  still prints it.
- Paired bootstrap intervals on every ablation delta (the CI columns of
  tab:ablation),
  the union of the discordant sets, and the development-set α sweep
  (thesis tab:sweep, from `results/phase3/score_run.csv`).
- A design-space table in §2 (Table 1); the thirteen prompt templates
  as supplementary material (`supplement.tex`, generated from the code
  by `scripts/build_paper_supplement.py`, so it cannot drift from the
  thesis's Appendix A, which `check_appendix_prompts.py` pins to the
  same code).

Not done, because each needs new labels or a colleague rather than a
script: hand-measuring the verifier's wrongful acceptance and rejection
from the drafts and rejected claims in the records; a second annotator
on the 105 flagged questions.

**The census total was 259 and is 256; the thesis and slides carry the
correction.** `scripts/synthesize_census.py` counted three *excluded*
questions in the histogram: two Stage A rows naming adjudicated
benchmark defects and the one Stage D row later promoted to a formal
exclusion. The thesis's appendix on the census denominator documented
all three as deliberate re-entries, which contradicted the chapter's own
rule that adjudicated defects leave the analysis altogether and the
abstract's "removed before the census began". The script now drops
excluded identifiers whatever label file they sit in and counts each
question once, so the histogram totals 256 (85 + 171); `thesis_numbers.json`
and the figures were regenerated (only the census blocks changed:
relation_selection 65 -> 64, kg_gap 44 -> 43, gold_noise 7 -> 6,
census-visible defects 17 -> 16, so 41 + 16 = 57 with no overlap). The
population after exclusions is 262 (86 + 176); the six the census does
not read (1 + 5) are the Stage B surface-form near-misses that
`dump_failure_packets.py` sets aside by design, which the paper's
population paragraph states and `check_paper_numbers.py` verifies against
the near-miss flags (an earlier draft of this note, and of that
paragraph, wrongly called them failures no labelling pass had reached).
The thesis chapters, the census-denominator appendix, the slides, and
`check_slides.py` were corrected in the same pass (2026-09-18).

## Editing notes

- **Register (September 2026).** The thesis chapters were rewritten to
  short, separate sentences, active voice where it reads at least as
  well, and few em-dashes; the paper follows them. Prose is filled at
  72 columns, and each file keeps whatever line ending it had. Two
  em-dashes are pinned by `check_paper_numbers.py` (the half-splits
  sentence and the census-found-defects sentence) and must stay.
- **Synchronised with the thesis at `d09866e` (September 2026).** What
  came across: the RoG comparison (`sec:rog`, Table 4), the dataset
  provenance (`rmanluo/RoG-webqsp`, `rmanluo/RoG-cwq`, used
  unmodified), the environment's expressiveness limit (no literals, no
  ordinals), the dated backbone snapshot, the four pre-specified
  decisions, CWQ assertion precision, the paired-test counts against
  the agentic baseline, the breadth check, the depth-cap binding rate,
  the planner's per-stratum effect, the no-multiple-comparison
  statement, the ban-list misalignment that bounds the backtracking
  null, the first-departure reading protocol, and the near-miss
  measurement. Every new figure is bound to its source in
  `check_paper_numbers.py`. Two thesis figures were checked and NOT
  carried: RoG's training-split sizes are 2,826 and 27,639 in the
  distribution's own parquet files (the thesis says 2,830 and 16,900),
  and the claim that PoG and ToG disagree about ToG's CWQ score is a
  misreading -- 58.9 / 69.5 are ToG-R, a variant from the ToG paper
  itself, and PoG quotes ToG's own 57.1 / 67.6 faithfully.
- **Figure 3's caption was wrong from the day it was written.** It said AGR sits above
  and to the *left* of Think-on-Graph. AGR spends more tokens than the
  baseline on both datasets, so it sits to the right; the halving is in
  calls, which the figure does not plot. The header comment of
  `results.tex` now records the geometry.
- **The verification layer sells auditability, not accuracy** (and since
  the September 2026 reframe, the paper is not AGR-led at all). The
  precision column does not move when the layer is removed, so the paper
  must never promise that it does. What it delivers is the output
  contract, at the width the next note states.
- **State the output contract at its real width, which is narrower than
  the phrase.** An earlier version of the note above said "every answer
  arrives with the traversed triples supporting it", and that is the
  overclaim the thesis spends §6.6 withdrawing, propagated here as
  guidance. Two independent bounds, both already in the paper — §3 for
  the first, §7 for the second:
  - **One route of three records evidence.** Traversed adjacency attaches
    the triples; a claim certified by `verify_connection` or by
    entailment is accepted with nothing attached. On the development set
    13 of 80 answers carry no supporting triples, and two of those did
    assert a claim.
  - **The pairing does not survive into the record.** `RunLogger` writes
    `n_supporting_triples`, an integer, and discards the list, so no
    committed artifact in this repository contains a single supporting
    triple — verified across 112,901 run records. A reader can confirm
    the answers came from a system that tracked its evidence; they
    cannot inspect it.

  So write *auditable in the run*, never *auditable* flat, and never
  "every answer". The thesis ranks this its most serious limitation,
  above the underpowered ablations.
- **Report the nulls at the same length as the positive result.** That is
  the methodological argument, not an apology.
- **A near-empty draft reports one overfull `\vbox`.** It is the
  declarations and the bibliography landing on a blank page, and it goes
  away as soon as there are a few pages of prose — verified by padding
  the sections to seven pages: 0 overfull, 0 underfull, 0 warnings of any
  class. Do not go hunting for it while the sections are still stubs, and
  do not "fix" it with `\raggedbottom`, which does nothing here.
- **`\url` needs `xurl`.** The repository URL in the data-availability
  statement has no punctuation where a break is needed, so plain `\url`
  set it 0.68pt overfull — and unlike the `\vbox` above, that one
  survives at any document length. `xurl` loads after `hyperref` and
  lets a URL break anywhere. Removing it today reports an *underfull*
  `\hbox` of badness 2564 rather than the overfull box measured then:
  `\emergencystretch=1em` arrived in between and stretches the line
  instead of letting it overrun. Same defect, and still a diagnostic.
- **`\corref` needs keeping out of the PDF string.** elsarticle hands
  hyperref the raw `\author` and `\title` arguments for the PDF's
  `/Author` and `/Title` fields, so the footnote marker designating the
  corresponding author reached a string that has no footnotes — four
  `Package hyperref Warning: Token not allowed in a PDF string` per
  build. The metadata was correct anyway, because hyperref drops what it
  cannot use, so nothing looked wrong on the page or in the file.
  `\pdfstringdefDisableCommands` in `preamble.tex` blanks the three
  title-block markers while a PDF string is being built and nowhere
  else; the asterisk still marks the author on page 1.
- **`\affiliation` needs a scalable font family.** Under `review`,
  elsarticle asks for a font at an empty size while typesetting the
  address block, and CM has no shape to give it — nine `Font shape …
  size <>` warnings. The class already sets T1 for text — the warnings
  are OT1/cmr, where maths lives — so `lmodern` alone clears all nine.
  Do not remove it.
- **Figure geometry targets the single-column review measure.** Widths
  are `\textwidth`-relative and adapt, but the fixed heights in
  `build_figures.py` assume roughly a 6in measure. A two-column proof is
  a 3.5in column and will need the `paper` target's heights revisited.
