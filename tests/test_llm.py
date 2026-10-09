from types import SimpleNamespace

import pytest

from app import config, llm


SOURCES = [
    {
        "filename": "contract.txt",
        "chunk_index": 2,
        "text": "Payment is due within 30 days.",
    }
]


def test_build_prompt_includes_source_metadata_and_text():
    prompt = llm.build_prompt("When is payment due?", SOURCES)

    assert "[1] (contract.txt, chunk 2)" in prompt
    assert "Payment is due within 30 days." in prompt
    assert "Question: When is payment due?" in prompt


def test_generate_uses_responses_api_and_returns_output_text(monkeypatch):
    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="Payment is due within 30 days. [1]")

    monkeypatch.setattr(llm, "_get_client", lambda: SimpleNamespace(responses=FakeResponses()))
    monkeypatch.setattr(config, "AZURE_OPENAI_DEPLOYMENT", "test-deployment")

    answer = llm.generate("When is payment due?", SOURCES)

    assert answer == "Payment is due within 30 days. [1]"
    assert captured == {
        "model": "test-deployment",
        "instructions": llm.SYSTEM,
        "input": llm.build_prompt("When is payment due?", SOURCES),
    }


def test_generate_returns_no_sources_answer_without_calling_model(monkeypatch):
    def fail_if_called():
        pytest.fail("Azure OpenAI client should not be created without sources")

    monkeypatch.setattr(llm, "_get_client", fail_if_called)

    assert llm.generate("Question?", []) == llm.NO_SOURCES_ANSWER


def test_get_client_requires_endpoint(monkeypatch):
    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "")
    llm._get_client.cache_clear()
    try:
        with pytest.raises(llm.LLMError, match="AZURE_OPENAI_ENDPOINT"):
            llm._get_client()
    finally:
        llm._get_client.cache_clear()


def test_get_client_configures_azure_identity_and_endpoint(monkeypatch):
    captured = {}
    token_provider = lambda: "access-token"
    credential = object()
    client = object()

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return client

    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "https://example/openai/v1")
    monkeypatch.setattr(llm, "DefaultAzureCredential", lambda: credential)
    monkeypatch.setattr(
        llm,
        "get_bearer_token_provider",
        lambda actual_credential, scope: (
            captured.update(credential=actual_credential, scope=scope) or token_provider
        ),
    )
    monkeypatch.setattr(llm, "OpenAI", fake_openai)
    llm._get_client.cache_clear()
    try:
        assert llm._get_client() is client
        assert captured == {
            "credential": credential,
            "scope": "https://ai.azure.com/.default",
            "base_url": "https://example/openai/v1",
            "api_key": token_provider,
            "timeout": config.LLM_TIMEOUT,
        }
    finally:
        llm._get_client.cache_clear()
