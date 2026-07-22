def main():
    import json
    for ds in ("webqsp", "cwq"):
        half_qids = {q["qid"] for q in json.load(
            open(f"results/phase4/test_{ds}_half.json", encoding="utf-8"))}
        with open(f"logs/test_{ds}_half_abl_full.jsonl", "w",
                encoding="utf-8") as out:
            for l in open(f"results/phase4/test_{ds}_agr.jsonl", encoding="utf-8"):
                if json.loads(l)["qid"] in half_qids:
                    out.write(l)

if __name__ == "__main__":
    main()
