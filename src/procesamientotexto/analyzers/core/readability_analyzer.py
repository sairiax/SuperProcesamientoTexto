import re
from typing import Any, Dict
from procesamientotexto.analyzers.core.base import Analyzer
from procesamientotexto.models.text_document import TextDocument


class ReadabilityAnalyzer(Analyzer):
    """
    Analyzer that calculates basic readability metrics.

    Calculates average sentence length and average word length to estimate
    complexity, adjusting for the document's language if available.
    """

    def analyze(self, document: TextDocument) -> Dict[str, Any]:
        """
        Analyzes the readability of the document.

        Args:
            document (TextDocument): The document to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'avg_sentence_length': Average number of words per sentence.
                - 'avg_word_length': Average characters per word.
                - 'complexity': 'low', 'medium', 'high', or 'unknown'.
        """
        text = document.content
        sentences = re.split(r"[.!?]+", text)
        sentences = [s for s in sentences if s.strip()]

        words = re.findall(r"\w+", text)

        if not words or not sentences:
            result = {
                "avg_sentence_length": 0.0,
                "avg_word_length": 0.0,
                "complexity": "unknown",
            }
            document.add_analysis("readability_analyzer", result)
            return result

        avg_sentence_len = len(words) / len(sentences)
        avg_word_len = sum(len(w) for w in words) / len(words)

        # Determine language context from previous analysis
        lang_result = document.get_analysis("language_detector")
        language = lang_result.get("language") if lang_result else "unknown"

        # Adjust thresholds based on language
        # Spanish tends to have slightly longer sentences and words than English
        if language == "es":
            sent_threshold_high = 30
            sent_threshold_med = 20
            word_threshold_high = 6.5
            word_threshold_med = 5.5
        elif language == "en":
            sent_threshold_high = 25
            sent_threshold_med = 15
            word_threshold_high = 6.0
            word_threshold_med = 5.0
        else:
            # Fallback / Unknown - use conservative/English-like defaults
            sent_threshold_high = 25
            sent_threshold_med = 15
            word_threshold_high = 6.0
            word_threshold_med = 5.0

        if avg_sentence_len > sent_threshold_high or avg_word_len > word_threshold_high:
            complexity = "high"
        elif avg_sentence_len > sent_threshold_med or avg_word_len > word_threshold_med:
            complexity = "medium"
        else:
            complexity = "low"

        result = {
            "avg_sentence_length": round(avg_sentence_len, 2),
            "avg_word_length": round(avg_word_len, 2),
            "complexity": complexity,
        }
        document.add_analysis("readability_analyzer", result)
        return result
