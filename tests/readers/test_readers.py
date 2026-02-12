from pathlib import Path

import pytest

from text_toolkit.readers import HtmlReader, MarkdownReader, TxtReader


def test_read_txt_correctly(fixtures_dir: Path):
    file_path = fixtures_dir / "txt_sample.txt"

    reader = TxtReader()
    lines = list(reader.read(file_path))

    assert len(lines) > 0
    assert "Hola mundo" in lines[0]

def test_read_mkd_correctly(fixtures_dir: Path):
    file_path = fixtures_dir / "markdown_sample.md"

    reader = MarkdownReader()
    lines = list(reader.read(file_path))

    assert any("Título" in line for line in lines)

def test_read_html_correctly(fixtures_dir: Path):
    file_path = fixtures_dir / "html_sample.html"

    reader = HtmlReader()
    lines = list(reader.read(file_path))

    assert any("Título" in line for line in lines)
    assert any("Hola" in line for line in lines)
    assert any("mundo" in line for line in lines)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
