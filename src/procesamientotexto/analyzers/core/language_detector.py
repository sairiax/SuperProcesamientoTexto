import re
from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument


class LanguageDetector(Analyzer):
    """Detects text language based on common stopword overlap."""

    STOPWORDS = {
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

    def analyze(self, document: TextDocument) -> dict:

        # TODO: Cambiar esto por tokenizer + normalizer?
        text = document.content.lower()
        words = set(re.findall(r"\w+", text))

        if not words:
            result = {"language": "unknown", "confidence": 0.0}
            document.add_analysis("language_detector", result)
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
        document.add_analysis("language_detector", result)
        return result
