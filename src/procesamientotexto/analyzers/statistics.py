from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.analyzers.core import (
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer,
)
from procesamientotexto.models.text_document import TextDocument


class Statistics(Analyzer):
    """Calculates document statistics by orchestrating other analyzers."""

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
            result = analyzer.analyze(document)
            pass

        freq_results = document.get_analysis("frequency_analyzer")

        summary = {
            "word_stats": {
                "total_words": freq_results.get("total_words", 0) if freq_results else 0
            },
            "frequencies": freq_results,
            "language": document.get_analysis("language_detector"),
            "sentiment": document.get_analysis("sentiment_analyzer"),
            "readability": document.get_analysis("readability_analyzer"),
            "total_chars": len(document.content),
            "total_chars_no_spaces": len(
                document.content.replace(" ", "").replace("\n", "")
            ),
        }

        document.add_analysis("statistics", summary)
        return summary
