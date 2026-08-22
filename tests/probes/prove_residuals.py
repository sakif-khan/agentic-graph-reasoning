"""Prove the four residuals are held, and by what.

Case 1 reinstates the thesis caption verbatim -- "Two cycles exist ...
Both are bounded" -- beside a figure whose own source comments call the
third arrow a cycle. Cases 2 and 3 do the same to the paper, which said
"with two cycles" in the body and "Both cycles are bounded" in the
caption. Correcting the deck alone in an earlier round had made the deck
the outlier against the two documents it is drawn from.

Case 4 swaps the deck's limitations 4 and 5 back. Presence was checked
and order was not, past the first item, while the slide's own comment
claimed the thesis's severity order.

Case 5 removes the sentence accounting for "pre-specified" on the one
slide whose premise is that the six contributions are the thesis's, in
its order -- a rigour point that reads as a discrepancy unspoken.

Cases 6-12 are the hop curve, which was the last transcription in this
material bound to nothing: 0.46/0.55/0.57 could become 0.96/0.95/0.97
with the whole suite still green, and the shape claims around it were
assertions about four other systems that no rule read.

Cases 13-17 are the two limitations that reached neither document.
Two of them move sources rather than prose: config.py's
use_gold_entities, whose being on is the answer's whole premise, and one
label sheet, which is where the nine instances are counted.

Case 18 gives slide 19 back the seventy-five seconds it shipped with,
against 156 words -- 125 wpm on a script that states 93. It is the only
case here that has to repair the document as it corrupts it: the
cumulative column, the headings and the budget line all agreed with that
table, and without repairing them the probe would prove one of those
three rules instead of the achievability rule it is for.

Cases 19-21 are three rules that could not fail. "Nine of the 38" was
guarded on its digits and not on its number word, so Nineteen passed.
Contribution 6 was allowed either spelling, and the rule that explains
the divergence keyed off the deck -- so a slide drifting back to
"pre-registered" also switched off its own guard. And the entity-linking
answer grouped two systems as "the static baselines" while naming Static
GraphRAG two clauses earlier as one of the three that do seed.

The caps case has a twin on the script, section 6, which said "four
operations with fixed signatures and hard caps" one round longer than
the card did. Removing three words fixed it and the timing table did not
move, because the achievability rule only flags rows SHORT of their word
count.

Cases 22-24 revert three wordings on the event card, each of which was
corrected with nothing behind it. Its numbers are generated and cannot
drift; these were typed. "Gold labels were wrong" is untrue of the 22
ambiguous questions among the 57; "4 tools with hard caps" is untrue of
verify_connection and search_entity; and hedge_pct is a share of
questions, which makes "of answers" contradict itself, since a hedge is
not an answer.

Every file is restored in a finally block.
"""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
BOOK = ROOT / "thesis_book" / "chapters" / "framework.tex"
PAPER = ROOT / "thesis_paper" / "sections" / "framework.tex"
DECK = ROOT / "thesis_presentation" / "content-main.tex"
SCRIPT = ROOT / "thesis_presentation" / "transcript.md"
CFG = ROOT / "agr" / "config.py"
CARD = ROOT / "thumbnail" / "thumbnail.tex"
SHEET = ROOT / "results" / "phase4" / "labels_webqsp.csv"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (BOOK, PAPER, DECK, SCRIPT, CFG, SHEET, CARD)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0][:88] if fail else "")


def edit(path, old, new):
    """Rewrite one passage, tolerating rewrap and blockquote markers.

    An anchor that spans a line break must not carry the wrapping with
    it, and in the script every continuation line opens with "> ".
    """
    def go():
        pattern = re.compile(r"\s+(?:>\s*)?".join(
            re.escape(w) for w in old.split()))
        assert pattern.search(orig[path]), f"anchor gone in {path.name}: {old[:60]!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            pattern.sub(lambda _: new, orig[path], count=1))
    return go


def retime_row(n, secs):
    """Put one row's allocation back, repairing everything derived from it.

    The shipped table gave slide 19 seventy-five seconds for 156 words,
    which is 125 wpm against a script that states 93. Every other rule
    about this table passed on that: the cumulative column summed, the
    headings agreed, the budget line matched the total, and the total fit
    the limit. So the corruption has to repair all four, or the probe
    proves one of those rules instead of the one being tested.
    """
    def go():
        md = orig[SCRIPT]
        rows = re.findall(
            r"^\| (\d+) \| ([^|]*?) \| (\d+):(\d\d) \| (\d+):(\d\d) \|",
            md, re.M)
        assert rows, "no timing table"
        alloc = {int(r[0]): int(r[2]) * 60 + int(r[3]) for r in rows}
        assert alloc[n] != secs, "the corruption is a no-op"
        alloc[n] = secs

        def mmss(s):
            return f"{s // 60}:{s % 60:02d}"

        run, lines = 0, []
        for r in rows:
            run += alloc[int(r[0])]
            lines.append(f"| {r[0]} | {r[1]} | {mmss(alloc[int(r[0])])} "
                         f"| {mmss(run)} |")
        old = "\n".join(f"| {r[0]} | {r[1]} | {r[2]}:{r[3]} | {r[4]}:{r[5]} |"
                        for r in rows)
        assert old in md, "the table is not laid out as expected"
        md = md.replace(old, "\n".join(lines))
        md = re.sub(r"^## (\d+) — (.*?)\*\(\d+:\d\d\)\*",
                    lambda m: f"## {m.group(1)} — {m.group(2)}"
                              f"*({mmss(alloc[int(m.group(1))])})*",
                    md, flags=re.M)
        md = re.sub(r"\*\*Budget: \d+ min \d+ s of speaking",
                    f"**Budget: {run // 60} min {run % 60} s of speaking", md,
                    count=1)
        io.open(SCRIPT, "w", encoding="utf-8", newline="").write(md)
    return go


def drop_subtype():
    """Take one instance out of the census the answer counts from.

    The nine is read from the label sheets, not from the prose, so
    relabelling one row has to break the answer.
    """
    def go():
        s = orig[SHEET]
        assert s.count(",extraction_bug,") > 1
        io.open(SHEET, "w", encoding="utf-8", newline="").write(
            s.replace(",extraction_bug,", ",,", 1))
    return go


CASES = [
    # ---- the cycle count, in the two documents that still said two ----
    ("shipped: the thesis caption says two cycles", edit(
        BOOK,
        "The AGR state machine. Three cycles exist: the dashed region marks "
        "the Explorer\\,$\\leftrightarrow$\\,Evaluator search loop; "
        "Evaluator\\,$\\rightarrow$\\,Backtracker\\,$\\rightarrow$\\,Explorer "
        "restores an earlier frontier; and "
        "Verifier\\,$\\rightarrow$\\,Explorer is verification-driven "
        "re-exploration. All three are bounded",
        "The AGR state machine. Two cycles exist: the dashed region marks the\n"
        "    Explorer\\,$\\leftrightarrow$\\,Evaluator search loop, and\n"
        "    Verifier\\,$\\rightarrow$\\,Explorer is verification-driven "
        "re-exploration.\n    Both are bounded")),
    ("shipped: the paper's body says two cycles",
     edit(PAPER, "shared typed state, with three cycles.",
          "shared typed state, with two cycles.")),
    ("shipped: the paper's caption says both cycles", edit(
        PAPER,
        "Evaluator $\\rightarrow$ Backtracker $\\rightarrow$ Explorer restores "
        "an earlier frontier; Verifier $\\rightarrow$ Explorer is "
        "verification-driven re-exploration. All three cycles are bounded",
        "Verifier $\\rightarrow$ Explorer is verification-driven\n"
        "    re-exploration. Both cycles are bounded")),

    # ---- the limitations, in the thesis's severity order ----
    ("shipped: the deck's limitations 4 and 5 are swapped", edit(
        DECK,
        "\\item One environment, one backbone, one annotator "
        "\\item ToG leads where it finishes, from a \\alert{narrower "
        "candidate set}: $40$/$20$ vs $300$/$200$",
        "\\item ToG leads where it finishes, from a \\alert{narrower\n"
        "          candidate set}: $40$/$20$ vs $300$/$200$\n"
        "        \\item One environment, one backbone, one annotator")),

    # ---- the wording divergence ----
    ("shipped: nothing says why the slide diverges on pre-specified", edit(
        SCRIPT,
        "> The sixth is worded *pre-registered* in the thesis; nothing was "
        "filed with a registry, so I say *pre-specified*.\n>\n",
        "")),

    # ---- the hop curve ----
    ("the slide's AGR curve is corrupted",
     edit(DECK, "$0.46 \\to 0.55 \\to 0.57$", "$0.96 \\to 0.95 \\to 0.97$")),
    ("the script's AGR curve is corrupted",
     edit(SCRIPT, "AGR goes 0.46, 0.55, 0.57 as",
          "AGR goes 0.96, 0.95, 0.97 as")),
    ("the slide drops the ends-above claim",
     edit(DECK, "that ends above where it started",
          "that ends above where it began")),
    ("the script drops the ends-above claim",
     edit(SCRIPT, "It is the only system on that dataset that ends above "
                  "where it started.",
          "It is the strongest system on that dataset.")),
    ("the slide miscounts the systems that decay",
     edit(DECK, "Three of the other four decay",
          "Two of the other four decay")),
    ("the script miscounts the systems that decay",
     edit(SCRIPT, "Three of the other four decay monotonically",
          "Three of the other three decay monotonically")),
    ("ToG's shortfall is misquoted",
     edit(SCRIPT, "still 0.08 below its own one-hop score",
          "still 0.18 below its own one-hop score")),

    # ---- limitations 7 and 8 ----
    ("shipped: no answer on where topic entities come from", edit(
        SCRIPT,
        "**\"Where do the topic entities come from",
        "**\"Where do the tropic entities come from")),
    ("the entity-linking answer overclaims which systems share it", edit(
        SCRIPT,
        "The three systems that touch the graph \u2014 AGR, Think-on-Graph and "
        "GraphRAG \u2014 all seed from the same annotated mentions, and neither "
        "the parametric control nor Vector-RAG ever sees them.",
        "All five systems seed from the same annotated mentions.")),
    ("the gold-entity flag is turned off under the answer",
     edit(CFG, "use_gold_entities: bool = True",
          "use_gold_entities: bool = False")),
    ("shipped: no answer on the extraction bug", edit(
        SCRIPT, "**\"Nine of your failures are one bug.",
        "**\"Nine of your setbacks are one bug.")),
    ("the extraction bug is quoted against the wrong denominator",
     edit(SCRIPT, "Nine of the 38 `decomposition_error` cases",
          "Nine of the 17 `decomposition_error` cases")),
        ("a labelled instance is taken out of the census", drop_subtype()),

    # ---- the table said 24:26 while the words said 24:50 ----
    ("shipped: slide 19 gets 75 seconds for 156 words", retime_row(19, 75)),

    # ---- Nine matched inside Nineteen ----
    ("the extraction-bug count grows a syllable",
     edit(SCRIPT, "Nine of the 38 `decomposition_error` cases",
          "Nineteen of the 38 `decomposition_error` cases")),

    # ---- the spelling rule, stated three times and checked in none ----
    ("shipped: contribution 6 drifts back to the thesis's word",
     edit(DECK, r"\alert{Pre-specified} evaluation thresholds",
          r"\alert{Pre-registered} evaluation thresholds")),

    # ---- "static baselines" collides with Static GraphRAG ----
        ("the two systems that do not seed are grouped, not named",
     edit(SCRIPT, "and neither the parametric control nor Vector-RAG ever "
                  "sees them.",
          "and the two static baselines never see them.")),

    # ---- the event card's prose, which nothing read ----
    # Its numbers are generated and cannot drift. These three were typed,
    # and each was corrected with no rule behind it, so each could go
    # back in silence.
    ("shipped: the card calls all 57 defects wrong labels",
     edit(CARD, r"{questions where the benchmark,\\ not the system, was at "
                r"fault}",
          r"{benchmark questions whose own\\ gold labels were wrong}")),
    ("shipped: the script caps all four operations",
     edit(SCRIPT, "It gets four operations with fixed signatures \u2014",
          "It gets four operations with fixed signatures and hard caps \u2014")),
    ("shipped: the card caps all four tools",
     edit(CARD, "4 tools, no free-form queries",
          "4 tools with hard caps, no free-form queries")),
    ("shipped: the card counts hedges as a share of answers",
     edit(CARD, r"of WebQSP questions and 23.0\% of CWQ questions are hedged "
                r"rather than answered",
          r"of WebQSP answers and 23.0\% of CWQ answers are hedges rather "
          r"than guesses")),
]

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
