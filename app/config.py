from os import getenv

QDRANT_URL = getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = getenv("COLLECTION", "documents")

EMBED_MODEL = getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM = int(getenv("EMBED_DIM", "384"))
EMBED_BATCH_SIZE = int(getenv("EMBED_BATCH_SIZE", "64"))
MAX_UPLOAD_BYTES = int(getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))