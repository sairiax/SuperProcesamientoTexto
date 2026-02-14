"""Shared fixtures for ExtractorRunner tests."""

import pytest

from text_toolkit.extractors import ExtractorRunner


@pytest.fixture
def extractor_runner():
    """Fixture that provides an ExtractorRunner instance."""
    return ExtractorRunner()
