import json
from dataclasses import asdict
from pathlib import Path
from parsers.job_opening_parser import parse_job_opening
from models.job_opening import JobOpening


JOBS_DIR = Path("examples/jobs")


def test_job_opening_has_title():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)

    assert isinstance(job_opening, JobOpening)
    assert job_opening.title is not None
    assert len(job_opening.title.strip()) > 0


def test_job_opening_has_core_fields():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)

    assert job_opening.source_file == job_file.name
    assert job_opening.company is not None
    assert job_opening.location is not None
    assert job_opening.remote_status is not None
    assert job_opening.employment_type is not None


def test_job_opening_has_security_clearance_fields():
    job_file = JOBS_DIR / "STE_Sec_Clr.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)

    assert job_opening.security_clearance_required is True
    assert job_opening.security_clearance_level is not None


def test_job_opening_has_parser_metadata():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)

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
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)

    json_text = json.dumps(asdict(job_opening), indent=4)

    assert "title" in json_text
    assert "company" in json_text
    assert "parser_metadata" in json_text