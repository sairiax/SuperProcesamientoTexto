import sys
from pathlib import Path

# Ensure src is in the path
sys.path.insert(0, str(Path("src").resolve()))

from text_toolkit.cli import main as cli_main


def main():
    try:
        cli_main()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
