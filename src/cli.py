import argparse
import sys
from pathlib import Path
import json

from procesamientotexto.readers.txt_reader import TXTReader
from procesamientotexto.analyzers.analyzer import AnalyzerRunner


def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(description="Analyze text files.")
    parser.add_argument("file", type=str, help="Path to the text file to analyze.")

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Use the Reader
        reader = TXTReader()
        doc = reader.read(file_path)

        # Analyze
        stats_analyzer = AnalyzerRunner()
        results = stats_analyzer.analyze(doc)

        # Output results
        print(json.dumps(results, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
