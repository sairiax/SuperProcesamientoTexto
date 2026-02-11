from collections import Counter
from typing import Any
from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument

class WordCounter(Analyzer):
    """Counts the number of words in a document and their frequencies."""

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        # TODO: Usar normalizer.py y cleaner.py
        text = document.content.lower()

        # TODO: Usar el tokenizer de transformers
        words = ["hola", "mundo", "hola", "adios", "adios", "adios"]
        
        word_counts = Counter(words)
        result = {
            "total_words": len(words),
            "word_frequencies": dict(word_counts)
        }
        document.add_analysis("word_counter", result)
        return result
