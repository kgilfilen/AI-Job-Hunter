"""Data captured while fetching a job-posting web page."""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class FetchedJobPage:
    """Represent the raw information retrieved from a job URL."""

    requested_url: str
    visible_text: str

    page_title: Optional[str] = None
    canonical_url: Optional[str] = None

    metadata: Dict[str, str] = field(
        default_factory=dict
    )