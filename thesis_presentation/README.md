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
| `check_slides.py` | Verifies every number in both decks against its source |

## Build

```bash
cd thesis_presentation
latexmk -pdf pre-defense-0421052099.tex
latexmk -pdf pre-defense-0421052099-backup.tex
```

`latexmk -C` cleans. Both drivers `\input{preamble}`, so a change to the look
applies to both.

## Why two documents

The presented deck contains nothing you have to skip past on the day. The
backup slides are a separate PDF you open alongside it and jump into when a
question calls for one; `transcript.md` maps each to the question it answers.
`check_slides.py` fails if a backup slide ever leaks into the presented deck.

Budgeted at 22 min 30 s of speaking against a 25-minute limit.

## Figures

The three data figures are **generated** into `figures/` by

```bash
python scripts/build_figures.py --target presentation
```

from `results/phase4/thesis_numbers.json` — the same source the thesis reads.
Nothing plotted is transcribed. Running the script with no `--target` emits both
the thesis and the presentation variants.

The two targets exist because a thesis text column and a 16:9 slide are
different shapes: the slide variants are wider relative to their height, stack
the hop tick labels over two lines, drop the redundant *Hop stratum* axis label,
and use a deeper legend offset. Getting that offset wrong prints the legend on
top of the x-axis label, which is what the first version of this deck did.

`fig_claim_path.tex` is hand-drawn and has no slide variant, so both documents
`\input` it from `thesis_book/figures/`.

## Numbers

Numbers appearing as **table text or prose** are transcribed, so they are
checked:

```bash
python thesis_presentation/check_slides.py
```

This binds every result, cost, p-value, rate, and count in **both** decks back
to `thesis_numbers.json`, and asserts the decks' formatting invariants — 16:9,
12 pt base, nothing in body text below `\small`, figures generated rather than
hand-edited. Run it after editing any table. It exits non-zero on a mismatch.

## Editing notes

- **Font size is uniform.** `check_slides.py` fails if body text drops below
  `\small`. Sizes inside a TikZ `font=` declaration are diagram labels and are
  exempt.
- **Colour is semantic**, and shared with the book: `agrNode` blue for a step
  that does work, `agrSup` green for supported, `agrUns` vermillion for
  unsupported. The series palette is Okabe-Ito, which is colour-blind safe and
  separates by luminance, so the figures survive a greyscale print — the mark
  shapes carry the distinction independently of hue.
- **Watch for overfull boxes.** On a slide an overfull `\vbox` means content
  running off the bottom edge, where a thumbnail will not show it. Both decks
  build with zero bad boxes; keep it that way.
