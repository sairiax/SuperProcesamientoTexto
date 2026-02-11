from typing import Any, Dict
from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument


class LanguageDetector(Analyzer):
    """
    Analyzer that detects the language of a document.

    Uses a stopword overlap heuristic to identify the most likely language
    from a set of supported languages (es, en, fr, de, it, pt).
    """

    STOPWORDS: Dict[str, set[str]] = {
        "es": {
            "el",
            "la",
            "de",
            "que",
            "y",
            "a",
            "en",
            "un",
            "ser",
            "se",
            "no",
            "por",
            "con",
            "para",
            "lo",
        },
        "en": {
            "the",
            "be",
            "to",
            "of",
            "and",
            "a",
            "in",
            "that",
            "have",
            "i",
            "it",
            "for",
            "not",
            "on",
            "with",
        },
        "fr": {
            "le",
            "la",
            "de",
            "et",
            "un",
            "être",
            "en",
            "à",
            "que",
            "ne",
            "pas",
            "ce",
            "sur",
            "se",
            "pour",
        },
        "de": {
            "der",
            "die",
            "das",
            "und",
            "sein",
            "in",
            "ein",
            "zu",
            "haben",
            "von",
            "den",
            "mit",
            "für",
            "auf",
            "ist",
        },
        "it": {
            "il",
            "di",
            "e",
            "a",
            "che",
            "un",
            "in",
            "per",
            "non",
            "uno",
            "da",
            "con",
            "si",
            "lo",
            "la",
        },
        "pt": {
            "o",
            "a",
            "de",
            "que",
            "e",
            "do",
            "da",
            "em",
            "um",
            "para",
            "com",
            "não",
            "uma",
            "os",
            "as",
        },
    }

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
        for lang, stopwords in self.STOPWORDS.items():
            intersection = words.intersection(stopwords)
            scores[lang] = len(intersection) / len(stopwords)

        best_lang = max(scores, key=scores.get)
        confidence = scores[best_lang]

        # If no stopwords matched at all
        if confidence == 0:
            best_lang = "unknown"

        result = {"language": best_lang, "confidence": round(confidence, 2)}
        return result
