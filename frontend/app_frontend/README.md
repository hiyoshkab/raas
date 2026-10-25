# RaaS frontend

This is a React and TypeScript single-page app built with Vite. Vite is the
development server and build tool; production hosting serves the generated
static files from `dist/`.

## Local development

Run Qdrant locally (for example, with Docker):

```sh
docker run --rm -p 6333:6333 qdrant/qdrant:v1.13.2
```

In a second terminal, sign in to Azure CLI and start the FastAPI backend:

```sh
cd ~/projects/raas
az login
export AZURE_OPENAI_ENDPOINT="https://<your-foundry-endpoint>/openai/v1/"
source .venv/bin/activate
cd backend
uvicorn app_backend.main:app --reload
```

In a third terminal, from this directory:

```sh
cd ~/projects/raas/frontend/app_frontend
npm install
npm run dev
```

Open the local URL printed by Vite. It proxies `/ingest` and `/query` to
`http://127.0.0.1:8000`. The first backend start may download the embedding
model. Ensure your Azure identity has access to the configured Foundry model
when asking questions.

## Production build

```sh
npm run build
```

The generated `dist/` directory contains static files for a production web
server such as Nginx. Configure production routing so `/` serves those files
and `/ingest` and `/query` reach the FastAPI service on the same origin.
