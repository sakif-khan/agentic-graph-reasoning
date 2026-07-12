import json, time


class KGTools:
    def __init__(self, driver, resolver, log_path,
                 max_fanout=200, max_relations=300):
        self.driver = driver
        self.resolver = resolver
        self.max_fanout = max_fanout
        self.max_relations = max_relations
        self.log_f = open(log_path, "a", encoding="utf-8")
        self.qid = None                      # set per question by the runner

    def _log(self, tool, args, result, t0):
        self.log_f.write(json.dumps({
            "qid": self.qid, "tool": tool, "args": args,
            "ms": round((time.time() - t0) * 1000, 1), "result": result,
        }, ensure_ascii=False) + "\n")
        self.log_f.flush()

    def search_entity(self, surface_form: str, k: int = 5):
        t0 = time.time()
        tier, hits = self.resolver(surface_form, k)
        result = [{"id": i, "name": n, "score": round(float(s), 3),
                   "tier": tier} for i, n, s in hits]
        self._log("search_entity", {"q": surface_form}, result, t0)
        return result

    RELATION_BLOCKLIST = ("common.topic.", "common.", "freebase.", "type.",
                          "kg.", "user.", "dataworld.", "rdf-schema#", "owl#")

    def get_relations(self, entity_id: str):
        t0 = time.time()
        q = """
        MATCH (e:Entity {id:$id})-[r]->()
        RETURN r.fb_name AS rel, 'out' AS dir, count(*) AS n
        UNION ALL
        MATCH (e:Entity {id:$id})<-[r]-()
        RETURN r.fb_name AS rel, 'in' AS dir, count(*) AS n
        """
        with self.driver.session() as s:
            rows = s.run(q, id=entity_id).data()
        rows = [row for row in rows
                if not row["rel"].startswith(self.RELATION_BLOCKLIST)]
        rows.sort(key=lambda r: -r["n"])
        result = rows[: self.max_relations]
        self._log("get_relations", {"id": entity_id}, result, t0)
        return result

    def get_neighbors(self, entity_id: str, relation: str,
                      direction: str = "out"):
        t0 = time.time()
        pattern = ("(e)-[r {fb_name:$rel}]->(n)" if direction == "out"
                   else "(e)<-[r {fb_name:$rel}]-(n)")
        q = f"""
        MATCH (e:Entity {{id:$id}}) MATCH {pattern}
        RETURN n.id AS id, n.name AS name, n.is_cvt AS is_cvt LIMIT $cap
        """
        out = []
        with self.driver.session() as s:
            rows = s.run(q, id=entity_id, rel=relation,
                         cap=self.max_fanout + 1).data()
            truncated = len(rows) > self.max_fanout
            for row in rows[: self.max_fanout]:
                if not row["is_cvt"]:
                    out.append({"id": row["id"], "name": row["name"],
                                "via": [relation]})
                else:                       # hop through the CVT mediator
                    for r2 in s.run(
                        """MATCH (c:Entity {id:$cid})-[r2]-(m:Entity)
                           WHERE m.id <> $orig AND m.is_cvt = false
                           RETURN m.id AS id, m.name AS name,
                                  r2.fb_name AS rel2 LIMIT $cap""",
                        cid=row["id"], orig=entity_id,
                        cap=self.max_fanout).data():
                        out.append({"id": r2["id"], "name": r2["name"],
                                    "via": [relation, r2["rel2"]],
                                    "cvt": row["id"]})
        result = {"neighbors": out[: self.max_fanout], "truncated": truncated}
        self._log("get_neighbors",
                  {"id": entity_id, "rel": relation, "dir": direction},
                  {"n": len(result["neighbors"])}, t0)
        return result

    def verify_triple(self, head_id: str, relation: str, tail_id: str):
        t0 = time.time()
        q = """
        MATCH (h:Entity {id:$h}), (t:Entity {id:$t})
        RETURN
          EXISTS { MATCH (h)-[{fb_name:$rel}]-(t) } AS direct,
          EXISTS { MATCH (h)-[{fb_name:$rel}]-(c:Entity {is_cvt:true})-[]-(t) }
            AS via_cvt
        """
        with self.driver.session() as s:
            row = s.run(q, h=head_id, t=tail_id, rel=relation).single()
        result = {"direct": row["direct"], "via_cvt": row["via_cvt"],
                  "supported": row["direct"] or row["via_cvt"]}
        self._log("verify_triple",
                  {"h": head_id, "rel": relation, "t": tail_id}, result, t0)
        return result
    
    def verify_connection(self, a_id: str, b_id: str):
            """Are two entities adjacent (directly or via one CVT) in the KG?"""
            t0 = time.time()
            q = """
            MATCH (a:Entity {id:$a}), (b:Entity {id:$b})
            RETURN EXISTS { MATCH (a)-[]-(b) } AS direct,
                EXISTS { MATCH (a)-[]-(c:Entity {is_cvt:true})-[]-(b) } AS via_cvt
            """
            with self.driver.session() as s:
                row = s.run(q, a=a_id, b=b_id).single()
            result = {"direct": row["direct"], "via_cvt": row["via_cvt"],
                    "connected": row["direct"] or row["via_cvt"]}
            self._log("verify_connection", {"a": a_id, "b": b_id}, result, t0)
            return result
