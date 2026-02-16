from text_toolkit.cli_display import (
    _build_extraction_data_for_json,
    _build_json_output,
    _format_analyzer_value,
    _format_extraction_sample,
    _get_active_extractors,
    display_results,
    display_transformer_results,
)
from text_toolkit.models import ExtractionResult


def _make_extraction_result() -> ExtractionResult:
    return ExtractionResult(
        email_matches=["a@example.com"],
        url_matches=["https://example.com"],
        date_matches=["2026-02-16"],
        active_extractors=["email", "url", "date"],
    )


def test_get_active_extractors_sets_flags_based_on_result() -> None:
    result = _make_extraction_result()

    show_emails, show_urls, show_dates = _get_active_extractors(result)

    assert (show_emails, show_urls, show_dates) == (True, True, True)


def test_build_extraction_data_for_json_includes_summary() -> None:
    result = _make_extraction_result()

    data = _build_extraction_data_for_json(result)

    assert data["emails"] == result.email_matches
    assert data["urls"] == result.url_matches
    assert data["dates"] == result.date_matches
    assert data["summary"]["total_emails"] == 1
    assert data["summary"]["total_urls"] == 1
    assert data["summary"]["total_dates"] == 1


def test_build_json_output_includes_analysis_and_extraction_sections() -> None:
    analyzer_results = {"total_words": 10}
    extraction_result = _make_extraction_result()

    data = _build_json_output(analyzer_results, extraction_result)

    assert "analysis" in data
    assert "extraction" in data

    data_without_extraction = _build_json_output(analyzer_results, None)
    assert "analysis" in data_without_extraction
    assert "extraction" not in data_without_extraction


def test_format_analyzer_value_truncates_large_dicts() -> None:
    big_dict = {f"k{i}": i for i in range(10)}

    formatted = _format_analyzer_value(big_dict)

    assert "k0" in formatted
    assert "..." in formatted


def test_format_extraction_sample_limits_and_handles_empty() -> None:
    many_matches = ["one", "two", "three", "four"]

    limited = _format_extraction_sample(many_matches, max_samples=2)
    assert limited.startswith("one, two")
    assert "..." in limited

    empty = _format_extraction_sample([], max_samples=3)
    assert empty == "(none)"


def test_display_results_text_and_json_do_not_raise() -> None:
    analyzer_results = {"total_words": 10}
    extraction_result = _make_extraction_result()

    # Text mode (tables)
    display_results("text", analyzer_results, extraction_result)

    # JSON mode (panel with JSON payload)
    display_results("json", analyzer_results, extraction_result)


def test_display_transformer_results_text_and_json_do_not_raise() -> None:
    transformer_results = {
        "Cleaner": "clean text",
        "Normalizer": "normalized text",
    }

    display_transformer_results("text", transformer_results)
    display_transformer_results("json", transformer_results)

