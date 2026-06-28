from models.candidate_profile import CandidateProfile
from models.job_opening import JobOpening
from scoring.fit_scorer import score_job
from scoring.fit_scorer import normalize_skill
from scoring.fit_scorer import match_skills
from constants import Recommendation


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

def test_sdet_title_increases_score():
    profile = CandidateProfile(
        name="Test Candidate",
        target_titles=["SDET"],
    )

    non_matching_job = JobOpening(
        source_file="test.txt",
        title="Business Analyst",
        company="Example",
        location=None,
        remote_status=None,
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
    )

    matching_job = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status=None,
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
    )

    non_match_score = score_job(non_matching_job, profile).overall_score
    match_score = score_job(matching_job, profile).overall_score

    assert match_score > non_match_score

def test_clearance_lowers_score():
    profile = CandidateProfile(
        name="Test Candidate",
        target_titles=["SDET"],
        has_security_clearance=False,
    )

    job_with_clearance = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status=None,
        employment_type=None,
        security_clearance_required=True,
        security_clearance_level=None,
    )
    job_without_clearance = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status=None,
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
    )


    non_clr_score = score_job(job_without_clearance, profile).overall_score
    clr_score = score_job(job_with_clearance, profile).overall_score
    print("Clearance job score:", clr_score)
    print("Non-clearance job score:", non_clr_score)

    assert clr_score < non_clr_score


def test_recommendation_valid():
    profile = CandidateProfile(
        name="Test Candidate",
        target_titles=["SDET"],
        has_security_clearance=False,
        remote_preference="remote"
    )

    job_with_remote = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status="Remote",
        employment_type=None,
        security_clearance_required=True,
        security_clearance_level=None,
    )
    job_without_remote = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location="Onsite",
        remote_status=None,
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
    )


    non_rmt_score = score_job(job_without_remote, profile).recommendation
    rmt_score = score_job(job_with_remote, profile).recommendation

    assert rmt_score in Recommendation
    assert non_rmt_score in Recommendation

def test_normalize_skill():
    assert normalize_skill("REST API") == "REST API"
    assert normalize_skill("rest apis") == "REST API"
    assert normalize_skill("API Testing") == "API Testing"
    assert normalize_skill("pytest") == "pytest"
    assert normalize_skill("Playwright") == "Playwright"
    assert normalize_skill("Selenium") == "Selenium"
    assert normalize_skill("Python") == "Python"    

def test_match_skills():
    job_skills = ["REST API", "API Testing", "pytest"]
    candidate_skills = ["REST API", "Playwright", "pytest"]

    matched, missing = match_skills(job_skills, candidate_skills)

    assert matched == ["REST API", "pytest"]
    assert missing == ["API Testing"]

def test_missing_skills():
    job_skills = ["REST API", "API Testing", "pytest"]
    candidate_skills = ["REST API", "Playwright", "pytest"]

    matched, missing = match_skills(job_skills, candidate_skills)

    assert matched == ["REST API", "pytest"]
    assert missing == ["API Testing"]

def test_skill_match_increases_score():
    profile = CandidateProfile(
        name="Test Candidate",
        target_titles=["SDET"],
        core_skills=[
            "REST API",
            "Playwright",
            "pytest",
        ],
        has_security_clearance=False,
        remote_preference="remote",
    )

    weak_job = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status="Remote",
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=["Docker", "Kubernetes"],
        preferred_skills=[],
        responsibilities=[],
        salary_range=None,
        notes=[],
        parser_metadata={},
    )

    strong_job = JobOpening(
        source_file="test.txt",
        title="SDET III",
        company="Example",
        location=None,
        remote_status="Remote",
        employment_type=None,
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=["REST API", "pytest"],
        preferred_skills=[],
        responsibilities=[],
        salary_range=None,
        notes=[],
        parser_metadata={},
    )

    weak_score = score_job(weak_job, profile).overall_score
    strong_score = score_job(strong_job, profile).overall_score

    assert strong_score > weak_score