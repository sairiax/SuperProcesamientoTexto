import pytest

from text_toolkit.extractors import ExtractorRunner
from text_toolkit.models.extraction_result import ExtractionResult
from text_toolkit.models.text_document import TextDocument
from text_toolkit.transformers import TransformerPipeline


def test_extractor_runner_initialization(extractor_runner: ExtractorRunner):
    """Should verify that ExtractorRunner initializes with all core extractors."""
    assert extractor_runner.extractors is not None
    assert 'email' in extractor_runner.extractors
    assert 'url' in extractor_runner.extractors
    assert 'date' in extractor_runner.extractors
    assert len(extractor_runner.extractors) == 3


def test_extractor_runner_initialization_with_specific_extractors():
    """Should initialize with only specified extractors."""
    runner = ExtractorRunner(extractor_names=['EmailExtractor', 'URLExtractor'])

    assert len(runner.extractors) == 2
    assert 'email' in runner.extractors
    assert 'url' in runner.extractors
    assert 'date' not in runner.extractors


def test_extractor_runner_initialization_single_extractor():
    """Should initialize with a single extractor."""
    runner = ExtractorRunner(extractor_names=['EmailExtractor'])

    assert len(runner.extractors) == 1
    assert 'email' in runner.extractors
    assert 'url' not in runner.extractors
    assert 'date' not in runner.extractors


def test_extractor_runner_extract_all_method(
    extractor_runner: ExtractorRunner,
    pipeline: TransformerPipeline
):
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
    extractor_runner: ExtractorRunner,
    pipeline: TransformerPipeline,
    unique_occurrences: bool,
    expected_email_count: int
):
    """Should respect unique_occurrences parameter."""
    document = TextDocument(
        content="Emails: admin@test.com, admin@test.com",
        pipeline=pipeline,
    )
    result = extractor_runner.extract_all(document, unique_occurrences=unique_occurrences)

    assert len(result.email_matches) == expected_email_count


def test_extractor_runner_empty_document(extractor_runner:ExtractorRunner, empty_doc: TextDocument):
    """Should return empty result for empty document."""
    result = extractor_runner.extract_all(empty_doc)

    assert result.email_matches == []
    assert result.url_matches == []
    assert result.date_matches == []


def test_extractor_runner_with_single_email_extractor(pipeline: TransformerPipeline):
    """Should only extract emails when only EmailExtractor is enabled."""
    runner = ExtractorRunner(extractor_names=['EmailExtractor'])
    document = TextDocument(
        content="Contact: admin@example.com, visit https://example.com on 2026-03-15",
        pipeline=pipeline,
    )
    result = runner.extract_all(document)

    assert "admin@example.com" in result.email_matches
    assert len(result.url_matches) == 0  # URL not extracted
    assert len(result.date_matches) == 0  # Date not extracted


def test_extractor_runner_with_multiple_specific_extractors(pipeline: TransformerPipeline):
    """Should extract only from specified extractor types."""
    runner = ExtractorRunner(extractor_names=['EmailExtractor', 'DateExtractor'])
    document = TextDocument(
        content="Contact: admin@example.com, visit https://example.com on 2026-03-15",
        pipeline=pipeline,
    )
    result = runner.extract_all(document)

    assert "admin@example.com" in result.email_matches
    assert "2026-03-15" in result.date_matches
    assert len(result.url_matches) == 0  # URL not extracted


def test_extractor_runner_repr_includes_active_extractors(
    extractor_runner: ExtractorRunner,
) -> None:
    """__repr__ should summarize which extractor types are active."""
    representation = repr(extractor_runner)

    assert "ExtractorRunner(" in representation
    assert "email" in representation
    assert "url" in representation
    assert "date" in representation
