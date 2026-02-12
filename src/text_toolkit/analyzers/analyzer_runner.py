import logging

from text_toolkit.models.text_document import TextDocument

from .base import Analyzer
from .core import (
    FrequencyAnalyzer,
    LanguageDetector,
    ReadabilityAnalyzer,
    SentimentAnalyzer,
)

logger = logging.getLogger(__name__)


class AnalyzerRunner(Analyzer):
    """Calculates document statistics by orchestrating all core analyzers."""

    def __init__(self, analyzer_names: list[str] | None = None):
        all_analyzers: list[Analyzer] = [
            FrequencyAnalyzer(),
            LanguageDetector(),
            SentimentAnalyzer(),
            ReadabilityAnalyzer(),
        ]
        if analyzer_names:
            self.analyzers = [a for a in all_analyzers if a.__class__.__name__ in analyzer_names]
            logger.info("Initialized AnalyzerRunner with specific analyzers: %s", analyzer_names)
        else:
            self.analyzers = all_analyzers
            logger.info("Initialized AnalyzerRunner with all available analyzers.")
        logger.debug("Initialized %r", self)

    def analyze(self, document: TextDocument) -> dict:
        """Runs all core analyzers and consolidates results."""
        summary = {}

        logger.info("Initializing full document analysis with %d analyzers.", len(self.analyzers))
        for analyzer in self.analyzers:
            analyzer_name = analyzer.__class__.__name__
            logger.debug("Executing analyzer: %s", analyzer_name)

            result = analyzer.analyze(document)
            summary.update(result)
            logger.debug("Analyzer %s completed. Result: %s", analyzer_name, result)

        logger.info("Document analysis orchestration complete.")
        return summary

    def __repr__(self) -> str:
        """Return a concise representation for logging/debugging."""
        analyzer_names = [analyzer.__class__.__name__ for analyzer in self.analyzers]
        return (
            "AnalyzerRunner("
            f"analyzers={analyzer_names}, "
            f"count={len(analyzer_names)})"
        )
