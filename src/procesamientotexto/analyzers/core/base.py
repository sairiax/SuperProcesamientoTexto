from abc import ABC, abstractmethod
from typing import Any, Dict
from procesamientotexto.models.text_document import TextDocument

class Analyzer(ABC):
    """Base class for all analyzers."""

    @abstractmethod
    def analyze(self, document: TextDocument) -> Dict[str, Any]:
        """
        Analyzes the document and returns the result.
        The result should also be stored in the document's analysis_results.
        """
        pass
