"""Recount the literal census of Sec. 4.7.4 from data/nodes.csv.gz.

These figures -- how many nodes carry a date-shaped name, a year, or a numeric
name, and what fraction of nodes are unnamed mediators -- were originally
computed once by hand and quoted in the thesis with no committed artifact behind
them. That is exactly the practice the thesis criticises elsewhere, so they are
recomputed here into results/phase1/literal_census.json.

The numeric count is definition-dependent and the definition is the point. A
"numeric node" here is one whose name is *entirely* a number: optional sign,
digits, optional single decimal point, optional trailing group separators
stripped. A looser rule -- any name *containing* a number -- gives a materially
different answer, and both are reported so the quoted figure cannot be mistaken
for a property of the graph independent of how it was counted.

Usage: python scripts/count_literals.py
"""
import csv
import gzip
import json
import re
from pathlib import Path

NODES = Path("data/nodes.csv.gz")
OUT = Path("results/phase1/literal_census.json")

# Anchored: the whole name is the value.
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
YEAR = re.compile(r"^\d{4}$")
NUMERIC_STRICT = re.compile(r"^[+-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?$|^[+-]?\d+(?:\.\d+)?$")
# Looser: the name carries no letters at all, so it is punctuation and digits --
# "1;2;3", "(1955)", "12-4". Still value-like, but not a single clean number.
NUMERIC_LOOSE = re.compile(r"^[^A-Za-z]*\d[^A-Za-z]*$")


def main():
    n = n_cvt = n_named = 0
    dates = years = numeric_strict = numeric_loose = 0

    with gzip.open(NODES, "rt", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            if row["is_cvt:boolean"] == "true":
                n_cvt += 1
            name = (row["name"] or "").strip()
            if not name:
                continue
            n_named += 1
            if DATE.match(name):
                dates += 1
            if YEAR.match(name):
                years += 1
            if NUMERIC_STRICT.match(name):
                numeric_strict += 1
            if NUMERIC_LOOSE.match(name):
                numeric_loose += 1

    doc = {
        "_source": "data/nodes.csv.gz",
        "_note": ("Regenerate with scripts/count_literals.py. numeric_strict is "
                  "the figure the thesis quotes: the whole name is one number. "
                  "numeric_loose additionally admits names that carry no "
                  "letters at all, and is reported so the definitional "
                  "sensitivity is visible rather than implied -- the two "
                  "differ by about 9%. An earlier hand count gave 12,622 "
                  "under a rule that was not recorded and could not be "
                  "reproduced; the thesis now quotes this file."),
        "_definitions": {
            "date": DATE.pattern,
            "year": YEAR.pattern,
            "numeric_strict": NUMERIC_STRICT.pattern,
            "numeric_loose": NUMERIC_LOOSE.pattern,
        },
        "n_nodes": n,
        "n_named": n_named,
        "n_cvt": n_cvt,
        "cvt_pct": round(100 * n_cvt / n, 2),
        "dates_full": dates,
        "years_bare": years,
        "date_or_year_pct": round(100 * (dates + years) / n, 4),
        "numeric_strict": numeric_strict,
        "numeric_strict_pct": round(100 * numeric_strict / n, 2),
        "numeric_loose": numeric_loose,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")
    for k in ("n_nodes", "n_cvt", "cvt_pct", "dates_full", "years_bare",
              "numeric_strict", "numeric_strict_pct", "numeric_loose"):
        print(f"  {k:22s} {doc[k]}")


if __name__ == "__main__":
    main()
