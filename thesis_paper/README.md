# thesis_paper

Journal manuscript drawn from `thesis_book/`. Target: Elsevier —
*Knowledge-Based Systems* or *Information Processing & Management*.

| File | What it is |
| --- | --- |
| `agr-paper.tex` | **The document.** `elsarticle`, `preprint,review,12pt` |
| `preamble.tex` | Fonts, figure toolchain, palette, system-name macros |
| `sections/*.tex` | Nine sections. Undrafted ones carry their source chapter and word budget as comments |
| `figures/` | Generated. Do not edit |
| `highlights.txt` | Elsevier highlights, submitted as a separate file |

## Build

```bash
cd thesis_paper
latexmk -pdf agr-paper.tex
```

`review` gives the 1.5-spaced single column Elsevier wants for peer
review — all the option does is set the baseline stretch.

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
  directly, and `elsevier.com`, which 301s there. A journal may add its
  own requirement. If you can open that page in a browser, check it and
  replace this paragraph with what it says.
- An earlier version of this note claimed Editorial Manager builds the
  reviewer PDF itself. That may well be true, but it was never verified
  either, so it is gone rather than repeated.

If a checklist does ask for line numbers, it is two lines:
`\usepackage{lineno}` in `preamble.tex`, and `\linenumbers` *after*
`\end{frontmatter}` in `agr-paper.tex` — never in the preamble, which
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

Only `agr-paper.tex` is a document. `preamble.tex`, the nine sections
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

What gets uploaded is `thesis_paper/` and nothing above it, so the
manuscript must build with no parent directory present. It did not,
until this was fixed: `\bibliography` and one `\input` reached into
`../thesis_book/`, which resolved perfectly here and would have failed
at the publisher. Both are now local copies:

| file | copied from | differs by |
| --- | --- | --- |
| `agr-paper.bib` | `thesis_book/buetcsepgthesis.bib` | nothing |
| `figures/fig_claim_path.tex` | `thesis_book/figures/fig_claim_path.tex` | its `% !TEX root` line |

A copy is a thing that drifts, which is the same hazard the two
bibliographies already have a test for. `tests/test_paper_self_contained.py`
pins both against their originals, fails if any source names a path
outside `thesis_paper/`, and fails if an `\input` names a file that is
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

## Editing notes

- **AGR-led framing, but the verification layer sells auditability, not
  accuracy.** The precision column does not move when the layer is
  removed, so the paper must never promise that it does. What it delivers
  is the output contract: every answer arrives with the traversed triples
  supporting it. Claiming that, and only that, is what keeps
  §6 from reading as a retraction.
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
  lets a URL break anywhere.
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
