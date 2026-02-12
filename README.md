# TextToolkit

A professional suite for advanced linguistic analysis and text processing. Developed for the *Advanced Python for AI Engineering* module.

**Authors**: Sergi, Ainhoa, and Javier

---

## Installation & Usage

### Setup
This project uses `uv` for lightning-fast dependency management.
```bash
uv sync
```

### Execution
Run the toolkit directly from the root using the unified entry point:
```bash
# Basic analysis
uv run main.py sample.txt

# Advanced: Choose analyzers and JSON output
uv run main.py sample.txt -a SentimentAnalyzer -o json -v
```

---

## Architecture & Design Decisions

### Clean Architecture (`src/` layout)
The project follows the standard **src layout** to ensure that tests run against the installed package, preventing accidental imports of local developmental code.

### Core Patterns
- **Strategy Pattern**: Every analyzer (Sentiment, Frequency, etc.) implements a common interface, allowing for interchangeable logic.
- **Composite Pattern**: `AnalyzerRunner` orchestrates multiple analyzers seamlessly, consolidating their results into a single document summary.
- **Lazy Loading**: `TextDocument` tokenizes text only when needed, optimizing performance for large documents.

### Professional Data Validation (Pydantic)
We use **Pydantic `BaseModel`** to strictly enforce schemas on:
1.  **CLI Inputs**: User arguments are validated via `CLIConfig`.
2.  **Linguistic Data**: Readability thresholds from JSON files are parsed into `ReadabilityConfig` objects, ensuring data integrity before processing.

---

## Quality Assurance

### Validation Suite
We maintain a zero-tolerance policy for code smells and type errors:
- **Ruff**: 100% clean (E, F, B, SIM, I, etc.).
- **Pyright**: 100% type-safe in `basic` mode.
- **Pytest**: Over 80% coverage (69 tests) verifying edge cases and error handling.

Run the suite:
```bash
uv run ruff check .
uv run pyright
uv run pytest
```

---

## 📂 Project Structure
```text
src/text_toolkit/
├── analyzers/      # Core linguistic engines
│   ├── core/       # Implementation (Sentiment, Readability, etc.)
│   └── data/       # Linguistic JSON resources
├── models/         # Pydantic & Dataclass models
├── readers/        # IO logic (TXTReader)
└── cli.py          # Rich terminal interface
```