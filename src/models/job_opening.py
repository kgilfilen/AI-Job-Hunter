from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class JobOpening:
    source_file: str

    title: Optional[str]
    company: Optional[str]
    location: Optional[str]

    remote_status: Optional[str]
    employment_type: Optional[str]

    security_clearance_required: bool
    security_clearance_level: Optional[str]

    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)

    salary_range: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    parser_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)
