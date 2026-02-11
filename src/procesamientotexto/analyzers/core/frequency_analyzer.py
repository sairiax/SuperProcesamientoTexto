from collections import Counter
import re
from typing import Any

from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument


class FrequencyAnalyzer(Analyzer):
    """Analyzes word frequencies.

    Provides:
    - top_n words
    - total word count
    - most common token length
    """

    # TODO: Cambiar tokenización por la de mi compa
    TOKEN_REGEX = re.compile(r"\w+")

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        text = (
            document.content.lower()
        )  # TODO: Cambiar por la normalización de mi compa?
        tokens = self._tokenize(text)  # TODO: Cambiar tokenización por la de mi compa

        if not tokens:
            result = self._empty_result()
            document.add_analysis("frequency_analyzer", result)
            return result

        word_counts = Counter(tokens)
        length_counts = Counter(map(len, tokens))

        result = {
            "total_words": len(tokens),
            "top_words": dict(word_counts.most_common(10)),
            "most_common_length": length_counts.most_common(1)[0][0],
        }

        document.add_analysis("frequency_analyzer", result)
        return result

    @classmethod
    def _tokenize(cls, text: str) -> list[str]:
        return cls.TOKEN_REGEX.findall(text)

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        return {
            "total_words": 0,
            "top_words": {},
            "most_common_length": 0,
        }
