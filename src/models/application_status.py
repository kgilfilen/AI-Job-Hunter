"""Application-status values used by career-management workflows."""

from enum import Enum


class ApplicationStatus(str, Enum):
    """Lifecycle state for an application or tracked opportunity."""

    INTERESTED = "INTERESTED"
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    CLOSED = "CLOSED"