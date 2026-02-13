from pathlib import Path

import pytest

from text_toolkit.readers import HtmlReader, MarkdownReader, TxtReader


def test_read_txt_correctly(tmp_path: Path):
    file_path = tmp_path / "txt_sample.txt"

    lines = ["Hola mundo", "Este es un texto de prueba.", "Línea final."]

    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    reader = TxtReader()
    lines = list(reader.read(file_path))

    assert len(lines) > 0
    assert lines[0] == "Hola mundo"
    assert lines[2] == "Línea final."


def test_txt_file_not_found(tmp_path: Path):
    """Raise FileNotFoundError if input file doesn't exist."""

    file_path = tmp_path / "nonexistent.txt"

    with pytest.raises(FileNotFoundError):
        reader = TxtReader()
        list(reader.read(file_path))


def test_read_mkd_correctly(tmp_path: Path):
    file_path = tmp_path / "markdown_sample.md"

    lines = [
        "# Título Principal",
        "",
        "Este es un **texto** de ejemplo en _Markdown_.",
        "",
        "- Lista 1",
        "- Lista 2",
        "",
        "[Enlace](https://example.com)",
    ]

    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    reader = MarkdownReader()
    lines = list(reader.read(file_path))

    assert any("Título" in line for line in lines)
    assert lines[-1] == "[Enlace](https://example.com)"


def test_mkd_file_not_found(tmp_path: Path):
    """Raise FileNotFoundError if input file doesn't exist."""

    file_path = tmp_path / "nonexistent.md"

    with pytest.raises(FileNotFoundError):
        reader = TxtReader()
        list(reader.read(file_path))


def test_read_html_correctly(tmp_path: Path):
    file_path = tmp_path / "html_sample.html"

    lines = [
        "<html>",
        "  <body>",
        "    <h1>Título HTML</h1>",
        "    <p>Hola <b>mundo</b> desde HTML.</p>",
        "  </body>",
        "</html>",
    ]

    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    reader = HtmlReader()
    lines = list(reader.read(file_path))

    assert lines[0] == "Título HTML"
    assert lines[1] == "Hola"
    assert lines[2] == "mundo"


def test_html_file_not_found(tmp_path: Path):
    """Raise FileNotFoundError if input file doesn't exist."""

    file_path = tmp_path / "nonexistent.html"

    with pytest.raises(FileNotFoundError):
        reader = TxtReader()
        list(reader.read(file_path))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
