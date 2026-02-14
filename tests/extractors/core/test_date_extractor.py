import pytest

from text_toolkit.extractors.base import Extractor


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
def test_date_extractor(date_extractor: Extractor, text: str, expected_dates: list[str]):
    extracted_dates = date_extractor.extract(text)

    assert isinstance(extracted_dates, list), "Data structure should be a List"
    assert len(extracted_dates) == len(expected_dates), (
        "Size of extracted data doesnt match expected_dates size"
    )
    assert extracted_dates == expected_dates, f"Dates extracted should be {expected_dates}"
