import logging
import re
import unicodedata


class Normalizer:
    """Normalize text: lowercase, strip, remove accents"""

    def normalize_text(self, text: str) -> str:

        logging.info("Starting text normalizing...")

        text = text.strip().lower()

        text = unicodedata.normalize("NFKD", text)
        text = "".join(char for char in text if not unicodedata.combining(char))
        text = re.sub(r"\s+", " ", text)

        logging.info("File normalize completed!")

        return text
