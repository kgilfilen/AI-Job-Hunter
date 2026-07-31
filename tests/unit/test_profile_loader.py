import json

import pytest

from src.models.candidate_profile import (
    Education,
    Experience,
)
from src.profile_loader import load_candidate_profile


def build_profile_data() -> dict:
    return {
        "name": "Kenny Gilfilen",
        "email": "kgilfilen01@gmail.com",
        "phone": "720-270-5846",
        "linkedin": "https://www.linkedin.com/in/kennygilfilen",
        "github": "https://github.com/kgilfilen",
        "location": "Highlands Ranch, CO",
        "summary": "Experienced software engineer.",
        "target_titles": [
            "Software Development Engineer in Test",
        ],
        "core_skills": [
            "Python",
            "pytest",
        ],
        "preferred_skills": [],
        "industries": [],
        "certifications": [],
        "experience": [
            {
                "title": "Software Engineer III",
                "company": "Charter Communications",
                "dates": "2021–2025",
                "location": "Centennial, CO",
                "highlights": [
                    "Developed Python automation frameworks.",
                ],
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science",
                "institution": "DeVry University",
                "graduation_date": "1994",
                "field_of_study": (
                    "Computer Information Systems"
                ),
                "location": "Irving, TX",
            }
        ],
        "remote_preference": "remote",
        "has_security_clearance": False,
        "willing_to_relocate": False,
        "notes": [],
    }


def write_profile(tmp_path, profile_data: dict):
    profile_path = tmp_path / "candidate_profile.json"

    profile_path.write_text(
        json.dumps(profile_data),
        encoding="utf-8",
    )

    return profile_path


def test_load_candidate_profile_loads_top_level_fields(
    tmp_path,
):
    profile_path = write_profile(
        tmp_path,
        build_profile_data(),
    )

    profile = load_candidate_profile(
        str(profile_path),
    )

    assert profile.name == "Kenny Gilfilen"
    assert profile.email == "kgilfilen01@gmail.com"
    assert profile.linkedin == (
        "https://www.linkedin.com/in/kennygilfilen"
    )
    assert profile.github == (
        "https://github.com/kgilfilen"
    )


def test_load_candidate_profile_converts_experience_dicts(
    tmp_path,
):
    profile_path = write_profile(
        tmp_path,
        build_profile_data(),
    )

    profile = load_candidate_profile(
        str(profile_path),
    )

    assert len(profile.experience) == 1
    assert isinstance(
        profile.experience[0],
        Experience,
    )
    assert profile.experience[0].title == (
        "Software Engineer III"
    )
    assert profile.experience[0].location == (
        "Centennial, CO"
    )
    assert profile.experience[0].highlights == [
        "Developed Python automation frameworks.",
    ]


def test_load_candidate_profile_converts_education_dicts(
    tmp_path,
):
    profile_path = write_profile(
        tmp_path,
        build_profile_data(),
    )

    profile = load_candidate_profile(
        str(profile_path),
    )

    assert len(profile.education) == 1
    assert isinstance(
        profile.education[0],
        Education,
    )
    assert profile.education[0].institution == (
        "DeVry University"
    )
    assert profile.education[0].field_of_study == (
        "Computer Information Systems"
    )
    assert profile.education[0].location == (
        "Irving, TX"
    )


def test_load_candidate_profile_defaults_nested_lists(
    tmp_path,
):
    profile_data = build_profile_data()
    profile_data.pop("experience")
    profile_data.pop("education")
    profile_data.pop("certifications")

    profile_path = write_profile(
        tmp_path,
        profile_data,
    )

    profile = load_candidate_profile(
        str(profile_path),
    )

    assert profile.experience == []
    assert profile.education == []
    assert profile.certifications == []


def test_load_candidate_profile_raises_for_missing_file(
    tmp_path,
):
    missing_path = (
        tmp_path / "missing_profile.json"
    )

    with pytest.raises(
        FileNotFoundError,
        match="Candidate profile not found",
    ):
        load_candidate_profile(
            str(missing_path),
        )