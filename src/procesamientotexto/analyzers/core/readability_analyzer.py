from typing import Any, Dict
from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument
import re


class ReadabilityAnalyzer(Analyzer):
    """
    Analyzer that calculates basic readability metrics.

    Calculates average sentence length and average word length to estimate
    complexity, adjusting for the document's language if available.
    """

    # TODO: add more language support
    # Language-specific thresholds for complexity classification
    COMPLEXITY_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "es": {
            "sent_high": 30,
            "sent_med": 20,
            "word_high": 6.5,
            "word_med": 5.5,
        },
        "en": {
            "sent_high": 25,
            "sent_med": 15,
            "word_high": 6.0,
            "word_med": 5.0,
        },
        "default": {
            "sent_high": 25,
            "sent_med": 15,
            "word_high": 6.0,
            "word_med": 5.0,
        },
    }

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
        sentences = self._extract_sentences(document.content)
        words = document.tokens

        if not words or not sentences:
            return self._empty_result()

        avg_sentence_len = len(words) / len(sentences)
        avg_word_len = sum(len(w) for w in words) / len(words)

        language = self._get_document_language(document)
        complexity = self._calculate_complexity(
            avg_sentence_len, avg_word_len, language
        )

        return {
            "avg_sentence_length": round(avg_sentence_len, 2),
            "avg_word_length": round(avg_word_len, 2),
            "complexity": complexity,
        }

    def _extract_sentences(self, text: str) -> list[str]:
        """
        Extracts non-empty sentences from text.

        Args:
            text (str): The text to process.

        Returns:
            list[str]: List of non-empty sentence strings.
        """
        sentences = re.split(r"[.!?]+", text)
        return [s for s in sentences if s.strip()]

    def _get_document_language(self, document: TextDocument) -> str:
        """
        Retrieves the detected language from previous analysis.

        Args:
            document (TextDocument): The document being analyzed.

        Returns:
            str: Language code or 'unknown'.
        """
        lang_result = document.get_analysis("language_detector")
        return lang_result.get("language") if lang_result else "unknown"

    def _calculate_complexity(
        self, avg_sentence_len: float, avg_word_len: float, language: str
    ) -> str:
        """
        Calculates complexity level based on averages and language thresholds.

        Args:
            avg_sentence_len (float): Average sentence length in words.
            avg_word_len (float): Average word length in characters.
            language (str): Language code for threshold selection.

        Returns:
            str: Complexity level ('low', 'medium', or 'high').
        """
        thresholds = self.COMPLEXITY_THRESHOLDS.get(
            language, self.COMPLEXITY_THRESHOLDS["default"]
        )

        if (
            avg_sentence_len > thresholds["sent_high"]
            or avg_word_len > thresholds["word_high"]
        ):
            return "high"
        elif (
            avg_sentence_len > thresholds["sent_med"]
            or avg_word_len > thresholds["word_med"]
        ):
            return "medium"
        else:
            return "low"

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        """Generates a valid result for an empty document.

        All fields are set to default values.
        """
        return {
            "avg_sentence_length": 0.0,
            "avg_word_length": 0.0,
            "complexity": "unknown",
        }
