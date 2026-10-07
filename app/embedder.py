from fastembed import TextEmbedding

class EmbeddingError(RuntimeError):
    pass

def load_model(name: str):
    return TextEmbedding(model_name=name)

# Checks if embedded vectors have the expected dimension (e.g. 384)
def _check_dimension(vectors, expected_dim):
    if expected_dim is None:
        return
    
    for vector in vectors:
        if len(vector) != expected_dim:
            raise EmbeddingError(
                f"Model returned {len(vector)} numbers per vector, "
                f"but EMBED_DIM is {expected_dim}"
            )

# Embeds a list of text chunks into vectors. Batch processing is used for efficiency but comsumes more memory.
def embed_documents(model: TextEmbedding, chunks: list, batch_size: int = 64, expected_dim: int = None):
    if batch_size < 1:
        raise ValueError("Batch size must be a positive integer")

    if not chunks:
        return []

    vectors = [v.tolist() for v in model.embed(chunks, batch_size=batch_size)]
    _check_dimension(vectors, expected_dim)

    return vectors

# Embeds a single question into a vector. Returns a single list of numbers of expected dimension (e.g. 384).
def embed_query(model: TextEmbedding, question: str, expected_dim: int = None):
    vector = next(iter(model.query_embed(question))).tolist()
    _check_dimension([vector], expected_dim)
    
    return vector