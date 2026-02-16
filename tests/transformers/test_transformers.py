import pytest

from text_toolkit.transformers.cleaner import Cleaner
from text_toolkit.transformers.normalizer import Normalizer
from text_toolkit.transformers.pipeline import TransformerPipeline
from text_toolkit.transformers.tokenizer import Tokenizer


def test_normalizer_basic():
    n = Normalizer()
    assert n.normalize_text("  ÁRBOL  ") == "arbol"


def test_normalize_removes_extra_spaces():
    n = Normalizer()
    assert n.normalize_text("hello   world") == "hello world"


def test_cleaner_preserves_emails_urls_dates():
    c = Cleaner()
    text = """16 Feb 2026 Contacta: test@example.com!!! 
    o visita https://example.com?? antes de 15/03/2026!"""
    cleaned = c.clean_text(text)

    assert "test@example.com" in cleaned
    assert "test@example.com!!!" not in cleaned
    assert "https://example.com" in cleaned
    assert "!" not in cleaned
    assert "?" not in cleaned
    assert "16 Feb 2026" in cleaned
    assert "15/03/2026" in cleaned
    assert "15/03/2026!" not in cleaned


def test_tokenizer_splits_by_spaces():
    t = Tokenizer()
    tokens = t.tokenize_text("hola   mundo  prueba")
    assert tokens == ["hola", "mundo", "prueba"]


def test_transformer_pipeline_integration():
    pipeline = TransformerPipeline(
        tokenizer=Tokenizer(), cleaner=Cleaner(), normalizer=Normalizer()
    )
    text = "  HOLA   mundo!!!  "
    # Cleaner replaces "!" with space -> "  HOLA   mundo     "
    # Normalizer lowercases and strips -> "hola mundo"
    # Tokenizer splits -> ["hola", "mundo"]
    tokens = pipeline.transform(text)
    assert tokens == ["hola", "mundo"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
