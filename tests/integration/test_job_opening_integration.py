import json
from dataclasses import asdict
from pathlib import Path
import pytest

from src.parsers.job_opening_parser import parse_job_opening, parse_job_opening_file
from src.models.job_opening import JobOpening

# at present all tests in this file are live API tests, so we mark the whole file as such
pytestmark = pytest.mark.live_ai

TEST_JOB_DATA="tests/test_data/jobs/"

def test_job_opening_has_title():

    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA + "sdet_topstep.txt")
        )

    assert isinstance(job_opening, JobOpening)
    assert job_opening.title is not None
    assert len(job_opening.title.strip()) > 0

@pytest.mark.smoke_test_this
def test_job_opening_has_core_fields():

    job_file = "sdet_topstep.txt"
    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA) / job_file
        )

    assert job_opening.source_file == job_file
    assert job_opening.company is not None
    assert job_opening.location is not None
    assert job_opening.remote_status is not None


def test_job_opening_has_security_clearance_fields():

    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA + "STE_Sec_Clr.txt")
    )

    assert job_opening.security_clearance_required is True
    assert job_opening.security_clearance_level is not None


def test_job_opening_has_parser_metadata():

    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA + "sdet_topstep.txt")
        )

    expected_metadata_keys = [
        "title",
        "company",
        "location",
        "remote_status",
        "employment_type",
        "security_clearance",
    ]

    for key in expected_metadata_keys:
        assert key in job_opening.parser_metadata
        assert "confidence" in job_opening.parser_metadata[key]
        assert "evidence" in job_opening.parser_metadata[key]
        assert "warning" in job_opening.parser_metadata[key]


def test_job_opening_can_serialize_to_json():

    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA + "sdet_topstep.txt")
    )

    json_text = json.dumps(asdict(job_opening), indent=4)

    assert "title" in json_text
    assert "company" in json_text
    assert "parser_metadata" in json_text

@pytest.mark.smoke_test_this
def test_parse_explicit_full_time_employment_type():
    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA) / "dev_II_cpp.txt"
    )

    assert job_opening.employment_type == "full-time"

'''@pytest.mark.smoke_test_this
def test_missing_employment_type_remains_unknown():

    job_file = "sdet_topstep.txt"
    job_opening = parse_job_opening_file(
        Path(TEST_JOB_DATA) / job_file
        )

    assert job_opening.employment_type is None'''
