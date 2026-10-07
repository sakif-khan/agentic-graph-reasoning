"""Sweep the deck for values the checker does not actually check.

The other probes each reinstate one defect. This one is a census: it
corrupts every transcribed figure class in both decks, one at a time, and
asserts the checker notices each. It exists because check_slides.py was
measured rather than trusted and came out at 7 of 25.

Two causes, both now fixed and both guarded here. has() searched the three
source files concatenated, so it asked whether a value appeared anywhere
rather than whether a given cell held it -- and this deck prints several
figures twice, so corrupting the one on a main slide passed on the copy on
a backup slide. And whole classes were outside its coverage: the graph
statistics, the tool caps and names, the per-category census counts, the
opening slide's headline, the research-question numbering, and the entire
backup budget table.

Cell-scoping alone was not enough either. The call cap reads 0.0% in all
three columns, and "0.0" is a substring of "40.0", so the corrupted row
still passed until the match was made whole-number. That case is here.

Both decks are restored in a finally block.
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                    pathlib.Path(__file__).resolve().parents[2])
MAIN = ROOT / "thesis_presentation" / "content-main.tex"
# The backup frames are content-backup.tex again since 2026-10-07, a deck
# of their own as at the pre-defense. From 275fadc ("Freeze pre-defense
# files") until then they were the tail of content-main.tex, and BACK and
# MAIN were the same file.
BACK = ROOT / "thesis_presentation" / "content-backup.tex"
CHECK = ROOT / "thesis_presentation" / "check_slides.py"

FILES = (MAIN, BACK)
orig = {p: io.open(p, encoding="utf-8", newline="").read() for p in FILES}


def restore():
    for p, s in orig.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)


def run():
    r = subprocess.run([sys.executable, str(CHECK)],
                       cwd=ROOT, capture_output=True, text=True)
    fail = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return r.returncode, (fail[0][:88] if fail else "")


# (name, file, literal to replace, replacement). Literals rather than
# regexes: a sweep that quietly matched nothing would report the checker
# as sound, which is the failure this probe exists to rule out, so each
# anchor is asserted present before it is used.
CASES = [
    # Results, costs -- the classes has() did cover, kept as a regression
    # guard now that they go through the cell-scoped path.
    ("main results Hits@1 0.755 -> 0.855", MAIN, "0.755", "0.855"),
    ("main results F1 0.642 -> 0.842", MAIN, "0.642", "0.842"),
    ("cost 4,511 tokens -> 9,511", MAIN, "4{,}511", "9{,}511"),
    ("CWQ cost sentence 6,818 -> 9,818", MAIN, "6{,}818", "9{,}818"),
    # Question sets and the environment.
    ("multi-hop count 132 -> 232", MAIN, "$132$", "$232$"),
    ("reachability 97.0% -> 87.0%", MAIN, r"$97.0\%$", r"$87.0\%$"),
    ("gold median 1.5 -> 2.5", MAIN, "$1.5$", "$2.5$"),
    ("graph entities 2.59M -> 9.59M", MAIN, "$2{,}592{,}892$",
     "$9{,}592{,}892$"),
    ("graph triples 8.31M -> 1.31M", MAIN, "$8{,}309{,}194$",
     "$1{,}309{,}194$"),
    ("distinct relations 7,058 -> 9,058", MAIN, "$7{,}058$", "$9{,}058$"),
    ("import time 36.4s -> 96.4s", MAIN, "$36.4$", "$96.4$"),
    # The headline the talk opens on.
    # The groundedness slide reports both datasets POOLED now, and as a
    # table rather than a sentence. These three were the no-retrieval
    # control's WebQSP figures -- 661 asserted, 179 ungrounded, 27.1% -- and
    # its pooled row is 1,001 / 221 / 22.1%. Same trio, same row, same
    # defect: a cell that disagrees with the JSON.
    ("control asserted 1,001 -> 1,999", MAIN,
     r"$1{,}001$", r"$1{,}999$"),
    ("control ungrounded 221 -> 421", MAIN, "$221$", "$421$"),
    # Anchored on the table CELL. A bare "$22.1\%$" matched a LaTeX comment
    # further up the file first -- the note explaining the column width --
    # so the corruption edited a comment the checker strips and the case
    # reported MISSED against a live rule.
    ("control rate 22.1% -> 82.1%", MAIN,
     r"$221$ ($22.1\%$)", r"$221$ ($82.1\%$)"),
    # The state machine, counted from its own diagram. Both anchors lost
    # their punctuation in the October 2026 dash sweep: "Six nodes;" became
    # "Six nodes." and "Three cycles ---" became "Three cycles (".
    ("'Six nodes' -> 'Sixteen nodes'", MAIN, "Six nodes.", "Sixteen nodes."),
    ("'Three cycles' -> 'Seven cycles'", MAIN, r"Three cycles (\emph",
     r"Seven cycles (\emph"),
    # The tool API.
    # "offered" became "to the scorer" in the tool-API table.
    ("tool cap 300 -> 900", MAIN, r"$\leq 300$ to the scorer",
     r"$\leq 900$ to the scorer"),
    ("tool cap 200 -> 500", MAIN, r"$\leq 200$ per expansion",
     r"$\leq 500$ per expansion"),
    ("tool name search_entity -> quantum_entity", MAIN,
     r"\texttt{search\_entity}", r"\texttt{quantum\_entity}"),
    # The failure census, per category.
    # 64, not 65: the September 2026 census correction changed this count.
    ("census relation_selection 64 -> 84", MAIN,
     "Relation selection   & 64", "Relation selection   & 84"),
    ("census composite_claim 47 -> 74", MAIN,
     "Composite claim      & 47", "Composite claim      & 74"),
    ("census echo 13 -> 31", MAIN, r"\alert{13}", r"\alert{31}"),
    # Research-question numbering. Anchored on slide 8's label, which is
    # what the bare "RQ1" used to hit first. Since 2026-10 a comment above
    # slide 8 names RQ1 earlier in the file, and the bare anchor renamed
    # that comment, which the checker rightly ignores: MISSED, for the
    # probe's reason rather than the checker's.
    ("RQ1 renamed RQ9", MAIN, r"\textbf{RQ1}", r"\textbf{RQ9}"),
    # The backup deck, which nothing reached at all.
    ("budget max_llm_calls 25 -> 99", BACK,
     r"\texttt{max\_llm\_calls}   & 25", r"\texttt{max\_llm\_calls}   & 99"),
    ("budget beam_width 3 -> 8", BACK,
     r"\texttt{beam\_width}       & 3", r"\texttt{beam\_width}       & 8"),
    ("budget max_depth 4 -> 7", BACK,
     r"\texttt{max\_depth}        & 4", r"\texttt{max\_depth}        & 7"),
    ("budget max_seconds 300 -> 900", BACK,
     r"\texttt{max\_seconds}      & 300", r"\texttt{max\_seconds}      & 900"),
    ("binding depth cap 16.5% -> 61.5%", BACK, r"$16.5\%$", r"$61.5\%$"),
    # The substring trap: "0.0" is inside "40.0".
    # Anchored on the Call cap ROW. \mathbf{0.0\%} has five homes in this
    # deck and the first two are the groundedness table's zero-hallucination
    # cells, so a bare anchor corrupted a different slide's number and the
    # budget-binding rule never saw anything wrong.
    ("binding call cap 0.0% -> 40.0%", BACK,
     r"\textbf{Call cap} & $\mathbf{0.0\%}$",
     r"\textbf{Call cap} & $\mathbf{40.0\%}$"),
    # Named for the backup hedging slide it was written against. That slide
    # left with the pre-defense; 12.2 is a cell of the main deck's
    # "Does it just refuse more often?" table now.
    ("backup hedge rate 12.2 -> 52.2", MAIN, "12.2", "52.2"),
]

rc, first = run()
assert rc == 0, f"the deck is not clean before the sweep: {first}"

out = []
try:
    for name, path, old, new in CASES:
        assert orig[path].count(old) >= 1, f"anchor gone: {name} -> {old!r}"
        io.open(path, "w", encoding="utf-8", newline="").write(
            orig[path].replace(old, new, 1))
        rc, first = run()
        out.append((name, rc, first))
        restore()
finally:
    restore()

for name, rc, first in out:
    print(f"{'CAUGHT' if rc else 'MISSED':7s}  {name}")
    if not rc:
        print(f"{'':9s}the checker passed this corruption")

rc, first = run()
caught = sum(1 for _, rc_, _ in out if rc_)
print(f"\nrestored -> rc={rc}")
print(f"{caught} of {len(out)} corruptions caught")
passed = caught == len(out) and rc == 0
print("ALL CASES CAUGHT" if passed else "SOME CASE MISSED")
sys.exit(0 if passed else 1)
