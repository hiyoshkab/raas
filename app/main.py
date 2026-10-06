from fastapi import FastAPI, File, HTTPException, UploadFile
from schemass import IngestResponse, QueryRequest, QueryResponse
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="RaaS")

@app.get("/healthz")
def healthz():
    logging.info("Health check performed")
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    logging.info("Readiness check performed")
    return {"status": "ok"}

@app.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    logging.info(f"Ingesting file: {file.filename}")
    try:
        text = file.file.read().decode("utf-8")
    except UnicodeDecodeError as e:
        logging.error(f"Error reading file {file.filename}: {e}")
        raise HTTPException(status_code=400, detail="Error reading file")

    return IngestResponse(filename=file.filename, chunks=0)

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    logging.info(f"Processing query: {request.question}")
    return QueryResponse(answer="This is a sample answer.", sources=[])
