from enum import Enum

class Recommendation(Enum):
    APPLY = "Apply"
    CONSIDER = "Consider"
    PASS = "Pass"

VALID_RECOMMENDATIONS = (
    Recommendation.APPLY,
    Recommendation.CONSIDER,
    Recommendation.PASS,
)