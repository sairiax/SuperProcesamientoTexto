import logging
from typing import ClassVar

from text_toolkit.extractors.base import RegexExtractor

logger = logging.getLogger(__name__)


class DateExtractor(RegexExtractor):
    """Extractor for dates in various formats.

    This class supports different date formats:
    - YYYY-MM-DD (e.g., 2026-02-10)
    - DD/MM/YYYY or MM/DD/YYYY (e.g., 10/02/2026)
    - DD-MM-YYYY or MM-DD-YYYY (e.g., 10-02-2026)
    - D Month YYYY (e.g., 10 Feb 2026)
    - D-Month-YYYY (e.g., 10-Feb-2026)

    """

    name: ClassVar[str] = "DateExtractor"
    _date_patterns: ClassVar[list[str]] = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
        r"\d{2}/\d{2}/\d{4}",  # DD/MM/YYYY or MM/DD/YYYY
        r"\d{2}-\d{2}-\d{4}",  # DD-MM-YYYY or MM-DD-YYYY
        r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}",  # 01 Jan 2026
        r"\d{1,2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}",  # 01-Jan-2026
        r"\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{4}",  # 01 jan 2026
        r"\d{1,2}-(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-\d{4}",  # 01-jan-2026
    ]

    def __init__(self) -> None:
        super().__init__(self._date_patterns)
        logger.info("Initialized %s with %d patterns", self.name, len(self._date_patterns))

    def __repr__(self) -> str:
        """Return string representation of the extractor."""
        pattern_list = [item.pattern for item in self._regex_pattern_list]
        return f"{self.name}(patterns_amount={len(pattern_list)}, pattern_list={pattern_list})"
