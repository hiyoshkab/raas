from pathlib import PurePosixPath

from fastapi import FastAPI, File, HTTPException, UploadFile
from schemass import IngestResponse, QueryRequest, QueryResponse
import logging

import config
from chunker import chunk_text, read_limited

log = logging.getLogger(__name__)
app = FastAPI(title="RaaS")

@app.get("/healthz")
def healthz():
    log.info("Health check performed")
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    log.info("Readiness check performed")
    return {"status": "ok"}

# Ingest File Endpoint
@app.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    name = PurePosixPath(file.filename).name
    log.info("Ingesting file: %s", name)

    try:
        data = read_limited(file.file, config.MAX_UPLOAD_BYTES)
    except ValueError:
        raise HTTPException(status_code=413, detail="File too large")

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        log.warning("Rejected %s: not valid UTF-8", name)
        raise HTTPException(status_code=422, detail="File is not valid UTF-8 text")

    chunks = chunk_text(text, chunk_size=config.CHUNK_SIZE, overlap=config.OVERLAP)
    if not chunks:
        raise HTTPException(status_code=422, detail="File contains no text")

    return IngestResponse(filename=name, chunks=len(chunks))

# Query Endpoint
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    log.info(f"Processing query: {request.question}")
    return QueryResponse(answer="This is a sample answer.", sources=[])
