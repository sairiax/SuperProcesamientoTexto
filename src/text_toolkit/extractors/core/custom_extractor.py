import logging

from text_toolkit.extractors.base import RegexExtractor

logger = logging.getLogger(__name__)


class CustomExtractor(RegexExtractor):
    """
    Generic extractor for user-defined patterns.

    Allows users to create extractors with custom regex patterns
    without subclassing BaseExtractor.

    Attributes
    ----------
    name : str
        Identifier for this extractor (e.g., 'phone', 'ip_address')

    Example
    -------
    >>> # Extract phone numbers
    >>> phone_extractor = CustomExtractor(
    ...     name="phone",
    ...     patterns=[
    ...         r"\\d{3}-\\d{3}-\\d{4}",  # 555-123-4567
    ...         r"\\(\\d{3}\\)\\s*\\d{3}-\\d{4}",  # (555) 123-4567
    ...     ],
    ... )
    >>> text = "Call 555-123-4567 or (555) 987-6543"
    >>> phone_extractor.extract(text)
    ['555-123-4567', '(555) 987-6543']

    >>> # Extract IP addresses
    >>> ip_extractor = CustomExtractor(
    ...     name="ip_address", patterns=[r"\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\b"]
    ... )
    >>> ip_extractor.extract("Server at 192.168.1.1")
    ['192.168.1.1']
    """

    def __init__(self, name: str, patterns: list[str]) -> None:
        """
        Initialize custom extractor with a name and regex patterns.

        :param name: Identifier for this extractor (used for logging/debugging)
        :type name: str
        :param patterns: List of regex patterns to match
        :type patterns: list[str]
        :raises ValueError: If any pattern is invalid regex
        """
        self.name = name
        self._extractor: RegexExtractor = RegexExtractor(patterns)
        logger.info("Initialized CustomExtractor '%s' with %d patterns", name, len(patterns))

    def extract(self, text: str, unique_occurrences: bool = False) -> list[str]:
        """
        Extract all matches from the input text using all registered patterns.

        :param text: The text to extract patterns from
        :type text: str
        :param unique_occurrences: Whether to remove duplicate matches (default is False)
        :type unique_occurrences: bool
        :return: List of matched strings
        :rtype: list[str]
        """
        logger.debug(
            "Starting extraction with CustomExtractor '%s' on text of length %d",
            self.name,
            len(text),
        )
        results = self._extractor.extract(text, unique_occurrences=unique_occurrences)
        logger.info(
            "CustomExtractor '%s' found %d matches (unique_occurrences=%s)",
            self.name,
            len(results),
            unique_occurrences,
        )
        return results

    def add_patterns(self, patterns: list[str]) -> None:
        """
        Add multiple patterns to the extractor.

        :param patterns: List of regex patterns to add
        :type patterns: list[str]
        :raises ValueError: If any pattern is invalid regex
        """
        logger.info("Adding %d new patterns to CustomExtractor '%s'", len(patterns), self.name)
        self._extractor.add_patterns(patterns)
        logger.debug(
            "Total patterns in CustomExtractor '%s': %d",
            self.name,
            len(self._extractor._regex_pattern_list),
        )

    @property
    def pattern_count(self) -> int:
        """Return the number of registered regex patterns."""
        return len(self._extractor._regex_pattern_list)

    @property
    def patterns(self) -> list[str]:
        """Return the registered regex patterns as strings."""
        return [item.pattern for item in self._extractor._regex_pattern_list]

    def __repr__(self) -> str:
        """Return string representation of the extractor."""
        pattern_list = [item.pattern for item in self._extractor._regex_pattern_list]
        return (
            f"CustomExtractor(name='{self.name}', "
            f"patterns_amount={len(pattern_list)}, "
            f"pattern_list={pattern_list})"
        )
