import json
from collections.abc import Generator
from pathlib import Path
from typing import Any


class DataLoadError(Exception):
    """Custom exception for data loading failures."""


class DataLoader:
    """Utility for robust data loading from JSON files."""

    @staticmethod
    def get_data_path(filename: str) -> Path:
        """Resolves the absolute path to a data file.

        Args:
            filename (str): Name of the file in the data directory.

        Returns:
            Path: Absolute path to the file.
        """
        # Data directory is the directory containing this file
        data_dir = Path(__file__).parent
        return data_dir / filename

    @classmethod
    def load_json(cls, filename: str) -> dict[str, Any]:
        """Loads and parses a JSON file with defensive checks.

        Args:
            filename (str): Name of the file to load.

        Returns:
            dict[str, Any]: Parsed JSON content.

        Raises:
            DataLoadError: If file is missing or contains invalid JSON.
        """
        path = cls.get_data_path(filename)

        if not path.exists():
            raise DataLoadError(f"Required data file missing: {path}")

        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            raise DataLoadError(f"Malformed JSON in {path}: {exc}") from exc
        except Exception as exc:
            raise DataLoadError(f"Unexpected error loading {path}: {exc}") from exc

    @staticmethod
    def to_set_generator(items: list[str]) -> Generator[str, None, None]:
        """Generator-based conversion.

        Args:
            items (list[str]): List of items.

        Returns:
            Generator[str, None, None]: Generator yielding unique items.
        """
        return (item for item in set(items))

    @classmethod
    def load_stopwords(cls) -> dict[str, set[str]]:
        """Specialized loader for stopwords with schema validation.

        Returns:
            dict[str, set[str]]: Mapping of language codes to sets of stopwords.
        """
        data = cls.load_json("stopwords.json")
        return {lang: set(words) for lang, words in data.items()}

    @classmethod
    def load_sentiment_words(cls) -> tuple[set[str], set[str]]:
        """Specialized loader for sentiment words.

        Returns:
            tuple[set[str], set[str]]: (positive_words, negative_words)
        """
        data = cls.load_json("sentiment_words.json")
        pos = set(data.get("positive", []))
        neg = set(data.get("negative", []))
        return pos, neg

    @classmethod
    def load_readability_thresholds(cls) -> dict[str, dict[str, float]]:
        """Specialized loader for readability thresholds.

        Returns:
            dict[str, dict[str, float]]: Thresholds mapping.
        """
        return cls.load_json("readability_thresholds.json")
