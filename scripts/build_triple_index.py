"""One-time: embed every verbalized triple to a memmapped fp16 matrix."""
import csv, gzip, json
import numpy as np
from agr.runtime import get_embedder

model = get_embedder()
texts, meta = [], []
with gzip.open("data/rels.csv.gz", "rt", encoding="utf-8") as f:
    r = csv.DictReader(f)
    id2name = json.load(open("data/id2name.json", encoding="utf-8"))  # build
    # from nodes.csv.gz once if you don't have it: {id: name}
    for row in r:
        h, t = id2name.get(row[":START_ID"]), id2name.get(row[":END_ID"])
        if not h or not t:
            continue
        rel_words = row["fb_name"].replace(".", " ").replace("_", " ")
        texts.append(f"{h} {rel_words} {t}")
        meta.append((row[":START_ID"], row["fb_name"], row[":END_ID"]))

print(f"{len(texts):,} triples to embed")
mat = np.memmap("data/triple_index/vecs.fp16", dtype=np.float16, mode="w+",
                shape=(len(texts), 384))
B = 4096
for i in range(0, len(texts), B):
    vecs = model.encode(texts[i:i+B], batch_size=256,
                        normalize_embeddings=True)
    mat[i:i+B] = vecs.astype(np.float16)
    if i % (B * 20) == 0:
        print(f"{i:,}")
mat.flush()
json.dump({"n": len(texts)}, open("data/triple_index/shape.json", "w"))
with open("data/triple_index/texts.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(texts))
