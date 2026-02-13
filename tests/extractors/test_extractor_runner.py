import pytest

from text_toolkit.extractors import ExtractorRunner
from text_toolkit.models.text_document import ExtractionResult, TextDocument
from text_toolkit.transformers import TransformerPipeline


@pytest.fixture
def extractor_runner():
    """Fixture that provides an ExtractorRunner instance."""
    return ExtractorRunner()


def test_extractor_runner_initialization(extractor_runner):
    """Should verify that ExtractorRunner initializes with all core extractors."""
    assert extractor_runner.email_extractor is not None
    assert extractor_runner.url_extractor is not None
    assert extractor_runner.date_extractor is not None


def test_extractor_runner_extract_all_method(extractor_runner, pipeline: TransformerPipeline):
    """Should extract all types of data from a document."""
    document = TextDocument(
        content="Contact: admin@example.com, visit https://example.com on 2026-03-15",
        pipeline=pipeline,
    )
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert "admin@example.com" in result.email_matches
    assert "https://example.com" in result.url_matches
    assert "2026-03-15" in result.date_matches


@pytest.mark.parametrize(
    "unique_occurrences, expected_email_count",
    [
        (True, 1),
        (False, 2),
    ],
    ids=["unique", "duplicates"],
)
def test_extractor_runner_unique_occurrences(
    extractor_runner, pipeline: TransformerPipeline, unique_occurrences, expected_email_count
):
    """Should respect unique_occurrences parameter."""
    document = TextDocument(
        content="Emails: admin@test.com, admin@test.com",
        pipeline=pipeline,
    )
    result = extractor_runner.extract_all(document, unique_occurrences=unique_occurrences)

    assert len(result.email_matches) == expected_email_count


def test_extractor_runner_empty_document(extractor_runner, empty_doc):
    """Should return empty result for empty document."""
    result = extractor_runner.extract_all(empty_doc)

    assert result.email_matches == []
    assert result.url_matches == []
    assert result.date_matches == []
