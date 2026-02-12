import logging
from typing import Any

from text_toolkit.models.text_document import TextDocument

from ..base import Analyzer
from .data import DataLoader

logger = logging.getLogger(__name__)


class LanguageDetector(Analyzer):
    """
    Analyzer that detects the language of a document.

    Uses a stopword overlap heuristic to identify the most likely language
    from a set of supported languages (es, en, fr, de, it, pt).
    """

    def __init__(self) -> None:
        """Initializes the LanguageDetector by loading stopwords from JSON."""
        self._stopwords: dict[str, set[str]] = DataLoader.load_stopwords()

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

        scores: dict[str, float] = {}
        for lang, words_list in self._stopwords.items():
            intersection = words.intersection(words_list)
            scores[lang] = len(intersection) / len(words_list) if words_list else 0.0

        best_lang = max(scores, key=lambda lang_code: scores[lang_code])
        confidence = scores[best_lang]

        # If no stopwords matched at all
        if confidence == 0:
            best_lang = "unknown"

        result = {"language": best_lang, "confidence": round(confidence, 2)}
        logger.info("Language detection result: %s (confidence: %.2f)", best_lang, confidence)
        return result
