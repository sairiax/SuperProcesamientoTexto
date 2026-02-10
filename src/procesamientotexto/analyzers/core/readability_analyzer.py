import re
from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.models.text_document import TextDocument

class ReadabilityAnalyzer(Analyzer):
    """Basic readability metrics."""

    def analyze(self, document: TextDocument) -> dict:
        text = document.content
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        
        words = re.findall(r'\w+', text)
        
        if not words or not sentences:
            result = {
                "avg_sentence_length": 0.0,
                "avg_word_length": 0.0,
                "complexity": "unknown"
            }
            document.add_analysis("readability_analyzer", result)
            return result

        avg_sentence_len = len(words) / len(sentences)
        avg_word_len = sum(len(w) for w in words) / len(words)
        
        # Simple complexity heuristic
        if avg_sentence_len > 25 or avg_word_len > 6:
            complexity = "high"
        elif avg_sentence_len > 15 or avg_word_len > 5:
            complexity = "medium"
        else:
            complexity = "low"

        result = {
            "avg_sentence_length": round(avg_sentence_len, 2),
            "avg_word_length": round(avg_word_len, 2),
            "complexity": complexity
        }
        document.add_analysis("readability_analyzer", result)
        return result
