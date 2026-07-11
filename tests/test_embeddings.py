import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Load the model ONLY to encode your single query string
print("Loading model for query encoding...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2. Load your pre-computed local artifacts instantly
print("Loading pre-computed relationship vectors and names...")
vecs = np.load("data/relation_embeddings.npy")
with open("data/relation_names.json", "r", encoding="utf-8") as f:
    rel_names = json.load(f)

# 3. Encode your test query
query_str = "where was the person born"
q = model.encode([query_str], normalize_embeddings=True)[0]

# 4. Perform the vector dot product (Cosine Similarity matrix operation)
# Because both 'vecs' and 'q' are normalized, '@' yields the exact cosine score.
scores = vecs @ q
top = np.argsort(scores)[::-1][:5]

# 5. Output the results
print(f"\nTop 5 relationship matches for: '{query_str}':")
print("-" * 50)
for rank, i in enumerate(top, 1):
    print(f"{rank}. Score: {scores[i]:.4f} -> {rel_names[i]}")
