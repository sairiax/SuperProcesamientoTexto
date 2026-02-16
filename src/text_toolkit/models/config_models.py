from pydantic import BaseModel, Field


class ReadabilityThreshold(BaseModel):
    """Thresholds for linguistic complexity in a specific language."""

    sent_high: float = Field(gt=0, description="Upper bound for high sentence complexity")
    sent_med: float = Field(gt=0, description="Upper bound for medium sentence complexity")
    word_high: float = Field(gt=0, description="Upper bound for high word complexity")
    word_med: float = Field(gt=0, description="Upper bound for medium word complexity")


class ReadabilityConfig(BaseModel):
    """Full mapping of readability thresholds by language."""

    es: ReadabilityThreshold
    en: ReadabilityThreshold
    default: ReadabilityThreshold


class CLIConfig(BaseModel):
    """Validation model for CLI arguments."""

    input_path: str
    output: str = Field(pattern="^(text|json)$")
    verbose: bool = False
    analyzers: list[str] | None = None
    extractors: list[str] | None = None
    transformers: list[str] | None = None
