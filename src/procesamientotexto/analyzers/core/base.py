from abc import ABC, abstractmethod
from typing import Any
from procesamientotexto.models.text_document import TextDocument


class Analyzer(ABC):
    """Base class for all analyzers."""

    @abstractmethod
    def analyze(self, document: TextDocument) -> dict[str, Any]:
        """
        Analyzes the document and returns the result.
        """
        pass
