import pytest
from procesamientotexto.models.text_document import TextDocument
from procesamientotexto.analyzers.core import (
    WordCounter,
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer
)
from procesamientotexto.analyzers import Statistics

@pytest.fixture
def english_doc():
    return TextDocument(content="This is a great day. I love English! It is excellent.")

@pytest.fixture
def spanish_doc():
    return TextDocument(content="Este es un día excelente. Me encanta el español! Es maravilloso.")

def test_word_counter(english_doc):
    analyzer = WordCounter()
    result = analyzer.analyze(english_doc)
    assert result["total_words"] > 0
    assert "great" in result["word_frequencies"]
    assert english_doc.has_analysis("word_counter")

def test_frequency_analyzer(english_doc):
    analyzer = FrequencyAnalyzer()
    result = analyzer.analyze(english_doc)
    assert "top_words" in result
    assert result["most_common_length"] > 0

def test_language_detector(english_doc, spanish_doc):
    analyzer = LanguageDetector()
    en_result = analyzer.analyze(english_doc)
    es_result = analyzer.analyze(spanish_doc)
    assert en_result["language"] == "en"
    assert es_result["language"] == "es"

def test_sentiment_analyzer(english_doc):
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(english_doc)
    assert result["sentiment"] == "positive"
    assert result["score"] > 0

def test_readability_analyzer(english_doc):
    analyzer = ReadabilityAnalyzer()
    result = analyzer.analyze(english_doc)
    assert result["avg_sentence_length"] > 0
    assert result["avg_word_length"] > 0

def test_statistics_orchestrator(english_doc):
    orchestrator = Statistics()
    result = orchestrator.analyze(english_doc)
    assert "word_stats" in result
    assert "sentiment" in result
    assert "language" in result
    assert result["word_stats"]["total_words"] == 10 # This is a great day. I love English! It is excellent.
