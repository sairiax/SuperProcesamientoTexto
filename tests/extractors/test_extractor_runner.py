import pytest

from text_toolkit.extractors.core import (
    DateExtractor,
    URLExtractor,
    EmailExtractor,
)
from text_toolkit.extractors import ExtractorRunner
from text_toolkit.models.text_document import TextDocument, ExtractionResult

@pytest.fixture
def extractor_runner():
    """Fixture that provides an ExtractorRunner instance."""
    return ExtractorRunner()


def test_extractorengine_initialization(extractor_runner):
    """Should initialize the engine with all available extractors."""
    assert hasattr(extractor_runner, 'email_extractor'), "Should have email_extractor"
    assert hasattr(extractor_runner, 'url_extractor'), "Should have url_extractor"
    assert hasattr(extractor_runner, 'date_extractor'), "Should have date_extractor"
    assert isinstance(extractor_runner.email_extractor, EmailExtractor), "email_extractor should be EmailExtractor instance"
    assert isinstance(extractor_runner.url_extractor, URLExtractor), "url_extractor should be URLExtractor instance"
    assert isinstance(extractor_runner.date_extractor, DateExtractor), "date_extractor should be DateExtractor instance"

def test_extractorengine_extract_all_method(extractor_runner):
    """Should extract emails, URLs and dates simultaneously."""
    document = TextDocument(content="Contact: admin@example.com, visit https://example.com on 2026-03-15")
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == 1, "Should extract 1 email"
    assert len(result.url_matches) == 1, "Should extract 1 URL"
    assert len(result.date_matches) == 1, "Should extract 1 date"

def test_extractorengine_extract_all_returns_extraction_result(extractor_runner):
    """Should return an ExtractionResult object with all matches."""
    document = TextDocument(content="Email: test@example.com, URL: http://test.com, Date: 2026-01-01")
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert hasattr(result, 'email_matches'), "ExtractionResult should have email_matches"
    assert hasattr(result, 'url_matches'), "ExtractionResult should have url_matches"
    assert hasattr(result, 'date_matches'), "ExtractionResult should have date_matches"
    assert "test@example.com" in result.email_matches, "Should extract test@example.com"
    assert "http://test.com" in result.url_matches, "Should extract http://test.com"
    assert "2026-01-01" in result.date_matches, "Should extract 2026-01-01"

def test_extractorengine_extract_all_with_unique_occurrences(extractor_runner):
    """Should remove duplicates when unique_occurrences=True."""
    document = TextDocument(
        content="Emails: admin@test.com, admin@test.com, URLs: https://test.com, https://test.com, Dates: 2026-01-15, 2026-01-15"
    )
    result = extractor_runner.extract_all(document, unique_occurrences=True)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == 1, "Should return 1 unique email"
    assert len(result.url_matches) == 1, "Should return 1 unique URL"
    assert len(result.date_matches) == 1, "Should return 1 unique date"

def test_extractorengine_extract_all_with_duplicates(extractor_runner):
    """Should include duplicates when unique_occurrences=False."""
    document = TextDocument(
        content="Emails: admin@test.com, admin@test.com, URLs: https://test.com, https://test.com, Dates: 2026-01-15, 2026-01-15"
    )
    result = extractor_runner.extract_all(document, unique_occurrences=False)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == 2, "Should return 2 email occurrences (including duplicates)"
    assert len(result.url_matches) == 2, "Should return 2 URL occurrences (including duplicates)"
    assert len(result.date_matches) == 2, "Should return 2 date occurrences (including duplicates)"

def test_extractorengine_extract_from_empty_document(extractor_runner):
    """Should handle empty documents without errors."""
    document = TextDocument(content="")
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == 0, "Should return 0 email matches"
    assert len(result.url_matches) == 0, "Should return 0 URL matches"
    assert len(result.date_matches) == 0, "Should return 0 date matches"
    assert result.email_matches == [], "Email matches should be empty list"
    assert result.url_matches == [], "URL matches should be empty list"
    assert result.date_matches == [], "Date matches should be empty list"

def test_extractorengine_extract_from_document_with_no_matches(extractor_runner):
    """Should return empty lists when there are no matches."""
    document = TextDocument(content="Este es un texto simple sin datos extraíbles")
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert len(result.email_matches) == 0, "Should return 0 email matches"
    assert len(result.url_matches) == 0, "Should return 0 URL matches"
    assert len(result.date_matches) == 0, "Should return 0 date matches"
    assert result.email_matches == [], "Email matches should be empty list"
    assert result.url_matches == [], "URL matches should be empty list"
    assert result.date_matches == [], "Date matches should be empty list"

def test_extractorengine_extraction_result_structure(extractor_runner):
    """Should verify that ExtractionResult contains the expected fields."""
    document = TextDocument(content="Test content: user@example.com, https://example.com, 2026-02-15")
    result = extractor_runner.extract_all(document)

    assert isinstance(result, ExtractionResult), "Should return ExtractionResult instance"
    assert isinstance(result.email_matches, list), "email_matches should be a list"
    assert isinstance(result.url_matches, list), "url_matches should be a list"
    assert isinstance(result.date_matches, list), "date_matches should be a list"