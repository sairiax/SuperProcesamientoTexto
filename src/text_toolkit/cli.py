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
from text_toolkit.models.config_models import CLIConfig
from text_toolkit.readers.txt_reader import TXTReader

# Initialize global console
console = Console()


def setup_logging(verbose: bool) -> None:
    """Configures the logging system to use Rich for output if verbose is enabled."""
    level = logging.INFO if verbose else logging.WARNING
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
        epilog="[italic]Example: python main.py input.txt --output json[/italic]",
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

    # Verbose mode
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable detailed logging and processing information.",
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

    return parser.parse_args()


def display_results(results: dict[str, Any], output_format: str) -> None:
    """
    Displays the analysis results in the specified format using Rich.

    Args:
        results (dict[str, Any]): The analysis findings.
        output_format (str): How to display the results ('text' or 'json').
    """
    if output_format == "json":
        import json

        json_str = json.dumps(results, indent=2, ensure_ascii=False)
        console.print(
            Panel(json_str, title="[bold cyan]JSON Result[/bold cyan]", border_style="cyan")
        )
    else:
        table = Table(
            title="[bold blue]Analysis Summary[/bold blue]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Metric", style="dim", width=25)
        table.add_column("Value", style="bold green")

        for key, value in results.items():
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


def log_info(message: str, verbose: bool) -> None:
    """Logs information to stderr if verbose mode is enabled."""
    if verbose:
        console.print(f"[bold yellow]LOG:[/bold yellow] {message}", style="yellow")


def main() -> None:
    """Primary execution logic for the CLI."""
    # First pass to see if we need verbose logging for the rest of setup
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    setup_logging(verbose)

    try:
        args = parse_arguments()

        # Validate arguments using Pydantic for "professional" architecture
        try:
            config = CLIConfig(
                input_path=args.input_path,
                output=args.output,
                verbose=args.verbose,
                analyzers=args.analyzers,
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
        reader = TXTReader()
        document = reader.read(input_file)

        log_info("Running linguistic analysis...", config.verbose)
        runner = AnalyzerRunner(analyzer_names=config.analyzers)
        results = runner.analyze(document)

        display_results(results, config.output)
        log_info("Processing completed successfully.", config.verbose)

    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Critical Error:[/bold red] {e}")
        if "-v" in sys.argv or "--verbose" in sys.argv:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
