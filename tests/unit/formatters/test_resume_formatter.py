"""
Resume formatter.

Converts a candidate profile, job opening, fit analysis, and resume
recommendations into a tailored Markdown resume.
"""

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
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import ResumeRecommendation
from src.resume.resume_recommender import recommend_resume_changes
from tests.helpers.helpers import make_test_job


@pytest.fixture
def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Test Candidate",
        email="test.candidate@example.com",
        phone="123-456-7890",
        linkedin="linkedin.com/in/kennygilfilen",
        github="github.com/kgilfilen",
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


@pytest.fixture
def recommendations(
    candidate_profile: CandidateProfile,
    job_opening: JobOpening,
    fit_analysis: FitAnalysis,
) -> ResumeRecommendation:
    return recommend_resume_changes(
        job=job_opening,
        fit_analysis=fit_analysis,
        candidate=candidate_profile,
    )


def format_resume(
    candidate_profile: CandidateProfile,
    job_opening: JobOpening,
    fit_analysis: FitAnalysis,
    recommendations: ResumeRecommendation,
) -> str:
    """Format the standard test resume."""
    formatter = ResumeFormatter()

    return formatter.format(
        candidate=candidate_profile,
        job=job_opening,
        analysis=fit_analysis,
        recommendations=recommendations,
    )


def test_format_returns_string(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert isinstance(result, str)


def test_format_includes_candidate_name(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert candidate_profile.name in result


def test_format_includes_summary(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert candidate_profile.summary in result


def test_format_includes_target_role(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert job_opening.title in result


def test_format_includes_all_candidate_skills(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    for skill in candidate_profile.core_skills:
        assert f"- {skill}" in result


def test_format_prioritizes_recommended_skills(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    python_position = result.index("- Python")
    pytest_position = result.index("- pytest")
    selenium_position = result.index("- Selenium")
    docker_position = result.index("- Docker")

    assert python_position < docker_position
    assert pytest_position < docker_position
    assert selenium_position < docker_position


def test_format_includes_experience(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    experience = candidate_profile.experience[0]

    assert experience.title in result
    assert experience.company in result

    for highlight in experience.highlights:
        assert highlight in result


def test_format_prioritizes_relevant_experience_highlights(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    collaboration_highlight = (
        "Collaborated with development team to improve test coverage."
    )
    api_highlight = "Developed automated tests for REST APIs."
    python_highlight = (
        "Built automated test frameworks using Python and pytest."
    )

    assert result.index(api_highlight) < result.index(
        collaboration_highlight
    )
    assert result.index(python_highlight) < result.index(
        collaboration_highlight
    )


def test_format_does_not_add_missing_skills(
    candidate_profile,
    fit_analysis,
):
    job = make_test_job(
        title="Software Development Engineer in Test",
        company="Test Company",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=["Python", "Java"],
        preferred_skills=[],
    )

    recommendations = recommend_resume_changes(
        job=job,
        fit_analysis=fit_analysis,
        candidate=candidate_profile,
    )

    result = ResumeFormatter().format(
        candidate=candidate_profile,
        job=job,
        analysis=fit_analysis,
        recommendations=recommendations,
    )

    assert "Java" in recommendations.keywords_missing
    assert "Java" not in result

def test_format_renders_education_fields(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    education = candidate_profile.education[0]

    assert education.degree in result
    assert education.institution in result
    assert education.graduation_date in result
    assert "Education(" not in result


def test_format_renders_certification_fields(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    certification = candidate_profile.certifications[0]

    assert certification.name in result
    assert certification.issuing_organization in result
    assert certification.issue_date in result
    assert "Certification(" not in result


def test_format_includes_experience_location(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    candidate_profile.experience[0].location = "Denver, CO"

    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert "Denver, CO | 2021-2026" in result


def test_format_omits_empty_optional_sections(
    candidate_profile,
    job_opening,
    fit_analysis,
    recommendations,
):
    candidate_profile.education = []
    candidate_profile.certifications = []

    result = format_resume(
        candidate_profile,
        job_opening,
        fit_analysis,
        recommendations,
    )

    assert "## Education" not in result
    assert "## Certifications" not in result

