import json
from pathlib import Path

from src.models.candidate_profile import CandidateProfile


def load_candidate_profile(profile_path: str) -> CandidateProfile:
    path = Path(profile_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Candidate profile not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        profile_data = json.load(file)

    return CandidateProfile(**profile_data)
