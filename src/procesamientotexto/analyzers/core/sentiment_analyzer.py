import re
from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.models.text_document import TextDocument

class SentimentAnalyzer(Analyzer):
    """Heuristic sentiment analyzer based on keywords."""

    POS_WORDS = {
        "good", "great", "excellent", "happy", "love", "best", "positive", "awesome", "amazing",
        "bueno", "excelente", "feliz", "amor", "mejor", "positivo", "increible", "maravilloso"
    }
    NEG_WORDS = {
        "bad", "terrible", "awful", "sad", "hate", "worst", "negative", "horrible", "poor",
        "malo", "terrible", "horrible", "triste", "odio", "peor", "negativo", "pobre"
    }

    def analyze(self, document: TextDocument) -> dict:
        text = document.content.lower()
        words = re.findall(r'\w+', text)
        
        if not words:
            result = {"sentiment": "neutral", "score": 0.0}
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
            "neg_count": neg_count
        }
        document.add_analysis("sentiment_analyzer", result)
        return result
