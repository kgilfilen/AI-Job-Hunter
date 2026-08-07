from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class JobMetadata:
    """Structured job facts discovered before AI parsing."""

    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    date_posted: Optional[str] = None
    valid_through: Optional[str] = None

    salary: Optional[str] = None
    salary_currency: Optional[str] = None
    salary_interval: Optional[str] = None