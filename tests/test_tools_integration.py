import pytest
from tests.known import KNOWN

pytestmark = pytest.mark.integration


def test_search_tier1(tools):
    hits = tools.search_entity(KNOWN["entity_name"])
    assert hits and hits[0]["tier"] == 1


def test_relations_contains_known_sorted(tools):
    rels = tools.get_relations(KNOWN["entity_id"])
    assert any(r["rel"] == KNOWN["relation"] for r in rels)
    assert all(rels[i]["n"] >= rels[i + 1]["n"] for i in range(len(rels) - 1))


def test_neighbors_finds_known(tools):
    out = tools.get_neighbors(KNOWN["entity_id"], KNOWN["relation"])
    assert any(n["name"] == KNOWN["neighbor_name"] for n in out["neighbors"])


def test_verify_positive_negative(tools):
    assert tools.verify_triple(KNOWN["entity_id"], KNOWN["relation"],
                               KNOWN["neighbor_id"])["supported"]
    assert not tools.verify_triple(KNOWN["entity_id"],
                                   KNOWN["fake_relation"],
                                   KNOWN["neighbor_id"])["supported"]

# pytest -m integration
# Integration tests need Neo4j up and KNOWN filled in.
