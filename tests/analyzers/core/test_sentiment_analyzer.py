"""Tests for SentimentAnalyzer."""

import pytest
from procesamientotexto.analyzers.core import SentimentAnalyzer
from procesamientotexto.models.text_document import TextDocument


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer."""

    def test_positive_sentiment_english(self, english_doc):
        """Test positive sentiment detection in English."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(english_doc)

        assert result["sentiment"] == "positive"
        assert result["score"] > 0.1
        assert result["pos_count"] > 0
        assert result["neg_count"] == 0

    def test_negative_sentiment(self, negative_sentiment_doc):
        """Test negative sentiment detection."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(negative_sentiment_doc)

        assert result["sentiment"] == "negative"
        assert result["score"] < -0.1
        assert result["pos_count"] == 0
        assert result["neg_count"] > 0

    def test_neutral_sentiment(self, neutral_sentiment_doc):
        """Test neutral sentiment detection."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(neutral_sentiment_doc)

        assert result["sentiment"] == "neutral"
        assert -0.1 <= result["score"] <= 0.1
        assert result["pos_count"] == 0
        assert result["neg_count"] == 0

    def test_empty_document(self, empty_doc):
        """Test sentiment analysis on empty document."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(empty_doc)

        assert result["sentiment"] == "neutral"
        assert result["score"] == 0.0
        assert result["pos_count"] == 0
        assert result["neg_count"] == 0

    def test_mixed_sentiment(self):
        """Test document with both positive and negative words."""
        doc = TextDocument(content="This is good but also bad. Great and terrible.")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["pos_count"] > 0
        assert result["neg_count"] > 0
        # Score should be calculated as (pos - neg) / total
        assert "sentiment" in result
        assert "score" in result

    def test_spanish_positive_words(self):
        """Test that Spanish positive words are recognized."""
        doc = TextDocument(content="Es muy bueno y excelente. Maravilloso!")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["sentiment"] == "positive"
        assert result["pos_count"] >= 3  # bueno, excelente, maravilloso

    def test_spanish_negative_words(self):
        """Test that Spanish negative words are recognized."""
        doc = TextDocument(content="Es muy malo y terrible. Horrible!")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["sentiment"] == "negative"
        assert result["neg_count"] >= 3  # malo, terrible, horrible

    def test_score_calculation(self):
        """Test that score is correctly calculated."""
        # Document with 3 positive and 1 negative word
        doc = TextDocument(content="good great excellent bad")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        # Score should be (3 - 1) / (3 + 1) = 2/4 = 0.5
        assert result["score"] == 0.5
        assert result["pos_count"] == 3
        assert result["neg_count"] == 1

    def test_sentiment_threshold_positive(self):
        """Test positive sentiment threshold (> 0.1)."""
        # Slightly positive: 2 positive, 1 negative -> (2-1)/(2+1) = 0.33
        doc = TextDocument(content="good great bad")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] > 0.1
        assert result["sentiment"] == "positive"

    def test_sentiment_threshold_negative(self):
        """Test negative sentiment threshold (< -0.1)."""
        # Slightly negative: 1 positive, 2 negative -> (1-2)/(1+2) = -0.33
        doc = TextDocument(content="good bad terrible")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] < -0.1
        assert result["sentiment"] == "negative"

    def test_sentiment_threshold_neutral_edge(self):
        """Test neutral sentiment at edge of threshold."""
        # Exactly balanced: 1 positive, 1 negative -> (1-1)/(1+1) = 0.0
        doc = TextDocument(content="good bad")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] == 0.0
        assert result["sentiment"] == "neutral"

    def test_case_insensitivity(self):
        """Test that sentiment words are matched case-insensitively."""
        doc = TextDocument(content="GOOD Great EXCELLENT")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        # All should be recognized as positive
        assert result["pos_count"] == 3
        assert result["sentiment"] == "positive"

    def test_repeated_sentiment_words(self):
        """Test that repeated sentiment words are counted multiple times."""
        doc = TextDocument(content="good good good bad")
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["pos_count"] == 3
        assert result["neg_count"] == 1
        # Score: (3-1)/(3+1) = 0.5
        assert result["score"] == 0.5
