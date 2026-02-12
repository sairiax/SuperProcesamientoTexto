import logging
from pathlib import Path
from typing import Generator

from .base import Reader


class TxtReader:
    """Reader for plain TXT files"""

    def _open(self, path: Path):
        try:
            return open(path, "r", encoding="utf-8")
        except UnicodeDecodeError:
            return open(path, "r", encoding="latin-1")
    
    def read(self, path: str | Path) -> Generator[str, None, None]:
        path = Path(path)

        if not path.exists():
            raise FileExistsError(f"{path} does not exist")
        
        logging.info("Starting document reading...")

        with self._open(path) as file:
            for line in file:
                yield line.rstrip("\n")

        logging.info("File reading completed!")
