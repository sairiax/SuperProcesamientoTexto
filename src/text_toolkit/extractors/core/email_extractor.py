import logging
from typing import ClassVar

from text_toolkit.extractors.base import RegexExtractor

logger = logging.getLogger(__name__)


class EmailExtractor(RegexExtractor):
    """Extractor for email addresses.

    This class supports standard email formats like user@example.com
    and usern.name+tag@domain.co.uk by default.

    """
    name: ClassVar[str] = "EmailExtractor"
    _email_patterns: ClassVar[list[str]] = [
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Standard email
    ]

    def __init__(self) -> None:
        super().__init__(self._email_patterns)
        logger.info("Initialized %s with %d patterns", self.name, len(self._email_patterns))

    def __repr__(self) -> str:
        """Return string representation of the extractor."""
        pattern_list = [item.pattern for item in self._regex_pattern_list]
        return f"{self.name}(patterns_amount={len(pattern_list)}, pattern_list={pattern_list})"
