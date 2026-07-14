from agr.budget import BudgetConfig, BudgetMeter

BASELINE_SCHEMA = ('{"answer": "...", "answer_entities": ["..."]} '
                   '-- answer_entities exactly as named in any provided '
                   'facts; [] if the answer cannot be determined.')


def make_final(answer, entities, meter, trace, extra=None):
    """Shape a baseline result like an AGR final state for RunLogger."""
    return {"answer": answer,
            "answer_entities": entities,
            "draft": None, "unsupported_claims": [],
            "supporting_triples": extra.get("supporting", []) if extra else [],
            "budget": meter, "trace": trace}


def parse_entities(out):
    return [str(a).strip() for a in out.get("answer_entities", [])
            if str(a).strip()]
