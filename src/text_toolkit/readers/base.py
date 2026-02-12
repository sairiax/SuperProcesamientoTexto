from pathlib import Path
from typing import Protocol, runtime_checkable

from text_toolkit.models.text_document import TextDocument


@runtime_checkable
class Reader(Protocol):
    """Protocol defining the contract for all document readers."""

    def read(self, path: Path) -> TextDocument:
        """
        Reads a file and returns a TextDocument.
        """
        ...
