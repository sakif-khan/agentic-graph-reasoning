"""The deck's checker has to run, and it has to be able to fail.

thesis_presentation/check_slides.py binds the figures on the slides back to
the artifacts and code they came from. Nothing invoked it. The manuscript
has five test_paper_*.py files and a directory of probes; the deck, which
is the document most exposed to drift because the thesis keeps moving under
it, had neither -- so the checker's verdict was only ever seen by whoever
remembered to run it by hand.

That is the argument tests/probes/README.md opens with, applied to the
checker itself: a check nobody runs is indistinguishable from a clean
document. The second test is the non-vacuity half. It corrupts one figure
on a slide and asserts the checker notices, so this file cannot pass by
shelling out to something that has quietly stopped checking anything.
"""
import io
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "thesis_presentation" / "check_slides.py"
DECK = ROOT / "thesis_presentation" / "content-main.tex"

pytestmark = pytest.mark.skipif(
    not CHECK.exists(), reason="presentation sources absent")


def run_checker():
    return subprocess.run([sys.executable, str(CHECK)], cwd=ROOT,
                          capture_output=True, text=True)


def test_every_figure_on_the_slides_matches_its_source():
    r = run_checker()
    failed = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    assert r.returncode == 0, (
        "check_slides.py reports the deck disagrees with its sources:\n  "
        + "\n  ".join(failed[:20]))


def test_the_checker_can_fail():
    """Corrupt one cell, assert it is caught, restore.

    AGR's WebQSP Hits@1, because it is the headline number and it appears
    on more than one slide -- which is exactly the case a whole-file
    substring search used to pass.
    """
    before = io.open(DECK, encoding="utf-8", newline="").read()
    assert r"\textbf{0.755}" in before, "the headline cell moved"
    try:
        io.open(DECK, "w", encoding="utf-8", newline="").write(
            before.replace(r"\textbf{0.755}", r"\textbf{0.855}", 1))
        r = run_checker()
        assert r.returncode != 0, (
            "check_slides.py passed a deck whose headline Hits@1 had been "
            "changed from 0.755 to 0.855")
        assert "0.755" in r.stdout
    finally:
        io.open(DECK, "w", encoding="utf-8", newline="").write(before)

    assert io.open(DECK, encoding="utf-8", newline="").read() == before
    assert run_checker().returncode == 0, "the deck was left corrupted"
