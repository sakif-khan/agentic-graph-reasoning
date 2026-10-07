"""Prove the rules added after the October 2026 review of the deck fire.

The review read the deck against the book and found defects that
check_slides.py had passed: every one of them shipped. Each case below
reinstates one, verbatim where the old wording survives in git, and asserts
the checker now fails on it.

  1-2  RoG's training splits as 2,830 and 16,900, on the backup slide and in
       the spoken answer. The thesis says 2,826 and 27,639.
  3    The defect breakdown as "17 found inside the census, 1 counted in
       both". The JSON says 16 and none; "16" was matched inside "16.5%".
  4    "All 256" over a census column summing to 220.
  5-6  The Backtracker as an undo, on the slide and in the script. The
       thesis says popping the most recent snapshot "would make
       backtracking a simple undo", and it pops the highest-scoring one.
  7-8  The worked example's counter printed as a count rather than a bound,
       and one relation "taken" where each Explorer pass kept three.
  9    A McNemar bound read off the book's rounded figure, which the largest
       p exceeds by 0.00002.
  10   A slide inserted ahead of the results while the script keeps its
       numbering: the rehearsal and the deck come apart.
  11   The dashed panel explained with the wrong n.

The second pass, after the first round of fixes was swept again:

  12   A backup frame with nothing to balance the glue under its title, so
       its body sinks to the floor. "Which budgets actually bind" shipped
       82pt under its title and 2pt above the page number.
  13   The backup census histogram on the schema's identifiers
       (relation_selection) beside a census slide that names them in words.
       The generator is changed with the figure, so the figure is still
       current and only the naming rule can catch it.
  14   A slide's speech split across two pages of the speaking copy, read
       from the page labels its build wrote. The .aux is a build product,
       so this case is skipped, visibly, where the copy has not been built.

The third pass made the research questions the book's, word for word:

  15   Slide 8's RQ1 carrying sec:rqs's elaboration, "and does the
       advantage grow with hop count", as if it were the question.
  16   A slide that answers a question titled with its own heading instead,
       as slide 23 was, which leaves a gap in the run of question slides.
  17   A question slide whose title paraphrases its question, as slide 25's
       "RQ3: One effect, and its sign is backwards" did.

The rules on the built titles (each question on one line, and only the
questions set small) need a rebuilt deck to reinstate, so they were proved
once instead, on 2026-10-06, against two defective builds: the questions at
full size failed the one-line rule on all six RQ1 and RQ2 slides, and a
group closed one slide late failed the size rule on the census slide.

The fourth pass centred what was off centre:

  18   The deck's figures back on their word spaces. The generator writes
       the slide variants without the % that ends each line outside the
       picture, and the figures are regenerated with it, so they still
       match the generator and only the word-space rule can catch it. In a
       box those spaces set the RQ1 figure 10pt right of centre.

The fifth pass made the RoG comparison a presented slide, after the main
results, and added the two differences the book had not named: RoG searches
each question's own subgraph, and its released scorer finds a gold answer
anywhere inside the predicted text. AGR scored RoG's way moves by under a
point, a figure the slide, the book and the paper now state.

  19   Slide 7's sentence as it shipped: published Hits@1 not comparable
       "because of other backbones, subsets and full Freebase". RoG
       searched the subgraphs this thesis's graph is built from.
  20   The book adding its two differences and still counting three.
  21   The slide's RoG-scored row drifting from the JSON.
  22   The slide no longer saying the scorer moves AGR under a point.
  23   The slide dropping the search-space difference.
  24   The book quoting a RoG-scored figure wrongly.
  25   The book's specimen a question RoG's scorer did not change.
  26   The comparison back among the backup slides, titled as it is now.
       (Since 2026-10-07 the backups are their own file, and the case
       moves the frame into it.)

The fourth pass's page rules need a rebuilt deck too, and were proved once
on 2026-10-06, each against its own defective build. The takeaway bar's
old geometry (\\textwidth less 3.6mm, unmoved) failed the bar rule, slide 2
first at 24.35pt from the left and 34.55pt from the right. The old legend
position (1.08) failed the legend rule on slides 18 and 35, by 2.9pt and
4.5pt. The word spaces back failed the centring rule on slides 18 and 34
(+10.1pt, +10.7pt) and on 35 (-2.4pt, from the one space after the picture),
besides the word-space rule on all three files. RQ3 set small failed the
size rule, and the balance rule on slide 24. Slide 30 without its
\\bodyshift failed the balance rule, at 12.9pt under its header against
21.8pt over its foot.

Every file is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
DECK = ROOT / "thesis_presentation" / "content-main.tex"
# The backup slides, a deck of their own since 2026-10-07.
BACKUP = ROOT / "thesis_presentation" / "content-backup.tex"
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"
BUILD = ROOT / "scripts" / "build_figures.py"
HIST = ROOT / "thesis_presentation" / "figures" / "fig_failure_histogram.tex"
HOP = ROOT / "thesis_presentation" / "figures" / "fig_hop_strata.tex"
ACC = ROOT / "thesis_presentation" / "figures" / "fig_accuracy_cost.tex"
BOOK = ROOT / "thesis_book" / "chapters" / "evaluation.tex"
AUX = ROOT / "thesis_presentation" / "transcript-min.aux"

FILES = (DECK, BACKUP, SCRIPT, BUILD, HIST, HOP, ACC, BOOK) + (
    (AUX,) if AUX.exists() else ())
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0] if fail else r.stdout.strip()[-90:])


def edit(path, old, new):
    """Substitute, tolerating rewrap and the transcript's '>' markers."""
    def go():
        gap = r"\s+(?:>\s*)?"
        pattern = re.compile(gap.join(re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


# The deck's histogram, regenerated by the generator as it stands on disk.
REGEN = ("import sys; sys.path.insert(0, 'scripts'); "
         "import build_figures as BF; c = BF.TARGETS['presentation']; "
         "(c['outdir'] / 'fig_failure_histogram.tex').write_text("
         "BF.failure_histogram(BF.load(), c), encoding='utf-8', "
         "newline='\\n')")


def identifiers():
    """The deck's histogram back on identifiers, generator and figure both."""
    new = orig[BUILD].replace("hist_prose=True,", "hist_prose=False,", 1)
    assert new != orig[BUILD], "anchor gone in build_figures.py"
    io.open(BUILD, "w", encoding="utf-8", newline="").write(new)
    subprocess.run([sys.executable, "-c", REGEN], cwd=ROOT, check=True)


# All three of the deck's figures, regenerated the same way.
REGEN_ALL = ("import sys; sys.path.insert(0, 'scripts'); "
             "import build_figures as BF; c = BF.TARGETS['presentation']; "
             "d = BF.load(); "
             "[(c['outdir'] / (n + '.tex')).write_text(f(d, c), "
             "encoding='utf-8', newline='\\n') for n, f in ("
             "('fig_accuracy_cost', BF.accuracy_cost), "
             "('fig_hop_strata', BF.hop_strata), "
             "('fig_failure_histogram', BF.failure_histogram))]")


def word_spaces():
    """The deck's figures without their %s, generator and figures both."""
    new = orig[BUILD].replace("in_box=True,", "in_box=False,", 1)
    assert new != orig[BUILD], "anchor gone in build_figures.py"
    io.open(BUILD, "w", encoding="utf-8", newline="").write(new)
    subprocess.run([sys.executable, "-c", REGEN_ALL], cwd=ROOT, check=True)


def back_to_backup():
    """The RoG frame moved back among the backup slides, title unchanged.

    The backup slides are their own file since 2026-10-07, so the frame
    leaves the presented deck and lands in content-backup.tex, where it
    stood before the proposal frame while the backups were the deck's tail.
    """
    start = orig[DECK].index("% The board asked for this at the pre-defense")
    start = orig[DECK].rindex("% =====", 0, start)
    end = orig[DECK].index("\\end{frame}\n",
                           orig[DECK].index("\\begin{frame}{AGR against RoG}"))
    end += len("\\end{frame}\n")
    io.open(DECK, "w", encoding="utf-8", newline="").write(
        orig[DECK][:start] + orig[DECK][end:])
    at = orig[BACKUP].index("% Four departures from the approved proposal")
    io.open(BACKUP, "w", encoding="utf-8", newline="").write(
        orig[BACKUP][:at] + orig[DECK][start:end] + "\n" + orig[BACKUP][at:])


def split_speech():
    """Slide 17's speech ending a page after the page it starts on."""
    m = re.search(r"\\newlabel\{e-17\}\{\{[^{}]*\}\{(\d+)\}", orig[AUX])
    assert m, "no label e-17 in transcript-min.aux"
    io.open(AUX, "w", encoding="utf-8", newline="").write(
        orig[AUX][:m.start(1)] + str(int(m.group(1)) + 1)
        + orig[AUX][m.end(1):])


CASES = [
    ("shipped: RoG's training splits as 2,830 and 16,900 on the slide",
     edit(DECK, r"$2{,}826$ and $27{,}639$ questions",
          r"$2{,}830$ and $16{,}900$ questions")),
    ("shipped: the same two sizes in the spoken answer",
     edit(SCRIPT, "2,826 WebQSP and 27,639 CWQ questions",
          "2,830 WebQSP and 16,900 CWQ questions")),
    ("shipped: 17 inside the census, 1 counted in both",
     edit(BACKUP, r"\item $16$ more found inside it, as gold-noise or "
                r"ambiguous rows \item No question counted in both",
          r"\item $17$ found inside the census \item $1$ counted in both")),
    ("shipped: All 256 over a column summing to 220",
     edit(DECK, r"\midrule Six smaller categories & 36 \\", "")),
    ("shipped: the slide calls the Backtracker an undo",
     edit(DECK, r"\textbf{Backtracker}: best earlier frontier, ban list",
          r"\textbf{Backtracker}: undo + ban list")),
    ("shipped: the script says it undoes a bad expansion",
     edit(SCRIPT, "The backtracker returns to the best-scoring earlier "
                  "frontier and bans the edges that failed.",
          "The backtracker undoes a bad expansion and bans the edge that "
          "caused it.")),
    ("shipped: the counter printed as a count of triples",
     edit(DECK, r"at most $18$ supporting triples",
          r"$18$ supporting triples")),
    ("shipped: one relation taken where three were kept",
     edit(DECK, r"keeps three relations. The best is\\",
          r"scores relations, takes\\")),
    ("a significance bound read off a rounded figure",
     edit(DECK, r"($p < 0.004$)", r"($p \leq 0.0035$)")),
    # The inserted frame carries its \centrebody, or the frame-balance rule
    # catches it first and this case stops testing the renumbering.
    ("a slide inserted before the results, the script not renumbered",
     edit(DECK, r"\begin{frame}{Main results}",
          "\\begin{frame}{An inserted slide}\n\\centrebody\n\\end{frame}\n"
          r"\begin{frame}{Main results}")),
    ("the dashed panel explained with the wrong n",
     edit(DECK, r"WebQSP is dashed ($n{=}4$ at 3+).",
          r"WebQSP is dashed ($n{=}5$ at 3+).")),
    ("shipped: a backup frame with no glue to balance its title's",
     edit(BACKUP, r"Think-on-Graph a meaningful comparison.\par} \centrebody",
          r"Think-on-Graph a meaningful comparison.\par}")),
    ("shipped: the census histogram on the schema's identifiers",
     identifiers),
    ("shipped: slide 8's RQ1 carrying the elaboration as the question",
     edit(DECK, r"\item[\textbf{RQ1}] Does agentic navigation improve "
                r"\alert{multi-hop} factual accuracy?",
          r"\item[\textbf{RQ1}] Does agentic navigation improve multi-hop "
          r"factual accuracy, and does the advantage \alert{grow with hop "
          r"count}?")),
    ("shipped: an answering slide titled with its own heading",
     edit(DECK, r"\begin{frame}{RQ2: What does pre-generation verification "
                r"contribute beyond graph navigation?}{Does it just refuse "
                r"more often?}",
          r"\begin{frame}{Does it just refuse more often?}")),
    ("shipped: a question slide titled with a paraphrase of its question",
     edit(DECK, r"\begin{frame}{RQ3: Which components contribute what, at "
                r"what token cost?}{One effect, and its sign is backwards}",
          r"\begin{frame}{RQ3: One effect, and its sign is backwards}"
          r"{One effect, and its sign is backwards}")),
    ("shipped: the deck's figures on their word spaces", word_spaces),
    ("shipped: slide 7 gives RoG the full Freebase as its reason",
     edit(DECK, "comparable. RoG is fine-tuned on these benchmarks, and the "
                "others search the full Freebase with other backbones.",
          "comparable, because of other backbones, subsets and full "
          "Freebase.")),
    ("the book adds two differences and still counts three",
     edit(BOOK, "Five differences bound what", "Three differences bound what")),
    ("the RoG slide's RoG-scored row drifts from the JSON",
     edit(DECK, r"\quad scored by RoG's code & $76.0$",
          r"\quad scored by RoG's code & $77.0$")),
    ("the RoG slide stops saying the scorer moves AGR under a point",
     edit(DECK, "Scored by RoG's own code, AGR moves by under a point.", "")),
    ("the RoG slide drops the search-space difference",
     edit(DECK, r"And RoG searches each question's \alert{own subgraph}, "
                r"where AGR searches the union of them all.", "")),
    ("the book quotes a RoG-scored figure wrongly",
     edit(BOOK, "AGR's figures become $76.0$ and $64.9$ on WebQSP",
          "AGR's figures become $76.5$ and $64.9$ on WebQSP")),
    ("the book's specimen is a question RoG's scorer did not change",
     edit(BOOK, "``Kingdom of Denmark'' against the gold ``Denmark''",
          "``Kingdom of Sweden'' against the gold ``Sweden''")),
    ("the RoG comparison back in the backup tail", back_to_backup),
]
if AUX.exists():
    CASES.append(("a slide's speech split across two pages of the "
                  "speaking copy", split_speech))
else:
    print("SKIP     a slide's speech split across two pages: no "
          "transcript-min.aux here, build the speaking copy first")

rc, first = run()
assert rc == 0, f"not clean before the probe: {first}"

out = []
try:
    for name, mutate in CASES:
        mutate()
        rc, first = run()
        out.append((name, rc, first))
        restore()
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    print(f"{'':9s}{first[:96]}")

rc, first = run()
print(f"\nrestored -> rc={rc}  ({first[:70]})")
passed = all(rc for _, rc, _ in out) and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
