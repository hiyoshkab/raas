import uuid
import logging

from qdrant_client import QdrantClient, models

log = logging.getLogger(__name__)

def get_client(url="http://localhost:6333"):
    if url == ":memory:":
        return QdrantClient()
    log.info(f"Connecting to Qdrant at {url}")
    return QdrantClient(url=url)

# Ensures that a collection exists in the Qdrant client.
def ensure_collection(client: QdrantClient, collection_name: str, vector_size: int):
    if not client.collection_exists(collection_name):
        log.info(f"Creating collection {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
        )
    log.info(f"Ensuring collection {collection_name} exists")

# Generates a unique point ID for a given filename and index.
def _point_id(filename: str, index: int):
    log.info(f"Generating point ID for {filename}:{index}")
    
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{filename}:{index}"))

# Upserts chunks into the Qdrant client.
def upsert_chunks(client: QdrantClient, collection_name: str, filename: str, chunks: list, vectors: list):
    log.info(f"Upserting chunks for {filename}")
    
    points = [
        models.PointStruct(
            id=_point_id(filename, i),
            vector=vector
        )
        for i, vector in enumerate(vectors)
    ]

    log.info(f"Generated points for {filename}: {len(points)}")
    if points:
        try:
            client.upsert(collection_name=collection_name, points=points)

        except Exception as e:
            log.error(f"Error occurred while upserting chunks for {filename}: {e}")
            raise

    return len(points)

# Searches for similar vectors in the Qdrant client.
def search(client: QdrantClient, collection_name: str, vector: list, limit: int = 3):
    log.info(f"Searching in collection {collection_name}")

    try:
        results = client.query_points(
            collection_name=collection_name, 
            query_vector=vector, 
            limit=limit, 
            with_payload=True
            )
        
    except Exception as e:
        log.error(f"Error occurred while searching in collection {collection_name}: {e}")
        raise

    return [(hit.score, hit.payload) for hit in results.points]
