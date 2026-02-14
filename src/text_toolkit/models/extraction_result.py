"""Model for extraction results from text analysis."""

from dataclasses import dataclass, field


@dataclass
class ExtractionResult:
    """
    Model for data extracted, merging emails, url and dates ocurrences in the same class
    """

    email_matches: list[str] = field(default_factory=list)
    url_matches: list[str] = field(default_factory=list)
    date_matches: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        """Return a concise representation for logging/debugging."""
        return (
            "ExtractionResult("
            f"emails={len(self.email_matches)}, "
            f"urls={len(self.url_matches)}, "
            f"dates={len(self.date_matches)})"
        )
