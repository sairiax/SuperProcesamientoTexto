import logging
import re


class Cleaner:
    """Remove punctuation noise (does not remove emails, URL or numbers)"""

    _email_re = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
    _url_http_re = re.compile(r"\bhttps?://[^\s]+\b")
    _url_www_re = re.compile(r"\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b")
    _punct_re = re.compile(r"[^\w\s]", re.UNICODE)

    def _email_url_protect(self, protected: list[str]):
        def protect(match: re.Match) -> str:
            protected.append(match.group(0))
            return f"__PROT{len(protected)-1}__"
        return protect

    def clean_text(self, text: str) -> str:
        logging.info("Cleaning text")

        url_emails = []
        protect = self._email_url_protect(url_emails)

        text = self._email_re.sub(protect, text)
        text = self._url_http_re.sub(protect, text)
        text = self._url_www_re.sub(protect, text)

        cleaned = self._punct_re.sub(" ", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        for i, value in enumerate(url_emails):
            cleaned = cleaned.replace(f"__PROT{i}__", value)

        return cleaned
