from pathlib import Path

from text_toolkit.cli_runner import (
    _apply_transformers_to_content,
    _determine_what_to_run,
    _get_reader_for_path,
    _run_transformers_only,
    process_document,
)
from text_toolkit.models import CLIConfig, ExtractionResult


def test_get_reader_for_path_chooses_reader_by_extension(tmp_path: Path) -> None:
    md_reader = _get_reader_for_path(tmp_path / "doc.md")
    html_reader = _get_reader_for_path(tmp_path / "page.html")
    txt_reader = _get_reader_for_path(tmp_path / "plain.txt")

    from text_toolkit.readers import HtmlReader, MarkdownReader, TxtReader

    assert isinstance(md_reader, MarkdownReader)
    assert isinstance(html_reader, HtmlReader)
    assert isinstance(txt_reader, TxtReader)


def test_determine_what_to_run_for_various_configs(tmp_path: Path) -> None:
    base_path = str(tmp_path / "input.txt")

    # No analyzers/extractors/transformers specified -> analyzers and extractors run
    cfg_all_default = CLIConfig(
        input_path=base_path,
        output="text",
        verbose=False,
        analyzers=None,
        extractors=None,
        transformers=None,
    )
    run_analyzers, run_extractors, run_transformers_only = _determine_what_to_run(cfg_all_default)
    assert (run_analyzers, run_extractors, run_transformers_only) == (True, True, False)

    # Only transformers specified -> transformers-only mode
    cfg_transformers_only = CLIConfig(
        input_path=base_path,
        output="text",
        verbose=False,
        analyzers=None,
        extractors=None,
        transformers=["Cleaner", "Normalizer"],
    )
    run_analyzers, run_extractors, run_transformers_only = _determine_what_to_run(
        cfg_transformers_only
    )
    assert (run_analyzers, run_extractors, run_transformers_only) == (False, False, True)

    # Analyzers and extractors explicitly requested
    cfg_analysis_and_extraction = CLIConfig(
        input_path=base_path,
        output="json",
        verbose=True,
        analyzers=["FrequencyAnalyzer"],
        extractors=["EmailExtractor"],
        transformers=None,
    )
    run_analyzers, run_extractors, run_transformers_only = _determine_what_to_run(
        cfg_analysis_and_extraction
    )
    assert (run_analyzers, run_extractors, run_transformers_only) == (True, True, False)


def test_run_transformers_only_returns_all_intermediate_results() -> None:
    content = "  HOLA   mundo!!!  "

    results = _run_transformers_only(
        content=content,
        transformer_names=["Cleaner", "Normalizer", "Tokenizer"],
        verbose=False,
    )

    assert set(results.keys()) == {"Cleaner", "Normalizer", "Tokenizer"}
    # Final tokenizer output should be tokenized normalized content
    assert results["Tokenizer"].split() == ["hola", "mundo"]


def test_apply_transformers_to_content_uses_selected_transformers() -> None:
    content = "  HOLA   mundo!!!  "

    transformed = _apply_transformers_to_content(
        content=content,
        transformer_names=["Cleaner", "Normalizer", "Tokenizer"],
        verbose=False,
    )

    # Cleaner + Normalizer + Tokenizer should produce normalized tokens joined by spaces
    assert transformed == "hola mundo"

    # When transformer_names is None, it should still return a non-empty string
    transformed_default = _apply_transformers_to_content(
        content=content,
        transformer_names=None,
        verbose=False,
    )
    assert isinstance(transformed_default, str)
    assert transformed_default


def test_process_document_runs_analyzers_and_extractors(tmp_path: Path) -> None:
    file_path = tmp_path / "document.txt"
    file_path.write_text(
        "Contact: admin@example.com. Visit https://example.com on 2026-03-15.",
        encoding="utf-8",
    )

    config = CLIConfig(
        input_path=str(file_path),
        output="text",
        verbose=False,
        analyzers=None,
        extractors=None,
        transformers=None,
    )

    analyzer_results, extractor_results, transformer_results = process_document(config)

    assert isinstance(analyzer_results, dict)
    assert isinstance(extractor_results, ExtractionResult)
    assert transformer_results is None
    assert "total_words" in analyzer_results
    assert "admin@example.com" in extractor_results.email_matches


def test_process_document_transformers_only_mode(tmp_path: Path) -> None:
    file_path = tmp_path / "document_transformers.txt"
    file_path.write_text("  HOLA   mundo!!!  ", encoding="utf-8")

    config = CLIConfig(
        input_path=str(file_path),
        output="json",
        verbose=False,
        analyzers=None,
        extractors=None,
        transformers=["Cleaner", "Normalizer", "Tokenizer"],
    )

    analyzer_results, extractor_results, transformer_results = process_document(config)

    assert analyzer_results == {}
    assert extractor_results is None
    assert transformer_results is not None
    assert set(transformer_results.keys()) == {"Cleaner", "Normalizer", "Tokenizer"}
