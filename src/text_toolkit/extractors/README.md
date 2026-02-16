# Extractors Package

The `extractors` package provides a modular and extensible framework for extracting structured data from text documents. It supports extracting emails, URLs, dates, and custom patterns through a unified interface.

## Architectural Design

### 1. Pattern-Based Extraction Strategy
Extractors use regex-based pattern matching to identify and extract specific data from text. This approach ensures:
- **Flexibility**: Multiple patterns can be combined to match different variations of the same data type.
- **Efficiency**: Direct regex compilation with caching for optimal performance.
- **Simplicity**: No external dependencies for core extraction logic, reducing complexity.

### 2. The Extractor Interface (`base.py`)
Every extractor in the system follows the `Extractor` protocol. This ensures a consistent API:
```python
def extract(self, text: str, unique_occurrences: bool = False) -> list[str]:
    """Extract matches from text and return a list of matched strings."""
```

The `RegexExtractor` base class provides the concrete implementation of this protocol, handling:
- Pattern compilation with error handling
- Multi-pattern matching across text
- Duplicate elimination when requested
- Comprehensive logging for debugging

### 3. Core Implementations (`core/`)
The `core` subpackage contains specialized extractors for common data types:

- **`EmailExtractor`**: Extracts email addresses using standard email format patterns. Supports variations like `user@example.com` and `user.name+tag@domain.co.uk`.
- **`URLExtractor`**: Extracts URLs with support for multiple protocols (HTTP/HTTPS, FTP) and formats (with or without protocol prefix).
- **`DateExtractor`**: Extracts dates in various formats including `YYYY-MM-DD`, `DD/MM/YYYY`, and `Day Month Year` patterns.
- **`CustomExtractor`**: Allows users to define extractors with custom regex patterns without creating new classes.

### 4. Orchestration (`extractor_runner.py`)
The `ExtractorRunner` implements the **Composite** pattern. It orchestrates all core extractors in a single pass, providing a unified interface to extract all data types and returning an `ExtractionResult` object containing all matches organized by type.

## Checklist Fulfillment

This package adheres to the following principles from the project checklist:

- **[x] Separation of Concerns (SRP)**: Each extractor handles a specific data type. The `RegexExtractor` base class handles pattern matching logic, while specialized extractors define their own patterns.
- **[x] Composition over Inheritance**: Extractors are composed with regex patterns, and `ExtractorRunner` is composed of multiple individual extractors.
- **[x] Open/Closed Principle (OCP)**: The system is easily extensible. You can add new extractors to the `core` package or the runner without modifying existing logic.
- **[x] Dependency Inversion (DIP)**: High-level modules (like the CLI or Runner) depend on abstractions (the `Extractor` protocol) rather than concrete implementations.
- **[x] Type Hinting & Quality**: Fully compliant with `pyright` and `ruff`, using advanced type hints like `Protocol` and `runtime_checkable`.
- **[x] Logging & Debugging**: All extractors include comprehensive logging for monitoring and troubleshooting.

## Usage Examples

### Using the Orchestrator (Recommended)
```python
from text_toolkit.models.text_document import TextDocument
from text_toolkit.extractors import ExtractorRunner

# Create a document with contact information
doc = TextDocument(
    content="Contact us at support@example.com or visit https://example.com. Meeting on 2026-03-15."
)

# Run all extractors
runner = ExtractorRunner()
result = runner.extract_all(doc, unique_occurrences=True)

print(result.email_matches)   # ['support@example.com']
print(result.url_matches)     # ['https://example.com']
print(result.date_matches)    # ['2026-03-15']
```

### Using Individual Extractors
```python
from text_toolkit.extractors.core import EmailExtractor, URLExtractor

# Extract only emails
email_extractor = EmailExtractor()
text = "Email us at admin@example.com or support@company.org"
emails = email_extractor.extract(text, unique_occurrences=True)
print(emails)  # ['admin@example.com', 'support@company.org']

# Extract only URLs
url_extractor = URLExtractor()
text = "Visit https://example.com or ftp://ftp.example.com/file.txt"
urls = url_extractor.extract(text)
print(urls)  # ['https://example.com', 'ftp://ftp.example.com/file.txt']
```

### Using Custom Extractors
```python
from text_toolkit.extractors.core import CustomExtractor

# Extract phone numbers
phone_extractor = CustomExtractor(
    name="phone",
    patterns=[
        r"\d{3}-\d{3}-\d{4}",           # 555-123-4567
        r"\(\d{3}\)\s*\d{3}-\d{4}",     # (555) 123-4567
    ],
)
text = "Call 555-123-4567 or (555) 987-6543"
phones = phone_extractor.extract(text, unique_occurrences=True)
print(phones)  # ['555-123-4567', '(555) 987-6543']

# Extract IP addresses
ip_extractor = CustomExtractor(
    name="ip_address",
    patterns=[r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"],
)
text = "Server at 192.168.1.1 and 10.0.0.1"
ips = ip_extractor.extract(text)
print(ips)  # ['192.168.1.1', '10.0.0.1']
```

### Adding Custom Patterns to Existing Extractors
```python
from text_toolkit.extractors.core import DateExtractor

# Extend date extractor with additional patterns
date_extractor = DateExtractor()
date_extractor.add_patterns([
    r"\d{1,2}/\d{1,2}/\d{2}",  # MM/DD/YY format
])
text = "Dates: 2026-02-14, 14/02/26"
dates = date_extractor.extract(text)
print(dates)  # ['2026-02-14', '14/02/26']
```
