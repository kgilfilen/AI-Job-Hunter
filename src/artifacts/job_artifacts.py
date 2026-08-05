"""Helpers for organizing job-specific output artifacts."""

from pathlib import Path


DEFAULT_ARTIFACT_ROOT = Path("outputs/jobs")


def get_job_artifact_directory(
    job_id: int,
    artifact_root: Path = DEFAULT_ARTIFACT_ROOT,
) -> Path:
    """Create and return the artifact directory for one stored job."""

    if job_id <= 0:
        raise ValueError("job_id must be greater than zero")

    job_directory = artifact_root / f"{job_id:06d}"
    job_directory.mkdir(parents=True, exist_ok=True)

    return job_directory

def write_original_job_artifact(
    job_id: int,
    job_text: str,
    artifact_root: Path = DEFAULT_ARTIFACT_ROOT,
) -> Path:
    """Write the untouched original job text into its artifact directory."""

    job_directory = get_job_artifact_directory(
        job_id=job_id,
        artifact_root=artifact_root,
    )

    output_path = job_directory / "original_job.txt"

    output_path.write_text(
        job_text,
        encoding="utf-8",
    )

    return output_path