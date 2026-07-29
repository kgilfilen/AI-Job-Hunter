from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Experience:
    title: str
    company: str
    dates: Optional[str] = None
    location: Optional[str] = None
    highlights: List[str] = field(default_factory=list)

@dataclass
class Education:
    degree: str
    institution: str
    graduation_date: Optional[str] = None
    field_of_study: Optional[str] = None

@dataclass
class Certification:
    name: str
    issuing_organization: str
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None


@dataclass
class CandidateProfile:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

    target_titles: List[str] = field(default_factory=list)
    core_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    industries: List[str] = field(default_factory=list)

    certifications: List[Certification] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)

    remote_preference: Optional[str] = None
    has_security_clearance: bool = False
    willing_to_relocate: bool = False

    notes: List[str] = field(default_factory=list)

