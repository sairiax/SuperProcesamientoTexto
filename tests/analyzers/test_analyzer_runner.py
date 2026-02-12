"""Tests for AnalyzerRunner."""

from text_toolkit.analyzers.analyzer_runner import AnalyzerRunner
from text_toolkit.models.text_document import TextDocument


class TestAnalyzerRunner:
    """Test suite for AnalyzerRunner."""

    def test_all_analyzers_executed(self, english_doc: TextDocument):
        """Test that all analyzers are executed and results are present."""
        runner = AnalyzerRunner()
        result = runner.analyze(english_doc)

        # Frequency analyzer results
        assert "total_words" in result
        assert "top_words" in result
        assert "word_counts" in result
        assert "most_common_length" in result

        # Language detector results
        assert "language" in result
        assert "confidence" in result

        # Sentiment analyzer results
        assert "sentiment" in result
        assert "score" in result
        assert "pos_count" in result
        assert "neg_count" in result

        # Readability analyzer results
        assert "avg_sentence_length" in result
        assert "avg_word_length" in result
        assert "complexity" in result

    def test_flat_structure(self, english_doc: TextDocument):
        """Test that results are returned in a flat dictionary structure."""
        runner = AnalyzerRunner()
        result = runner.analyze(english_doc)

        # Should be a flat dict, not nested
        assert isinstance(result, dict)
        # Check that keys are at the top level
        assert "total_words" in result
        assert "language" in result
        assert "sentiment" in result
        # Should NOT have nested structures like result['frequency']['total_words']
        assert "frequency" not in result
        assert "language_detector" not in result

    def test_empty_document(self, empty_doc: TextDocument):
        """Test that all analyzers handle empty documents gracefully."""
        runner = AnalyzerRunner()
        result = runner.analyze(empty_doc)

        # Frequency analyzer empty results
        assert result["total_words"] == 0
        assert result["top_words"] == {}

        # Language detector empty results
        assert result["language"] == "unknown"
        assert result["confidence"] == 0.0

        # Sentiment analyzer empty results
        assert result["sentiment"] == "neutral"
        assert result["score"] == 0.0

        # Readability analyzer empty results
        assert result["avg_sentence_length"] == 0.0
        assert result["avg_word_length"] == 0.0
        assert result["complexity"] == "unknown"

    def test_positive_sentiment_document(self, english_doc: TextDocument):
        """Test runner with a positive sentiment document."""
        runner = AnalyzerRunner()
        result = runner.analyze(english_doc)

        assert result["sentiment"] == "positive"
        assert result["score"] > 0
        assert result["language"] == "en"
        assert result["total_words"] > 0

    def test_negative_sentiment_document(self, negative_sentiment_doc: TextDocument):
        """Test runner with a negative sentiment document."""
        runner = AnalyzerRunner()
        result = runner.analyze(negative_sentiment_doc)

        assert result["sentiment"] == "negative"
        assert result["score"] < 0
        assert result["neg_count"] > 0

    def test_spanish_document(self, spanish_doc: TextDocument):
        """Test runner with a Spanish document."""
        runner = AnalyzerRunner()
        result = runner.analyze(spanish_doc)

        assert result["language"] == "es"
        assert result["sentiment"] == "positive"
        assert result["total_words"] > 0

    def test_consistency_across_analyzers(self, english_doc: TextDocument):
        """Test that analyzers produce consistent results."""
        runner = AnalyzerRunner()
        result = runner.analyze(english_doc)

        # Word count from frequency analyzer should be consistent
        # with the number of tokens used by other analyzers
        assert result["total_words"] > 0

        # Language should be detected consistently
        assert result["language"] in ["en", "es", "fr", "de", "it", "pt", "unknown"]

        # Sentiment should be one of the valid values
        assert result["sentiment"] in ["positive", "negative", "neutral"]

    def test_multiple_runs_same_document(self, english_doc: TextDocument):
        """Test that running the same document multiple times gives consistent results."""
        runner = AnalyzerRunner()
        result1 = runner.analyze(english_doc)
        result2 = runner.analyze(english_doc)

        # Results should be identical
        assert result1["total_words"] == result2["total_words"]
        assert result1["language"] == result2["language"]
        assert result1["sentiment"] == result2["sentiment"]
        assert result1["score"] == result2["score"]
        assert result1["complexity"] == result2["complexity"]

    def test_different_documents(self, english_doc: TextDocument, spanish_doc: TextDocument):
        """Test that different documents produce different results."""
        runner = AnalyzerRunner()
        en_result = runner.analyze(english_doc)
        es_result = runner.analyze(spanish_doc)

        # Languages should be different
        assert en_result["language"] != es_result["language"]

    def test_result_types(self, english_doc: TextDocument):
        """Test that all result values have the correct types."""
        runner = AnalyzerRunner()
        result = runner.analyze(english_doc)

        # Frequency analyzer
        assert isinstance(result["total_words"], int)
        assert isinstance(result["top_words"], dict)
        assert isinstance(result["word_counts"], dict)
        assert isinstance(result["most_common_length"], int)

        # Language detector
        assert isinstance(result["language"], str)
        assert isinstance(result["confidence"], float)

        # Sentiment analyzer
        assert isinstance(result["sentiment"], str)
        assert isinstance(result["score"], float)
        assert isinstance(result["pos_count"], int)
        assert isinstance(result["neg_count"], int)

        # Readability analyzer
        assert isinstance(result["avg_sentence_length"], float)
        assert isinstance(result["avg_word_length"], float)
        assert isinstance(result["complexity"], str)

    def test_analyzers_list_initialized(self):
        """Test that AnalyzerRunner initializes all analyzers."""
        runner = AnalyzerRunner()

        assert len(runner.analyzers) == 4
        # Verify all analyzer types are present
        from text_toolkit.analyzers.core import (
            FrequencyAnalyzer,
            LanguageDetector,
            ReadabilityAnalyzer,
            SentimentAnalyzer,
        )

        analyzer_types = [type(a) for a in runner.analyzers]
        assert FrequencyAnalyzer in analyzer_types
        assert LanguageDetector in analyzer_types
        assert SentimentAnalyzer in analyzer_types
        assert ReadabilityAnalyzer in analyzer_types
