import re
from re import Pattern
from typing import Protocol, runtime_checkable


@runtime_checkable
class Extractor(Protocol):
    """Protocol defining the contract for all extractors."""

    def extract(self, text: str, unique_occurrences: bool = False) -> list[str]:
        """
        Extract matches from text.

        Parameters
        ----------
        text : str
            The text to extract patterns from
        unique_occurrences : bool, optional
            Whether to remove duplicate matches (default is False)

        Returns
        -------
        list[str]
            List of matched strings
        """
        ...


class RegexExtractor:
    """Concrete base class for regex-based extractors."""

    _regex_pattern_list: list[Pattern[str]]

    def __init__(self, pattern_list: list[str]) -> None:
        """
        Initialize extractor with a list of regex patterns.
        """
        self._regex_pattern_list = []
        self.add_patterns(pattern_list)

    def add_patterns(self, patterns: list[str]) -> None:
        """
        Add multiple patterns to the extractor.
        """
        for pattern in patterns:
            try:
                compiled_pattern = re.compile(pattern)
                self._regex_pattern_list.append(compiled_pattern)
            except re.error as exc:
                raise ValueError(f"Invalid regex pattern: {pattern}") from exc

    def extract(self, text: str, unique_occurrences: bool = False) -> list[str]:
        """
        Extract all matches from the input text using all registered patterns.

        Parameters
        ----------
        text : str
            The text to extract patterns from
        unique_occurrences : bool, optional
            Whether to remove duplicate matches while preserving order (default is False)

        Returns
        -------
        list[str]
            List of matched strings
        """
        results = []
        for pattern in self._regex_pattern_list:
            results.extend(pattern.findall(text))

        if unique_occurrences:
            return list(dict.fromkeys(results))

        return results
