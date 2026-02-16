import pytest

from text_toolkit.extractors.base import Extractor
from text_toolkit.extractors.core import DateExtractor
from text_toolkit.transformers import Normalizer


@pytest.mark.parametrize(
    "text, expected_dates",
    [
        ("The event is scheduled for 13-02-2026", ["13-02-2026"]),
        ("Meeting on 2026-03-20 and deadline 2026-04-10", ["2026-03-20", "2026-04-10"]),
        ("Birth date: 15/08/1990", ["15/08/1990"]),
        ("Conference starts on 10 Feb 2026", ["10 Feb 2026"]),
        (
            "Event on 2026-01-15, meeting 20/03/2026, and deadline 10-Apr-2026",
            ["2026-01-15", "20/03/2026", "10-Apr-2026"],
        ),
        ("Event will be in the downtown at midnight", []),
    ],
    ids=[
        "single_date_extraction",
        "iso_format",
        "slash_format",
        "month_name_abb_format",
        "mixed_formats",
        "text_without_dates",
    ],
)
def test_date_extractor(
    date_extractor: Extractor,
    normalizer: Normalizer,
    text: str,
    expected_dates: list[str],
):
    normalized_text = normalizer.normalize_text(text)
    normalized_expected = [normalizer.normalize_text(value) for value in expected_dates]
    extracted_dates = date_extractor.extract(normalized_text)

    assert isinstance(extracted_dates, list), "Data structure should be a List"
    assert len(extracted_dates) == len(normalized_expected), (
        "Size of extracted data doesnt match expected_dates size"
    )
    assert (
        extracted_dates == normalized_expected
    ), f"Dates extracted should be {normalized_expected}"


def test_date_extractor_repr_includes_pattern_information() -> None:
    extractor = DateExtractor()

    representation = repr(extractor)

    assert "DateExtractor" in representation
    assert "patterns_amount=" in representation
