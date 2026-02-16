"""Shared fixtures for analyzer tests."""

import pytest

from text_toolkit.models.text_document import TextDocument
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer, TransformerPipeline


@pytest.fixture
def pipeline() -> TransformerPipeline:
    """Standard pipeline for testing."""
    return TransformerPipeline(
        tokenizer=Tokenizer(),
        cleaner=Cleaner(),
        normalizer=Normalizer(),
    )


@pytest.fixture
def empty_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Empty document for edge case testing."""
    return TextDocument(content="", pipeline=pipeline)


@pytest.fixture
def english_doc(pipeline: TransformerPipeline) -> TextDocument:
    """English text with positive sentiment."""
    return TextDocument(
        content="This is a great day. I love English! It is excellent and amazing.",
        pipeline=pipeline,
    )


@pytest.fixture
def spanish_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Spanish text with positive sentiment."""
    return TextDocument(
        content="Este es un día excelente. Me encanta el español! Es maravilloso e increíble.",
        pipeline=pipeline,
    )


@pytest.fixture
def chinese_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Chinese text for testing language detection edge cases."""
    return TextDocument(content="这是一个美好的一天。我喜欢学习中文非常好。", pipeline=pipeline)


@pytest.fixture
def negative_sentiment_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Document with negative sentiment."""
    return TextDocument(
        content="This is a terrible day. I hate this awful situation. It is horrible and bad.",
        pipeline=pipeline,
    )


@pytest.fixture
def neutral_sentiment_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Document with neutral sentiment (no sentiment words)."""
    return TextDocument(
        content="""The document contains several sentences. The data was processed yesterday.
        Results are available now.""",
        pipeline=pipeline,
    )


@pytest.fixture
def mixed_doc(pipeline: TransformerPipeline) -> TextDocument:
    """Complex document with multiple sentences and mixed characteristics."""
    return TextDocument(
        content="""
        The quick brown fox jumps over the lazy dog. This is a sentence with moderate complexity.
        Another sentence follows here. Testing readability metrics requires varied sentence
        structures. Short one. This is getting more complex as we add additional subordinate clauses
         and longer words.
        """,
        pipeline=pipeline,
    )
