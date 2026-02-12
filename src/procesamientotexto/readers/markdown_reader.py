from typing import Generator
from pathlib import Path

from .base import Reader
from .txt_reader import TxtReader


class MarkdownReader:
    """Reader for Markdown files, stripping Markdown syntax"""

    def __init__(self) -> None:
        self._txt_reader = TxtReader()
    
    def read(self, path: str | Path) -> Generator[str, None, None]:
        yield from self._txt_reader.read(path)