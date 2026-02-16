import logging
import re
from re import Pattern
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)


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
                logger.debug("Added pattern: %s", pattern)
            except re.error as exc:
                logger.error("Invalid regex pattern: %s", pattern)
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
        if not text:
            logger.warning("Empty text provided for extraction")
            return []

        logger.debug(
            "Starting extraction on text of length %d with %d patterns",
            len(text),
            len(self._regex_pattern_list),
        )
        results = []
        for pattern in self._regex_pattern_list:
            matches = pattern.findall(text)
            if matches:
                logger.debug("Pattern '%s' found %d matches", pattern.pattern, len(matches))
            results.extend(matches)

        if unique_occurrences:
            results = list(dict.fromkeys(results))
            logger.debug("Removed duplicates, %d unique matches remain", len(results))

        logger.info(
            "Extraction completed: found %d matches (unique_occurrences=%s)",
            len(results),
            unique_occurrences,
        )
        return results
