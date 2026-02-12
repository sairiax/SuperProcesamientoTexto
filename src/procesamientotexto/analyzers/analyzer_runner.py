from procesamientotexto.models.text_document import TextDocument

from .base import Analyzer
from .core import (
    FrequencyAnalyzer,
    LanguageDetector,
    ReadabilityAnalyzer,
    SentimentAnalyzer,
)


class AnalyzerRunner(Analyzer):
    """Calculates document statistics by orchestrating all core analyzers."""

    def __init__(self):
        self.analyzers = [
            FrequencyAnalyzer(),
            LanguageDetector(),
            SentimentAnalyzer(),
            ReadabilityAnalyzer(),
        ]

    def analyze(self, document: TextDocument) -> dict:
        """Runs all core analyzers and consolidates results."""
        summary = {}

        for analyzer in self.analyzers:
            # Run the analyzer and merge results directly
            result = analyzer.analyze(document)
            summary.update(result)

        return summary
