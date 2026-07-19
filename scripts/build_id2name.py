"""One-time: build data/id2name.json ({id: name}) from data/nodes.csv.gz."""
import csv, gzip, json


def main():
    id2name = {}
    with gzip.open("data/nodes.csv.gz", "rt", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            id2name[row["id:ID"]] = row["name"]

    print(f"{len(id2name):,} nodes")
    json.dump(id2name, open("data/id2name.json", "w", encoding="utf-8"))


if __name__ == "__main__":
    main()
