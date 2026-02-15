import logging

from text_toolkit.extractors.core import DateExtractor, EmailExtractor, URLExtractor
from text_toolkit.models.extraction_result import ExtractionResult
from text_toolkit.models.text_document import TextDocument

logger = logging.getLogger(__name__)


class ExtractorRunner:
    """
    Runner that coordinates multiple extractors to extract emails, URLs, and dates from text.

    This class initializes and manages extractors (EmailExtractor, URLExtractor, DateExtractor)
    and provides a unified interface to extract data from a document. You can specify which
    extractors to use or run all of them by default.

    Attributes
    ----------
    extractors : dict
        Dictionary mapping extractor types ('email', 'url', 'date') to their instances

    Parameters
    ----------
    extractor_names : list[str] | None, optional
        List of extractor class names to use (e.g., ['EmailExtractor', 'URLExtractor']).
        If None, all extractors are used.

    Example
    -------
    >>> from text_toolkit.extractors import ExtractorRunner
    >>> from text_toolkit.models.text_document import TextDocument
    >>> # Use all extractors
    >>> runner = ExtractorRunner()
    >>> # Use only specific extractors
    >>> runner_emails = ExtractorRunner(extractor_names=['EmailExtractor', 'URLExtractor'])
    >>> doc = TextDocument(
    ...     content="Contact: admin@example.com, visit https://example.com on 2026-03-15"
    ... )
    >>> result = runner.extract_all(doc)
    >>> result.email_matches
    ['admin@example.com']
    >>> result.url_matches
    ['https://example.com']
    >>> result.date_matches
    ['2026-03-15']
    """

    def __init__(self, extractor_names: list[str] | None = None) -> None:
        """
        Initialize the runner with specified or all available extractors.

        Parameters
        ----------
        extractor_names : list[str] | None, optional
            List of extractor class names to initialize. Valid values:
            'EmailExtractor', 'URLExtractor', 'DateExtractor'.
            If None, all extractors are initialized.
        """
        # Create all available extractors with their corresponding keys
        all_extractors = {
            'email': EmailExtractor(),
            'url': URLExtractor(),
            'date': DateExtractor(),
        }

        # Map extractor class names to their keys
        name_to_key = {
            'EmailExtractor': 'email',
            'URLExtractor': 'url',
            'DateExtractor': 'date',
        }

        if extractor_names:
            # only specified extractors
            self.extractors = {}
            for name in extractor_names:
                if name in name_to_key:
                    key = name_to_key[name]
                    self.extractors[key] = all_extractors[key]
                else:
                    logger.warning("Unknown extractor name: %s", name)
            logger.info("Initialized ExtractorRunner with specific extractors: %s", extractor_names)
        else:
            # all extractors
            self.extractors = all_extractors
            logger.info("Initialized ExtractorRunner with all core extractors")

        logger.debug("Active extractors: %s", list(self.extractors.keys()))
        logger.info("ExtractorRunner initialized successfully")

    def extract_all(
        self, document: TextDocument, unique_occurrences: bool = True
    ) -> ExtractionResult:
        """
        Extract emails, URLs, and dates from a document using configured extractors.

        Only extracts data for the extractor types that were initialized.

        Parameters
        ----------
        document : TextDocument
            The document to extract data from
        unique_occurrences : bool, optional
            Whether to remove duplicate matches (default is True)

        Returns
        -------
        ExtractionResult
            Object containing all extracted emails, URLs, and dates.
            Fields will be empty lists if the corresponding extractor is not active.

        Example
        -------
        >>> doc = TextDocument(content="Email: test@example.com, URL: https://test.com")
        >>> runner = ExtractorRunner(extractor_names=['EmailExtractor'])
        >>> result = runner.extract_all(doc, unique_occurrences=True)
        >>> len(result.email_matches)
        1
        >>> len(result.url_matches)
        0
        """
        if document.is_empty():
            logger.warning("Document is empty, returning empty extraction result")
            return ExtractionResult()

        logger.info("Starting extraction on document (content length: %d)", len(document.content))

        # Extract using only active extractors
        email_matches = []
        url_matches = []
        date_matches = []

        if 'email' in self.extractors:
            email_matches = self.extractors['email'].extract(document.content)
            logger.debug("Extracted %d emails", len(email_matches))

        if 'url' in self.extractors:
            url_matches = self.extractors['url'].extract(document.content)
            logger.debug("Extracted %d URLs", len(url_matches))

        if 'date' in self.extractors:
            date_matches = self.extractors['date'].extract(document.content)
            logger.debug("Extracted %d dates", len(date_matches))

        if unique_occurrences:
            email_matches = list(dict.fromkeys(email_matches))
            url_matches = list(dict.fromkeys(url_matches))
            date_matches = list(dict.fromkeys(date_matches))
            logger.debug("Applied unique_occurrences filter")

        logger.info(
            "Extraction completed: %d emails, %d URLs, %d dates",
            len(email_matches),
            len(url_matches),
            len(date_matches),
        )

        result = ExtractionResult(
            email_matches=email_matches,
            url_matches=url_matches,
            date_matches=date_matches,
            active_extractors=list(self.extractors.keys()),
        )

        logger.debug("Extraction result: %r", result)
        return result

    def __repr__(self) -> str:
        """Return string representation of the runner."""
        extractor_types = list(self.extractors.keys())
        return f"ExtractorRunner(extractors={extractor_types}, count={len(extractor_types)})"
