from dataclasses import dataclass, field
from pathlib import Path

@dataclass(slots=True)  # Genera el __slots__ para optimizar memoria + __init__ automaticamente
class TextDocument:
    """
    Represents a document with its content, associated metadata and analysis results.

    Attributes
    ----------
    content : str
        Raw, unmodified text of the document.
    source_path : Path | None
        Original file path.
    metadata : dict
        Reader- or transformer-provided metadata (format, structure hints, etc.).
        This should not contain analysis results.
    analysis_results : dict
        Results produced by analyzers, keyed by analyzer identifier.

    Example
    -------
    >>> from pathlib import Path
    >>> from textkit.models.text_document import TextDocument
    >>> doc = TextDocument(content="Hello world!", source_path=Path("example.txt"))
    >>> doc.metadata["language"] = "en"
    >>> doc.add_analysis("word_count", 2)
    >>> doc.get_analysis("word_count")
    2
    >>> doc.is_empty()
    False
    >>> doc.has_analysis("word_count")
    True
    """

    content: str
    source_path: Path | None = None
    metadata: dict = field(default_factory=dict)
    analysis_results: dict = field(default_factory=dict)

    def add_analysis(self, key: str, result) -> None:
        self.analysis_results[key] = result

    def get_analysis(self, key: str):
        return self.analysis_results.get(key)

    def has_analysis(self, key: str) -> bool:
        return key in self.analysis_results

    def is_empty(self) -> bool:
        return not self.content.strip()


@dataclass
class ExtractionResult():
    """
    Model for data extracted, merging emails, url and dates ocurrences in the same class
    """

    email_matches: list[str] = field(default_factory=list)
    url_matches: list[str] = field(default_factory=list)
    date_matches: list[str] = field(default_factory=list)

