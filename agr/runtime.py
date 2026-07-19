from functools import lru_cache

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.config import BACKBONE
from agr.env import EMBED_MODEL, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY
from agr.llm import LLMClient
from agr.scorer import HybridScorer


@lru_cache(maxsize=1)
def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer(EMBED_MODEL)


@lru_cache(maxsize=1)
def get_llm():
    return LLMClient(api_key=OPENAI_API_KEY, **BACKBONE)


@lru_cache(maxsize=None)
def get_scorer(alpha: float):
    return HybridScorer("data/relation_embeddings.npy",
                        "data/relation_names.json",
                        llm=get_llm(), alpha=alpha)
