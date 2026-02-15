import argparse
import logging
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich_argparse import RichHelpFormatter

from text_toolkit.analyzers import AnalyzerRunner
from text_toolkit.extractors import ExtractorRunner
from text_toolkit.models import ExtractionResult
from text_toolkit.models.config_models import CLIConfig
from text_toolkit.models.text_document import TextDocument
from text_toolkit.readers import TxtReader, MarkdownReader, HtmlReader
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer, TransformerPipeline

# Initialize global console
console = Console()


def setup_logging(verbosity: int) -> None:
    """Configures the logging system using a verbosity level."""
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
    )


# TODO: Add try-cath?
def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments using RichHelpFormatter for a better interface.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="text-toolkit",
        description="[bold blue]TextToolkit[/bold blue]: A professional suite for "
        "advanced linguistic analysis.",
        epilog="[italic]Examples:\n"
               "  python main.py input.txt                          # Run both analyzers and extractors\n"
               "  python main.py input.txt -a FrequencyAnalyzer     # Run only specific analyzer\n"
               "  python main.py input.txt -e                       # Run all extractors only\n"
               "  python main.py input.txt -e EmailExtractor        # Run only email extractor\n"
               "  python main.py input.txt -e EmailExtractor URLExtractor  # Multiple extractors\n"
               "  python main.py input.txt -o json                  # Both with JSON output[/italic]",
        formatter_class=RichHelpFormatter,
    )

    # Positional argument: Input file
    parser.add_argument(
        "input_path",
        help="Path to the text file to be processed.",
    )

    # Output format
    parser.add_argument(
        "-o",
        "--output",
        choices=["text", "json"],
        default="text",
        help="Format of the analysis results (default: %(default)s).",
    )

    # Verbosity (-v for info, -vv for debug)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for info, -vv for debug).",
    )

    # Specific analyzers (optional)
    parser.add_argument(
        "-a",
        "--analyzers",
        nargs="+",
        choices=[
            "FrequencyAnalyzer",
            "LanguageDetector",
            "ReadabilityAnalyzer",
            "SentimentAnalyzer",
        ],
        metavar="ANALYZER",
        help="List of specific analyzers to run (e.g., SentimentAnalyzer). If omitted, all run.",
    )

    # Enable extractors
    parser.add_argument(
        "-e",
        "--extractors",
        nargs="+",
        choices=[
            "EmailExtractor",
            "DateExtractor",
            "URLExtractor",
        ],
        metavar="EXTRACTOR",
        help="Specify which extractors to run. Options: EmailExtractor, URLExtractor, DateExtractor (required).",
    )

    return parser.parse_args()


def display_results(
    output_format: str,
    analyzer_results: dict[str, Any],
    extractor_results: ExtractionResult | None,
) -> None:
    """
    Displays the analysis results in the specified format using Rich.

    Args:
        results (dict[str, Any]): The analysis findings.
        output_format (str): How to display the results ('text' or 'json').
        extraction_result (ExtractionResult | None): Extracted data (emails, URLs, dates).
    """
    if output_format == "json":
        import json

        # Build complete output with analysis and extraction
        output_data = {}

        if analyzer_results:
            output_data["analysis"] = analyzer_results

        if extractor_results:
            # Determine which extractors to include in the output
            active_extractors = extractor_results.active_extractors or []
            show_emails = 'email' in active_extractors
            show_urls = 'url' in active_extractors
            show_dates = 'date' in active_extractors

            extraction_data = {}
            summary = {}

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
            output_data["extraction"] = extraction_data

        json_str = json.dumps(output_data, indent=2, ensure_ascii=False)
        console.print(
            Panel(json_str, title="[bold cyan]JSON Result[/bold cyan]", border_style="cyan")
        )
    else:
        # Display analysis results if available
        if analyzer_results:
            table = Table(
                title="[bold blue]Analysis Summary[/bold blue]",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Metric", style="dim", width=25)
            table.add_column("Value", style="bold green")

            for key, value in analyzer_results.items():
                formatted_key = key.replace("_", " ").title()

                # Special formatting for certain types
                if isinstance(value, dict):
                    # Format sub-dictionaries (like top words) as a more readable string
                    val_str = ", ".join([f"{k}: {v}" for k, v in list(value.items())[:5]])
                    if len(value) > 5:
                        val_str += " ..."
                else:
                    val_str = str(value)

                table.add_row(formatted_key, val_str)

            console.print("\n")
            console.print(table)
            console.print("\n")

        # Display extraction results if available
        if extractor_results:
            extraction_table = Table(
                title="[bold cyan]Extracted Data[/bold cyan]",
                show_header=True,
                header_style="bold blue",
            )
            extraction_table.add_column("Type", style="dim", width=15)
            extraction_table.add_column("Count", style="bold yellow", width=10)
            extraction_table.add_column("Samples", style="bold green")

            # Determine which extractors to display
            active_extractors = extractor_results.active_extractors or []
            show_emails = 'email' in active_extractors
            show_urls = 'url' in active_extractors
            show_dates = 'date' in active_extractors

            # Emails
            if show_emails:
                email_sample = ", ".join(extractor_results.email_matches[:3])
                if len(extractor_results.email_matches) > 3:
                    email_sample += " ..."
                extraction_table.add_row(
                    "Emails",
                    str(len(extractor_results.email_matches)),
                    email_sample or "(none)",
                )

            # URLs
            if show_urls:
                url_sample = ", ".join(extractor_results.url_matches[:3])
                if len(extractor_results.url_matches) > 3:
                    url_sample += " ..."
                extraction_table.add_row(
                    "URLs",
                    str(len(extractor_results.url_matches)),
                    url_sample or "(none)",
                )

            # Dates
            if show_dates:
                date_sample = ", ".join(extractor_results.date_matches[:3])
                if len(extractor_results.date_matches) > 3:
                    date_sample += " ..."
                extraction_table.add_row(
                    "Dates",
                    str(len(extractor_results.date_matches)),
                    date_sample or "(none)",
                )

            console.print(extraction_table)
            console.print("\n")


def log_info(message: str, verbose: bool) -> None:
    """Logs information to stderr if verbose mode is enabled."""
    if verbose:
        console.print(f"[bold yellow]LOG:[/bold yellow] {message}", style="yellow")


def main() -> None:
    """Primary execution logic for the CLI."""
    args: argparse.Namespace | None = None

    try:
        args = parse_arguments()
        setup_logging(args.verbose)

        # Validate arguments using Pydantic for "professional" architecture
        try:
            config = CLIConfig(
                input_path=args.input_path,
                output=args.output,
                verbose=args.verbose > 0,
                analyzers=args.analyzers,
                extractors=args.extractors,
            )
        except ValidationError as ve:
            console.print(f"[bold red]Configuration Error:[/bold red] {ve}")
            sys.exit(1)

        log_info(f"Starting processing of: {config.input_path}", config.verbose)

        input_file = Path(config.input_path)
        if not input_file.exists():
            console.print(
                f"[bold red]Error:[/bold red] File not found: [italic]{config.input_path}[/italic]"
            )
            sys.exit(1)

        log_info("Reading document...", config.verbose)
        # Select reader based on file extension
        file_extension = input_file.suffix.lower()
        if file_extension == ".md":
            reader = MarkdownReader()
            log_info(f"Using MarkdownReader for {input_file.name}", config.verbose)
        elif file_extension == ".html":
            reader = HtmlReader()
            log_info(f"Using HtmlReader for {input_file.name}", config.verbose)
        else:
            reader = TxtReader()
            log_info(f"Using TxtReader for {input_file.name}", config.verbose)
        lines = list(reader.read(input_file))
        content = "\n".join(lines)

        log_info("Initializing processing pipeline...", config.verbose)
        cleaner = Cleaner()
        normalizer = Normalizer()
        tokenizer = Tokenizer()
        pipeline = TransformerPipeline(tokenizer=tokenizer, cleaner=cleaner, normalizer=normalizer)

        document = TextDocument(content=content, source_path=input_file, pipeline=pipeline)


        # determine what to run
        no_args = config.extractors is None and config.analyzers is None
        run_analyzers = no_args or config.analyzers is not None
        run_extractors = no_args or config.extractors is not None

        analyzers_results = {}

        if run_analyzers:
            log_info("Running linguistic analysis...", config.verbose)
            analyzer_runner = AnalyzerRunner(analyzer_names=config.analyzers)
            analyzers_results = analyzer_runner.analyze(document)

        # Run extractors if enabled
        extractors_results = None
        if run_extractors:
            log_info("Running extractors...", config.verbose)
            # If extractors is an empty list [], use all extractors (None)
            # If extractors is a list with names, use those specific extractors

            extractor_runner = ExtractorRunner(extractor_names=config.extractors)
            extractors_results = extractor_runner.extract_all(document)
            log_info(
                f"Extraction completed: {len(extractors_results.email_matches)} emails, "
                f"{len(extractors_results.url_matches)} URLs, {len(extractors_results.date_matches)} dates",
                config.verbose,
            )

        display_results(config.output, analyzers_results, extractors_results)
        log_info("Processing completed successfully.", config.verbose)

    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Critical Error:[/bold red] {e}")
        if args and args.verbose > 0:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
