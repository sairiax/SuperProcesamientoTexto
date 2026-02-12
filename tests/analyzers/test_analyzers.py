import pytest
from procesamientotexto.models.text_document import TextDocument
from procesamientotexto.analyzers.core import (
    FrequencyAnalyzer,
    LanguageDetector,
    SentimentAnalyzer,
    ReadabilityAnalyzer,
)
from procesamientotexto.analyzers import AnalyzerRunner


@pytest.fixture
def english_doc():
    return TextDocument(content="This is a great day. I love English! It is excellent.")


@pytest.fixture
def spanish_doc():
    return TextDocument(
        content="Este es un día excelente. Me encanta el español! Es maravilloso."
    )


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


def test_analyzer_runner_orchestrator(english_doc):
    """Test that AnalyzerRunner orchestrates all analyzers with flat structure."""
    orchestrator = AnalyzerRunner()
    result = orchestrator.analyze(english_doc)

    # Check for flat structure (not nested)
    assert "total_words" in result  # From FrequencyAnalyzer
    assert "sentiment" in result  # From SentimentAnalyzer
    assert "language" in result  # From LanguageDetector
    assert "complexity" in result  # From ReadabilityAnalyzer

    # Verify it's a flat dict, not nested
    assert isinstance(result, dict)
    assert (
        result["total_words"] == 11
    )  # This is a great day. I love English! It is excellent.
