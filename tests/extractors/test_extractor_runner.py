import pytest

from text_toolkit.extractors import ExtractorRunner
from text_toolkit.extractors.core import (
    DateExtractor,
    EmailExtractor,
    URLExtractor,
)
from text_toolkit.models.text_document import ExtractionResult, TextDocument


@pytest.fixture
def extractor_runner():
    """Fixture that provides an ExtractorRunner instance."""
    return ExtractorRunner()


def test_extractorengine_initialization(extractor_runner: ExtractorRunner):
    """Should initialize the engine with all available extractors."""
    assert hasattr(extractor_runner, "email_extractor"), "Should have email_extractor"
    assert hasattr(extractor_runner, "url_extractor"), "Should have url_extractor"
    assert hasattr(extractor_runner, "date_extractor"), "Should have date_extractor"
    assert isinstance(
        extractor_runner.email_extractor,
        EmailExtractor,
    ), "email_extractor should be EmailExtractor instance"
    assert isinstance(
        extractor_runner.url_extractor,
        URLExtractor,
    ), "url_extractor should be URLExtractor instance"
    assert isinstance(
        extractor_runner.date_extractor,
        DateExtractor,
    ), "date_extractor should be DateExtractor instance"


@pytest.mark.parametrize(
    "content, expected_emails, expected_urls, expected_dates",
    [
        (
            "Contact: admin@example.com, visit https://example.com on 2026-03-15",
            ["admin@example.com"],
            ["https://example.com"],
            ["2026-03-15"],
        ),
        (
            "Email: test@example.com, URL: http://test.com, Date: 2026-01-01",
            ["test@example.com"],
            ["http://test.com"],
            ["2026-01-01"],
        ),
        ("", [], [], []),
        ("Este es un texto simple sin datos extraibles", [], [], []),
    ],
    ids=[
        "extract_all",
        "extract_all_with_content",
        "empty_document",
        "no_matches",
    ],
)
def test_extractorengine_extract_all_expected_matches(
    extractor_runner: ExtractorRunner,
    content: str,
    expected_emails: list[str],
    expected_urls: list[str],
    expected_dates: list[str],
):
    """Should extract emails, URLs and dates for different documents."""
    document = TextDocument(content=content)
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert hasattr(result, "email_matches"), "ExtractionResult should have email_matches"
    assert hasattr(result, "url_matches"), "ExtractionResult should have url_matches"
    assert hasattr(result, "date_matches"), "ExtractionResult should have date_matches"
    assert len(result.email_matches) == len(expected_emails)
    assert len(result.url_matches) == len(expected_urls)
    assert len(result.date_matches) == len(expected_dates)
    for email in expected_emails:
        assert email in result.email_matches
    for url in expected_urls:
        assert url in result.url_matches
    for date in expected_dates:
        assert date in result.date_matches

@pytest.mark.parametrize(
    "unique_occurrences, expected_count",
    [
        (True, 1),
        (False, 2),
    ],
    ids=[
        "unique_occurrences",
        "allow_duplicates",
    ],
)
def test_extractorengine_extract_all_occurrence_modes(
    extractor_runner: ExtractorRunner,
    unique_occurrences: bool,
    expected_count: int,
):
    """Should include or remove duplicates depending on unique_occurrences."""
    document = TextDocument(
        content=(
            "Emails: admin@test.com, admin@test.com, URLs: https://test.com, "
            "https://test.com, Dates: 2026-01-15, 2026-01-15"
        )
    )
    result = extractor_runner.extract_all(document, unique_occurrences=unique_occurrences)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == expected_count
    assert len(result.url_matches) == expected_count
    assert len(result.date_matches) == expected_count

def test_extractorengine_extraction_result_structure(extractor_runner: ExtractorRunner):
    """Should verify that ExtractionResult contains the expected fields."""
    document = TextDocument(
        content="Test content: user@example.com, https://example.com, 2026-02-15"
    )
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert isinstance(result.email_matches, list), "email_matches should be a list"
    assert isinstance(result.url_matches, list), "url_matches should be a list"
    assert isinstance(result.date_matches, list), "date_matches should be a list"
