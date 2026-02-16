"""Display functions for CLI output formatting."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from text_toolkit.models import ExtractionResult

# Initialize global console
console = Console()


def _get_active_extractors(extractor_results: ExtractionResult) -> tuple[bool, bool, bool]:
    """
    Determines which extractors are active based on the extraction results.

    Args:
        extractor_results: The extraction result object.

    Returns:
        Tuple of (show_emails, show_urls, show_dates) boolean flags.
    """
    active_extractors = extractor_results.active_extractors or []
    show_emails = 'email' in active_extractors
    show_urls = 'url' in active_extractors
    show_dates = 'date' in active_extractors
    return show_emails, show_urls, show_dates


def _build_extraction_data_for_json(extractor_results: ExtractionResult) -> dict[str, Any]:
    """
    Builds the extraction data dictionary for JSON output.

    Args:
        extractor_results: The extraction result object.

    Returns:
        Dictionary containing extraction data and summary.
    """
    show_emails, show_urls, show_dates = _get_active_extractors(extractor_results)

    extraction_data: dict[str, Any] = {}
    summary: dict[str, int] = {}

    if show_emails:
        extraction_data["emails"] = extractor_results.email_matches
        summary["total_emails"] = len(extractor_results.email_matches)

    if show_urls:
        extraction_data["urls"] = extractor_results.url_matches
        summary["total_urls"] = len(extractor_results.url_matches)

    if show_dates:
        extraction_data["dates"] = extractor_results.date_matches
        summary["total_dates"] = len(extractor_results.date_matches)

    extraction_data["summary"] = summary
    return extraction_data


def _build_json_output(
    analyzer_results: dict[str, Any],
    extractor_results: ExtractionResult | None,
) -> dict[str, Any]:
    """
    Builds the complete JSON output structure.

    Args:
        analyzer_results: Analysis results dictionary.
        extractor_results: Extraction results object or None.

    Returns:
        Complete output dictionary ready for JSON serialization.
    """
    output_data: dict[str, Any] = {}

    if analyzer_results:
        output_data["analysis"] = analyzer_results

    if extractor_results:
        output_data["extraction"] = _build_extraction_data_for_json(extractor_results)

    return output_data


def _format_analyzer_value(value: Any) -> str:
    """
    Formats an analyzer value for display in a table.

    Args:
        value: The value to format (can be dict, list, or primitive).

    Returns:
        Formatted string representation.
    """
    if isinstance(value, dict):
        # Format sub-dictionaries (like top words) as a more readable string
        val_str = ", ".join([f"{k}: {v}" for k, v in list(value.items())[:5]])
        if len(value) > 5:
            val_str += " ..."
        return val_str
    return str(value)


def _display_analysis_table(analyzer_results: dict[str, Any]) -> None:
    """
    Displays analysis results in a Rich table format.

    Args:
        analyzer_results: Dictionary containing analysis metrics.
    """
    table = Table(
        title="[bold blue]Analysis Summary[/bold blue]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Metric", style="dim", width=25)
    table.add_column("Value", style="bold green")

    for key, value in analyzer_results.items():
        formatted_key = key.replace("_", " ").title()
        val_str = _format_analyzer_value(value)
        table.add_row(formatted_key, val_str)

    console.print("\n")
    console.print(table)
    console.print("\n")


def _format_extraction_sample(matches: list[str], max_samples: int = 3) -> str:
    """
    Formats a sample of extraction matches for display.

    Args:
        matches: List of matched strings.
        max_samples: Maximum number of samples to show.

    Returns:
        Formatted string with samples.
    """
    sample = ", ".join(matches[:max_samples])
    if len(matches) > max_samples:
        sample += " ..."
    return sample or "(none)"


def _display_extraction_table(extractor_results: ExtractionResult) -> None:
    """
    Displays extraction results in a Rich table format.

    Args:
        extractor_results: The extraction result object.
    """
    extraction_table = Table(
        title="[bold cyan]Extracted Data[/bold cyan]",
        show_header=True,
        header_style="bold blue",
    )
    extraction_table.add_column("Type", style="dim", width=15)
    extraction_table.add_column("Count", style="bold yellow", width=10)
    extraction_table.add_column("Samples", style="bold green")

    show_emails, show_urls, show_dates = _get_active_extractors(extractor_results)

    if show_emails:
        email_sample = _format_extraction_sample(extractor_results.email_matches)
        extraction_table.add_row(
            "Emails",
            str(len(extractor_results.email_matches)),
            email_sample,
        )

    if show_urls:
        url_sample = _format_extraction_sample(extractor_results.url_matches)
        extraction_table.add_row(
            "URLs",
            str(len(extractor_results.url_matches)),
            url_sample,
        )

    if show_dates:
        date_sample = _format_extraction_sample(extractor_results.date_matches)
        extraction_table.add_row(
            "Dates",
            str(len(extractor_results.date_matches)),
            date_sample,
        )

    console.print(extraction_table)
    console.print("\n")


def display_results(
    output_format: str,
    analyzer_results: dict[str, Any],
    extractor_results: ExtractionResult | None,
) -> None:
    """
    Displays the analysis results in the specified format using Rich.

    Args:
        output_format: How to display the results ('text' or 'json').
        analyzer_results: The analysis findings.
        extractor_results: Extracted data (emails, URLs, dates).
    """
    if output_format == "json":
        output_data = _build_json_output(analyzer_results, extractor_results)
        json_str = json.dumps(output_data, indent=2, ensure_ascii=False)
        console.print(
            Panel(json_str, title="[bold cyan]JSON Result[/bold cyan]", border_style="cyan")
        )
    else:
        if analyzer_results:
            _display_analysis_table(analyzer_results)

        if extractor_results:
            _display_extraction_table(extractor_results)


def display_transformer_results(output_format: str, results: dict[str, str]) -> None:
    """Displays transformer results in the specified format."""
    if output_format == "json":
        json_str = json.dumps(results, indent=2, ensure_ascii=False)
        console.print(
            Panel(json_str, title="[bold cyan]Transformer Results[/bold cyan]", border_style="cyan")
        )
    else:
        for name, content in results.items():
            console.print(f"\n[bold blue]{name} Result:[/bold blue]")
            console.print(Panel(content, border_style="blue"))
            console.print()
