"""Shared fixtures for analyzer tests."""

import pytest

from procesamientotexto.models.text_document import TextDocument


@pytest.fixture
def empty_doc():
    """Empty document for edge case testing."""
    return TextDocument(content="")


@pytest.fixture
def english_doc():
    """English text with positive sentiment."""
    return TextDocument(content="This is a great day. I love English! It is excellent and amazing.")


@pytest.fixture
def spanish_doc():
    """Spanish text with positive sentiment."""
    return TextDocument(
        content="Este es un día excelente. Me encanta el español! Es maravilloso e increíble."
    )


@pytest.fixture
def chinese_doc():
    """Chinese text for testing language detection edge cases."""
    return TextDocument(content="这是一个美好的一天。我喜欢学习中文非常好。")


@pytest.fixture
def negative_sentiment_doc():
    """Document with negative sentiment."""
    return TextDocument(
        content="This is a terrible day. I hate this awful situation. It is horrible and bad."
    )


@pytest.fixture
def neutral_sentiment_doc():
    """Document with neutral sentiment (no sentiment words)."""
    return TextDocument(
        content="""The document contains several sentences. The data was processed yesterday.
        Results are available now."""
    )


@pytest.fixture
def mixed_doc():
    """Complex document with multiple sentences and mixed characteristics."""
    return TextDocument(
        content="""
        The quick brown fox jumps over the lazy dog. This is a sentence with moderate complexity.
        Another sentence follows here. Testing readability metrics requires varied sentence
        structures. Short one. This is getting more complex as we add additional subordinate clauses
         and longer words.
        """
    )
