from collections import Counter
from typing import Any

from procesamientotexto.models.text_document import TextDocument

from ..base import Analyzer


class FrequencyAnalyzer(Analyzer):
    """
    Analyzer that calculates word frequencies and token AnalyzerRunner.

    This analyzer counts the occurrences of each word, the total number of words,
    and determines the most common token length.
    """

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Analyzes the document to extract frequency AnalyzerRunner.

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
            # TODO: log.warning -> Zero tokens to analyze
            return self._empty_result()

        # TODO: log.info -> starting frequency analysis
        word_counts = Counter(tokens)
        length_counts = Counter(map(len, tokens))

        most_common_len_data = length_counts.most_common(1)
        most_common_len = most_common_len_data[0][0] if most_common_len_data else 0
        # TODO: log.info -> ends frequency analysis

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
