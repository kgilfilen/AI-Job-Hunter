import json

from pathlib import Path

from src.models.candidate_profile import (
    CandidateProfile,
    Certification,
    Education,
    Experience,
)


def load_candidate_profile(
    profile_path: str,
) -> CandidateProfile:
    """Load a candidate profile and construct nested dataclasses."""
    path = Path(profile_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Candidate profile not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        profile_data = json.load(file)

    experience_data = profile_data.pop(
        "experience",
        [],
    )
    education_data = profile_data.pop(
        "education",
        [],
    )
    certification_data = profile_data.pop(
        "certifications",
        [],
    )

    experiences = [
        Experience(**experience)
        for experience in experience_data
    ]

    education = [
        Education(**education_entry)
        for education_entry in education_data
    ]

    certifications = [
        Certification(**certification)
        for certification in certification_data
    ]

    return CandidateProfile(
        **profile_data,
        experience=experiences,
        education=education,
        certifications=certifications,
    )