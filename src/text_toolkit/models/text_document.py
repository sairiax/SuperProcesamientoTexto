from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from text_toolkit.transformers import TransformerPipeline


@dataclass()
class TextDocument:
    """
    Represents a document with its content, associated metadata and analysis results.
    """

    content: str
    pipeline: "TransformerPipeline"
    source_path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    analysis_results: dict[str, Any] = field(default_factory=dict)
    _tokens: list[str] | None = field(default=None, init=False)

    @property
    def tokens(self) -> list[str]:
        """Lazy loads and returns the list of tokens (words) using the pipeline."""
        if self._tokens is None:
            self._tokens = self.pipeline.transform(self.content)
        return self._tokens

    def add_analysis(self, key: str, result: Any) -> None:
        self.analysis_results[key] = result

    def get_analysis(self, key: str) -> Any:
        return self.analysis_results.get(key)

    def has_analysis(self, key: str) -> bool:
        return key in self.analysis_results

    def is_empty(self) -> bool:
        return not self.content.strip()

    def __repr__(self) -> str:
        """Return a concise representation for logging/debugging."""
        content_len = len(self.content)
        metadata_keys = sorted(self.metadata.keys())
        analysis_keys = sorted(self.analysis_results.keys())
        tokens_cached = self._tokens is not None
        return (
            "TextDocument("
            f"content_len={content_len}, "
            f"source_path={self.source_path}, "
            f"metadata_keys={metadata_keys}, "
            f"analysis_keys={analysis_keys}, "
            f"tokens_cached={tokens_cached})"
        )
