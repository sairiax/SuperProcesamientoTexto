from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.analyzers.core import (
    WordCounter,
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer
)
from procesamientotexto.models.text_document import TextDocument

class Statistics(Analyzer):
    """Calculates document statistics by orchestrating other analyzers."""

    def __init__(self):
        self.analyzers = [
            WordCounter(),
            FrequencyAnalyzer(),
            LanguageDetector(),
            SentimentAnalyzer(),
            ReadabilityAnalyzer()
        ]

    def analyze(self, document: TextDocument) -> dict:
        """Runs all core analyzers and consolidates results."""
        summary = {}
        for analyzer in self.analyzers:
            result = analyzer.analyze(document)
            # Use the class name lowercase (minus 'analyzer') as the key if possible
            # but for now we follow the internal add_analysis keys
            pass # The results are already added to document.analysis_results by the analyzers themselves
            
        summary = {
            "word_stats": document.get_analysis("word_counter"),
            "frequencies": document.get_analysis("frequency_analyzer"),
            "language": document.get_analysis("language_detector"),
            "sentiment": document.get_analysis("sentiment_analyzer"),
            "readability": document.get_analysis("readability_analyzer"),
            "total_chars": len(document.content),
            "total_chars_no_spaces": len(document.content.replace(" ", "").replace("\n", ""))
        }
        
        document.add_analysis("statistics", summary)
        return summary
