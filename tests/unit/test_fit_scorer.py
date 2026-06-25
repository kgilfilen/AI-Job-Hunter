from models.candidate_profile import CandidateProfile
from models.job_opening import JobOpening
from scoring.fit_scorer import score_job


def test_fit_score_is_between_0_and_100():
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