import os
from dotenv import load_dotenv

load_dotenv()          # reads .env from CWD/repo root, no-op if absent

NEO4J_URI = os.environ.get("NEO4J_URI")
if not NEO4J_URI:
    raise RuntimeError(
        "NEO4J_URI is not set — create a .env in the repo root "
        "or set the variable in this terminal.")

NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
if not NEO4J_USERNAME:
    raise RuntimeError(
        "NEO4J_USERNAME is not set — create a .env in the repo root "
        "or set the variable in this terminal.")

NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
if not NEO4J_PASSWORD:
    raise RuntimeError(
        "NEO4J_PASSWORD is not set — create a .env in the repo root "
        "or set the variable in this terminal.")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set — create a .env in the repo root "
        "or set the variable in this terminal.")

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
