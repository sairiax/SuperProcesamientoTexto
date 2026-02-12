import logging

from text_toolkit.extractors.core import DateExtractor, EmailExtractor, URLExtractor
from text_toolkit.models.text_document import ExtractionResult, TextDocument

logger = logging.getLogger(__name__)


class ExtractorRunner:
    """
    Runner that coordinates multiple extractors to extract emails, URLs, and dates from text.

    This class initializes and manages the three main extractors (EmailExtractor,
    URLExtractor, DateExtractor) and provides a unified interface to extract all
    types of data from a document.

    Attributes
    ----------
    email_extractor : EmailExtractor
        Extractor for email addresses
    url_extractor : URLExtractor
        Extractor for URLs
    date_extractor : DateExtractor
        Extractor for dates in various formats

    Example
    -------
    >>> from text_toolkit.extractors import ExtractorRunner
    >>> from text_toolkit.models.text_document import TextDocument
    >>> runner = ExtractorRunner()
    >>> doc = TextDocument(content="Contact: admin@example.com, visit https://example.com on 2026-03-15")
    >>> result = runner.extract_all(doc)
    >>> result.email_matches
    ['admin@example.com']
    >>> result.url_matches
    ['https://example.com']
    >>> result.date_matches
    ['2026-03-15']
    """

    def __init__(self) -> None:
        """Initialize the runner with all available extractors."""
        logger.info("Initializing ExtractorRunner with all core extractors")
        self.email_extractor = EmailExtractor()
        self.url_extractor = URLExtractor()
        self.date_extractor = DateExtractor()
        logger.info("ExtractorRunner initialized successfully")

    def extract_all(
        self, document: TextDocument, unique_occurrences: bool = True
    ) -> ExtractionResult:
        """
        Extract emails, URLs, and dates from a document.

        Parameters
        ----------
        document : TextDocument
            The document to extract data from
        unique_occurrences : bool, optional
            Whether to remove duplicate matches (default is True)

        Returns
        -------
        ExtractionResult
            Object containing all extracted emails, URLs, and dates

        Example
        -------
        >>> doc = TextDocument(content="Email: test@example.com, URL: https://test.com")
        >>> runner = ExtractorRunner()
        >>> result = runner.extract_all(doc, unique_occurrences=True)
        >>> len(result.email_matches)
        1
        """
        if document.is_empty():
            logger.warning("Document is empty, returning empty extraction result")
            return ExtractionResult()

        logger.info("Starting extraction on document (content length: %d)", len(document.content))

        email_matches = self.email_extractor.extract(document.content)
        url_matches = self.url_extractor.extract(document.content)
        date_matches = self.date_extractor.extract(document.content)

        if unique_occurrences:
            email_matches = list(dict.fromkeys(email_matches))
            url_matches = list(dict.fromkeys(url_matches))
            date_matches = list(dict.fromkeys(date_matches))
            logger.debug("Applied unique_occurrences filter")

        logger.info(
            "Extraction completed: %d emails, %d URLs, %d dates",
            len(email_matches),
            len(url_matches),
            len(date_matches)
        )

        return ExtractionResult(
            email_matches=email_matches,
            url_matches=url_matches,
            date_matches=date_matches,
        )

    def __repr__(self) -> str:
        """Return string representation of the runner."""
        return (
            f"ExtractorRunner("
            f"email_extractor={self.email_extractor}, "
            f"url_extractor={self.url_extractor}, "
            f"date_extractor={self.date_extractor})"
        )
