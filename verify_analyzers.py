import sys
import os

# Add src to sys.path
sys.path.append(os.path.abspath("src"))

from procesamientotexto.models.text_document import TextDocument
from procesamientotexto.analyzers.core import (
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer,
)
from procesamientotexto.analyzers import AnalyzerRunner


def run_tests():
    print("Starting verification...")

    # Test English Doc
    en_content = "This is a great day. I love English! It is excellent."
    doc = TextDocument(content=en_content)

    # 2. FrequencyAnalyzer
    fa = FrequencyAnalyzer()
    fa_res = fa.analyze(doc)
    print(f"FrequencyAnalyzer: Total words {fa_res['total_words']}.")
    print(f"FrequencyAnalyzer: Most common length is {fa_res['most_common_length']}.")
    assert fa_res["total_words"] == 11
    assert fa_res["most_common_length"] > 0
    assert fa_res["top_words"]["great"] == 1

    # 3. LanguageDetector
    ld = LanguageDetector()
    ld_res = ld.analyze(doc)
    print(
        f"LanguageDetector: Detected {ld_res['language']} with confidence {ld_res['confidence']}."
    )
    assert ld_res["language"] == "en"

    # 4. SentimentAnalyzer
    sa = SentimentAnalyzer()
    sa_res = sa.analyze(doc)
    print(
        f"SentimentAnalyzer: Detected {sa_res['sentiment']} sentiment (score: {sa_res['score']})."
    )
    assert sa_res["sentiment"] == "positive"

    # 5. ReadabilityAnalyzer
    ra = ReadabilityAnalyzer()
    ra_res = ra.analyze(doc)
    print(f"ReadabilityAnalyzer: Avg word length {ra_res['avg_word_length']}.")
    assert ra_res["avg_word_length"] > 0

    # 6. AnalyzerRunner (Orchestrator)
    stats = AnalyzerRunner()
    stats_res = stats.analyze(doc)
    print("AnalyzerRunner: Summary consolidated successfully.")
    assert "word_stats" in stats_res
    assert "sentiment" in stats_res
    assert stats_res["total_chars"] == len(en_content)

    # Test Spanish Doc
    es_content = "Este es un día excelente. Me encanta el español! Es maravilloso."
    es_doc = TextDocument(content=es_content)

    stats_es = stats.analyze(es_doc)
    print(f"Spanish LanguageDetector: Detected {stats_es['language']['language']}.")
    assert stats_es["language"]["language"] == "es"
    assert stats_es["sentiment"]["sentiment"] == "positive"

    print("\nVerification COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        sys.exit(1)
