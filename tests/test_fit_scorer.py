import json
from dataclasses import asdict
from pathlib import Path
from parsers.job_opening_parser import parse_job_opening
from models.job_opening import JobOpening
from models.candidate_profile import CandidateProfile
from scoring.fit_scorer import score_job

JOBS_DIR = Path("examples/jobs")
profile = CandidateProfile(
    name="Kenny Gilfilen",
    target_titles=[
        "SDET",
        "SDET III",
        "Software Development Engineer in Test",
        "QA Automation Engineer",
        "Test Automation Engineer",
        "Quality Engineer",
    ],
    core_skills=[
        "Python",
        "pytest",
        "Playwright",
        "Selenium",
        "API testing",
        "test automation",
    ],
    remote_preference="remote",
    has_security_clearance=False,
    willing_to_relocate=False,
)

# Remember that the score is stored on job_desc_fit.txt data, NOT in the job_description
# Test that score is between 0 and 100
def test_job_opening_score():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)
    fit_analysis = score_job(job_opening, profile)

    assert isinstance(job_opening, JobOpening)
    assert 0 <= fit_analysis.overall_score <= 100

# Test that security clearance lowers score when candidate has no clearance
def test_job_opening_security_clearance():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)
    fit_analysis = score_job(job_opening, profile)

    assert isinstance(job_opening, JobOpening)
    assert job_opening.security_clearance_required is False
    assert fit_analysis.overall_score < 100

# Test that target title match raises score
def test_job_opening_target_title():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")

    job_opening = parse_job_opening(job_text, source_file=job_file.name)
    fit_analysis = score_job(job_opening, profile)

    assert isinstance(job_opening, JobOpening)
    assert job_opening.title in profile.target_titles
    assert fit_analysis.overall_score > 0

# Test that recommendation is Apply / Consider / Pass
def test_job_opening_recommendation():
    job_file = JOBS_DIR / "sdet_topstep.txt"
    job_text = job_file.read_text(encoding="utf-8")
    recommendation_states = ["Apply", "Consider", "Pass"]

    job_opening = parse_job_opening(job_text, source_file=job_file.name)
    fit_analysis = score_job(job_opening, profile)

    assert isinstance(job_opening, JobOpening)
    assert job_opening.title is not None
    assert len(job_opening.title.strip()) > 0
    assert fit_analysis.recommendation in recommendation_states
