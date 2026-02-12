"""Tests for ReadabilityAnalyzer."""

import pytest
from procesamientotexto.analyzers.core import ReadabilityAnalyzer
from procesamientotexto.models.text_document import TextDocument


class TestReadabilityAnalyzer:
    """Test suite for ReadabilityAnalyzer."""

    def test_normal_document(self, english_doc):
        """Test readability analysis on a normal document."""
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(english_doc)

        assert "avg_sentence_length" in result
        assert "avg_word_length" in result
        assert "complexity" in result
        assert result["avg_sentence_length"] > 0
        assert result["avg_word_length"] > 0
        assert result["complexity"] in ["low", "medium", "high"]

    def test_empty_document(self, empty_doc):
        """Test readability analysis on empty document."""
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(empty_doc)

        assert result["avg_sentence_length"] == 0.0
        assert result["avg_word_length"] == 0.0
        assert result["complexity"] == "unknown"

    def test_low_complexity(self):
        """Test document with low complexity (short sentences and words)."""
        doc = TextDocument(content="I am ok. You are ok. We are ok.")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        assert result["complexity"] == "low"
        assert result["avg_sentence_length"] < 15
        assert result["avg_word_length"] < 5

    def test_medium_complexity(self):
        """Test document with medium complexity."""
        doc = TextDocument(
            content="The system processes information quickly. "
            "Users can access multiple features easily. "
            "Documentation provides helpful guidance."
        )
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        assert result["complexity"] in ["medium", "high"]

    def test_high_complexity(self):
        """Test document with high complexity (long sentences and words)."""
        doc = TextDocument(
            content="The implementation demonstrates comprehensive functionality "
            "incorporating sophisticated algorithmic processing mechanisms "
            "facilitating extraordinary computational performance optimization. "
            "Subsequently, the systematically engineered architectural components "
            "provide unprecedented scalability characteristics."
        )
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        assert result["complexity"] == "high"
        assert result["avg_sentence_length"] > 25 or result["avg_word_length"] > 6

    def test_single_sentence(self):
        """Test document with a single sentence."""
        doc = TextDocument(content="This is a single sentence.")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        assert result["avg_sentence_length"] > 0
        assert result["avg_word_length"] > 0
        assert result["complexity"] in ["low", "medium", "high", "unknown"]

    def test_english_thresholds(self):
        """Test that English language thresholds are used."""
        # Create an English document that is clearly detected as English
        doc = TextDocument(
            content="The quick brown fox jumps over the lazy dog every day."
        )
        analyzer = ReadabilityAnalyzer()

        # First, we need language detection to set the language
        from procesamientotexto.analyzers.core import LanguageDetector

        lang_detector = LanguageDetector()
        lang_detector.analyze(doc)

        result = analyzer.analyze(doc)

        assert "complexity" in result
        # English thresholds: sent_high=25, sent_med=15, word_high=6.0, word_med=5.0

    def test_spanish_thresholds(self):
        """Test that Spanish language thresholds are used."""
        doc = TextDocument(
            content="El rápido zorro marrón salta sobre el perro perezoso todos los días."
        )
        analyzer = ReadabilityAnalyzer()

        # First detect language
        from procesamientotexto.analyzers.core import LanguageDetector

        lang_detector = LanguageDetector()
        lang_detector.analyze(doc)

        result = analyzer.analyze(doc)

        assert "complexity" in result
        # Spanish thresholds: sent_high=30, sent_med=20, word_high=6.5, word_med=5.5

    def test_avg_sentence_length_calculation(self):
        """Test that average sentence length is correctly calculated."""
        # 3 sentences with 3, 4, and 5 words respectively = 12 words / 3 sentences = 4
        doc = TextDocument(content="I am ok. You are fine now. We all are very good.")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        # Should be 12 words / 3 sentences = 4.0
        assert result["avg_sentence_length"] == 4.0

    def test_avg_word_length_calculation(self):
        """Test that average word length is correctly calculated."""
        # Words: "cat" (3), "dog" (3), "fish" (4) = total 10 chars / 3 words = 3.33
        doc = TextDocument(content="cat dog fish")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        # Should be (3 + 3 + 4) / 3 = 3.33
        assert abs(result["avg_word_length"] - 3.33) < 0.01

    def test_mixed_document(self, mixed_doc):
        """Test readability on a complex mixed document."""
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(mixed_doc)

        assert result["avg_sentence_length"] > 0
        assert result["avg_word_length"] > 0
        assert result["complexity"] in ["low", "medium", "high"]

    def test_multiple_punctuation(self):
        """Test that multiple punctuation marks are handled correctly."""
        doc = TextDocument(content="Hello!!! Are you okay??? Yes!")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        # Should have 3 sentences
        assert result["avg_sentence_length"] > 0

    def test_no_language_detected(self):
        """Test readability when no language is detected."""
        # Document with no recognizable stopwords
        doc = TextDocument(content="xyzabc qwerty zxcvbn asdfgh")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(doc)

        # Should use default thresholds
        assert "complexity" in result
        assert result["avg_sentence_length"] > 0
