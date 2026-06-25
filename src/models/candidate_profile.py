from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CandidateProfile:
    name: str

    target_titles: List[str] = field(default_factory=list)
    core_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    industries: List[str] = field(default_factory=list)

    remote_preference: Optional[str] = None
    has_security_clearance: bool = False
    willing_to_relocate: bool = False

    notes: List[str] = field(default_factory=list)
