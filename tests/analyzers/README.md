# Analyzers Test Suite

This directory contains the complete test suite for the `analyzers` package. It is designed to ensure the reliability, accuracy, and type-safety of all linguistic analysis components.

## Testing Hierarchy

The testing suite is organized into three levels of granularity:

### 1. Unit Tests (`core/`)
Focuses on individual components in isolation:
- **`test_frequency_analyzer.py`**: Verifies word counting, normalization, and top-word extraction.
- **`test_language_detector.py`**: Validates language identification across 6 supported languages and handles edge cases for unknown scripts.
- **`test_sentiment_analyzer.py`**: Ensures correct polarity scoring and count accuracy for both English and Spanish.
- **`test_readability_analyzer.py`**: Checks complexity calculations and validates language-specific thresholds.
- **`data/test_data_loader.py`**: Tests the robustness of linguistic resource loading, including malformed files and missing resource handling.

### 2. Orchestration Tests (`test_analyzer_runner.py`)
Tests the **Composite** pattern implementation:
- Verifies that `AnalyzerRunner` correctly executes all sub-analyzers.
- Ensures results are consolidated into a consistent, flat dictionary structure.
- Validates consistency across multiple analyzers running on the same document.

### 3. Smoke Tests (`test_analyzers.py`)
Quick verification of the top-level package API, ensuring all components are correctly exported and basic flows work as expected.

## Why are we testing this?

- **Linguistic Logic Accuracy**: Heuristics (like stopword overlap) must be verified against diverse text samples to ensure confidence scores are meaningful.
- **Defensive Data Handling**: Since analyzers depend on external JSON resources, we must ensure the system handles missing or corrupt data gracefully without crashing.
- **Consistency**: We ensure that different analyzers produce coherent results when processing the same `TextDocument` tokens.
- **Regression Prevention**: This suite protects the type-safe foundations and modular structure against future changes.

## Test Coverage Highlights
- **Edge Cases**: Empty documents, single-word texts, and documents with unsupported languages.
- **Multi-language Support**: Specific tests for English and Spanish thresholds and vocabularies.
- **Robustness**: Fakes and mocks are used in `TestDataLoader` to simulate system failures (I/O errors, malformed JSON).

## How to Run

To run the full suite:
```bash
python -m pytest tests/analyzers/ -v
```

To run a specific group:
```bash
python -m pytest tests/analyzers/core/ -v
```
