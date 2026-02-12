from typing import ClassVar

from text_toolkit.extractors.base import BaseExtractor
from text_toolkit.models.text_document import TextDocument


class EmailExtractor(BaseExtractor):
    """Extractor for email addresses.

    This class supports standard email formats like user@example.com
    and usern.name+tag@domain.co.uk by default.

    """

    _email_patterns: ClassVar[list[str]] = [
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Standard email
    ]

    def __init__(self, text_document: TextDocument) -> None:
        super().__init__(text_document, self._email_patterns)
