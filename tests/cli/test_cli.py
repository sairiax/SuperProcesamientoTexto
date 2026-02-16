import argparse

import pytest
from rich.console import Console

from text_toolkit import cli as cli_module
from text_toolkit.cli import (
    apply_transformers,
    collect_transformer_results,
    log_info,
    parse_arguments,
)


def test_apply_transformers_runs_selected_transformers() -> None:
    content = "  HOLA   mundo!!!  "

    transformed = apply_transformers(
        content,
        transformer_names=["Cleaner", "Normalizer", "Tokenizer"],
        verbose=False,
    )

    assert transformed == "hola mundo"


def test_collect_transformer_results_returns_all_steps() -> None:
    content = "  HOLA   mundo!!!  "

    results = collect_transformer_results(content, transformer_names=None, verbose=False)

    # When no explicit list is provided, all transformers should run in default order
    assert set(results.keys()) == {"Cleaner", "Normalizer", "Tokenizer"}
    assert results["Tokenizer"].split() == ["hola", "mundo"]


def test_log_info_prints_only_when_verbose(monkeypatch: pytest.MonkeyPatch) -> None:
    test_console = Console(record=True)
    monkeypatch.setattr(cli_module, "console", test_console)

    log_info("visible message", verbose=True)
    output = test_console.export_text()
    assert "visible message" in output

    test_console.clear()
    log_info("hidden message", verbose=False)
    output_after = test_console.export_text()
    assert "hidden message" not in output_after


def test_parse_arguments_parses_basic_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        cli_module.sys,
        "argv",
        [
            "text-toolkit",
            "input.txt",
            "-o",
            "json",
            "-v",
            "-a",
            "FrequencyAnalyzer",
            "-e",
            "EmailExtractor",
            "-t",
            "Cleaner",
            "Normalizer",
        ],
    )

    args = parse_arguments()

    assert args.input_path == "input.txt"
    assert args.output == "json"
    assert args.verbose == 1
    assert args.analyzers == ["FrequencyAnalyzer"]
    assert args.extractors == ["EmailExtractor"]
    assert args.transformers == ["Cleaner", "Normalizer"]


def test_main_exits_on_configuration_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_parse_arguments() -> argparse.Namespace:
        # Invalid output format will cause CLIConfig validation error
        return argparse.Namespace(
            input_path="input.txt",
            output="invalid",
            verbose=0,
            analyzers=None,
            extractors=None,
            transformers=None,
        )

    monkeypatch.setattr(cli_module, "parse_arguments", fake_parse_arguments)

    with pytest.raises(SystemExit) as exc_info:
        cli_module.main()

    assert exc_info.value.code == 1

