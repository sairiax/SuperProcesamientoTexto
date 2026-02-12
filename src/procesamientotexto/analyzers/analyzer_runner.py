from .base import Analyzer
from .core import (
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer,
)
from procesamientotexto.models.text_document import TextDocument
import inspect
import sys


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
        for analyzer in self.analyzers:
            result = analyzer.analyze(document)

        freq_results = document.get_analysis("frequency_analyzer")

        # Consolidate results into a single summary
        summary = {}

        return summary
