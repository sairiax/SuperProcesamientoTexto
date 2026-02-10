from abc import ABC, abstractmethod
from pathlib import Path
from procesamientotexto.models.text_document import TextDocument

class BaseReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> TextDocument:
        pass