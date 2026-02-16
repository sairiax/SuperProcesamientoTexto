from collections.abc import Generator
from pathlib import Path
from typing import Protocol


class Reader(Protocol):
    """Base Protocol for reading documents."""

    def read(self, path: str | Path) -> Generator[str, None, None]:
        """Yield lines from a file

        :param path: path of the file
        :type path: str | Path
        :return: yield lines
        :rtype: Generator[str, None, None]
        """
        raise NotImplementedError
