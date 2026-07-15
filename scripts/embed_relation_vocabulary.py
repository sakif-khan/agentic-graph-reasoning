import csv, gzip, json, re
import numpy as np
from agr.runtime import get_embedder

# 1. Collect distinct relation names from the CSV generated in Step 1.2
rel_names = set()
with gzip.open("rels.csv.gz", "rt", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rel_names.add(row["fb_name"])
rel_names = sorted(rel_names)
print(f"{len(rel_names)} distinct relations")   # expect a few thousand

# 2. Verbalize: dotted schema paths -> natural-ish phrases
def verbalize(rel: str) -> str:
    words = re.split(r"[._]", rel)
    # drop consecutive duplicates: "people.person.person..." -> cleaner text
    out = [w for i, w in enumerate(words) if w and (i == 0 or w != words[i-1])]
    return " ".join(out)

phrases = [verbalize(r) for r in rel_names]
# spot check
for rel_name, phrase in list(zip(rel_names, phrases))[:5]:
    print(f"{rel_name}  ->  {phrase}")

# 3. Embed with the SAME model used for entities (critical for comparability)
model = get_embedder()
vecs = model.encode(phrases, batch_size=256,
                    normalize_embeddings=True, show_progress_bar=True)

# 4. Persist as local artifacts
np.save("relation_embeddings.npy", vecs.astype(np.float32))
with open("relation_names.json", "w", encoding="utf-8") as f:
    json.dump(rel_names, f)