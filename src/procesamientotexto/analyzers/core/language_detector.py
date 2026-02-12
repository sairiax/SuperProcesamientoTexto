from typing import Any

from procesamientotexto.models.text_document import TextDocument

from ..base import Analyzer
from ._language_data import STOPWORDS


class LanguageDetector(Analyzer):
    """
    Analyzer that detects the language of a document.

    Uses a stopword overlap heuristic to identify the most likely language
    from a set of supported languages (es, en, fr, de, it, pt).
    """

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Detects the language of the document.

        Args:
           document (TextDocument): The document to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'language': Detected language code (e.g., 'en', 'es') or 'unknown'.
                - 'confidence': Confidence score between 0.0 and 1.0.
        """
        # Note: document.tokens already provides lowercased tokens via standard tokenization
        words = set(document.tokens)

        if not words:
            result = {"language": "unknown", "confidence": 0.0}
            return result

        scores = {}
        for lang, stopwords in STOPWORDS.items():
            intersection = words.intersection(stopwords)
            scores[lang] = len(intersection) / len(stopwords)

        best_lang = max(scores, key=scores.get)
        confidence = scores[best_lang]

        # If no stopwords matched at all
        if confidence == 0:
            best_lang = "unknown"

        result = {"language": best_lang, "confidence": round(confidence, 2)}
        return result
