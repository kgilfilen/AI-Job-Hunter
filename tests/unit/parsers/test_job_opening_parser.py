"""Unit tests for job-opening title parsing."""
from pathlib import Path
import json
from unittest.mock import patch, sentinel

from src.parsers.job_opening_parser import parse_job_opening, parse_job_opening_file
from src.parsers.job_title_normalizer import normalize_job_title
from src.models.job_opening import JobOpening
from src.main import _write_json



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


def test_normalize_sr_sdet_to_full_canonical_title() -> None:
    """SR SDET should normalize to the complete canonical title."""

    normalized_title = normalize_job_title("SR SDET")

    assert normalized_title == "Senior Software Development Engineer in Test"

    
def test_parse_job_opening_file_loads_text_and_calls_parser(tmp_path):
    """The file wrapper should load the file and delegate to parse_job_opening()."""

    job_file = tmp_path / "sample_job.txt"
    job_file.write_text(
        "Senior QA Engineer\nPython\nPlaywright\n",
        encoding="utf-8",
    )

    with patch(
        "src.parsers.job_opening_parser.parse_job_opening",
        return_value=sentinel.job,
    ) as mock_parse:

        result = parse_job_opening_file(job_file)

    assert result is sentinel.job

    mock_parse.assert_called_once_with(
        job_text="Senior QA Engineer\nPython\nPlaywright\n",
        source_file="sample_job.txt",
    )

def test_write_json_includes_company(tmp_path) -> None:
    job = JobOpening(
        source_file="applied_systems_sdet.txt",
        title="Software Development Engineer in Test",
        company="Applied Systems",
        location="Remote",
        remote_status="Remote",
        employment_type="Full-time",
        security_clearance_required=False,
        security_clearance_level=None,
    )

    output_file = tmp_path / "job.json"

    _write_json(
        output_file=output_file,
        value=job,
    )

    saved = json.loads(output_file.read_text(encoding="utf-8"))

    assert saved["company"] == "Applied Systems"

'''def test_job_opening_serialization_includes_company() -> None:
    job = JobOpening(
        source_file="applied_systems_sdet.txt",
        title="Software Development Engineer in Test",
        company="Applied Systems",
        location="Remote",
        remote_status="REMOTE",
        employment_type="FULL_TIME",
        security_clearance_required=False,
        security_clearance_level=None,
        # Supply other required constructor fields.
    )

    result = job.to_dict()

    assert result["company"] == "Applied Systems"'''