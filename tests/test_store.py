import pytest
from qdrant_client import QdrantClient

from app import store


@pytest.fixture
def qdrant():
    client = QdrantClient(location=":memory:")
    store.ensure_collection(client, "documents", vector_size=3)
    yield client
    client.close()


def test_ensure_collection_is_idempotent(qdrant):
    store.ensure_collection(qdrant, "documents", vector_size=3)

    assert [collection.name for collection in qdrant.get_collections().collections] == [
        "documents"
    ]


def test_upsert_chunks_stores_searchable_payload(qdrant):
    count = store.upsert_chunks(
        qdrant,
        "documents",
        "contract.txt",
        ["payment is due in 30 days", "the agreement renews annually"],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
    )

    results = store.search(qdrant, "documents", [1.0, 0.0, 0.0], limit=1)

    assert count == 2
    assert results == [
        (
            pytest.approx(1.0),
            {
                "filename": "contract.txt",
                "chunk_index": 0,
                "text": "payment is due in 30 days",
            },
        )
    ]


def test_upsert_chunks_returns_zero_for_no_chunks(qdrant):
    assert store.upsert_chunks(qdrant, "documents", "empty.txt", [], []) == 0


def test_search_returns_empty_list_for_empty_collection(qdrant):
    assert store.search(qdrant, "documents", [1.0, 0.0, 0.0]) == []
