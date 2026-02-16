import logging
from typing import ClassVar

from text_toolkit.extractors.base import RegexExtractor

logger = logging.getLogger(__name__)


class URLExtractor(RegexExtractor):
    """Extractor for URLs

    This class support URLs with different protocols:

    - HTTP/HTTPS (e.g., https://www.example.com, http://example.com:8080)
    - FTP (e.g., ftp://ftp.example.com/file.txt)
    - URLs without protocol (e.g., www.example.com)

    """

    name: ClassVar[str] = "URLExtractor"
    _url_patterns: ClassVar[list[str]] = [
        r"https?://(?:[-\w./?%&=+#]|(?:%[\da-fA-F]{2}))+",  # HTTP/HTTPS URLs
        r"ftp://(?:[-\w./?%&=+#]|(?:%[\da-fA-F]{2}))+",  # FTP URLs
        r"www\.(?:[-\w./?%&=+#]|(?:%[\da-fA-F]{2}))+",  # www URLs without protocol
    ]

    def __init__(self) -> None:
        super().__init__(self._url_patterns)
        logger.info("Initialized %s with %d patterns", self.name, len(self._url_patterns))

    def __repr__(self) -> str:
        """Return string representation of the extractor."""
        pattern_list = [item.pattern for item in self._regex_pattern_list]
        return f"{self.name}(patterns_amount={len(pattern_list)}, pattern_list={pattern_list})"
