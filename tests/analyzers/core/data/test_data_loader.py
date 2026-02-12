from pathlib import Path
from unittest.mock import patch

import pytest

from text_toolkit.analyzers.core.data import DataLoader, DataLoadError


class TestDataLoader:
    """Test suite for the DataLoader utility."""

    def test_get_data_path(self):
        """Test that get_data_path returns a Path object pointing to the data directory."""
        path = DataLoader.get_data_path("test.json")
        assert isinstance(path, Path)
        assert path.name == "test.json"
        # Directory should be src/text_toolkit/analyzers/core/data/
        assert "text_toolkit/analyzers/core/data" in str(path).replace("\\", "/")

    def test_load_stopwords_real_data(self):
        """Integration test: Verify that real stopwords can be loaded."""
        stopwords = DataLoader.load_stopwords()
        assert isinstance(stopwords, dict)
        assert "en" in stopwords
        assert "es" in stopwords
        assert isinstance(stopwords["en"], set)
        assert len(stopwords["en"]) > 0

    def test_load_sentiment_words_real_data(self):
        """Integration test: Verify that real sentiment words can be loaded."""
        pos, neg = DataLoader.load_sentiment_words()
        assert isinstance(pos, set)
        assert isinstance(neg, set)
        assert len(pos) > 0
        assert len(neg) > 0

    def test_load_readability_thresholds_real_data(self):
        """Integration test: Verify that real readability thresholds can be loaded."""
        thresholds = DataLoader.load_readability_thresholds()
        assert isinstance(thresholds, dict)
        assert "en" in thresholds
        assert "es" in thresholds
        assert "sent_high" in thresholds["en"]
        assert "word_high" in thresholds["en"]

    def test_load_json_missing_file(self):
        """Edge case: Verify that DataLoadError is raised for missing files."""
        # Use a clearly non-existent filename
        with pytest.raises(DataLoadError, match="Required data file missing"):
            DataLoader.load_json("non_existent_file_9999.json")

    def test_load_json_malformed_json(self, tmp_path: Path):
        """Edge case: Verify that DataLoadError is raised for malformed JSON."""
        bad_file = tmp_path / "malformed.json"
        bad_file.write_text("{ this is not json }", encoding="utf-8")

        with (
            patch(
                "text_toolkit.analyzers.core.data.DataLoader.get_data_path",
                return_value=bad_file,
            ),
            pytest.raises(DataLoadError, match="Malformed JSON"),
        ):
            DataLoader.load_json("malformed.json")

    def test_load_json_unexpected_error(self):
        """Edge case: Verify that unexpected errors are wrapped in DataLoadError."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.open", side_effect=RuntimeError("Generic error")),
            pytest.raises(DataLoadError, match="Unexpected error loading"),
        ):
            DataLoader.load_json("any_file.json")

    def test_to_set_generator(self):
        """Test the utility generator for uniqueness."""
        input_list = ["apple", "banana", "apple", "cherry"]
        gen = DataLoader.to_set_generator(input_list)
        # It's a generator
        assert hasattr(gen, "__next__")

        result = set(gen)
        assert result == {"apple", "banana", "cherry"}
        assert len(result) == 3
