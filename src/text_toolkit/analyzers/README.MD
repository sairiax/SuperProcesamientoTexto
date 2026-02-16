# Analyzers Package

The `analyzers` package provides a modular and extensible framework for extracting linguistic insights from `TextDocument` objects.

## Architectural Design

### 1. Transformer-Powered Tokenization
Analyzers no longer handle tokenization, cleaning, or normalization internally. Instead, they rely on the `TextDocument.tokens` property, which delegates these tasks to a `TransformerPipeline`. This ensures:
- **Consistency**: The same tokenization logic is used across all analyzers.
- **Efficiency**: Tokenization is lazy-loaded and performed only once per document.
- **Flexibility**: The processing pipeline can be customized (e.g., changing cleaners or normalizers) without modifying the analyzers.

### 2. The Analyzer Interface (`base.py`)
Every analyzer in the system follows the `Analyzer` protocol. This ensures a consistent API:
```python
def analyze(self, document: TextDocument) -> dict[str, Any]:
    """Perform analysis and return a dictionary of results."""
```

### 3. Core Implementations (`core/`)
The `core` subpackage contains the specialized analysis logic:
- **`FrequencyAnalyzer`**: Calculates total word count and identifies the most frequent terms.
- **`LanguageDetector`**: Uses a stopword-overlap heuristic to identify the document's language.
- **`SentimentAnalyzer`**: Performs keyword-based sentiment analysis, providing a polarity score and counts.
- **`ReadabilityAnalyzer`**: Computes text complexity metrics and categorizes the reading level.

### 4. Orchestration (`analyzer_runner.py`)
The `AnalyzerRunner` implements the **Composite** pattern. It allows you to run all core analyzers in a single pass, consolidating their findings into a flat summary dictionary.

## Checklist Fulfillment

This package adheres to the following principles from the project checklist:

- **[x] Separation of Concerns (SRP)**: Logic is strictly divided. Analyzers handle extracted tokens, `TransformerPipeline` handles text transformation, and `TextDocument` maintains the state.
- **[x] Composition over Inheritance**: `TextDocument` is composed with a `TransformerPipeline`, and `AnalyzerRunner` is composed of multiple individual analyzers.
- **[x] Open/Closed Principle (OCP)**: The system is easily extensible. You can add new analyzers to the `core` package or the runner without modifying existing logic.
- **[x] Dependency Inversion (DIP)**: High-level modules (like the CLI or Runner) depend on abstractions (the `Analyzer` protocol) rather than concrete implementations.
- **[x] Lazy Loading**: Using the `@property` decorator in `TextDocument` for tokens optimizes resource usage.
- **[x] Type Hinting & Quality**: Fully compliant with `pyright` and `ruff`, using advanced type hints like `Protocol` and `Generic`.

## Usage Examples

### Using the Orchestrator (Recommended)
```python
from text_toolkit.models.text_document import TextDocument
from text_toolkit.analyzers import AnalyzerRunner
from text_toolkit.transformers import Tokenizer, TransformerPipeline

# Setup pipeline
pipeline = TransformerPipeline(tokenizer=Tokenizer())
doc = TextDocument(content="I love this toolkit. It is amazing!", pipeline=pipeline)

runner = AnalyzerRunner()
result = runner.analyze(doc)

print(result["sentiment"])  # "positive"
print(result["total_words"]) # 7
```

### Using an Individual Analyzer
```python
from text_toolkit.models.text_document import TextDocument
from text_toolkit.analyzers.core import LanguageDetector
from text_toolkit.transformers import Tokenizer, TransformerPipeline

pipeline = TransformerPipeline(tokenizer=Tokenizer())
doc = TextDocument(content="Hola, ¿cómo estás?", pipeline=pipeline)

detector = LanguageDetector()
result = detector.analyze(doc)
print(f"Detected: {result['language']} (Confidence: {result['confidence']})")
```