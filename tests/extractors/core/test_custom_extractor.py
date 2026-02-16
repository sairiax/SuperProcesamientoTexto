import pytest

from text_toolkit.extractors.core import CustomExtractor


@pytest.mark.parametrize(
    "name, patterns, expected_count",
    [
        ("phone", [r"\d{3}-\d{3}-\d{4}"], 1),
        (
            "phone",
            [r"\d{3}-\d{3}-\d{4}", r"\(\d{3}\)\s*\d{3}-\d{4}"],
            2,
        ),
    ],
    ids=[
        "single_pattern",
        "multiple_patterns",
    ],
)
def test_create_with_patterns(name: str, patterns: list[str], expected_count: int):
    """Should create a custom extractor with expected pattern count."""
    extractor = CustomExtractor(name=name, patterns=patterns)

    assert extractor.name == name, "Extractor name should match"
    assert extractor.pattern_count == expected_count, "Unexpected pattern count"


@pytest.mark.parametrize(
    "name, patterns, text, expected, unique_occurrences",
    [
        (
            "phone",
            [r"\d{3}-\d{3}-\d{4}", r"\(\d{3}\)\s*\d{3}-\d{4}"],
            "Call 555-123-4567 or (555) 987-6543 for assistance",
            ["555-123-4567", "(555) 987-6543"],
            True,
        ),
        (
            "ip_address",
            [r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"],
            "Server at 192.168.1.1 and backup at 10.0.0.5",
            ["192.168.1.1", "10.0.0.5"],
            True,
        ),
        (
            "phone",
            [r"\d{3}-\d{3}-\d{4}"],
            "Este texto no contiene números de teléfono",
            [],
            True,
        ),
        ("phone", [r"\d{3}-\d{3}-\d{4}"], "", [], True),
        (
            "phone",
            [r"\d{3}-\d{3}-\d{4}"],
            "Numbers: 555-123-4567, 555-987-6543, 555-123-4567",
            ["555-123-4567", "555-987-6543", "555-123-4567"],
            False,
        ),
        (
            "phone",
            [r"\d{3}-\d{3}-\d{4}"],
            "Numbers: 555-123-4567, 555-987-6543, 555-123-4567",
            ["555-123-4567", "555-987-6543"],
            True,
        ),
        (
            "mixed",
            [r"\d{3}-\d{3}-\d{4}", r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"],
            "Contact: 555-123-4567, Server: 192.168.1.1",
            ["555-123-4567", "192.168.1.1"],
            True,
        ),
        ("empty", [], "Some text with data", [], True),
    ],
    ids=[
        "extract_phone_numbers",
        "extract_ip_addresses",
        "no_matches",
        "empty_string",
        "include_duplicates",
        "unique_occurrences",
        "mixed_patterns",
        "empty_pattern_list",
    ],
)
def test_extract_from_various_patterns(
    name: str, patterns: list[str], text: str, expected: list[str], unique_occurrences: bool
):
    """Should extract matches for various patterns and modes."""
    extractor = CustomExtractor(name=name, patterns=patterns)
    extracted_data = extractor.extract(text, unique_occurrences=unique_occurrences)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == len(expected)
    for value in set(expected):
        assert extracted_data.count(value) == expected.count(value)


def test_invalid_regex_pattern():
    """Should raise ValueError when regex pattern is invalid."""
    with pytest.raises(ValueError) as exc_info:
        CustomExtractor(name="invalid", patterns=[r"[invalid(regex"])

    assert "Invalid regex pattern" in str(exc_info.value), (
        "Should raise ValueError with proper message"
    )


def test_add_patterns_dynamically():
    """Should allow adding patterns dynamically after creation."""
    phone_extractor = CustomExtractor(name="phone", patterns=[r"\d{3}-\d{3}-\d{4}"])

    assert phone_extractor.pattern_count == 1, "Should have 1 pattern initially"
    new_phone_pattern = r"\(\d{3}\)\s*\d{3}-\d{4}"
    phone_extractor.add_patterns([new_phone_pattern])
    assert phone_extractor.pattern_count == 2, "Should have 2 patterns after adding"
    assert new_phone_pattern in phone_extractor.patterns, (
        f"Pattern {new_phone_pattern} should be included in the extractor"
    )
    example_text = "Call 555-123-4567 or (555) 987-6543"
    extracted_data = phone_extractor.extract(example_text)
    assert len(extracted_data) == 2, "Should extract with both patterns"
