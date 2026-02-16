"""Execution and document loading functions for CLI."""

from pathlib import Path
from typing import Any

from text_toolkit.analyzers import AnalyzerRunner
from text_toolkit.extractors import ExtractorRunner
from text_toolkit.models import ExtractionResult
from text_toolkit.models.config_models import CLIConfig
from text_toolkit.models.text_document import TextDocument
from text_toolkit.readers import HtmlReader, MarkdownReader, TxtReader
from text_toolkit.transformers import Cleaner, Normalizer, Tokenizer, TransformerPipeline


def _get_reader_for_path(file_path: Path):
    """
    Selects the appropriate reader based on file extension.

    Args:
        file_path: Path to the file.

    Returns:
        Reader instance (MarkdownReader, HtmlReader, or TxtReader).
    """
    file_extension = file_path.suffix.lower()
    if file_extension == ".md":
        return MarkdownReader()
    if file_extension == ".html":
        return HtmlReader()
    return TxtReader()


def _load_document(input_path: str, verbose: bool) -> TextDocument:
    """
    Loads a document from file and creates a TextDocument with pipeline.

    Args:
        input_path: Path to the input file.
        verbose: Whether to log verbose messages.

    Returns:
        TextDocument instance ready for processing.
    """
    from text_toolkit.cli import log_info

    input_file = Path(input_path)
    log_info("Reading document...", verbose)

    reader = _get_reader_for_path(input_file)
    reader_name = reader.__class__.__name__
    log_info(f"Using {reader_name} for {input_file.name}", verbose)

    lines = list(reader.read(input_file))
    content = "\n".join(lines)

    log_info("Initializing processing pipeline...", verbose)
    cleaner = Cleaner()
    normalizer = Normalizer()
    tokenizer = Tokenizer()
    pipeline = TransformerPipeline(tokenizer=tokenizer, cleaner=cleaner, normalizer=normalizer)

    return TextDocument(content=content, source_path=input_file, pipeline=pipeline)


def _determine_what_to_run(config: CLIConfig) -> tuple[bool, bool, bool]:
    """
    Determines what processing should be run based on configuration.

    Args:
        config: CLI configuration object.

    Returns:
        Tuple of (run_analyzers, run_extractors, run_transformers_only) flags.
    """
    no_args = (
        config.extractors is None
        and config.analyzers is None
        and config.transformers is None
    )
    run_analyzers = no_args or config.analyzers is not None
    run_extractors = no_args or config.extractors is not None
    run_transformers_only = (
        config.transformers is not None
        and config.analyzers is None
        and config.extractors is None
    )
    return run_analyzers, run_extractors, run_transformers_only


def _run_transformers_only(
    content: str, transformer_names: list[str] | None, verbose: bool
) -> dict[str, str]:
    """
    Runs transformers in standalone mode and returns all intermediate results.

    Args:
        content: Text content to transform.
        transformer_names: List of transformer names to apply.
        verbose: Whether to log verbose messages.

    Returns:
        Dictionary mapping transformer names to their output.
    """
    from text_toolkit.cli import collect_transformer_results

    return collect_transformer_results(content, transformer_names, verbose)


def _apply_transformers_to_content(
    content: str, transformer_names: list[str] | None, verbose: bool
) -> str:
    """
    Applies transformers to content and returns the final transformed text.

    Args:
        content: Text content to transform.
        transformer_names: List of transformer names to apply.
        verbose: Whether to log verbose messages.

    Returns:
        Final transformed content string.
    """
    from text_toolkit.cli import apply_transformers

    return apply_transformers(content, transformer_names, verbose)


def _run_analyzers(
    document: TextDocument, analyzer_names: list[str] | None, verbose: bool
) -> dict[str, Any]:
    """
    Runs analyzers on the document.

    Args:
        document: TextDocument to analyze.
        analyzer_names: List of analyzer names to run, or None for all.
        verbose: Whether to log verbose messages.

    Returns:
        Dictionary containing analysis results.
    """
    from text_toolkit.cli import log_info

    log_info("Running linguistic analysis...", verbose)
    analyzer_runner = AnalyzerRunner(analyzer_names=analyzer_names)
    return analyzer_runner.analyze(document)


def _run_extractors(
    document: TextDocument, extractor_names: list[str] | None, verbose: bool
) -> ExtractionResult:
    """
    Runs extractors on the document.

    Args:
        document: TextDocument to extract from.
        extractor_names: List of extractor names to run, or None for all.
        verbose: Whether to log verbose messages.

    Returns:
        ExtractionResult containing all extracted data.
    """
    from text_toolkit.cli import log_info

    log_info("Running extractors...", verbose)
    extractor_runner = ExtractorRunner(extractor_names=extractor_names)
    result = extractor_runner.extract_all(document)
    log_info(
        (
            f"Extraction completed: {len(result.email_matches)} emails, "
            f"{len(result.url_matches)} URLs, "
            f"{len(result.date_matches)} dates"
        ),
        verbose,
    )
    return result


def process_document(
    config: CLIConfig,
) -> tuple[dict[str, Any], ExtractionResult | None, dict[str, str] | None]:
    """
    Main processing function that orchestrates document loading and execution.

    Args:
        config: CLI configuration object.

    Returns:
        Tuple of (analyzer_results, extractor_results, transformer_results).
        transformer_results is only populated when transformers run standalone.
    """
    from text_toolkit.cli import log_info

    log_info(f"Starting processing of: {config.input_path}", config.verbose)

    document = _load_document(config.input_path, config.verbose)
    run_analyzers, run_extractors, run_transformers_only = _determine_what_to_run(config)

    analyzers_results: dict[str, Any] = {}
    extractors_results: ExtractionResult | None = None
    transformers_results: dict[str, str] | None = None

    # Apply transformers if specified
    if config.transformers is not None:
        log_info("Applying transformers...", config.verbose)
        if run_transformers_only:
            transformers_results = _run_transformers_only(
                document.content, config.transformers, config.verbose
            )
        else:
            processed_content = _apply_transformers_to_content(
                document.content, config.transformers, config.verbose
            )
            document.content = processed_content

    # Run analysis/extraction if not transformers-only
    if not run_transformers_only:
        if run_analyzers:
            analyzers_results = _run_analyzers(document, config.analyzers, config.verbose)

        if run_extractors:
            extractors_results = _run_extractors(document, config.extractors, config.verbose)

    return analyzers_results, extractors_results, transformers_results
