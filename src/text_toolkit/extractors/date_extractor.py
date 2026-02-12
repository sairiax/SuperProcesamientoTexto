from typing import ClassVar

from text_toolkit.extractors.base import BaseExtractor
from text_toolkit.models.text_document import TextDocument


class DateExtractor(BaseExtractor):
    """Extractor for dates in various formats.

    This class supports different date formats:
    - YYYY-MM-DD (e.g., 2026-02-10)
    - DD/MM/YYYY or MM/DD/YYYY (e.g., 10/02/2026)
    - DD-MM-YYYY or MM-DD-YYYY (e.g., 10-02-2026)
    - D Month YYYY (e.g., 10 Feb 2026)
    - D-Month-YYYY (e.g., 10-Feb-2026)

    """

    _date_patterns: ClassVar[list[str]] = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
        r"\d{2}/\d{2}/\d{4}",  # DD/MM/YYYY or MM/DD/YYYY
        r"\d{2}-\d{2}-\d{4}",  # DD-MM-YYYY or MM-DD-YYYY
        r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}",  # 01 Jan 2026
        r"\d{1,2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}",  # 01-Jan-2026
    ]

    def __init__(self, text_document: TextDocument) -> None:
        super().__init__(text_document, self._date_patterns)
