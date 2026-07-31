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


def test_generate_resume_contains_expected_sections():
    """Regression test for end-to-end resume formatting."""

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


    candidate = candidate_profile()

    recommendation = ResumeRecommendation(
        summary_additions=[
            "Relevant strengths for this role include Python and pytest."
        ],
        prioritized_skills=[
            "Python",
            "pytest",
        ],
        prioritized_experience=[],
        highlighted_projects=[],
    )

    markdown = ResumeFormatter().format(
        candidate,
        recommendation,
    )

    assert "# Kenny Gilfilen" in markdown

    assert "## Professional Summary" in markdown
    assert "## Core Skills" in markdown
    assert "## Professional Experience" in markdown
    assert "## Education" in markdown

    assert "Charter Communications" in markdown
    assert "Software Engineer III" in markdown

    assert "DeVry University" in markdown

    assert "Python" in markdown
    assert "pytest" in markdown

    assert (
        "Relevant strengths for this role include Python and pytest."
        in markdown
    )