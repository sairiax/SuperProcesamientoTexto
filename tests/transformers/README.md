# Transformers Package

The `transformers` package provides a modular and extensible framework for cleaning, normalizing, and tokenizing text. It forms the preprocessing layer of the text toolkit, converting raw strings into a structured format suitable for analysis.

## Architectural Design

### 1. Single-Responsibility Transformers
Each transformer in the package is responsible for a single, well-defined text manipulation task:
- **Cleaning**: Removes unwanted characters while preserving meaningful patterns.
- **Normalizing**: Standardizes text case and spacing.
- **Tokenizing**: Splits text into atomic units (tokens).

This granularity ensures maximum flexibility, as transformers can be mixed, matched, and reordered without side effects.

### 2. The Transformer Protocol (implied)
While not strictly enforced by an abstract base class in the tests, each transformer follows a consistent pattern, typically exposing a method like `clean_text`, `normalize_text`, or `tokenize_text` that takes a string and returns a transformed result.

### 3. Core Implementations
The package contains three core transformers:

- **`Normalizer`**: Performs basic text normalization. Its primary responsibilities are converting text to lowercase and collapsing multiple whitespace characters into a single space. This ensures that "Hello", "HELLO", and "hello   world" are treated consistently in later stages.
- **`Cleaner`**: Removes punctuation and other unwanted special characters. Crucially, it is designed with **contextual awareness**. It uses regular expressions to identify and preserve important patterns like email addresses, URLs, and dates, ensuring they are not inadvertently broken during the cleaning process.
- **`Tokenizer`**: The simplest of the three. It splits a string into a list of tokens based on whitespace. After cleaning and normalization, this is typically the final step before analysis.

### 4. Orchestration (transformer_pipeline.py)
The `TransformerPipeline` implements the **Pipeline** design pattern. It composes multiple transformers into a single, callable unit. When `transform()` is called, the text is passed through each transformer in sequence. This approach provides:
- **Reusability**: A pipeline can be configured once (e.g., `Cleaner -> Normalizer -> Tokenizer`) and reused across many documents.
- **Maintainability**: The processing logic is centralized, making it easy to understand and modify the entire preprocessing flow.
- **Extensibility**: New transformers can be added to the pipeline without changing the code that uses it.

## Checklist Fulfillment

This package adheres to the following principles from the project checklist:

- **[x] Separation of Concerns (SRP)**: `Cleaner`, `Normalizer`, and `Tokenizer` each have a single, distinct job. The `TransformerPipeline` is solely responsible for orchestrating them.
- **[x] Composition over Inheritance**: The `TransformerPipeline` is composed of transformer instances. It delegates the work to its components rather than inheriting behavior from them.
- **[x] Open/Closed Principle (OCP)**: The system is easily extensible. You can create new transformers (e.g., a `Stemmer` or `Lemmatizer`) and plug them into the existing pipeline without modifying the core classes.
- **[x] Single Source of Truth**: The `TransformerPipeline` centralizes the preprocessing configuration, ensuring that the same steps are applied consistently wherever it is used.
- **[x] Type Hinting & Quality**: Fully compliant with `pyright` and `ruff`, ensuring code quality and readability.

## Usage Examples

### Using Individual Transformers

from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer

cleaner = Cleaner()
normalizer = Normalizer()
tokenizer = Tokenizer()

text = "  Contact us at SUPPORT@EXAMPLE.COM!!! before 15/03/2026?  "

## Clean preserves emails and dates
cleaned = cleaner.clean_text(text)
print(cleaned)  # "  Contact us at SUPPORT@EXAMPLE.COM before 15/03/2026  "

## Normalize lowercases and trims spaces
normalized = normalizer.normalize_text(cleaned)
print(normalized)  # "contact us at support@example.com before 15/03/2026"

## Tokenize splits into words
tokens = tokenizer.tokenize_text(normalized)
print(tokens)  # ['contact', 'us', 'at', 'support@example.com', 'before', '15/03/2026']

### Using the Pipeline (Recommended)

from text_toolkit.transformers import TransformerPipeline, Cleaner, Normalizer, Tokenizer

## Configure the pipeline once
pipeline = TransformerPipeline(
    cleaner=Cleaner(),
    normalizer=Normalizer(),
    tokenizer=Tokenizer()
)

## Reuse it on multiple texts
text1 = "  Hello!!!   WORLD?  "
text2 = "16 Feb 2026: Contact test@example.com."

tokens1 = pipeline.transform(text1)
tokens2 = pipeline.transform(text2)

print(tokens1)  # ['hello', 'world']
print(tokens2)  # ['16', 'feb', '2026', 'contact', 'test@example.com']

### Integration with TextDocument
The pipeline is designed to work seamlessly with the `TextDocument` model, providing lazy-loaded, consistent tokenization.

from text_toolkit.models.text_document import TextDocument
from text_toolkit.transformers import TransformerPipeline, Cleaner, Normalizer, Tokenizer

pipeline = TransformerPipeline(
    cleaner=Cleaner(),
    normalizer=Normalizer(),
    tokenizer=Tokenizer()
)

doc = TextDocument(
    content="  VISIT https://example.com!!!  ",
    pipeline=pipeline
)

## Tokens are generated on-demand using the pipeline
print(doc.tokens)  # ['visit', 'https://example.com']