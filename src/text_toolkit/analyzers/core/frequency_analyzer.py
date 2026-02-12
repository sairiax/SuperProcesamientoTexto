import logging
from collections import Counter
from typing import Any

from text_toolkit.models.text_document import TextDocument

from ..base import Analyzer

# Use the package-level logger hierarchy
logger = logging.getLogger(__name__)


class FrequencyAnalyzer(Analyzer):
    """
    Analyzer that calculates word frequencies and token statistics.

    This analyzer counts the occurrences of each word, the total number of words,
    and determines the most common token length.
    """

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Analyzes the document to extract frequency statistics.

        Args:
            document (TextDocument): The document to analyze.

        Returns:
            dict[str, Any]: A dictionary containing:
                - 'total_words': Total count of tokens.
                - 'top_words': Dictionary of top 10 most common words.
                - 'word_counts': Dictionary of Word:Occurrences.
                - 'most_common_length': The most frequent token length.
        """
        tokens = document.tokens

        if not tokens:
            logger.warning("Document contains no tokens. Skipping frequency analysis.")
            return self._empty_result()

        logger.info("Starting frequency analysis on %d tokens.", len(tokens))
        word_counts = Counter(tokens)
        length_counts = Counter(map(len, tokens))

        most_common_len_data = length_counts.most_common(1)
        most_common_len = most_common_len_data[0][0] if most_common_len_data else 0

        logger.info("Frequency analysis completed. Most common word length: %d", most_common_len)

        result = {
            "total_words": len(tokens),
            "top_words": dict(word_counts.most_common(10)),
            "word_counts": dict(word_counts),
            "most_common_length": most_common_len,
        }

        return result

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        """Generates a valid result for an empty document.

        All fields are set to default values.
        """
        return {
            "total_words": 0,
            "top_words": {},
            "word_counts": {},
            "most_common_length": 0,
        }
