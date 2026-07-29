import pytest
from typing import List, Optional
from src.models.job_opening import JobOpening
from src.models.fit_analysis import FitAnalysis
from tests.helpers import make_test_job

from src.formatters.resume_formatter import ResumeFormatter
from src.models.candidate_profile import (
    CandidateProfile,
    Experience,
    Education,
    Certification,
)

@pytest.fixture
def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Test Candidate",
        email="test.candidate@example.com",
        phone="123-456-7890",
        location="Denver, CO",
        summary="Experienced software test automation engineer.",
        core_skills=["Python", "pytest", "Selenium", "Docker", "REST API"],
        certifications=[
            Certification(
                name="Example Certified Software Test Engineer",
                issuing_organization="Example Organization",
                issue_date="2020-01-01",
            )
        ],
        experience=[
            Experience(
                title="Senior QA Automation Engineer",
                company="Example Company",
                dates="2021-2026",
                highlights=["Developed automated tests for REST APIs.", 
                "Collaborated with development team to improve test coverage.",
                "Built automated test frameworks using Python and pytest."],
            )
        ],
        education=[
            Education(
                degree="Bachelor of Science in Computer Information Systems",
                institution="Devry University",
                graduation_date="1991-1994",
            )
        ],
    )

@pytest.fixture
def job_opening() -> JobOpening:
    return make_test_job(
        title="Software Development Engineer in Test",
        company="Test Company",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=["Python", "pytest", "Selenium"],
        preferred_skills=["Docker", "REST API"],
    )

@pytest.fixture
def fit_analysis() -> FitAnalysis:
    return FitAnalysis(
        overall_score=85,
        recommendation="CONSIDER",
    )

def test_format_returns_string(candidate_profile, job_opening, fit_analysis):
    formatter = ResumeFormatter()

    result = formatter.format(
        candidate_profile,
        job_opening,
        fit_analysis,
    )

    assert isinstance(result, str)


def test_format_includes_candidate_name(
    candidate_profile,
    job_opening,
    fit_analysis,
):
    formatter = ResumeFormatter()

    result = formatter.format(
        candidate_profile,
        job_opening,
        fit_analysis,
    )

    assert candidate_profile.name in result


def test_format_includes_summary(
    candidate_profile,
    job_opening,
    fit_analysis,
):
    formatter = ResumeFormatter()

    result = formatter.format(
        candidate_profile,
        job_opening,
        fit_analysis,
    )

    assert candidate_profile.summary in result


def test_format_includes_skills(
    candidate_profile,
    job_opening,
    fit_analysis,
):
    formatter = ResumeFormatter()

    result = formatter.format(
        candidate_profile,
        job_opening,
        fit_analysis,
    )

    assert candidate_profile.core_skills[0] in result


def test_format_includes_experience(
    candidate_profile,
    job_opening,
    fit_analysis,
):
    formatter = ResumeFormatter()

    result = formatter.format(
        candidate_profile,
        job_opening,
        fit_analysis,
    )

    experience = candidate_profile.experience[0]

    assert experience.title in result
    assert experience.company in result
    assert experience.highlights[0] in result
