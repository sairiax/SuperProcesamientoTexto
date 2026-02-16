import pytest

from text_toolkit.extractors.base import Extractor
from text_toolkit.extractors.core import URLExtractor


@pytest.mark.parametrize(
    "text, expected_urls",
    [
        ("Visit our site at http://example.com for more info", ["http://example.com"]),
        ("Secure connection: https://secure.example.com", ["https://secure.example.com"]),
        ("Download file from ftp://ftp.example.com/file.zip", ["ftp://ftp.example.com/file.zip"]),
        ("Check www.example.com for details", ["www.example.com"]),
        (
            "Documentation at https://docs.example.com/api/v1/documentation",
            ["https://docs.example.com/api/v1/documentation"],
        ),
    ],
    ids=[
        "http_url",
        "https_url",
        "ftp_url",
        "www_url",
        "url_with_path",
    ],
)
def test_url_extractor(url_extractor: Extractor, text: str, expected_urls: list[str]):
    extracted_data = url_extractor.extract(text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == len(expected_urls), (
        "Size of extracted data doesnt match expected_urls size"
    )
    assert extracted_data == expected_urls, f"Urls extracted should be {expected_urls}"


def test_url_extractor_repr_includes_pattern_information() -> None:
    extractor = URLExtractor()

    representation = repr(extractor)

    assert "URLExtractor" in representation
    assert "patterns_amount=" in representation
