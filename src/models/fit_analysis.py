from dataclasses import dataclass, field
from typing import List


@dataclass
class FitAnalysis:
    overall_score: int
    recommendation: str

    strengths: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
