# Extractors Test Suite

This directory contains the complete test suite for the `extractors` package. It is designed to ensure the reliability, accuracy, and robustness of all extraction components.

## Testing Hierarchy

The testing suite is organized into two levels of granularity:

### 1. Unit Tests (`core/`)
Focuses on individual extractor components in isolation:
- **`test_email_extractor.py`**: Verifies email address extraction across various formats (standard emails, with dots, with plus tags, special characters).
- **`test_url_extractor.py`**: Validates URL extraction for multiple protocols (HTTP/HTTPS, FTP, www without protocol) and complex URLs with parameters.
- **`test_date_extractor.py`**: Ensures correct date identification across multiple formats (ISO 8601, DD/MM/YYYY, Month name variants).
- **`test_custom_extractor.py`**: Tests the flexibility of custom extractors with user-defined regex patterns (phone numbers, IP addresses) and validates error handling for invalid patterns.

### 2. Integration Tests (`test_extractor_runner.py`)
Tests the orchestration layer that coordinates multiple extractors:
- Verifies that `ExtractorRunner` correctly initializes with all core extractors or only specific ones.
- Ensures selective initialization works properly (only instantiating requested extractors).
- Validates extraction methods process documents and return results in the expected `ExtractionResult` format.
- Tests the `unique_occurrences` parameter works consistently across all extractors.
- Checks edge cases like empty documents and documents with missing data types.
- Verifies multi-extractor coordination produces coherent results.

## Why are we testing this?

- **Pattern Accuracy**: Regex patterns must be thoroughly tested against diverse text samples to ensure they correctly match target data without false positives or false negatives.
- **Multi-Format Support**: Since extractors must handle various formats (e.g., different date patterns, URL structures), we need comprehensive test coverage of format variations.
- **Robustness**: Extractors must handle edge cases gracefully: empty text, malformed input, special characters, and texts without any matches.
- **Deduplication Logic**: When `unique_occurrences=True`, the system must correctly eliminate duplicates while preserving order.
- **Selective Initialization**: We ensure that `ExtractorRunner` only instantiates the extractors requested by the user, avoiding unnecessary initialization overhead.
- **Consistency**: We ensure that `ExtractorRunner` produces coherent results when running multiple extractors on the same document.
- **Protocol Compliance**: Tests verify that all extractors implement the `Extractor` protocol correctly through duck typing.
- **Regression Prevention**: This suite protects the modular structure and type-safe implementation against future changes.

## Test Coverage Highlights

- **Edge Cases**: Empty documents, documents with no matches, and documents with only partial matches.
- **Format Variations**: Multiple date formats, URL protocols, email address formats, and custom patterns (phone numbers, IP addresses).
- **Duplicate Handling**: Tests with parametrized `unique_occurrences` flags to verify duplicate removal works correctly.
- **Special Characters**: Emails and URLs with special characters, dots, plus signs, hyphens, and underscores.
- **Error Handling**: Invalid regex patterns in custom extractors and malformed input text.
- **Selective Initialization**: Tests verify that only requested extractors are instantiated, not all available extractors.
- **Multi-Extractor Coordination**: Tests ensure that running multiple extractors concurrently produces consistent and accurate results.
- **Protocol Compliance**: Verifies that all extractor implementations satisfy the `Extractor` protocol through duck typing.

## Pytest Techniques Used

This test suite leverages pytest's powerful features to ensure comprehensive, maintainable, and efficient testing:

### Fixtures (`conftest.py`)
Fixtures provide reusable test components and setup logic:
- **`extractor_runner`**: Pre-configured `ExtractorRunner` instance with all core extractors
- **`email_extractor`**, **`url_extractor`**, **`date_extractor`**: Individual extractor instances for isolated testing
- **`custom_phone_extractor`**, **`custom_ip_extractor`**: Pre-configured custom extractors for phone numbers and IP addresses
- **Fixture scoping**: All fixtures use function scope for test isolation

### Parametrized Tests (`@pytest.mark.parametrize`)
Used extensively to test multiple scenarios with minimal code duplication:
- **Format variations**: Testing different date formats, email patterns, URL structures with a single test function
- **Edge cases**: Empty text, no matches, multiple matches, special characters
- **Configuration combinations**: Testing extractors with different `unique_occurrences` flags
- **Test IDs**: Custom IDs (`ids=[...]`) make test output readable and debuggable

Example from `test_email_extractor.py`:
```python
@pytest.mark.parametrize(
    "text, expected_emails",
    [
        ("Contact: admin@example.com", ["admin@example.com"]),
        ("Multiple: a@ex.com, b@ex.com", ["a@ex.com", "b@ex.com"]),
    ],
    ids=["single_email", "multiple_emails"]
)
def test_email_extractor(email_extractor, text, expected_emails):
    ...
```

### Benefits of This Approach
- **DRY Principle**: Fixtures eliminate repetitive setup code
- **Comprehensive Coverage**: Parametrization enables testing many scenarios efficiently
- **Clear Test Reports**: Descriptive IDs make failures easy to identify
- **Maintainability**: Changes to setup logic only require updating fixtures
- **Isolation**: Function-scoped fixtures ensure tests don't interfere with each other

## How to Run

To run the full test suite:
```bash
pytest tests/extractors/ -v
```

To run a specific group of tests:
```bash
pytest tests/extractors/core/ -v
```

To run tests for a specific extractor:
```bash
pytest tests/extractors/core/test_email_extractor.py -v
```

To run a specific parametrized test case:
```bash
pytest tests/extractors/core/test_email_extractor.py::test_email_extractor[single_email] -v
```

To see test coverage:
```bash
pytest tests/extractors/ --cov=text_toolkit.extractors --cov-report=html
```
