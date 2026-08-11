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

class ApplicationEventType(Enum):
    APPLICATION_SUBMITTED = "Application submitted"
    FOLLOW_UP_SENT = "Follow-up sent"
    RECRUITER_CONTACT = "Recruiter contact"
    INTERVIEW_SCHEDULED = "Interview scheduled"
    INTERVIEW_COMPLETED = "Interview completed"
    THANK_YOU_SENT = "Thank-you sent"
    REJECTED = "Rejected"
    OFFER_RECEIVED = "Offer received"
    OFFER_ACCEPTED = "Offer accepted"
    OFFER_DECLINED = "Offer declined"
    HIRED = "Hired"
    CLOSED = "Application closed"
    WITHDRAWN = "Withdrawn"