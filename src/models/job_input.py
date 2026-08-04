"""Input data used to process one job."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class JobInput:
    """Represent original and parser-ready job input."""

    source_name: str
    original_text: str
    parser_text: str
    source: str
    source_url: Optional[str] = None