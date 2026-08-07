import json
import shutil

from dataclasses import asdict
from datetime import datetime, timezone

from pathlib import Path

from src.models.candidate_profile import CandidateProfile
from src.profile_loader import load_candidate_profile


class ProfileService:
    """Load, validate, and persist the candidate profile."""

    def load(
        self,
        profile_path: Path,
    ) -> CandidateProfile:
        """Load a candidate profile from disk."""

        return load_candidate_profile(
            profile_path
        )

    def save(
        self,
        profile: CandidateProfile,
        profile_path: Path,
    ) -> Path:
        """Validate and safely persist a candidate profile."""

        self.validate(profile)

        profile_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if profile_path.exists():
            self._create_backup(profile_path)

        profile_data = asdict(profile)

        temporary_path = profile_path.with_suffix(
            f"{profile_path.suffix}.tmp"
        )

        temporary_path.write_text(
            json.dumps(
                profile_data,
                indent=4,
            ),
            encoding="utf-8",
        )

        temporary_path.replace(profile_path)

        return profile_path

    def validate(
        self,
        profile: CandidateProfile,
    ) -> None:
        """Validate a candidate profile before saving."""

        if not isinstance(profile, CandidateProfile):
            raise TypeError(
                "profile must be a CandidateProfile"
            )

    def _create_backup(
        self,
        profile_path: Path,
    ) -> Path:
        """Create a timestamped backup of an existing profile."""

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%SZ")

        backup_directory = (
            profile_path.parent
            / "profile_history"
        )

        backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_path = (
            backup_directory
            / (
                f"{profile_path.stem}_"
                f"{timestamp}"
                f"{profile_path.suffix}"
            )
        )

        shutil.copy2(
            profile_path,
            backup_path,
        )

        return backup_path

    def add_skill(
        self,
        profile: CandidateProfile,
        skill: str,
    ) -> CandidateProfile:
        """Return a profile with one verified skill added."""

        normalized_skill = skill.strip()

        if not normalized_skill:
            raise ValueError("Skill cannot be empty")

        if normalized_skill in profile.core_skills:
            return profile

        if normalized_skill not in profile.core_skills:
            profile.core_skills.append(
                normalized_skill
            )

        return profile

    def remove_skill(
        self,
        profile: CandidateProfile,
        skill: str,
    ) -> CandidateProfile:
        """Return a profile with one skill removed."""

        normalized_skill = skill.strip()

        profile.core_skills = [
            existing_skill
            for existing_skill in profile.core_skills
            if existing_skill != normalized_skill
        ]

        return profile