from os import getenv

OLLAMA_URL = getenv("OLLAMA_URL", "http://localhost:11434")
LLM_MODEL = getenv("LLM_MODEL", "llama3.1:latest")
LLM_NUM_CTX = int(getenv("LLM_NUM_CTX", "8192"))
LLM_TEMPERATURE = float(getenv("LLM_TEMPERATURE", "0.1"))
LLM_TIMEOUT = float(getenv("LLM_TIMEOUT", "300"))

QDRANT_URL = getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = getenv("COLLECTION", "documents")

EMBED_MODEL = getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM = int(getenv("EMBED_DIM", "384"))
EMBED_BATCH_SIZE = int(getenv("EMBED_BATCH_SIZE", "64"))
MAX_UPLOAD_BYTES = int(getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))

CHUNK_SIZE = int(getenv("CHUNK_SIZE", "512"))
OVERLAP = int(getenv("OVERLAP", "64"))