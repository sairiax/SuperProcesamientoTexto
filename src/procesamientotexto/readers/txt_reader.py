from pathlib import Path
from procesamientotexto.models.text_document import TextDocument
from procesamientotexto.readers.base import BaseReader


class TXTReader(BaseReader):
    """Refined reader for text files."""

    def read(self, path: Path) -> TextDocument:
        """
        Reads a text file and returns a TextDocument.

        Args:
            path (Path): Path to the text file.

        Returns:
            TextDocument: The document with the content read from the file.

        Raises:
            FileNotFoundError: If failure to find the file.
            IOError: If failure to read the file.
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        try:
            content = path.read_text(encoding="utf-8")
            return TextDocument(content=content, source_path=path)
        except Exception as e:
            raise IOError(f"Error reading file {path}: {e}")
