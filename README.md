# TextToolkit

A professional suite for advanced linguistic analysis and text processing. TextToolkit provides a comprehensive set of tools for analyzing text documents, extracting structured data, and transforming content through a modular, extensible architecture.

Developed for the *Advanced Python for AI Engineering* module.

**Authors**: Sergi, Ainhoa, and Javier

---

## Overview

TextToolkit is a production-ready Python library designed for comprehensive text analysis workflows. It combines linguistic analysis engines, data extraction capabilities, and text transformation pipelines into a unified, type-safe framework. The toolkit supports multiple input formats, provides rich terminal output, and maintains strict code quality standards.

### Key Features

- **Linguistic Analysis**: Sentiment analysis, readability metrics, language detection, and frequency analysis
- **Data Extraction**: Pattern-based extraction of emails, URLs, dates, and custom patterns
- **Text Transformation**: Cleaning, normalization, and tokenization pipelines
- **Multi-format Support**: Automatic reader selection for TXT, Markdown, and HTML files
- **Rich CLI Interface**: Beautiful terminal output with JSON export capabilities
- **Type Safety**: Full type hints with Pyright validation
- **Code Quality**: Zero-tolerance policy enforced by Ruff linting

---

## Installation

### Prerequisites

- Python 3.11 or higher
- `uv` package manager (recommended) or pip

### Setup

This project uses `uv` for lightning-fast dependency management:

```bash
uv sync
```

This will install all required dependencies including Rich for terminal output, Pydantic for data validation, and development tools.

---

## Quick Start

### Basic Usage

Run the toolkit with a text file:

```bash
uv run main.py data_samples/sample.txt
```

This executes all analyzers and extractors by default, displaying results in a formatted table.

### Advanced Usage

#### Selective Analyzer Execution

Run specific analyzers:

```bash
# Single analyzer
uv run main.py sample.txt -a SentimentAnalyzer

# Multiple analyzers
uv run main.py sample.txt -a FrequencyAnalyzer ReadabilityAnalyzer

# JSON output format
uv run main.py sample.txt -a SentimentAnalyzer -o json
```

#### Data Extraction

Extract specific data types:

```bash
# Extract only emails
uv run main.py sample.txt -e EmailExtractor

# Extract multiple types
uv run main.py sample.txt -e EmailExtractor URLExtractor DateExtractor

# Extract all types
uv run main.py sample.txt -e
```

#### Text Transformation

Apply transformers to clean and normalize text:

```bash
# Transformers only (displays transformed output)
uv run main.py sample.txt -t Cleaner

# Multiple transformers
uv run main.py sample.txt -t Cleaner Normalizer Tokenizer

# Transformers with analysis (analysis runs on transformed text)
uv run main.py sample.txt -t Normalizer -a FrequencyAnalyzer
```

#### Verbose Output

Enable detailed logging:

```bash
# Info level logging
uv run main.py sample.txt -v

# Debug level logging
uv run main.py sample.txt -vv
```

---

## Command-Line Interface

### Arguments

- `input_path` (required): Path to the text file to process
- `-o, --output`: Output format (`text` or `json`), default: `text`
- `-v, --verbose`: Increase verbosity (`-v` for info, `-vv` for debug)
- `-a, --analyzers`: Run specific analyzers (FrequencyAnalyzer, LanguageDetector, ReadabilityAnalyzer, SentimentAnalyzer)
- `-e, --extractors`: Run specific extractors (EmailExtractor, URLExtractor, DateExtractor)
- `-t, --transformers`: Apply transformers (Cleaner, Normalizer, Tokenizer)

### Analyzers

- **FrequencyAnalyzer**: Calculates word counts and identifies most frequent terms
- **LanguageDetector**: Detects document language using stopword overlap (supports: en, es, fr, de, it, pt)
- **ReadabilityAnalyzer**: Computes complexity metrics and categorizes reading level
- **SentimentAnalyzer**: Performs keyword-based sentiment analysis with polarity scores

### Extractors

- **EmailExtractor**: Extracts email addresses (supports standard formats and subdomains)
- **URLExtractor**: Extracts URLs (HTTP, HTTPS, FTP, and www-prefixed URLs)
- **DateExtractor**: Extracts dates in multiple formats (ISO, US, European, written formats)

### Transformers

- **Cleaner**: Removes punctuation while preserving emails and URLs
- **Normalizer**: Standardizes text case and spacing
- **Tokenizer**: Splits text into word tokens

### Readers

The toolkit automatically selects the appropriate reader based on file extension:
- `.txt` → TxtReader
- `.md` → MarkdownReader
- `.html` → HtmlReader

---

## Architecture

### Design Principles

TextToolkit follows clean architecture principles with clear separation of concerns:

- **Separation of Concerns**: Each module handles a specific responsibility
- **Composition over Inheritance**: Components are composed rather than inherited
- **Dependency Inversion**: High-level modules depend on abstractions
- **Open/Closed Principle**: Extensible without modifying existing code

### Core Patterns

**Strategy Pattern**: Analyzers and extractors implement common protocols, allowing interchangeable logic without modifying client code.

**Composite Pattern**: `AnalyzerRunner` and `ExtractorRunner` orchestrate multiple components, consolidating results into unified outputs.

**Lazy Loading**: `TextDocument` tokenizes text only when needed via the `tokens` property, optimizing performance for large documents.

**Transformer Pipeline**: Text transformation is handled through a composable pipeline that can be customized without modifying analyzers.

### Data Validation

The project uses **Pydantic** for strict schema validation:

- **CLI Configuration**: User arguments are validated via `CLIConfig` model
- **Linguistic Data**: Readability thresholds and sentiment keywords are loaded from JSON and validated as `ReadabilityConfig` objects
- **Type Safety**: All models include comprehensive type hints

### Project Structure

```
src/text_toolkit/
├── analyzers/          # Linguistic analysis engines
│   ├── core/           # Core implementations
│   │   ├── frequency_analyzer.py
│   │   ├── language_detector.py
│   │   ├── readability_analyzer.py
│   │   └── sentiment_analyzer.py
│   ├── data/           # Linguistic resources (JSON)
│   │   ├── stopwords.json
│   │   ├── sentiment_words.json
│   │   └── readability_thresholds.json
│   ├── base.py         # Analyzer protocol
│   └── analyzer_runner.py
│
├── extractors/         # Data extraction framework
│   ├── core/           # Extractor implementations
│   │   ├── email_extractor.py
│   │   ├── url_extractor.py
│   │   ├── date_extractor.py
│   │   └── custom_extractor.py
│   ├── base.py         # Extractor protocol
│   └── extractor_runner.py
│
├── transformers/       # Text transformation
│   ├── cleaner.py
│   ├── normalizer.py
│   ├── tokenizer.py
│   └── pipeline.py
│
├── readers/           # Input format handlers
│   ├── base.py
│   ├── txt_reader.py
│   ├── markdown_reader.py
│   └── html_reader.py
│
├── models/            # Data models
│   ├── text_document.py
│   ├── extraction_result.py
│   └── config_models.py
│
├── cli.py             # Main CLI entry point
├── cli_display.py      # Output formatting
└── cli_runner.py       # Execution orchestration
```

---

## Quality Assurance

### Code Quality Standards

The project maintains strict quality standards with automated validation:

**Ruff Linting**: Comprehensive linting covering:
- Code style (PEP 8 compliance)
- Complexity metrics (cyclomatic complexity, branch limits)
- Code smells (unused code, print statements, magic values)
- Type safety (imports, naming conventions)

**Pyright Type Checking**: Full type safety validation in `basic` mode, ensuring:
- Complete type coverage
- Correct type usage
- Missing type stub detection

**Test Coverage**: Over 80% coverage with 112 tests across 13 test files, including:
- Unit tests for individual components
- Integration tests for orchestration
- Edge case handling
- Error condition validation

### Running Quality Checks

```bash
# Run linter
uv run ruff check .

# Run type checker
uv run pyright

# Run test suite
uv run pytest

# Run with coverage report
v run pytest --cov=text_toolkit --cov-report=term-missing
```

---

## Examples

### Example 1: Complete Analysis

```bash
uv run main.py data_samples/complex_en.txt -o json -v
```

This performs full analysis including sentiment, readability, language detection, and frequency analysis, outputting results in JSON format with verbose logging.

### Example 2: Email Extraction

```bash
uv run main.py data_samples/complex_en.txt -e EmailExtractor
```

Extracts all email addresses from the document and displays them in a formatted table.

### Example 3: Text Transformation Pipeline

```bash
uv run main.py data_samples/complex_mixed.txt -t Cleaner Normalizer -a FrequencyAnalyzer
```

Applies cleaning and normalization transformations, then performs frequency analysis on the transformed text.

### Example 4: Multi-language Support

```bash
# Spanish text
uv run main.py data_samples/complex_es.txt -a LanguageDetector

# Portuguese text
uv run main.py data_samples/sample_pt.txt -a LanguageDetector

# Chinese text (detected as unknown, but other analyzers work)
uv run main.py data_samples/sample_zh.txt -a LanguageDetector
```

---

## Development

### Project Requirements

- Python 3.11+
- `uv` package manager
- Development dependencies: pytest, ruff, pyright

### Contributing

When contributing to this project:

1. Ensure all code passes `ruff check` with zero errors
2. Maintain type safety with `pyright` validation
3. Add tests for new features
4. Follow the existing architecture patterns
5. Update documentation as needed

### Module Documentation

Each major module includes detailed README files:
- `src/text_toolkit/analyzers/README.MD`
- `src/text_toolkit/extractors/README.md`

---

## License

This project is developed for educational purposes as part of the Advanced Python for AI Engineering module.

---

## Version

Current version: 0.1.0
