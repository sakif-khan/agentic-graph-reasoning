import pytest

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.runtime import get_driver, get_embedder


class FakeScorer:
    """Deterministic, model-free scorer for mechanics tests."""
    def __call__(self, objective, rel_rows, state=None):
        return [(r, 1.0 / (i + 1)) for i, r in enumerate(rel_rows)]

    def top_facts(self, objective, triples, k=30):
        return triples[-k:]

class LowScoreFakeScorer(FakeScorer):
    """Every candidate scores below any reasonable tau."""
    def __call__(self, objective, rel_rows, state=None):
        self.last_info = {"emb_max": 0.05, "llm_max": 0.0}
        return [(r, 0.05) for r in rel_rows]

@pytest.fixture(scope="session")
def driver():
    driver = get_driver()
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def tools(driver, tmp_path_factory):
    embed = get_embedder()
    log = tmp_path_factory.mktemp("logs") / "test_tools.jsonl"
    return KGTools(driver, EntityResolver(driver, embed), str(log))


@pytest.fixture
def fake_scorer():
    return FakeScorer()

@pytest.fixture
def low_scorer():
    return LowScoreFakeScorer()
