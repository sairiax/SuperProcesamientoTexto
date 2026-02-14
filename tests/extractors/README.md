# Extractors Test Suite

This directory contains the complete test suite for the `extractors` package. It is designed to ensure the reliability, accuracy, and robustness of all extraction components.

## Testing Hierarchy

The testing suite is organized into three levels of granularity:

### 1. Unit Tests (`core/`)
Focuses on individual extractor components in isolation:
- **`test_email_extractor.py`**: Verifies email address extraction across various formats (standard emails, with dots, with plus tags).
- **`test_url_extractor.py`**: Validates URL extraction for multiple protocols (HTTP/HTTPS, FTP, www without protocol) and complex URLs with parameters.
- **`test_date_extractor.py`**: Ensures correct date identification across multiple formats (ISO 8601, DD/MM/YYYY, Month name variants).
- **`test_custom_extractor.py`**: Tests the flexibility of custom extractors with user-defined regex patterns and validates error handling for invalid patterns.
- **`test_extractor_base.py`**: Verifies the core `RegexExtractor` functionality including pattern compilation, caching, and duplicate removal.

### 2. Orchestration Tests (`test_extractor_runner.py`)
Tests the **Composite** pattern implementation:
- Verifies that `ExtractorRunner` correctly initializes all sub-extractors.
- Ensures extraction methods process documents and return results in the expected `ExtractionResult` format.
- Validates the `unique_occurrences` parameter works consistently across all extractors.
- Checks edge cases like empty documents and documents with missing data types.

### 3. Smoke Tests (`test_extractors.py`)
Quick verification of the top-level package API, ensuring all components are correctly exported and basic extraction flows work as expected.

## Why are we testing this?

- **Pattern Accuracy**: Regex patterns must be thoroughly tested against diverse text samples to ensure they correctly match target data without false positives or false negatives.
- **Multi-Format Support**: Since extractors must handle various formats (e.g., different date patterns, URL structures), we need comprehensive test coverage of format variations.
- **Robustness**: Extractors must handle edge cases gracefully: empty text, malformed input, special characters, and texts without any matches.
- **Deduplication Logic**: When `unique_occurrences=True`, the system must correctly eliminate duplicates while preserving order.
- **Consistency**: We ensure that `ExtractorRunner` produces coherent results when running multiple extractors on the same document.
- **Regression Prevention**: This suite protects the modular structure and type-safe implementation against future changes.

## Test Coverage Highlights

- **Edge Cases**: Empty documents, documents with no matches, and documents with only partial matches.
- **Format Variations**: Multiple date formats, URL protocols, and email address formats.
- **Duplicate Handling**: Tests with parametrized `unique_occurrences` flags to verify duplicate removal works correctly.
- **Special Characters**: Emails and URLs with special characters, unicode in text, and escaped patterns.
- **Error Handling**: Invalid regex patterns in custom extractors and malformed input text.
- **Performance**: Tests to ensure pattern matching is efficient and log output is appropriate for debugging.

## How to Run

To run the full test suite:
```bash
python -m pytest tests/extractors/ -v
```

To run a specific group of tests:
```bash
python -m pytest tests/extractors/core/ -v
```
