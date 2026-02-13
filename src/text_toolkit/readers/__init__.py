from .base import Reader
from .html_reader import HtmlReader
from .markdown_reader import MarkdownReader
from .txt_reader import TxtReader

__all__ = ["HtmlReader", "MarkdownReader", "Reader", "TxtReader"]
