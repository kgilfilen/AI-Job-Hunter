"""Application activity-history domain model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ApplicationEvent:
    """Represent one historical event for a tracked application."""

    id: int
    application_id: int

    event_type: str
    occurred_at: str
    notes: Optional[str] = None

    created_at: Optional[str] = None