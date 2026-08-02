"""Helpers for loading parser regression-test data."""

from pathlib import Path


JOB_TEST_DATA_DIR = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "jobs"
)


def load_job_description(filename: str) -> str:
    """Load a job description from the parser test-data directory."""

    path = JOB_TEST_DATA_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Job test-data file not found: {path}")

    return path.read_text(encoding="utf-8")