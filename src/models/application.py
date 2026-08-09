"""Application-tracking domain model."""

from dataclasses import dataclass
from typing import Optional

from src.models.application_status import ApplicationStatus


@dataclass
class Application:
    """Track candidate activity associated with one stored job."""

    id: int
    job_id: int

    status: ApplicationStatus

    applied_at: Optional[str] = None
    next_action: Optional[str] = None
    follow_up_at: Optional[str] = None
    notes: Optional[str] = None

    created_at: Optional[str] = None
    updated_at: Optional[str] = None