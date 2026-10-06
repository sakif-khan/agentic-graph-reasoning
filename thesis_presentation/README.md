# thesis_presentation

The defense slide deck for the thesis in `thesis_book/`.

| File | What it is |
| --- | --- |
| `thesis_defense_0421052099.tex` / `.pdf` | **The deck.** 38 pages: 32 presented, 6 backup |
| `preamble.tex` | Shared preamble — 16:9, 12 pt, palette, styles |
| `content-main.tex` | Every frame: title, body slides, closing slide, then the backup slides |
| `figures/` | Slide-geometry figures, generated |
| `check_slides.py` | Verifies every number in the deck against its source |
| `transcript.md` | The rehearsal script, timed per slide, with the anticipated questions |
| `transcript-min.tex` / `.pdf` | **The speaking copy.** Each slide's number, title, time and spoken lines, and nothing else |
| `build_min.py` | Generates `transcript-min.tex` from `transcript.md` |
| `pre-defense-frozen-2026-08-29/` | The pre-defense as delivered — its two decks, its rehearsal transcript, and the scripts that built them. Frozen; not expected to build from here. |

## Build

```bash
cd thesis_presentation
latexmk -pdf thesis_defense_0421052099.tex
```

`latexmk -C` cleans.

**Only `thesis_defense_0421052099.tex` is a document.** `preamble.tex` and
`content-main.tex` have no `\begin{document}` and stop with `Emergency stop
... no legal \end found` if you build them directly. Each carries a `% !TEX
root` line so an editor's build button compiles the driver instead. The figures
under `figures/` are generated, so their directive comes from
`scripts/build_figures.py` — editing it into the files themselves would last
until the next regeneration.
`python scripts/check_tex_roots.py` checks all three modules — this one, the
book, and the paper.

## One document, not two

Through the pre-defense this module built two PDFs: a presented deck, and a
separate backup deck opened alongside it and jumped into when a question called
for one. They are one file now — the backup frames are the tail of
`content-main.tex`, after the closing slide, reached by paging past it rather
than by switching windows. `check_slides.py` holds them there: a backup frame
appearing *before* the close is the defect it now looks for.

## The transcript

`transcript.md` is the rehearsal script for this deck: one section per slide,
the speech in quoted lines, a timing table, the backup map, and the
anticipated questions. Every row of the table is what its own words take at the
rate the file states (93 wpm), and `check_slides.py` holds the arithmetic, the
rate, the slide count and roughly fifty claims in the speech to their sources.
It finds a section by the slide title it speaks to and checks that the section
number is that slide's position in the deck, so a reordering of the deck fails
until the script follows.

`transcript-min.pdf` is the speaking copy, the one to hold while presenting.
It carries each slide's number, title and time and the words spoken, and
nothing else from `transcript.md`. No slide's speech is split across two
pages. A slide that will not fit in what is left of a page starts on the next
one, because the document measures each slide's section before placing it.
Rebuild it after any edit to the script:

```bash
cd thesis_presentation
python build_min.py
latexmk -pdf transcript-min.tex
```

`check_slides.py` fails if the copy is out of date. It also reads back the
page each slide's speech starts and ends on (`python build_min.py --pages`),
so a slide split across two pages fails too.

The pre-defense script and its two typeset renderings are in
`pre-defense-frozen-2026-08-29/`, with the `build_transcript.py` and
`build_min.py` that generated them, and those stay frozen there. The full
typeset transcript is not built here, and the checker reports it as not built
rather than stale.

## Figures

The three data figures are **generated** into `figures/` by

```bash
python scripts/build_figures.py --target presentation
```

from `results/phase4/thesis_numbers.json` — the same source the thesis reads.
Nothing plotted is transcribed, and `check_slides.py` re-renders all three to
confirm the committed copies are what `build_figures.py` would write today — a
generated file is only current until the JSON moves under it. Running the
script with no `--target` emits every variant, the thesis's, the deck's and
the paper's. Every run also rewrites the thesis's two generated tables, which
come out unchanged unless the JSON has moved.

The two targets exist because a thesis text column and a 16:9 slide are
different shapes: the slide variants are wider relative to their height, stack
the hop tick labels over two lines, drop the redundant *Hop stratum* axis label,
and use a deeper legend offset. Getting that offset wrong prints the legend on
top of the x-axis label, which is what the first version of this deck did.
The slide variant of the census histogram also names its categories in words,
as the census slide does, where the book and the paper print the schema's
identifiers (`relation_selection`). `check_slides.py` holds the six largest
to the census slide's own names.

Two more settings are the deck's alone. The deck sets two of the figures
inside a box (`\scalebox`, `\resizebox`), where every line end outside the
`tikzpicture` is a word space, so the slide variants end those lines with `%`.
Without that the RQ1 figure sat 10pt right of centre and the census histogram
11pt. And the two-panel figures place their shared legend by `legend_x`,
measured on the slide so the legend is centred under both panels. Both are set
for the presentation target only, and the book's and the paper's files keep
their bytes.

The accuracy-against-cost slide labels its token axis 100, 1,000 and 10,000
rather than as powers of ten, whose exponents printed at 6 pt. That is set on
the slide rather than in `build_figures.py`, so no generated file changes for
it.

The deck draws the claim path itself, on the "One claim, three routes"
slide. The book's `thesis_book/figures/fig_claim_path.tex` is a tall vertical
chain, and scaled into a 16:9 frame its labels printed at 5.2 pt; the slide
lays the same routing out left to right at its own size, where the smallest
label is 10 pt. The two cannot drift: `check_slides.py` reads the book figure
and requires each of its tests, buckets and edge labels, in its words, on the
slide. The module therefore builds from its own directory alone, as `journal/`
does.

## Numbers

Numbers appearing as **table text or prose** are transcribed, so they are
checked:

```bash
python thesis_presentation/check_slides.py
```

This binds the figures in the deck and its transcript back to the artifact,
code, or thesis section each came from, and asserts the deck's formatting
invariants — 16:9,
12 pt base, nothing in body text below `\small`, both justification hooks. Run
it after editing any table. It exits non-zero on a mismatch, and
`tests/test_slide_numbers.py` runs it, so a red checker fails the suite rather
than waiting to be noticed by whoever remembers.

Sources, not one source: results and rates come from `thesis_numbers.json`;
the tool caps, the budget table and the operation names from `agr/`; the graph
statistics from the thesis's own `tab:graphstats`; the contributions and
limitations from `introduction.tex` and `conclusion.tex`; the cycle and node
counts from the tikzpicture on the slide itself; and RoG's published row from
the thesis's `tab:rog`. The RoG slide's third row is AGR's own answers scored
by RoG's released scorer, which finds a gold answer anywhere inside the
predicted text. `scripts/rog_scorer.py` carries that scorer, copied unchanged,
and `build_thesis_numbers.py` writes the result into the JSON's `rog_scorer`
block.

**How a value is matched matters more than whether it is present.** This file
used to claim it bound *every* result, cost, p-value, rate and count. Measured
against a sweep of 25 single-value corruptions, it caught 7. The rest slipped
through for two reasons, both fixed:

- `has()` searched the three source files concatenated, so it asked whether a
  value appeared *anywhere* rather than whether a given cell held it. Any
  figure printed twice was effectively unchecked, and this deck deliberately
  prints several twice — corrupting a headline on a main slide passed because
  a backup slide still carried the same number. Table figures now go through
  `holds()`, scoped to one frame, one row, one column, matching a whole
  number: `0.0` no longer matches inside `40.0`.
- Whole classes were outside its coverage: the graph statistics and import
  time, the tool caps and operation names, the per-category census counts, the
  opening slide's headline figures, the research-question numbering, and the
  entire backup budget table.

The same sweep now catches 25 of 25, and `tests/probes/prove_coverage.py`
keeps it that way.

It also reads the build logs, if they are there, and requires **zero warnings
of any class** — not just `LaTeX Warning`. Grepping for that one string is how
a `Package hyperref Warning` about `\quad` reaching the PDF metadata survived
two rounds of builds described as clean.

## Editing notes

- **Font size is uniform.** `check_slides.py` fails if body text drops below
  `\small`. Sizes inside a TikZ `font=` declaration are diagram labels and are
  exempt.
- **Body text is justified**, and it takes two hooks, both checked. Prose,
  columns and lists reach ragged right through `\raggedright`, so the preamble
  repoints that command. A block body does not: it is a `beamercolorbox`, and
  `beamercolorbox` assigns `\rightskip` from its own key, so the block template
  gets its own `\justifying`. Table cells stay **ragged** — the `L` column type
  is bound to the original command first, because justification spaces badly on
  a 40mm measure.
- **Loose lines are bounded, not banished.** A 65mm column at 11pt runs about
  38 characters, so justification has to buy its flush edge with either a
  hyphen or a wide word space. `\hbadness=2000` names the accepted ceiling;
  anything looser still reports in the log and still has to be fixed. Names
  (WebQSP, GraphRAG, …) are in a `\hyphenation` list and are never broken.
- **No em-dashes and no colon explanations in slide text**, the rule the book
  follows: a thought that needs a dash is two sentences. Colons stay where
  they introduce a list or follow a bold or alert label.
- **Lists in narrow columns are set ragged.** Beamer's list code re-issues
  `\raggedright`, which the preamble repoints at `\justifying`, so a list is
  justified unless the column says `\let\raggedright\agrraggedright`. At a
  60mm measure justified items hyphenated words and spread short ones.
- **Watch for the single orphaned word.** Several tables here once ran to two
  lines for the sake of one trailing word. Measure the cells (`\settowidth`)
  and set the column to fit, rather than guessing a width — the deck's 140mm
  text block is the whole budget.
- **Colour is semantic**, and shared with the book: `agrNode` blue for a step
  that does work, `agrSup` green for supported, `agrUns` vermillion for
  unsupported. The series palette is Okabe-Ito, which is colour-blind safe and
  separates by luminance, so the figures survive a greyscale print — the mark
  shapes carry the distinction independently of hue.
- **The research-question slides are the one exception to the title size.**
  Slides 19 to 26 are each titled with their question exactly as the book's
  `sec:rqs` words it, on one line, and what that slide answers is its
  subtitle. A question is set smaller only if it would otherwise wrap, and
  only as far as one line needs. RQ3 fits at `\large` and keeps it. RQ1 is
  set at 14pt and RQ2 at 11.6pt, each by a group around that question's
  slides: `{\rqtitlesize{...}` before the first and `}` after the last. Keep
  the closing braces where they are. A frame option cannot carry the size,
  because beamer applies frame options outside the frame and the size leaked
  into every later frame. `check_slides.py` holds the questions to the book
  (slide 8 and every question title) and reads the built titles: each
  question on one line, at full size wherever it fits, and every other title
  at full size.
- **Centred means centred on the page, and it is measured.** The takeaway bar
  spans the text block, 1cm in from each edge. A rounded beamer box draws its
  background 4bp outside the box on either side, which `\takeaway` allows
  for. Until October 2026 the bar sat 5pt left of centre on every slide. Each
  generated figure is centred on its slide, and the shared legends are
  centred under both panels. Vertically, every slide's body sits midway
  between the header and the foot (the takeaway bar, the `\sinkfoot` line, or
  the frame number). The gap runs from the header's last baseline to the
  body's first ink, and from the body's last baseline to the foot. A table, a
  list or a block brings space of its own above or below it, so a slide that
  starts or ends with one carries `\bodyshift{<len>}` at the head of its
  frame, measured to put it back. `check_slides.py` renders the pages and
  fails a bar off the text block, a figure or legend off centre, or a body
  more than 1pt from midway. That failure prints both gaps. To balance the
  slide, add half of (the gap over the foot minus the gap under the header)
  to its `\bodyshift`.
- **Every titled frame ends in `\takeaway`, `\sinkfoot` or `\centrebody`.**
  The preamble puts stretchable glue under every frame title so that a thin
  slide settles midway, and that needs a matching stretch at the foot. Without
  one the body sinks to the floor, as four backup slides did until October
  2026. `check_slides.py` fails on a titled frame that has none of the three.
- **Watch for overfull boxes.** On a slide an overfull `\vbox` means content
  running off the bottom edge, where a thumbnail will not show it. The deck
  builds with **zero overfull boxes and zero underfull ones above the stated
  badness ceiling**; keep it that way.
- **Read the rendered page, not the log.** Every defect fixed in this deck so
  far — an edge label sitting on top of the box it pointed at, a legend printed
  over an axis label, a table row breaking for one word — is invisible to
  LaTeX and shows up only in a raster. `pdftoppm -png -r 130 <deck>.pdf p`
  after any change to a figure.
