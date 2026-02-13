from .cleaner import Cleaner
from .normalizer import Normalizer
from .tokenizer import Tokenizer


class TransformerPipeline:
    """
    Orchestrates the transformation of raw text into tokens.

    It sequentially applies optional cleaning and normalization before tokenization.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        cleaner: Cleaner | None = None,
        normalizer: Normalizer | None = None,
    ):
        self.tokenizer = tokenizer
        self.cleaner = cleaner
        self.normalizer = normalizer

    def transform(self, text: str) -> list[str]:
        """
        Processes text through the pipeline and returns tokens.

        Args:
            text: Raw input text.

        Returns:
            list[str]: Resulting tokens.
        """
        processed_text = text

        if self.cleaner:
            processed_text = self.cleaner.clean_text(processed_text)

        if self.normalizer:
            processed_text = self.normalizer.normalize_text(processed_text)

        return self.tokenizer.tokenize_text(processed_text)
