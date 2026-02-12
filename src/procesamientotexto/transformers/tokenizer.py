
class Tokenizer:
    """Simple tokenizer that splits text by whitespace"""

    def tokenize_text(self, text:str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("Tokenizer.tokenize_text() requires a string")
        
        return text.split()