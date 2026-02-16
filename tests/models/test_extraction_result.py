from text_toolkit.models import ExtractionResult


def test_extraction_result_repr_shows_match_counts() -> None:
    result = ExtractionResult(
        email_matches=["a@example.com", "b@example.com"],
        url_matches=["https://example.com"],
        date_matches=[],
    )

    representation = repr(result)

    assert "emails=2" in representation
    assert "urls=1" in representation
    assert "dates=0" in representation

