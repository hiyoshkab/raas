import re
from functools import lru_cache

from app_backend import config
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI, OpenAIError

SYSTEM = (
    "You answer questions using only the numbered sources provided. "
    "Cite sources inline like [1] or [2]. "
    "If the sources do not contain the answer, say you could not find it in the documents. "
    "Answer in the same language as the question."
)

NO_SOURCES_ANSWER = "No relevant documents were found."
AZURE_TOKEN_SCOPE = "https://ai.azure.com/.default"


class LLMError(RuntimeError):
    pass


def build_prompt(question, sources):
    blocks = []
    for number, source in enumerate(sources, start=1):
        header = f"[{number}] ({source['filename']}, chunk {source['chunk_index']})"
        blocks.append(f"{header}\n{source['text']}")
    context = "\n\n".join(blocks)
    return f"Sources:\n\n{context}\n\nQuestion: {question}"


@lru_cache(maxsize=1)
def _get_client():
    if not config.AZURE_OPENAI_ENDPOINT:
        raise LLMError("Set AZURE_OPENAI_ENDPOINT to your Azure AI endpoint")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), AZURE_TOKEN_SCOPE
    )
    return OpenAI(
        base_url=config.AZURE_OPENAI_ENDPOINT,
        api_key=token_provider,
        timeout=config.LLM_TIMEOUT,
    )


def generate(question, sources):
    if not sources:
        return NO_SOURCES_ANSWER

    try:
        response = _get_client().responses.create(
            model=config.AZURE_OPENAI_DEPLOYMENT,
            instructions=SYSTEM,
            input=build_prompt(question, sources),
        )
    except (AzureError, OpenAIError) as e:
        raise LLMError(f"Azure OpenAI request failed: {e}") from e

    return response.output_text


def extract_citations(answer, n_sources):
    found = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}

    return sorted(n for n in found if 1 <= n <= n_sources)