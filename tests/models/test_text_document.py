from pathlib import Path

from text_toolkit.models.text_document import TextDocument
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer, TransformerPipeline


def _make_document(content: str = "Hola mundo") -> TextDocument:
    pipeline = TransformerPipeline(
        tokenizer=Tokenizer(),
        cleaner=Cleaner(),
        normalizer=Normalizer(),
    )
    return TextDocument(
        content=content,
        pipeline=pipeline,
        source_path=Path("sample.txt"),
        metadata={"author": "tester"},
    )


def test_tokens_are_lazy_and_cached() -> None:
    doc = _make_document("Hola mundo prueba")

    first_tokens = doc.tokens
    second_tokens = doc.tokens

    assert first_tokens == ["hola", "mundo", "prueba"]
    assert first_tokens is second_tokens


def test_analysis_helpers_store_and_retrieve_results() -> None:
    doc = _make_document()

    assert not doc.has_analysis("frequency")
    assert doc.get_analysis("frequency") is None

    doc.add_analysis("frequency", {"total_words": 2})

    assert doc.has_analysis("frequency")
    assert doc.get_analysis("frequency") == {"total_words": 2}


def test_is_empty_flag_for_documents() -> None:
    empty_doc = _make_document("   \n  ")
    non_empty_doc = _make_document("contenido")

    assert empty_doc.is_empty() is True
    assert non_empty_doc.is_empty() is False


def test_text_document_repr_contains_key_information() -> None:
    doc = _make_document("Hola mundo")

    representation = repr(doc)

    assert "TextDocument(" in representation
    assert "content_len=" in representation
    assert "metadata_keys=" in representation
    assert "analysis_keys=" in representation
    assert "tokens_cached=" in representation

