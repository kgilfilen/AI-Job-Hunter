from dataclasses import dataclass, field
from typing import List


@dataclass
class FitAnalysis:
    overall_score: int
    recommendation: str

    strengths: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    matched_required_skills: List[str] = field(default_factory=list)
    missing_required_skills: List[str] = field(default_factory=list)
    matched_preferred_skills: List[str] = field(default_factory=list)
    missing_preferred_skills: List[str] = field(default_factory=list)
