# thesis_presentation

Pre-defense slide decks for the thesis in `thesis_book/`.

| File | What it is |
| --- | --- |
| `pre-defense-0421052099.tex` / `.pdf` | **The deck that is presented.** 22 pages |
| `pre-defense-0421052099-backup.tex` / `.pdf` | Backup slides for questions only. 5 pages |
| `preamble.tex` | Shared preamble — 16:9, 12 pt, palette, styles |
| `content-main.tex` | Title, 20 body slides, closing slide |
| `content-backup.tex` | The 4 backup slides |
| `figures/` | Slide-geometry figures, generated |
| `transcript.md` | Rehearsal script with per-slide timings |
| `transcript.tex` / `.pdf` | Typeset rendering of `transcript.md`, for printing or reading on a second screen |
| `check_slides.py` | Verifies every number in both decks against its source |

## Build

```bash
cd thesis_presentation
latexmk -pdf pre-defense-0421052099.tex
latexmk -pdf pre-defense-0421052099-backup.tex
latexmk -pdf transcript.tex
```

`latexmk -C` cleans. Both slide drivers `\input{preamble}`, so a change to the
look applies to both — edit the preamble and you must rebuild **both** decks.
`transcript.tex` carries its own preamble instead (see below) and is
unaffected by either.

**Only the two `pre-defense-*.tex` files and `transcript.tex` are documents.**
`preamble.tex`, `content-main.tex` and `content-backup.tex` have no
`\begin{document}` and stop with `Emergency stop ... no legal \end found` if
you build them directly. Each carries a `% !TEX root` line so an editor's
build button compiles the right driver instead; `preamble.tex` points at the
main deck, which leaves the backup deck to rebuild by hand. The figures under
`figures/` are generated, so their directive comes from
`scripts/build_figures.py` — editing it into the files themselves would last
until the next regeneration. `transcript.tex` is the odd one out: it is a
plain working document (portrait, article class, no beamer), not a slide, and
it does not `\input{preamble}` — it duplicates the handful of preamble
settings it actually needs (palette, base size, hyphenation list) so that it
still builds standalone if this file is ever the only one that travels,
matching how `thesis_paper` keeps its own copy of shared material rather than
reaching across a directory boundary. Regenerate it by hand after editing
`transcript.md`; there is no automated `.md` → `.tex` build step.
`python scripts/check_tex_roots.py` checks all three modules — this one, the
book, and the paper — and confirms `transcript.tex` is correctly seen as its
own document rather than a fragment.

## Why two documents

The presented deck contains nothing you have to skip past on the day. The
backup slides are a separate PDF you open alongside it and jump into when a
question calls for one; `transcript.md` maps each to the question it answers.
`check_slides.py` fails if a backup slide ever leaks into the presented deck.

Budgeted at 24 min 26 s of speaking against a 25-minute limit; `check_slides.py`
holds that figure to the transcript's own timing table.

## Figures

The three data figures are **generated** into `figures/` by

```bash
python scripts/build_figures.py --target presentation
```

from `results/phase4/thesis_numbers.json` — the same source the thesis reads.
Nothing plotted is transcribed, and `check_slides.py` re-renders all three to
confirm the committed copies are what `build_figures.py` would write today — a
generated file is only current until the JSON moves under it. Running the script with no `--target` emits both
the thesis and the presentation variants.

The two targets exist because a thesis text column and a 16:9 slide are
different shapes: the slide variants are wider relative to their height, stack
the hop tick labels over two lines, drop the redundant *Hop stratum* axis label,
and use a deeper legend offset. Getting that offset wrong prints the legend on
top of the x-axis label, which is what the first version of this deck did.

`fig_claim_path.tex` is hand-drawn and has no slide variant. The presented deck
`\input`s it across the directory boundary, from `thesis_book/figures/`; the
backup deck does not use it at all.

That reach is harmless here — the two modules are always checked out together
— but it does mean `thesis_presentation/` is the one module that will not build
from its own directory alone. `thesis_paper/` was deliberately fixed the other
way: it keeps its own copy, because a manuscript uploaded to a publisher has no
`../thesis_book/`, and `tests/test_paper_self_contained.py` fails if that copy
drifts. Do the same here if this deck ever has to travel on its own.

## Numbers

Numbers appearing as **table text or prose** are transcribed, so they are
checked:

```bash
python thesis_presentation/check_slides.py
```

This binds the figures in **both** decks back to the artifact, code, or thesis
section each came from, and asserts the decks' formatting invariants — 16:9,
12 pt base, nothing in body text below `\small`, both justification hooks. Run
it after editing any table. It exits non-zero on a mismatch, and
`tests/test_slide_numbers.py` runs it, so a red checker fails the suite rather
than waiting to be noticed by whoever remembers.

Sources, not one source: results and rates come from `thesis_numbers.json`;
the tool caps, the budget table and the operation names from `agr/`; the graph
statistics from the thesis's own `tab:graphstats`; the contributions and
limitations from `introduction.tex` and `conclusion.tex`; and the cycle and
node counts from the tikzpicture on the slide itself.

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
- **Watch for the single orphaned word.** Several tables here once ran to two
  lines for the sake of one trailing word. Measure the cells (`\settowidth`)
  and set the column to fit, rather than guessing a width — the deck's 140mm
  text block is the whole budget.
- **Colour is semantic**, and shared with the book: `agrNode` blue for a step
  that does work, `agrSup` green for supported, `agrUns` vermillion for
  unsupported. The series palette is Okabe-Ito, which is colour-blind safe and
  separates by luminance, so the figures survive a greyscale print — the mark
  shapes carry the distinction independently of hue.
- **Watch for overfull boxes.** On a slide an overfull `\vbox` means content
  running off the bottom edge, where a thumbnail will not show it. Both decks
  build with **zero overfull boxes and zero underfull ones above the stated
  badness ceiling**; keep it that way.
- **Read the rendered page, not the log.** Every defect fixed in this deck so
  far — an edge label sitting on top of the box it pointed at, a legend printed
  over an axis label, a table row breaking for one word — is invisible to
  LaTeX and shows up only in a raster. `pdftoppm -png -r 130 <deck>.pdf p`
  after any change to a figure.
