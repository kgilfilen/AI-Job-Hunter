from typing import List, Optional

from src.models.candidate_profile import CandidateProfile
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.resume.resume_recommender import recommend_resume_changes


def make_job(
    required_skills: List[str],
    preferred_skills: Optional[List[str]] = None,
) -> JobOpening:
    return JobOpening(
        source_file="test_job.txt",
        title="Software Development Engineer in Test",
        company="Test Company",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=required_skills,
        preferred_skills=preferred_skills or [],
    )
    
def make_fit_analysis(
    overall_score: int = 80,
) -> FitAnalysis:
    return FitAnalysis(
        overall_score=overall_score,
        recommendation="CONSIDER",
    )


def make_candidate(
    core_skills: List[str],
    preferred_skills: Optional[List[str]] = None,
) -> CandidateProfile:
    return CandidateProfile(
        name="Test Candidate",
        core_skills=core_skills,
        preferred_skills=preferred_skills or [],
    )


def test_recommends_matching_python_skills():
    job = make_job(
        required_skills=["Python", "pytest", "Java"],
    )
    candidate = make_candidate(
        core_skills=["Python", "pytest", "Selenium"],
    )

    result = recommend_resume_changes(
        job,
        make_fit_analysis(),
        candidate,
    )

    assert "Python" in result.skills_to_emphasize
    assert "pytest" in result.skills_to_emphasize
    assert "Java" in result.keywords_missing


def test_recommends_docker_experience():
    job = make_job(
        required_skills=["Docker"],
    )
    candidate = make_candidate(
        core_skills=["Docker", "Python"],
    )

    result = recommend_resume_changes(
        job,
        make_fit_analysis(),
        candidate,
    )

    assert any(
        "containerized testing" in item.lower()
        for item in result.experience_to_highlight
    )


def test_does_not_recommend_unmatched_skill():
    job = make_job(
        required_skills=["Kubernetes"],
    )
    candidate = make_candidate(
        core_skills=["Python", "Selenium"],
    )

    result = recommend_resume_changes(
        job,
        make_fit_analysis(),
        candidate,
    )

    assert "Kubernetes" not in result.skills_to_emphasize
    assert "Kubernetes" in result.keywords_missing


def test_flags_missing_security_clearance():
    job = JobOpening(
        source_file="clearance_job.txt",
        title="Software Test Engineer",
        company="Defense Company",
        location="Denver, CO",
        remote_status="onsite",
        employment_type="full-time",
        security_clearance_required=True,
        security_clearance_level="Secret clearance",
        required_skills=["Python"],
    )
    candidate = make_candidate(
        core_skills=["Python"],
    )

    result = recommend_resume_changes(
        job,
        make_fit_analysis(),
        candidate,
    )

    assert any(
        "secret clearance" in concern.lower()
        for concern in result.possible_concerns
    )
