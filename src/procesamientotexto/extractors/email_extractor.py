from procesamientotexto.extractors.base import BaseExtractor
from procesamientotexto.models.text_document import TextDocument


class EmailExtractor(BaseExtractor):
    """Extractor for email addresses.

    This class support by default standar email formats: user@example.com, usern.name+tag@domain.co.uk

    """
    _email_patterns = [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Standard email
    ]

    def __init__(self, text_document: TextDocument) -> None:
        super().__init__(text_document, self._email_patterns)