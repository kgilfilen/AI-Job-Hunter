"""Unit tests for job-opening title parsing."""

import pytest
from pathlib import Path

from src.parsers.job_opening_parser import parse_job_opening, parse_job_opening_file
from src.parsers.job_title_normalizer import normalize_job_title
from tests.helpers.job_test_data import (load_job_description)


SENIOR_SDET_JOB_DESCRIPTION = """
SR SDET Remote, Oregon, United States | Posted:7/31/2026

Job Code

JPC - 207165

Posted Date

2026-07-31 09:00:22

Experience

N/A

Primary Skills

Word SR SDET - Senior Software Development Engineer in Test
Location: Remote, United States | Contract (C2C)

About the Role

Step into a pivotal Senior SDET role where you will shape the quality and
delivery of scalable, enterprise-grade software solutions. As a technical
leader in Quality Engineering and Test Automation, you'll drive best practices,
champion test automation strategies, and collaborate with cross-functional
Agile teams.

Responsibilities

Lead the design and implementation of robust Java-based test automation
frameworks for web, API, backend, and data platforms.

Develop and integrate automated test suites into CI/CD pipelines.

Required Skills and Experience

3+ years in SDET, Test Automation, or Software Quality Assurance roles.

Advanced Java programming with solid understanding of OOP, design patterns,
and automation architecture.

Hands-on experience with Selenium WebDriver.

Proficiency in API testing using REST Assured, Karate, Postman, or similar
tools.
"""

TEST_JOB_DATA="tests/test_data/jobs/"

@pytest.mark.live_ai
def test_parse_job_title_preserves_in_test_suffix() -> None:
    """The parser must not truncate 'Software Development Engineer in Test'."""

    job = parse_job_opening_file(
        Path(TEST_JOB_DATA + "indotronix_sr_sdet.txt")
    )

    assert normalize_job_title(job.title) == (
        "Senior Software Development Engineer in Test"
    )

@pytest.mark.live_ai
def test_parse_company_from_business_unit_and_division() -> None:
    """The parser should recognize labeled business-unit metadata."""

    job = parse_job_opening_file(
        Path(TEST_JOB_DATA + "piper_snr_sdet.txt")
    )

    assert job.company == "Piper Companies"


@pytest.mark.live_ai
@pytest.mark.smoke_test_this
def test_parse_company_from_brand_name_and_domain() -> None:
    """The parser should identify Applied Systems from repeated brand evidence."""

    job = parse_job_opening_file(
        Path(TEST_JOB_DATA + "company_from_brand_and_domain_applied_systems.txt")
        )


    assert job.company == "Applied Systems"

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