import logging
import re


class Cleaner:
    """Remove punctuation noise (does not remove emails, URL or numbers)"""

    _email_re = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

    _url_http_re = re.compile(r"\bhttps?://[^\s]+\b")
    _url_www_re = re.compile(r"\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b")

    _percent_re = re.compile(r"\b\d+(?:[.,]\d+)?%\b")

    _date_ymd_sep_re = re.compile(r"\b\d{4}[-/.]\d{2}[-/.]\d{2}\b")
    _date_dmy_slash_re = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
    _months = (
        r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
    )
    _date_month_name_long_re = re.compile(
        rf"\b(?:{_months})\s+\d{{1,2}}(?:st|nd|rd|th)?\,?\s+\d{{4}}\b",
        re.IGNORECASE,
    )
    _date_month_name_short_re = re.compile(
        rf"\b\d{{1,2}}\s+(?:{_months})\s+\d{{4}}\b",
        re.IGNORECASE,
    )

    _punct_re = re.compile(r"[^\w\s]", re.UNICODE)

    def _protect(self, protected: list[str]):
        def protect(match: re.Match) -> str:
            protected.append(match.group(0))
            return f"__PROT{len(protected) - 1}__"

        return protect

    def clean_text(self, text: str) -> str:
        logging.info("Cleaning text")

        url_emails_dates = []
        protect = self._protect(url_emails_dates)

        text = self._email_re.sub(protect, text)
        text = self._url_http_re.sub(protect, text)
        text = self._url_www_re.sub(protect, text)
        text = self._percent_re.sub(protect, text)
        text = self._date_ymd_sep_re.sub(protect, text)
        text = self._date_dmy_slash_re.sub(protect, text)
        text = self._date_month_name_long_re.sub(protect, text)
        text = self._date_month_name_short_re.sub(protect, text)

        cleaned = self._punct_re.sub(" ", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        for i, value in enumerate(url_emails_dates):
            cleaned = cleaned.replace(f"__PROT{i}__", value)

        return cleaned
