import logging
import re


class Cleaner:
    """Remove punctuation noise (does not remove emails, URL or numbers)"""

    _punct_re = re.compile(r"[^\w\s@.:/+-]", re.UNICODE)

    def clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Cleaner.clean_text() requires a string")
        
        logging.info("Cleaning text")
        cleaned = self._punct_re.sub("", text)
        return re.sub(r"\s+", " ", cleaned).strip()