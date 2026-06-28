from models.candidate_profile import CandidateProfile
from models.job_opening import JobOpening
from models.fit_analysis import FitAnalysis
from scoring.fit_scorer import score_job
from constants import Recommendation

"""
Usage: python3 -m pytest tests/unit -v
"""

def test_job_skills_list_can_be_empty():
    """
    Tests that a job opening can be created with empty required and preferred skills.
    """
    job = JobOpening(
        source_file="unit_test_job.txt",
        title="SDET III",
        company="Example Company",
        location="Remote",
        remote_status="Flexible",
        employment_type="Full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=[],
        preferred_skills=[],
        responsibilities=[],
        salary_range=None,
        notes=[],
        parser_metadata={},
    )

    profile = CandidateProfile(
        name="Test Candidate",
        target_titles=[
            "SDET",
            "SDET III",
            "Software Development Engineer in Test",
        ],
        core_skills=[
            "Python",
            "pytest",
            "Playwright",
        ],
        preferred_skills=[],
        industries=[],
        remote_preference="remote",
        has_security_clearance=False,
        willing_to_relocate=False,
        notes=[],
    )

    analysis = score_job(job, profile)

    assert analysis.overall_score >= 0
    assert analysis.overall_score <= 100

def test_candidate_profile_defaults_empty():
    """
    Tests that a candidate profile can be created with empty fields.
    """
    profile = CandidateProfile(
        name="Test Candidate",
        remote_preference=None,
        has_security_clearance=False,
        willing_to_relocate=False,
    )
    assert profile.target_titles == []
    assert profile.core_skills == []
    assert profile.preferred_skills == []
    assert profile.industries == []
    assert profile.notes == []

def test_FitAnalysis_defaults_strengths_concerns_notes_to_empty():
    """
    Tests that a FitAnalysis can be created with empty fields.
    """
    analysis = FitAnalysis(
        overall_score=75,
        recommendation=Recommendation.CONSIDER,
    )
    assert analysis.strengths == []
    assert analysis.concerns == []
    assert analysis.notes == []

def test_FitAnalysis_default_lists_are_not_shared():
    first = FitAnalysis(
        overall_score=75,
        recommendation=Recommendation.CONSIDER,
    )
    first.strengths.append("Python")

    second = FitAnalysis(
        overall_score=85,
        recommendation=Recommendation.APPLY,
    )
    assert first.strengths == ["Python"]
    assert second.strengths == []
