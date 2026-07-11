import pytest
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.resolver import EntityResolver
from agr.kg_tools import KGTools
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class FakeScorer:
    """Deterministic, model-free scorer for mechanics tests."""
    def __call__(self, objective, rel_rows):
        return [(r, 1.0 / (i + 1)) for i, r in enumerate(rel_rows)]

    def top_facts(self, objective, triples, k=30):
        return triples[-k:]          # deterministic, model-free

@pytest.fixture(scope="session")
def driver():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def tools(driver, tmp_path_factory):
    embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    log = tmp_path_factory.mktemp("logs") / "test_tools.jsonl"
    return KGTools(driver, EntityResolver(driver, embed), str(log))


@pytest.fixture
def fake_scorer():
    return FakeScorer()
