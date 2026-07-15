from functools import lru_cache

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

from agr.config import EMBED_MODEL
from agr.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


@lru_cache(maxsize=1)
def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer(EMBED_MODEL)
