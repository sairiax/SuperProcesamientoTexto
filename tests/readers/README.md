# Readers Package

The `readers` package provides a modular and extensible framework for reading and extracting plain text content from various file formats. It abstracts away the complexities of parsing different document types, offering a simple and consistent interface for text ingestion.

## Architectural Design

### 1. Stream-Based Reading Strategy
Readers operate on a line-by-line basis, yielding text lines as they are processed. This approach ensures:
- **Memory Efficiency**: Large files can be processed without loading the entire content into memory.
- **Simplicity**: The interface returns a standard Python iterator, making it easy to integrate with other text processing tools.
- **Lazy Evaluation**: Content is read and processed only when requested by the caller.

### 2. The Reader Interface (base.py)
Every reader in the system follows the `Reader` protocol. This ensures a consistent API:

def read(self, file_path: Path) -> Iterator[str]:
    """Read a file and yield its content as cleaned text lines."""

The `BaseReader` abstract class provides a foundation for concrete readers, implementing common error handling (e.g., `FileNotFoundError`) and logging, while delegating the format-specific parsing to subclasses.

### 3. Core Implementations
The package contains specialized readers for common text-based formats:

- **`TxtReader`**: The simplest reader. It reads a plain text file line by line, stripping whitespace from the beginning and end of each line and filtering out empty lines. It serves as the base case for plain text ingestion.
- **`MarkdownReader`**: Parses Markdown files. It reads the file line by line and removes common Markdown formatting syntax while preserving the textual content. This includes stripping heading markers (`#`), list markers (`-`, `*`), and bold/italic indicators (`**`, `_`).
- **`HtmlReader`**: Extracts human-readable text from HTML files. It uses a simple tag-stripping approach to remove HTML tags, leaving only the text content. This allows for the extraction of clean text from web pages or HTML documents.

### 4. Error Handling & Logging
All readers share a robust error-handling mechanism:
- **File Not Found**: A `FileNotFoundError` is raised immediately if the input file path does not exist, preventing ambiguous behavior later in the pipeline.
- **Logging**: Each read operation is logged, including the file path and the number of lines yielded. Errors are also logged with appropriate detail, facilitating debugging in larger applications.

## Checklist Fulfillment

This package adheres to the following principles from the project checklist:

- **[x] Separation of Concerns (SRP)**: Each reader handles a single file format. The `BaseReader` manages common infrastructure (error handling, logging), while format-specific logic is isolated in its own subclass.
- **[x] Composition over Inheritance**: Readers are composed with a `Path` object and are designed to be used as components in larger processing pipelines.
- **[x] Open/Closed Principle (OCP)**: The system is easily extensible. Adding support for a new format (e.g., PDF or DOCX) requires creating a new reader class without modifying existing ones.
- **[x] Lazy Loading**: By implementing `read` as a generator, readers process data on demand, which is ideal for working with large files or streaming data.
- **[x] Type Hinting & Quality**: Fully compliant with `pyright` and `ruff`, using advanced type hints like `Iterator` and `Path` for clarity and robustness.
- **[x] Error Handling**: Consistent and predictable error management, starting with an immediate `FileNotFoundError` for missing files.

## Usage Examples

### Reading Different File Formats

from pathlib import Path
from text_toolkit.readers import TxtReader, MarkdownReader, HtmlReader

## Read a simple text file
txt_reader = TxtReader()
txt_path = Path("document.txt")
for line in txt_reader.read(txt_path):
    print(f"Text line: {line}")

## Read and clean a Markdown file
md_reader = MarkdownReader()
md_path = Path("article.md")
print("Markdown content (cleaned):")
for line in md_reader.read(md_path):
    print(line)

## Extract text from an HTML file
html_reader = HtmlReader()
html_path = Path("webpage.html")
print("\nHTML content (tags stripped):")
for line in html_reader.read(html_path):
    print(line)

### Error Handling

from pathlib import Path
from text_toolkit.readers import TxtReader

reader = TxtReader()
try:
    for line in reader.read(Path("nonexistent.txt")):
        print(line)
except FileNotFoundError:
    print("The specified file was not found.")

### Integration with Other Toolkit Components
The readers are designed to be the first step in a text processing pipeline, feeding raw text into transformers or analyzers.

from pathlib import Path
from text_toolkit.readers import TxtReader
from text_toolkit.transformers import TransformerPipeline, Tokenizer

## Read a file and immediately tokenize its content
reader = TxtReader()
pipeline = TransformerPipeline(tokenizer=Tokenizer())

file_path = Path("my_document.txt")
all_tokens = []
for line in reader.read(file_path):
    tokens = pipeline.transform(line)
    all_tokens.extend(tokens)

print(f"Total tokens: {len(all_tokens)}")