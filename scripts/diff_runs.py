# paired per-question comparison of two RunLogger files.
import json, sys

def load(p):
    return {json.loads(l)["qid"]: json.loads(l) for l in open(p, encoding="utf-8")}


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python scripts/diff_runs.py logs/dev80_a0.7_t0.2.jsonl logs/dev80_a0.7_t0.2_draftonly.jsonl")

    a, b = load(sys.argv[1]), load(sys.argv[2])
    for qid in a:
        ra, rb = a[qid], b.get(qid)
        if rb and (ra["answer_entities"] != rb["answer_entities"]):
            print(f'[{qid}]')
            print(f'  A: {ra["answer_entities"]}  verifier={ra.get("verifier_outcome")}')
            print(f'  B: {rb["answer_entities"]}  verifier={rb.get("verifier_outcome")}')
            print(f'  gold: {ra["gold"]}')


if __name__ == "__main__":
    main()
