"""Unit tests for deterministic employment-type normalization."""

from src.parsers.employment_type_normalizer import (
    detect_employment_type,
    normalize_employment_type,
)


def test_normalize_full_time_with_space() -> None:
    assert normalize_employment_type("Full time") == "full-time"


def test_normalize_fulltime_without_space() -> None:
    assert normalize_employment_type("Fulltime") == "full-time"


def test_normalize_full_time_with_hyphen() -> None:
    assert normalize_employment_type("Full-time") == "full-time"


def test_detect_full_time_from_job_description() -> None:
    job_text = """
    Software Development Engineer in Test

    Employment Type: Full time

    The successful candidate will develop automated tests.
    """

    assert detect_employment_type(job_text) == "full-time"
