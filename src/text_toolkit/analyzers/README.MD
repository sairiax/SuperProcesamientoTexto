# Analyzers Package

The `analyzers` package provides a modular and extensible framework for extracting linguistic insights from `TextDocument` objects.

## Package Structure

```text
analyzers/
├── base.py              # Abstract Base Class (Interface)
├── analyzer_runner.py   # Orchestrator (Composite Runner)
├── README.md            # Documentation
└── core/                # Analyzer Implementations
    ├── __init__.py      # Easy access to core components
    ├── frequency_analyzer.py
    ├── language_detector.py
    ├── readability_analyzer.py
    ├── sentiment_analyzer.py
    └── data/            # Externalized linguistic resources
        ├── _data_loader.py
        └── *.json       # Dictionaries and thresholds
```

## Architectural Design

### 1. The Analyzer Interface (`base.py`)
Every analyzer in the system must inherit from the `Analyzer` abstract base class. This ensures a consistent API:
```python
def analyze(self, document: TextDocument) -> dict[str, Any]:
    """Perform analysis and return a dictionary of results."""
```

### 2. Core Implementations (`core/`)
The `core` subpackage contains the specialized analysis logic:
- **`FrequencyAnalyzer`**: Calculates total word count and identifies the most frequent terms.
- **`LanguageDetector`**: Uses a stopword-overlap heuristic to identify the document's language (supporting 'es', 'en', 'fr', 'de', 'it', 'pt').
- **`SentimentAnalyzer`**: Performs keyword-based sentiment analysis, providing a polarity score and counts.
- **`ReadabilityAnalyzer`**: Computes text complexity metrics (average sentence/word length) and categorizes the reading level.

### 3. Orchestration (`analyzer_runner.py`)
The `AnalyzerRunner` implements the **Composite** pattern. It allows you to run all core analyzers in a single pass, consolidating their findings into a flat summary dictionary.

## Why this structure?

- **Separation of Concerns**: Linguistic data is externalized in JSON files, isolated from the algorithmic logic in Python modules.
- **Extensibility**: Adding a new analyzer is as simple as creating a new class that inherits from `Analyzer` and adding it to the `core` package or the `AnalyzerRunner`.
- **Type Safety**: The entire package is fully annotated with Python type hints and compliant with `pyright`.
- **Performance**: Analyzers leverage the lazy-loaded `tokens` property of the `TextDocument` to avoid redundant tokenization.

## Usage Examples

### Using the Orchestrator (Recommended)
```python
from text_toolkit.models.text_document import TextDocument
from text_toolkit.analyzers import AnalyzerRunner

doc = TextDocument(content="I love this toolkit. It is amazing!")
runner = AnalyzerRunner()

result = runner.analyze(doc)
print(result["language"])   # "en"
print(result["sentiment"])  # "positive"
print(result["total_words"]) # 7
```

### Using an Individual Analyzer
```python
from text_toolkit.models.text_document import TextDocument
from text_toolkit.analyzers.core import LanguageDetector

doc = TextDocument(content="Hola, ¿cómo estás?")
detector = LanguageDetector()

result = detector.analyze(doc)
print(f"Detected: {result['language']} (Confidence: {result['confidence']})")
```