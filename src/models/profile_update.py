class ProfileService:
    """Load, validate, and persist the candidate profile."""

    def load(self) -> CandidateProfile:
        ...

    def save(
        self,
        profile: CandidateProfile,
    ) -> None:
        ...

    def validate(
        self,
        profile: CandidateProfile,
    ) -> None:
        ...