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
