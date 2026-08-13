# thesis_presentation

Pre-defense slide deck for the thesis in `thesis_book/`.

| File | What it is |
| --- | --- |
| `presentation.tex` | Beamer source, 16:9, 12 pt uniform |
| `presentation.pdf` | Built deck — 26 pages |
| `transcript.md` | Rehearsal script with per-slide timings |
| `check_slides.py` | Verifies every number in the deck against its source |

## Build

```bash
cd thesis_presentation
latexmk -pdf presentation.tex
```

Requires the same TeX installation as the thesis. `latexmk -C` cleans.

## Structure

26 pages: title, **20 body slides**, a closing slide, and 4 backup slides. The
backup slides are not presented — they are there to jump to during questions.
`transcript.md` maps each one to the question it answers.

Budgeted at 22 min 30 s of speaking against a 25-minute limit.

## Where the numbers come from

The four figures are `\input` directly from `../thesis_book/figures/`, which
`scripts/build_figures.py` generates from `results/phase4/thesis_numbers.json`.
Nothing plotted is transcribed, and the deck cannot drift from the thesis
without the build breaking.

Numbers that appear as **table text or prose** are transcribed, so they are
checked instead:

```bash
python thesis_presentation/check_slides.py
```

This binds every result, cost, p-value, rate, and count in the deck back to
`thesis_numbers.json`, and also asserts the deck's own formatting invariants —
16:9, 12 pt base, nothing in body text smaller than `\small`. Run it after
editing any table. It exits non-zero on a mismatch.

## Editing notes

- **Font size is uniform.** `check_slides.py` fails the build if any body text
  drops below `\small`. Sizes inside a TikZ `font=` declaration are diagram
  labels and are exempt.
- **The plot style is redefined here.** `agrplot` in the preamble sets a smaller
  `width`/`height` than `buetcsepgthesis.sty` does, because the thesis sizes
  those figures for a text column and they overflow a 16:9 slide. Sizing them
  natively is better than wrapping in `\resizebox`, which would scale the tick
  and label fonts down with the plot.
- **Watch for overfull boxes.** On a slide an overfull `\vbox` means content
  running off the bottom edge, where you will not see it in a thumbnail. The
  deck currently builds with zero bad boxes; keep it that way.
