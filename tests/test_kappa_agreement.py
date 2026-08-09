"""The two Cohen's kappa implementations must agree, and the thesis says so.

judge_validation._note in thesis_numbers.json claims that
scripts/compute_kappa.py recomputes the reported kappa independently from the
same two files and agrees with the embedded implementation in
scripts/build_thesis_numbers.py. Nothing checked that. An agreement claim that
nothing runs is the same kind of unbacked statement the thesis is careful to
avoid elsewhere, so it is checked here.

The duplication is deliberate rather than an oversight to be refactored away: a
slip in a chance-correction formula yields a plausible number, not a crash, and
two hand-written readings of the same inputs is the cheap guard against that.
This test is what makes the second reading worth having.
"""
import importlib.util
import io
import re
from contextlib import redirect_stdout
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "results" / "phase4" / "tier2_judge" / "kappa_sheet.csv"
KEY = ROOT / "results" / "phase4" / "tier2_judge" / "kappa_key.json"

pytestmark = pytest.mark.skipif(
    not (SHEET.exists() and KEY.exists()),
    reason="tier-2 judge artifacts absent")


def _load(name):
    """Import a script by path: scripts/ is not a package."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_two_implementations_agree(monkeypatch):
    embedded = _load("build_thesis_numbers").compute_kappa(SHEET, KEY)

    # compute_kappa.py does its work at import time and prints the result, and
    # it reads relative paths, so it runs from the repo root and is read back
    # off stdout. Four places, because that is the precision it prints and the
    # precision the thesis quotes -- 0.6995 is reported as missing its 0.70 bar
    # and rounding it further is the one presentation the thesis argues against.
    monkeypatch.chdir(ROOT)
    buf = io.StringIO()
    with redirect_stdout(buf):
        _load("compute_kappa")
    printed = re.search(r"Cohen's kappa = (-?[\d.]+)", buf.getvalue())

    assert printed, f"compute_kappa.py printed no kappa:\n{buf.getvalue()}"
    assert float(printed.group(1)) == embedded["cohens_kappa"], (
        f"the two implementations disagree: standalone {printed.group(1)} vs "
        f"embedded {embedded['cohens_kappa']}; judge_validation._note claims "
        f"they must agree")


def test_reported_kappa_misses_its_preregistered_bar():
    """The thesis reports kappa as below its bar; that is a claim about a number.

    Reported rather than rounded up is the integrity point the thesis makes
    about this figure, so a rerun that lifted kappa over the bar has to change
    the prose, not just the table.
    """
    k = _load("build_thesis_numbers").compute_kappa(SHEET, KEY)
    assert k["cohens_kappa"] < k["preregistered_threshold"], (
        f"kappa is now {k['cohens_kappa']}, at or above the pre-registered "
        f"{k['preregistered_threshold']}; the thesis describes it as falling "
        f"marginally short and that description no longer holds")
