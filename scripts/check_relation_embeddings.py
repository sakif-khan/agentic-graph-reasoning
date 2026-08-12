"""Spot-check the relation embeddings by ranking the vocabulary against a
free-text query. Prints the five closest relation names.

This is the functional check Sec 4.5 reports: if the verbaliser were degenerate,
the top five would come back unordered. Its output is archived as
results/phase1/check_relation_embeddings_log.txt, and
tests/test_relation_embeddings.py holds the prose to that archive, so the
numbers in the text cannot drift from the run they came from.

The file used to live in tests/ under a test_ name. It defines no test, so
pytest collected it, ran this module body at collection time, and a bare run
both loaded the sentence encoder and broke on a checkout where the two data
files below had not been built yet.

Usage: python scripts/check_relation_embeddings.py
"""
import json
import numpy as np
from agr.runtime import get_embedder

# 1. The model is needed only to encode the query string
print("Loading model for query encoding...")
model = get_embedder()

# 2. The relation vectors and names were precomputed by
#    scripts/embed_relation_vocabulary.py
print("Loading pre-computed relationship vectors and names...")
vecs = np.load("data/relation_embeddings.npy")
with open("data/relation_names.json", "r", encoding="utf-8") as f:
    rel_names = json.load(f)

# 3. Encode the query
query_str = "where was the person born"
q = model.encode([query_str], normalize_embeddings=True)[0]

# 4. Both vecs and q are normalized, so the dot product is the cosine score
scores = vecs @ q
top = np.argsort(scores)[::-1][:5]

# 5. Output the results
print(f"\nTop 5 relationship matches for: '{query_str}':")
print("-" * 50)
for rank, i in enumerate(top, 1):
    print(f"{rank}. Score: {scores[i]:.4f} -> {rel_names[i]}")
