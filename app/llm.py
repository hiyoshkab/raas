import os
import re

from app import config
import app.config
import httpx

SYSTEM = (
    "You answer questions using only the numbered sources provided. "
    "Cite sources inline like [1] or [2]. "
    "If the sources do not contain the answer, say you could not find it in the documents. "
    "Answer in the same language as the question."
)

NO_SOURCES_ANSWER = "No relevant documents were found."


class LLMError(RuntimeError):
    pass


def build_prompt(question, sources):
    blocks = []
    for number, source in enumerate(sources, start=1):
        header = f"[{number}] ({source['filename']}, chunk {source['chunk_index']})"
        blocks.append(f"{header}\n{source['text']}")
    context = "\n\n".join(blocks)
    return f"Sources:\n\n{context}\n\nQuestion: {question}"


def generate(question, sources):
    if not sources:
        return NO_SOURCES_ANSWER

    url = config.OLLAMA_URL
    model = config.LLM_MODEL
    if not model:
        raise LLMError("Set LLM_MODEL to the name of a model you have pulled in Ollama")

    payload = {
        "model": model,
        "stream": False,
        "options": {
            "num_ctx": config.LLM_NUM_CTX,
            "temperature": config.LLM_TEMPERATURE,
        },
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": build_prompt(question, sources)},
        ],
    }

    try:
        response = httpx.post(
            f"{url}/api/chat",
            json=payload,
            timeout=float(config.LLM_TIMEOUT),
        )
        response.raise_for_status()
    except httpx.ConnectError as e:
        raise LLMError(f"Cannot reach Ollama at {url}. Is it running?") from e
    except httpx.HTTPStatusError as e:
        raise LLMError(f"Ollama returned {e.response.status_code}: {e.response.text}") from e

    return response.json()["message"]["content"]


def extract_citations(answer, n_sources):
    found = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}

    return sorted(n for n in found if 1 <= n <= n_sources)