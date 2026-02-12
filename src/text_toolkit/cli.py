import argparse
import sys
from pathlib import Path
from typing import Any

from text_toolkit.analyzers import AnalyzerRunner
from text_toolkit.readers.txt_reader import TXTReader


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the text processing toolkit.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="text_toolkit",
        description="A professional toolkit for advanced text processing and analysis.",
        epilog="Example: python main.py input.txt --output json",
    )
    # ... (rest of arguments)
    parser.add_argument(
        "input_path",
        help="Path to the text file to be processed.",
    )

    parser.add_argument(
        "-o",
        "--output",
        choices=["text", "json"],
        default="text",
        help="Format of the analysis results (default: %(default)s).",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable detailed logging and processing information.",
    )

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
        help="List of specific analyzers to run. If omitted, all run.",
    )

    return parser.parse_args()


def display_results(results: dict[str, Any], output_format: str) -> None:
    """
    Displays the analysis results in the specified format.

    Args:
        results (dict[str, Any]): The analysis findings.
        output_format (str): How to display the results ('text' or 'json').
    """
    if output_format == "json":
        import json

        print(json.dumps(results, indent=2, ensure_ascii=False))  # noqa: T201
    else:
        print("\n" + "=" * 40)  # noqa: T201
        print(" ANALYSIS RESULTS ".center(40, "="))  # noqa: T201
        print("=" * 40)  # noqa: T201
        for key, value in results.items():
            formatted_key = key.replace("_", " ").title()
            print(f"{formatted_key:<20}: {value}")  # noqa: T201
        print("=" * 40 + "\n")  # noqa: T201


def log_info(message: str, verbose: bool) -> None:
    """Logs information to stderr if verbose mode is enabled."""
    if verbose:
        print(f"[INFO] {message}", file=sys.stderr)  # noqa: T201


def main() -> None:
    """Primary execution logic for the CLI."""
    args = parse_arguments()

    log_info(f"Starting processing of: {args.input_path}", args.verbose)

    input_file = Path(args.input_path)
    if not input_file.exists():
        print(f"Error: File not found: {args.input_path}", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    try:
        log_info("Reading document...", args.verbose)
        reader = TXTReader()
        document = reader.read(input_file)

        log_info("Running linguistic analysis...", args.verbose)
        runner = AnalyzerRunner(analyzer_names=args.analyzers)
        results = runner.analyze(document)

        display_results(results, args.output)
        log_info("Processing completed successfully.", args.verbose)

    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)  # noqa: T201
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
