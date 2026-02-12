"""Tests for FrequencyAnalyzer."""

import pytest
from procesamientotexto.analyzers.core import FrequencyAnalyzer
from procesamientotexto.models.text_document import TextDocument


class TestFrequencyAnalyzer:
    """Test suite for FrequencyAnalyzer."""

    def test_normal_document(self, english_doc):
        """Test frequency analysis on a normal English document."""
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(english_doc)

        assert result["total_words"] > 0
        assert "total_words" in result
        assert "top_words" in result
        assert "word_counts" in result
        assert "most_common_length" in result
        assert isinstance(result["top_words"], dict)
        assert isinstance(result["word_counts"], dict)
        assert result["most_common_length"] > 0

    def test_empty_document(self, empty_doc):
        """Test frequency analysis on an empty document."""
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(empty_doc)

        assert result["total_words"] == 0
        assert result["top_words"] == {}
        assert result["word_counts"] == {}
        assert result["most_common_length"] == 0

    def test_repeated_words(self):
        """Test that word frequencies are counted correctly."""
        doc = TextDocument(content="test test test hello hello world")
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(doc)

        assert result["total_words"] == 6
        assert result["word_counts"]["test"] == 3
        assert result["word_counts"]["hello"] == 2
        assert result["word_counts"]["world"] == 1
        # The most frequent word should be "test" with count 3
        assert result["top_words"]["test"] == 3

    def test_top_words_limit(self):
        """Test that top_words returns at most 10 words."""
        # Create a document with more than 10 unique words
        words = [f"word{i}" for i in range(15)]
        doc = TextDocument(content=" ".join(words))
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(doc)

        assert len(result["top_words"]) == 10
        assert result["total_words"] == 15

    def test_single_word_document(self):
        """Test analysis of a document with a single word."""
        doc = TextDocument(content="hello")
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(doc)

        assert result["total_words"] == 1
        assert result["word_counts"]["hello"] == 1
        assert result["most_common_length"] == 5

    def test_most_common_length(self):
        """Test that most common word length is calculated correctly."""
        # Create document where 4-letter words are most common
        doc = TextDocument(content="test word help love test word help")
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(doc)

        # Most words are 4 letters (test, word, help, love)
        assert result["most_common_length"] == 4

    def test_mixed_case_normalization(self):
        """Test that words are normalized to lowercase."""
        doc = TextDocument(content="Hello HELLO hello HeLLo")
        analyzer = FrequencyAnalyzer()
        result = analyzer.analyze(doc)

        # All should be counted as "hello"
        assert result["total_words"] == 4
        assert result["word_counts"]["hello"] == 4
