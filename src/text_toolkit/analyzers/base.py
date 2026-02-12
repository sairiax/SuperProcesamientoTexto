from typing import Any, Protocol, runtime_checkable

from text_toolkit.models.text_document import TextDocument


@runtime_checkable
class Analyzer(Protocol):
    """Protocol defining the contract for all analyzers."""

    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Analyzes the document and returns the result.
        """
        ...
