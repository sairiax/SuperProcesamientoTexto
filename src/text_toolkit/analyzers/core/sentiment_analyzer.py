import logging
from typing import Any

from text_toolkit.models.text_document import TextDocument

from ..base import Analyzer
from .data import DataLoader

logger = logging.getLogger(__name__)


class SentimentAnalyzer(Analyzer):
    """
    Analyzer that estimates sentiment polarity using keyword heuristics.

    Classifies sentiment as positive, negative, or neutral based on
    the presence of predefined keywords.
    """

    def __init__(self) -> None:
        """Initializes the SentimentAnalyzer by loading keywords from JSON."""
        self._pos_words: set[str]
        self._neg_words: set[str]
        self._pos_words, self._neg_words = DataLoader.load_sentiment_words()

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Analyzes the sentiment of the document.

        Args:
            document (TextDocument): The document to analyze.

        Returns:
            dict[str, Any]: A dictionary containing:
                - 'sentiment': 'positive', 'negative', or 'neutral'.
                - 'score': A float score between -1.0 and 1.0.
                - 'pos_count': Number of positive words found.
                - 'neg_count': Number of negative words found.
        """
        words = document.tokens
        if not words:
            return self._empty_result()

        pos_count = sum(1 for w in words if w in self._pos_words)
        neg_count = sum(1 for w in words if w in self._neg_words)
        total_sentiment_words = pos_count + neg_count

        score = (
            (pos_count - neg_count) / total_sentiment_words if total_sentiment_words > 0 else 0.0
        )
        sentiment = self._get_label(score)

        result = {
            "sentiment": sentiment,
            "score": round(score, 2),
            "pos_count": pos_count,
            "neg_count": neg_count,
        }
        logger.info(
            "Sentiment result: %s (score: %.2f, pos: %d, neg: %d)",
            sentiment,
            score,
            pos_count,
            neg_count,
        )
        return result

    def _get_label(self, score: float) -> str:
        if score > 0.1:
            return "positive"
        if score < -0.1:
            return "negative"
        return "neutral"

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        """Generates a valid result for a text with no words.

        All values are set to default.
        """
        return {
            "sentiment": "neutral",
            "score": 0.0,
            "pos_count": 0,
            "neg_count": 0,
        }
