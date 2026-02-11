from typing import Any, Dict
from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.models.text_document import TextDocument


class SentimentAnalyzer(Analyzer):
    """
    Analyzer that estimates sentiment polarity using keyword heuristics.

    Classifies sentiment as positive, negative, or neutral based on
    the presence of predefined keywords.
    """

    POS_WORDS = {
        "good",
        "great",
        "excellent",
        "happy",
        "love",
        "best",
        "positive",
        "awesome",
        "amazing",
        "bueno",
        "excelente",
        "feliz",
        "amor",
        "mejor",
        "positivo",
        "increible",
        "maravilloso",
    }
    NEG_WORDS = {
        "bad",
        "terrible",
        "awful",
        "sad",
        "hate",
        "worst",
        "negative",
        "horrible",
        "poor",
        "malo",
        "terrible",
        "horrible",
        "triste",
        "odio",
        "peor",
        "negativo",
        "pobre",
    }

    def analyze(self, document: TextDocument) -> Dict[str, Any]:
        """
        Analyzes the sentiment of the document.

        Args:
            document (TextDocument): The document to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'sentiment': 'positive', 'negative', or 'neutral'.
                - 'score': A float score between -1.0 and 1.0.
                - 'pos_count': Number of positive words found.
                - 'neg_count': Number of negative words found.
        """
        words = document.tokens

        if not words:
            result = {
                "sentiment": "neutral",
                "score": 0.0,
                "pos_count": 0,
                "neg_count": 0,
            }
            document.add_analysis("sentiment_analyzer", result)
            return result

        pos_count = sum(1 for w in words if w in self.POS_WORDS)
        neg_count = sum(1 for w in words if w in self.NEG_WORDS)

        total_sentiment_words = pos_count + neg_count
        if total_sentiment_words == 0:
            score = 0.0
            sentiment = "neutral"
        else:
            score = (pos_count - neg_count) / total_sentiment_words
            if score > 0.1:
                sentiment = "positive"
            elif score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"

        result = {
            "sentiment": sentiment,
            "score": round(score, 2),
            "pos_count": pos_count,
            "neg_count": neg_count,
        }
        document.add_analysis("sentiment_analyzer", result)
        return result
