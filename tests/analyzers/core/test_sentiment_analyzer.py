"""Tests for SentimentAnalyzer."""

import pytest

from text_toolkit.analyzers.core import SentimentAnalyzer
from text_toolkit.models.text_document import TextDocument
from text_toolkit.transformers import TransformerPipeline


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer."""

    @pytest.mark.parametrize(
        "text, expected_sentiment",
        [
            ("This is a great day. I love English! It is excellent and amazing.", "positive"),
            (
                "This is a terrible day. I hate this awful situation. It is horrible and bad.",
                "negative",
            ),
            (
                "The document contains several sentences. The data was processed yesterday.",
                "neutral",
            ),
            ("", "neutral"),
            ("Es muy bueno y excelente. Maravilloso!", "positive"),
            ("Es muy malo y terrible. Horrible!", "negative"),
        ],
    )
    def test_sentiment_detection(
        self,
        text: str,
        expected_sentiment: str,
        pipeline: TransformerPipeline
    ) -> None:
        """Test sentiment detection across different languages and intensities."""
        doc = TextDocument(content=text, pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)
        assert result["sentiment"] == expected_sentiment

    def test_empty_document(self, empty_doc: TextDocument):
        """Test sentiment analysis on empty document."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(empty_doc)

        assert result["sentiment"] == "neutral"
        assert result["score"] == 0.0
        assert result["pos_count"] == 0
        assert result["neg_count"] == 0

    def test_mixed_sentiment(self, pipeline: TransformerPipeline) -> None:
        """Test document with both positive and negative words."""
        doc = TextDocument(
            content="This is good but also bad. Great and terrible.", pipeline=pipeline
        )
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["pos_count"] > 0
        assert result["neg_count"] > 0
        # Score should be calculated as (pos - neg) / total
        assert "sentiment" in result
        assert "score" in result

    def test_score_calculation(self, pipeline: TransformerPipeline) -> None:
        """Test that score is correctly calculated."""
        # Document with 3 positive and 1 negative word
        doc = TextDocument(content="good great excellent bad", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        # Score should be (3 - 1) / (3 + 1) = 2/4 = 0.5
        assert result["score"] == 0.5
        assert result["pos_count"] == 3
        assert result["neg_count"] == 1

    def test_sentiment_threshold_positive(self, pipeline: TransformerPipeline) -> None:
        """Test positive sentiment threshold (> 0.1)."""
        # Slightly positive: 2 positive, 1 negative -> (2-1)/(2+1) = 0.33
        doc = TextDocument(content="good great bad", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] > 0.1
        assert result["sentiment"] == "positive"

    def test_sentiment_threshold_negative(self, pipeline: TransformerPipeline) -> None:
        """Test negative sentiment threshold (< -0.1)."""
        # Slightly negative: 1 positive, 2 negative -> (1-2)/(1+2) = -0.33
        doc = TextDocument(content="good bad terrible", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] < -0.1
        assert result["sentiment"] == "negative"

    def test_sentiment_threshold_neutral_edge(self, pipeline: TransformerPipeline) -> None:
        """Test neutral sentiment at edge of threshold."""
        # Exactly balanced: 1 positive, 1 negative -> (1-1)/(1+1) = 0.0
        doc = TextDocument(content="good bad", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["score"] == 0.0
        assert result["sentiment"] == "neutral"

    def test_case_insensitivity(self, pipeline: TransformerPipeline) -> None:
        """Test that sentiment words are matched case-insensitively."""
        doc = TextDocument(content="GOOD Great EXCELLENT", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        # All should be recognized as positive
        assert result["pos_count"] == 3
        assert result["sentiment"] == "positive"

    def test_repeated_sentiment_words(self, pipeline: TransformerPipeline) -> None:
        """Test that repeated sentiment words are counted multiple times."""
        doc = TextDocument(content="good good good bad", pipeline=pipeline)
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(doc)

        assert result["pos_count"] == 3
        assert result["neg_count"] == 1
        assert result["score"] == 0.5  # Score: (3-1)/(3+1) = 0.5

    def test_sentiment_analyzer_repr_includes_word_counts(self) -> None:
        """__repr__ should summarize configured sentiment word lists."""
        analyzer = SentimentAnalyzer()

        representation = repr(analyzer)

        assert "SentimentAnalyzer(" in representation
        assert "pos_words_count=" in representation
        assert "neg_words_count=" in representation
