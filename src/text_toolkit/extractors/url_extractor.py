from typing import ClassVar

from text_toolkit.extractors.base import BaseExtractor
from text_toolkit.models.text_document import TextDocument


class URLExtractor(BaseExtractor):
    """Extractor for URLs

    This class support URLs with different protocols:

    - HTTP/HTTPS (e.g., https://www.example.com, http://example.com:8080)
    - FTP (e.g., ftp://ftp.example.com/file.txt)
    - URLs without protocol (e.g., www.example.com)

    """

    _url_patterns: ClassVar[list[str]] = [
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",  # HTTP/HTTPS URLs
        r"ftp://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",  # FTP URLs
        r"www\.(?:[-\w.]|(?:%[\da-fA-F]{2}))+",  # www URLs without protocol
    ]

    def __init__(self, text_document: TextDocument) -> None:
        super().__init__(text_document, self._url_patterns)
