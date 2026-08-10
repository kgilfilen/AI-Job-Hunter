from __future__ import annotations

import pytest

from src.formatters.resume_formatter import ResumeFormatter
from src.models.candidate_profile import (
    CandidateProfile,
    Certification,
    Education,
    Experience,
)
from src.models.fit_analysis import FitAnalysis
from src.resume.resume_recommender import recommend_resume_changes
from tests.helpers.helpers import make_test_job


@pytest.fixture
def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Test Candidate",
        email="test.candidate@example.com",
        phone="123-456-7890",
        linkedin="linkedin.com/in/testcandidate",
        github="github.com/testcandidate",
        location="Denver, CO",
        summary="Experienced software test automation engineer.",
        core_skills=[
            "Docker",
            "REST API",
            "Selenium",
            "Python",
            "pytest",
        ],
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
                location="Denver, CO",
                highlights=[
                    "Collaborated with development team to improve test coverage.",
                    "Developed automated tests for REST APIs.",
                    "Built automated test frameworks using Python and pytest.",
                ],
            )
        ],
        education=[
            Education(
                degree="Bachelor of Science in Computer Information Systems",
                institution="Example University",
                graduation_date="1994",
                location="Denver, CO",
            )
        ],
    )


def test_generate_resume_contains_expected_sections(
    candidate_profile: CandidateProfile,
) -> None:
    """Exercise recommendation generation and Markdown resume formatting."""

    job = make_test_job(
        title="Software Development Engineer in Test",
        company="Example Employer",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=[
            "Python",
            "pytest",
            "Selenium",
        ],
        preferred_skills=[
            "Docker",
            "REST API",
        ],
    )

    fit_analysis = FitAnalysis(
        overall_score=85,
        recommendation="Apply",
        matched_required_skills=[
            "Python",
            "pytest",
            "Selenium",
        ],
        matched_preferred_skills=[
            "Docker",
            "REST API",
        ],
    )

    recommendation = recommend_resume_changes(
        job=job,
        fit_analysis=fit_analysis,
        candidate=candidate_profile,
    )

    markdown = ResumeFormatter().format(
        candidate=candidate_profile,
        job=job,
        analysis=fit_analysis,
        recommendations=recommendation,
    )

    assert "# Test Candidate" in markdown
    assert "## Professional Summary" in markdown
    assert "## Core Skills" in markdown
    assert "## Professional Experience" in markdown
    assert "## Education" in markdown
    assert "## Certifications" in markdown

    assert "Software Development Engineer in Test" in markdown
    assert "Senior QA Automation Engineer" in markdown
    assert "Example Company" in markdown
    assert "Example University" in markdown

    assert "Python" in markdown
    assert "pytest" in markdown
    assert "Docker" in markdown


def test_generate_resume_does_not_add_missing_job_skill(
    candidate_profile: CandidateProfile,
) -> None:
    """The integrated recommender/formatter path must not invent skills."""

    job = make_test_job(
        title="Software Development Engineer in Test",
        company="Example Employer",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=[
            "Python",
            "Kubernetes",
        ],
        preferred_skills=[],
    )

    fit_analysis = FitAnalysis(
        overall_score=70,
        recommendation="Consider",
        matched_required_skills=["Python"],
        missing_required_skills=["Kubernetes"],
    )

    recommendation = recommend_resume_changes(
        job=job,
        fit_analysis=fit_analysis,
        candidate=candidate_profile,
    )

    markdown = ResumeFormatter().format(
        candidate=candidate_profile,
        job=job,
        analysis=fit_analysis,
        recommendations=recommendation,
    )

    assert "Kubernetes" in recommendation.keywords_missing
    assert "Kubernetes" not in markdown
