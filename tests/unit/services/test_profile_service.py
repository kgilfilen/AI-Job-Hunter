import json

import pytest

from src.models.candidate_profile import CandidateProfile
from src.services.profile_service import ProfileService


def test_profile_service_can_be_created() -> None:
    service = ProfileService()

    assert service is not None

def test_save_and_reload_profile(
    tmp_path,
) -> None:
    profile_path = (
        tmp_path / "candidate_profile.json"
    )

    profile = CandidateProfile(
        # Use the fields required by your model.
    )

    service = ProfileService()

    saved_path = service.save(
        profile=profile,
        profile_path=profile_path,
    )

    reloaded_profile = service.load(
        profile_path
    )

    assert saved_path == profile_path
    assert profile_path.exists()
    assert reloaded_profile == profile

def test_save_creates_backup_of_existing_profile(
    tmp_path,
) -> None:
    profile_path = (
        tmp_path / "candidate_profile.json"
    )

    original_data = {
        # Use a valid profile JSON document.
    }

    profile_path.write_text(
        json.dumps(original_data),
        encoding="utf-8",
    )

    updated_profile = CandidateProfile(
        # Use the fields required by your model.
    )

    service = ProfileService()

    service.save(
        profile=updated_profile,
        profile_path=profile_path,
    )

    history_directory = (
        tmp_path / "profile_history"
    )

    backup_files = list(
        history_directory.glob(
            "candidate_profile_*.json"
        )
    )

    assert len(backup_files) == 1

    backed_up_data = json.loads(
        backup_files[0].read_text(
            encoding="utf-8"
        )
    )

    assert backed_up_data == original_data

def test_validate_rejects_non_profile() -> None:
    service = ProfileService()

    with pytest.raises(
        TypeError,
        match="profile must be a CandidateProfile",
    ):
        service.validate(
            {"name": "Not a profile"}
        )

def test_add_skill_adds_new_skill() -> None:
    service = ProfileService()
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=[],
    )
    updated_profile = service.add_skill(profile, "Python")
    assert "Python" in updated_profile.core_skills

def test_add_skill_does_not_duplicate_existing_skill() -> None:
    service = ProfileService()
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=["Python"],
    )
    updated_profile = service.add_skill(profile, "Python")
    updated_profile = service.add_skill(updated_profile, "Python")
    updated_profile = service.add_skill(updated_profile, "Python")
    assert updated_profile.core_skills == ["Python"]


def test_add_skill_rejects_empty_skill() -> None:
    service = ProfileService()
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=["Python"],
    )
    with pytest.raises(
        ValueError,
        match="Skill cannot be empty"
    ):
        service.add_skill(profile, "")
        
def test_remove_skill_removes_existing_skill() -> None:
    service = ProfileService()
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=["Python"],
    )
    updated_profile = service.remove_skill(profile, "Python")
    assert "Python" not in updated_profile.core_skills

def test_add_skill_strips_whitespace() -> None:
    service = ProfileService()
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=[],
    )

    updated_profile = service.add_skill(
        profile,
        "  Python  ",
    )

    assert updated_profile.core_skills == ["Python"]