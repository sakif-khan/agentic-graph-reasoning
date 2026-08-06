"""Known-good graph facts used by the integration tests.

Entity and node IDs are assigned at import time, so they differ between graph
builds. Refresh the values below against the loaded graph before running
`pytest -m integration`, using this query in the Neo4j Browser:

MATCH (e:Entity {name: 'Justin Bieber'})-[r {fb_name: 'people.person.parents'}]-(n:Entity)
WHERE n.is_cvt = false
RETURN e.id  AS entity_id,
       r.fb_name AS relation,
       n.id  AS neighbor_id,
       n.name AS neighbor_name;
"""
KNOWN = {
    "entity_name": "Justin Bieber",
    "entity_id": "15",
    "relation": "people.person.parents",
    "neighbor_name": "Jeremy Bieber",
    "neighbor_id": "362",
    "fake_relation": "people.person.owns_spaceship",
}
