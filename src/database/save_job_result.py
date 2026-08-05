"""Result returned when saving an original job."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SaveJobResult:
    """Describe whether a job record was created or already existed."""

    job_id: int
    created: bool
    duplicate_reason: Optional[str] = None