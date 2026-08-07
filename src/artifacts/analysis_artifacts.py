"""Write generated job-analysis artifacts."""

import json

from dataclasses import asdict
from enum import Enum
from pathlib import Path

from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import (
    ResumeRecommendation,
)


def save_job_opening(
    job_opening: JobOpening,
    job_artifact_directory: Path,
) -> Path:
    """Save a parsed job opening as JSON."""

    output_file = (
        job_artifact_directory / "job.json"
    )

    _write_json(
        output_file=output_file,
        value=job_opening,
    )

    return output_file


def save_fit_analysis(
    fit_analysis: FitAnalysis,
    job_artifact_directory: Path,
) -> Path:
    """Save fit-analysis results as JSON."""

    output_file = (
        job_artifact_directory / "_fit.json"
    )

    _write_json(
        output_file=output_file,
        value=fit_analysis,
    )

    return output_file


def save_resume_recommendation(
    recommendation: ResumeRecommendation,
    job_artifact_directory: Path,
) -> Path:
    """Save resume recommendations as JSON."""

    output_file = (
        job_artifact_directory
        / "_resume_recommendation.json"
    )

    _write_json(
        output_file=output_file,
        value=recommendation,
    )

    return output_file


def save_tailored_resume(
    resume_text: str,
    job_artifact_directory: Path,
) -> Path:
    """Save a tailored resume as Markdown."""

    job_artifact_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        job_artifact_directory
        / "tailored_resume.md"
    )

    output_file.write_text(
        resume_text,
        encoding="utf-8",
    )

    return output_file


def _write_json(
    output_file: Path,
    value: object,
) -> None:
    """Serialize a dataclass as formatted JSON."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_dict = make_json_safe(
        asdict(value)
    )

    output_file.write_text(
        json.dumps(
            safe_dict,
            indent=4,
        ),
        encoding="utf-8",
    )


def make_json_safe(
    value: object,
) -> object:
    """Convert nested values to JSON-safe representations."""

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    return value