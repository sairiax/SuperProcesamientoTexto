import argparse
import logging
import sys
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.logging import RichHandler
from rich_argparse import RawDescriptionRichHelpFormatter

from text_toolkit.cli_display import display_results, display_transformer_results
from text_toolkit.cli_runner import process_document
from text_toolkit.models.config_models import CLIConfig
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer

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
               "  python main.py input.txt                          # Run both analyzers and extractors\n"  # noqa: E501
               "  python main.py input.txt -a FrequencyAnalyzer     # Run only specific analyzer\n"
               "  python main.py input.txt -e                       # Run all extractors only\n"
               "  python main.py input.txt -e EmailExtractor        # Run only email extractor\n"
               "  python main.py input.txt -e EmailExtractor URLExtractor  # Multiple extractors\n"
               "  python main.py input.txt -t Cleaner               # Run only cleaner transformer\n"       # noqa: E501
               "  python main.py input.txt -t Cleaner Normalizer    # Multiple transformers\n"
               "  python main.py input.txt -o json                  # Both with JSON output[/italic]",      # noqa: E501
        formatter_class=RawDescriptionRichHelpFormatter,
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
        help="Specify which extractors to run. Options: EmailExtractor, URLExtractor, DateExtractor (required).", # noqa: E501
    )

    # Enable transformers
    parser.add_argument(
        "-t",
        "--transformers",
        nargs="+",
        choices=[
            "Cleaner",
            "Normalizer",
            "Tokenizer",
        ],
        metavar="TRANSFORMER",
        help="Specify which transformers to run. Options: Cleaner, Normalizer, Tokenizer (required).", # noqa: E501
    )

    return parser.parse_args()


def apply_transformers(
    content: str, transformer_names: list[str] | None, verbose: bool
) -> str:
    """Applies specified transformers to content and returns the final output."""
    transformer_map = {
        "Cleaner": Cleaner(),
        "Normalizer": Normalizer(),
        "Tokenizer": Tokenizer(),
    }

    if transformer_names is None:
        transformer_names = list(transformer_map.keys())

    current_content = content

    for name in transformer_names:
        if name in transformer_map:
            transformer = transformer_map[name]
            log_info(f"Applying {name}...", verbose)
            if name == "Tokenizer":
                transformed = " ".join(transformer.tokenize_text(current_content))
            elif name == "Cleaner":
                transformed = transformer.clean_text(current_content)
            elif name == "Normalizer":
                transformed = transformer.normalize_text(current_content)

            current_content = transformed

    return current_content


def collect_transformer_results(
    content: str, transformer_names: list[str] | None, verbose: bool
) -> dict[str, str]:
    """Applies specified transformers to content and returns all intermediate outputs."""
    transformer_map = {
        "Cleaner": Cleaner(),
        "Normalizer": Normalizer(),
        "Tokenizer": Tokenizer(),
    }

    if transformer_names is None:
        transformer_names = list(transformer_map.keys())

    results: dict[str, str] = {}
    current_content = content

    for name in transformer_names:
        if name in transformer_map:
            transformer = transformer_map[name]
            log_info(f"Applying {name}...", verbose)
            if name == "Tokenizer":
                transformed = " ".join(transformer.tokenize_text(current_content))
            elif name == "Cleaner":
                transformed = transformer.clean_text(current_content)
            elif name == "Normalizer":
                transformed = transformer.normalize_text(current_content)

            results[name] = transformed
            current_content = transformed

    return results




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
                transformers=args.transformers,
            )
        except ValidationError as ve:
            console.print(f"[bold red]Configuration Error:[/bold red] {ve}")
            sys.exit(1)

        # Validate file exists
        input_file = Path(config.input_path)
        if not input_file.exists():
            console.print(
                f"[bold red]Error:[/bold red] File not found: [italic]{config.input_path}[/italic]"
            )
            sys.exit(1)

        # Process document and get results
        analyzers_results, extractors_results, transformers_results = process_document(config)

        # Display results based on what was run
        if transformers_results is not None:
            display_transformer_results(config.output, transformers_results)
        else:
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
