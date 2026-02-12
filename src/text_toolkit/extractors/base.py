import re
from abc import ABC
from re import Pattern

from text_toolkit.models.text_document import TextDocument


class BaseExtractor(ABC):
    """Base class for all extractors."""

    _regex_pattern_list: list[Pattern[str]]

    def __init__(self, text_document: TextDocument, pattern_list: list[str]) -> None:
        """
        Initialize extractor with a list of regex patterns.

        :param pattern_list: List of regular expression patterns
        :type pattern_list: list[str]
        :raises ValueError: If any pattern is invalid
        """
        self._regex_pattern_list = []
        self.add_patterns(pattern_list)

    def add_patterns(self, patterns: list[str]) -> None:
        """
        Add multiple patterns to the extractor.

        :param patterns: List of regular expression patterns
        :type patterns: list[str]
        :raises ValueError: If any pattern is invalid
        """
        for pattern in patterns:
            try:
                compiled_pattern = re.compile(pattern)
                self._regex_pattern_list.append(compiled_pattern)
            except re.error as exc:
                raise ValueError(f"Invalid regex pattern: {pattern}") from exc

    def extract(self, text: str) -> list[str]:
        """
        Extract all matches from the input text using all registered patterns.

        :param text: Input text to scan
        :type text: str
        :return: List of all matches
        :rtype: List[str]
        """
        results = []
        for pattern in self._regex_pattern_list:
            results.extend(pattern.findall(text))
        return results
