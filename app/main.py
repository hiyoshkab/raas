import logging
from contextlib import asynccontextmanager
from pathlib import PurePosixPath

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile

from app import config, embedder, store
from app.chunker import chunk_text
from app.schemas import IngestResponse, QueryRequest, QueryResponse, Source

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    app.state.model = embedder.load_model(config.EMBED_MODEL)
    app.state.client = store.get_client(config.QDRANT_URL)
    try:
        store.ensure_collection(app.state.client, config.COLLECTION, config.EMBED_DIM)
    except Exception:
        log.warning("Qdrant not reachable at startup; /readyz will report it")
    yield


app = FastAPI(title="RaaS", lifespan=lifespan)


def get_model(request: Request):
    return request.app.state.model


def get_client(request: Request):
    return request.app.state.client


def read_limited(upload_file, max_bytes, block=64 * 1024):
    data = bytearray()
    while block_bytes := upload_file.read(block):
        data.extend(block_bytes)
        if len(data) > max_bytes:
            raise ValueError("File too large")
    return bytes(data)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz(client=Depends(get_client)):
    try:
        client.get_collections()
    except Exception:
        raise HTTPException(status_code=503, detail="Vector database not reachable")
    return {"status": "ready"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...), model=Depends(get_model), client=Depends(get_client)):
    name = PurePosixPath(file.filename).name
    log.info("Ingesting file: %s", name)

    try:
        data = read_limited(file.file, config.MAX_UPLOAD_BYTES)
    except ValueError:
        raise HTTPException(status_code=413, detail="File too large")

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=422, detail="File is not valid UTF-8 text")

    chunks = chunk_text(text, chunk_size=config.CHUNK_SIZE, overlap=config.OVERLAP)
    if not chunks:
        raise HTTPException(status_code=422, detail="File contains no text")

    try:
        vectors = embedder.embed_documents(
            model, chunks,
            batch_size=config.EMBED_BATCH_SIZE, expected_dim=config.EMBED_DIM,
        )
    except embedder.EmbeddingError as e:
        log.error("Embedding failed for %s: %s", name, e)
        raise HTTPException(status_code=502, detail=str(e))

    store.ensure_collection(client, config.COLLECTION, config.EMBED_DIM)
    store.upsert_chunks(client, config.COLLECTION, name, chunks, vectors)

    return IngestResponse(filename=name, chunks=len(chunks))


@app.post("/query", response_model=QueryResponse)
def query( body: QueryRequest, model=Depends(get_model), client=Depends(get_client)):
    try:
        vector = embedder.embed_query(model, body.question, expected_dim=config.EMBED_DIM)
        
    except embedder.EmbeddingError as e:
        log.error("Embedding failed for query: %s", e)
        raise HTTPException(status_code=502, detail=str(e))

    store.ensure_collection(client, config.COLLECTION, config.EMBED_DIM)
    results = store.search(client, config.COLLECTION, vector, top_k=body.top_k)
    sources = [
        Source(filename=p["filename"], chunk_index=p["chunk_index"], score=score, text=p["text"])
        for score, p in results
    ]
    if not sources:
        return QueryResponse(answer="No documents have been ingested yet.", sources=[])
    
    return QueryResponse(
        answer="The language model isn't connected yet. These are the most relevant passages.",
        sources=sources,
    )