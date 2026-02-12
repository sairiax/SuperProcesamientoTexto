from typing import Any

from procesamientotexto.models.text_document import TextDocument

from ..base import Analyzer
from ._sentiment_data import NEG_WORDS, POS_WORDS


class SentimentAnalyzer(Analyzer):
    """
    Analyzer that estimates sentiment polarity using keyword heuristics.

    Classifies sentiment as positive, negative, or neutral based on
    the presence of predefined keywords.
    """

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

        pos_count = sum(1 for w in words if w in POS_WORDS)
        neg_count = sum(1 for w in words if w in NEG_WORDS)
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
