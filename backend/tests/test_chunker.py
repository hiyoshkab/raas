import pytest

from app_backend.chunker import chunk_text


def test_chunk_text_splits_words_into_chunks():
    assert chunk_text("one two three four five", chunk_size=2) == [
        "one two",
        "three four",
        "five",
    ]


def test_chunk_text_overlaps_adjacent_chunks():
    assert chunk_text("one two three four five", chunk_size=3, overlap=1) == [
        "one two three",
        "three four five",
    ]


def test_chunk_text_returns_empty_list_for_whitespace():
    assert chunk_text(" \n\t ", chunk_size=3) == []


@pytest.mark.parametrize("chunk_size", [0, -1])
def test_chunk_text_rejects_non_positive_chunk_size(chunk_size):
    with pytest.raises(ValueError, match="(?i)chunk size"):
        chunk_text("some text", chunk_size=chunk_size)


@pytest.mark.parametrize("overlap", [-1, 3])
def test_chunk_text_rejects_invalid_overlap(overlap):
    with pytest.raises(ValueError, match="(?i)overlap"):
        chunk_text("some text", chunk_size=3, overlap=overlap)
