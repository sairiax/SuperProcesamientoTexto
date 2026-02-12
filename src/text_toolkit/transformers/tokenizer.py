class Tokenizer:
    """Simple tokenizer that splits text by whitespace"""

    def tokenize_text(self, text:str) -> list[str]:

        return text.split()
