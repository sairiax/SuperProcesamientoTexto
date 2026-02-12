from typing import Generator
from pathlib import Path
from html.parser import HTMLParser

from .base import Reader
from .txt_reader import TxtReader

class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._texts: list[str] = []
        self._ignore_content = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self._ignore_content = True
    
    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self._ignore_content = False

    def handle_data(self, data: str):
        self._texts.append(data)

    @property
    def get_text(self) -> str:
        return "\n".join(text.strip() for text in self._texts if text.strip())


class HtmlReader:
    def __init__(self) -> None:
        self._txt_reader = TxtReader()
    
    def read(self, path: str | Path) -> Generator[str, None, None]:
        path = Path(path)

        if not path.exists():
            raise FileExistsError(f"{path} does not exist")
        
        raw_html = "\n".join(self._txt_reader.read(path))

        parser = _HTMLTextExtractor()
        parser.feed(raw_html)
        parser.close()

        text = parser.get_text

        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                yield stripped