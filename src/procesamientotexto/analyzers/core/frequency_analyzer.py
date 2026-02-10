from collections import Counter
import re
from .base import Analyzer
from procesamientotexto.models.text_document import TextDocument

class FrequencyAnalyzer(Analyzer):
    """Analyzes word frequencies and provides top words."""

    def analyze(self, document: TextDocument) -> dict:
        text = document.content.lower()
        words = re.findall(r'\w+', text)
        
        if not words:
            result = {"top_words": {}, "most_common_length": 0}
            document.add_analysis("frequency_analyzer", result)
            return result

        word_counts = Counter(words)
        top_words = dict(word_counts.most_common(10))
        
        lengths = [len(w) for w in words]
        length_counts = Counter(lengths)
        most_common_length = length_counts.most_common(1)[0][0] if lengths else 0
        
        result = {
            "top_words": top_words,
            "most_common_length": most_common_length
        }
        document.add_analysis("frequency_analyzer", result)
        return result
