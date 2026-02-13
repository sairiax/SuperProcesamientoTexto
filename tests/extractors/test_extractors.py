import pytest

from text_toolkit.extractors.core import (
    CustomExtractor,
    DateExtractor,
    EmailExtractor,
    URLExtractor,
)
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer, TransformerPipeline

# --- Fixtures for extractors


@pytest.fixture
def pipeline() -> TransformerPipeline:
    """Standard pipeline for testing."""
    return TransformerPipeline(
        tokenizer=Tokenizer(),
        cleaner=Cleaner(),
        normalizer=Normalizer(),
    )


@pytest.fixture
def email_extractor():
    """Fixture that provides an EmailExtractor instance."""
    return EmailExtractor()


@pytest.fixture
def date_extractor():
    """Fixture that provides a DateExtractor instance."""
    return DateExtractor()


@pytest.fixture
def url_extractor():
    """Fixture that provides a URLExtractor instance."""
    return URLExtractor()


# --- EmailExtractor Tests


def test_emailextractor_extract_single_email(email_extractor):
    """Should extract a single email from text."""
    example_text = "Contact mail: admin@example.com"
    extracted_data = email_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 email ocurrence"
    assert extracted_data[0] == "admin@example.com", (
        "Email extracted should match: admin@example.com"
    )


def test_emailextractor_extract_multiple_emails(email_extractor):
    """Should extract multiple emails from text."""
    example_text = "Contactos: admin@example.com, support@test.com, info@company.org"
    extracted_data = email_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 3, "Should return 3 email ocurrences"
    assert "admin@example.com" in extracted_data, "Email extracted should match: admin@example.com"
    assert "support@test.com" in extracted_data, "Email extracted should match: support@test.com"
    assert "info@company.org" in extracted_data, "Email extracted should match: info@company.org"


def test_emailextractor_extract_email_with_plus_sign(email_extractor):
    """Should extract emails with plus sign (tags)."""
    example_text = "Email: user+tag@example.com"
    extracted_data = email_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 email ocurrences"
    assert extracted_data[0] == "user+tag@example.com", (
        "Email extracted should match: user+tag@example.com"
    )


def test_emailextractor_extract_multiple_email_patterns(email_extractor):
    """Should extract emails with multiple complex formats."""
    example_text = """
    Project contact team:
    - Administrator: admin@example.com
    - Technical Support: support@example.com.mx
    - Sales: sales.team@company.co.uk
    - Development: dev+backend@tech-startup.io
    - Marketing: contact_marketing@agency.com
    For more information: info@help-center.org
    """

    extracted_data = email_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure must be a List"
    assert len(extracted_data) == 6, "Should return 6 email occurrences"
    assert "admin@example.com" in extracted_data, "Should extract admin@example.com"
    assert "support@example.com.mx" in extracted_data, "Should extract support@example.com.mx"
    assert "sales.team@company.co.uk" in extracted_data, "Should extract sales.team@company.co.uk"
    assert "dev+backend@tech-startup.io" in extracted_data, (
        "Should extract dev+backend@tech-startup.io"
    )


# --- DateExtractor Tests


def test_dateextractor_extract_single_date(date_extractor):
    """Should extract a single date in ISO format."""
    example_text = "The event is scheduled for 2026-02-15"
    extracted_data = date_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 date occurrence"
    assert extracted_data[0] == "2026-02-15", "Date extracted should match: 2026-02-15"


def test_dateextractor_extract_iso_format(date_extractor):
    """Should extract dates in ISO format (YYYY-MM-DD)."""
    example_text = "Meeting on 2026-03-20 and deadline 2026-04-10"
    extracted_data = date_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 2, "Should return 2 date occurrences"
    assert "2026-03-20" in extracted_data, "Date extracted should match: 2026-03-20"
    assert "2026-04-10" in extracted_data, "Date extracted should match: 2026-04-10"


def test_dateextractor_extract_slash_format(date_extractor):
    """Should extract dates with slashes (DD/MM/YYYY)."""
    example_text = "Birth date: 15/08/1990"
    extracted_data = date_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 date occurrence"
    assert extracted_data[0] == "15/08/1990", "Date extracted should match: 15/08/1990"


def test_dateextractor_extract_month_name_format(date_extractor):
    """Should extract dates with month names (10 Feb 2026)."""
    example_text = "Conference starts on 10 Feb 2026"
    extracted_data = date_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 date occurrence"
    assert extracted_data[0] == "10 Feb 2026", "Date extracted should match: 10 Feb 2026"


def test_dateextractor_extract_mixed_formats(date_extractor):
    """Should extract dates in different formats in the same text."""
    example_text = "Event on 2026-01-15, meeting 20/03/2026, and deadline 10-Apr-2026"
    extracted_data = date_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 3, "Should return 3 date occurrences"
    assert "2026-01-15" in extracted_data, "Date extracted should match: 2026-01-15"
    assert "20/03/2026" in extracted_data, "Date extracted should match: 20/03/2026"
    assert "10-Apr-2026" in extracted_data, "Date extracted should match: 10-Apr-2026"


# --- URLExtractor Tests


def test_urlextractor_extract_http_url(url_extractor):
    """Should extract URLs with HTTP protocol."""
    example_text = "Visit our site at http://example.com for more info"
    extracted_data = url_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 URL occurrence"
    assert extracted_data[0] == "http://example.com", (
        "URL extracted should match: http://example.com"
    )


def test_urlextractor_extract_https_url(url_extractor):
    """Should extract URLs with HTTPS protocol."""
    example_text = "Secure connection: https://secure.example.com"
    extracted_data = url_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 URL occurrence"
    assert extracted_data[0] == "https://secure.example.com", (
        "URL extracted should match: https://secure.example.com"
    )


def test_urlextractor_extract_ftp_url(url_extractor):
    """Should extract URLs with FTP protocol."""
    example_text = "Download file from ftp://ftp.example.com/file.zip"
    extracted_data = url_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 URL occurrence"
    assert extracted_data[0] == "ftp://ftp.example.com/file.zip", (
        "URL extracted should match: ftp://ftp.example.com/file.zip"
    )


def test_urlextractor_extract_www_url(url_extractor):
    """Should extract URLs with www without protocol."""
    example_text = "Check www.example.com for details"
    extracted_data = url_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 URL occurrence"
    assert extracted_data[0] == "www.example.com", "URL extracted should match: www.example.com"


def test_urlextractor_extract_url_with_path(url_extractor):
    """Should extract URLs with paths and subdirectories."""
    example_text = "Documentation at https://docs.example.com/api/v1/documentation"
    extracted_data = url_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 1, "Should return 1 URL occurrence"
    assert extracted_data[0] == "https://docs.example.com/api/v1/documentation", (
        "URL extracted should match: https://docs.example.com/api/v1/documentation"
    )


# --- CustomExtractor Tests


def test_customextractor_create_with_single_pattern():
    """Should create a custom extractor with a single pattern."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])

    assert phone_extractor.name == "phone", "Extractor name should be 'phone'"
    assert len(phone_extractor._extractor._regex_pattern_list) == 1, "Should have 1 pattern"


def test_customextractor_create_with_multiple_patterns():
    """Should create a custom extractor with multiple patterns."""
    phone_extractor = CustomExtractor(
        name="phone", patterns=[r"\d{3}-\d{3}-\d{4}", r"\(\d{3}\)\s*\d{3}-\d{4}"]
    )

    assert phone_extractor.name == "phone", "Extractor name should be 'phone'"
    assert len(phone_extractor._extractor._regex_pattern_list) == 2, "Should have 2 patterns"


def test_customextractor_extract_phone_numbers():
    """Should extract phone numbers with custom patterns."""
    phone_extractor = CustomExtractor(
        name="phone", patterns=[r"\d{3}-\d{3}-\d{4}", r"\(\d{3}\)\s*\d{3}-\d{4}"]
    )
    example_text = "Call 555-123-4567 or (555) 987-6543 for assistance"
    extracted_data = phone_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 2, "Should return 2 phone occurrences"
    assert "555-123-4567" in extracted_data, "Phone extracted should match: 555-123-4567"
    assert "(555) 987-6543" in extracted_data, "Phone extracted should match: (555) 987-6543"


def test_customextractor_extract_ip_addresses():
    """Should extract IP addresses with custom pattern."""
    ip_extractor = CustomExtractor(
        name="ip_address", patterns=[r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"]
    )
    example_text = "Server at 192.168.1.1 and backup at 10.0.0.5"
    extracted_data = ip_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 2, "Should return 2 IP occurrences"
    assert "192.168.1.1" in extracted_data, "IP extracted should match: 192.168.1.1"
    assert "10.0.0.5" in extracted_data, "IP extracted should match: 10.0.0.5"


def test_customextractor_no_matches_found():
    """Should return empty list when no matches are found."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])
    example_text = "Este texto no contiene números de teléfono"
    extracted_data = phone_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 0, "Should return 0 occurrences"
    assert extracted_data == [], "Extracted data should be an empty list"


def test_customextractor_empty_string():
    """Should handle empty string without errors."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])
    extracted_data = phone_extractor.extract("")

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 0, "Should return 0 occurrences"
    assert extracted_data == [], "Extracted data should be an empty list"


def test_customextractor_extract_with_duplicates():
    """Should include duplicates by default (unique_occurrences=False)."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])
    example_text = "Numbers: 555-123-4567, 555-987-6543, 555-123-4567"
    extracted_data = phone_extractor.extract(example_text, unique_occurrences=False)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 3, "Should return 3 occurrences"
    assert extracted_data.count("555-123-4567") == 2, (
        "Should return 2 occurrences for phone '555-123-4567'"
    )
    assert extracted_data.count("555-987-6543") == 1, (
        "Should return 1 occurrence for phone '555-987-6543'"
    )


def test_customextractor_extract_unique_occurrences():
    """Should remove duplicates when unique_occurrences=True."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])
    example_text = "Numbers: 555-123-4567, 555-987-6543, 555-123-4567"
    extracted_data = phone_extractor.extract(example_text, unique_occurrences=True)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 2, "Should return 2 occurrences"
    assert "555-123-4567" in extracted_data, "Should return 1 occurrence for phone '555-123-4567'"
    assert "555-987-6543" in extracted_data, "Should return 1 occurrence for phone '555-987-6543'"


def test_customextractor_invalid_regex_pattern():
    """Should raise ValueError when regex pattern is invalid."""
    with pytest.raises(ValueError) as exc_info:
        CustomExtractor(name="invalid", patterns=[r"[invalid(regex"])

    assert "Invalid regex pattern" in str(exc_info.value), (
        "Should raise ValueError with proper message"
    )


def test_customextractor_add_patterns_dynamically():
    """Should allow adding patterns dynamically after creation."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])

    assert len(phone_extractor._extractor._regex_pattern_list) == 1, (
        "Should have 1 pattern initially"
    )
    phone_extractor.add_patterns([r"\(\d{3}\)\s*\d{3}-\d{4}"])
    assert len(phone_extractor._extractor._regex_pattern_list) == 2, (
        "Should have 2 patterns after adding"
    )
    example_text = "Call 555-123-4567 or (555) 987-6543"
    extracted_data = phone_extractor.extract(example_text)
    assert len(extracted_data) == 2, "Should extract with both patterns"


def test_customextractor_extract_with_mixed_patterns():
    """Should extract multiple types of data with different patterns."""
    mixed_extractor = CustomExtractor(
        name="mixed",
        patterns=[
            r"\d{3}-\d{3}-\d{4}",  # Phone
            r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP
        ],
    )
    example_text = "Contact: 555-123-4567, Server: 192.168.1.1"
    extracted_data = mixed_extractor.extract(example_text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 2, "Should return 2 occurrences"
    assert "555-123-4567" in extracted_data, "Should extract phone number"
    assert "192.168.1.1" in extracted_data, "Should extract IP address"


def test_customextractor_empty_pattern_list():
    """Should handle empty pattern list."""
    empty_extractor = CustomExtractor(name="empty", patterns=[])

    assert len(empty_extractor._extractor._regex_pattern_list) == 0, "Should have 0 patterns"
    example_text = "Some text with data"
    extracted_data = empty_extractor.extract(example_text)
    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == 0, "Should return 0 occurrences"
    assert extracted_data == [], "Extracted data should be an empty list"
