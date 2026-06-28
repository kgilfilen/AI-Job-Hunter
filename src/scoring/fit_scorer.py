from models.candidate_profile import CandidateProfile
from models.fit_analysis import FitAnalysis
from models.job_opening import JobOpening
from constants import Recommendation


SKILL_NORMALIZATION_MAP = {
    "rest apis": "REST API",
    "rest api": "REST API",
    "restful apis": "REST API",
    "restful api": "REST API",
    "api testing": "API Testing",
    "pytest": "pytest",
    "py test": "pytest",
    "playwright": "Playwright",
    "selenium": "Selenium",
    "python": "Python",
}


def normalize_skill(skill: str) -> str:
    cleaned = skill.strip().lower()
    return SKILL_NORMALIZATION_MAP.get(cleaned, skill.strip())


def match_skills(job_skills, candidate_skills):
    normalized_job_skills = {
        normalize_skill(skill)
        for skill in job_skills
    }

    normalized_candidate_skills = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    matched_skills = sorted(
        normalized_job_skills.intersection(normalized_candidate_skills)
    )

    missing_skills = sorted(
        normalized_job_skills.difference(normalized_candidate_skills)
    )

    return matched_skills, missing_skills


def score_job(job: JobOpening, profile: CandidateProfile) -> FitAnalysis:
    score = 50
    strengths = []
    concerns = []
    notes = []

    title_text = (job.title or "").lower()
    remote_status = (job.remote_status or "").lower()

    for target_title in profile.target_titles:
        if target_title.lower() in title_text:
            score += 15
            strengths.append(f"Target title match: {target_title}")

    if job.security_clearance_required and not profile.has_security_clearance:
        score -= 25
        concerns.append("Security clearance required, but candidate does not currently have one.")

    if profile.remote_preference:
        if profile.remote_preference.lower() in remote_status:
            score += 10
            strengths.append(f"Matches remote preference: {job.remote_status}")
        elif remote_status in ["flexible", "remote or hybrid", "hybrid or remote"]:
            score += 8
            strengths.append(f"Flexible work arrangement: {job.remote_status}")

    matched_required_skills, missing_required_skills = match_skills(
        job.required_skills,
        profile.core_skills,
    )

    if matched_required_skills:
        score += len(matched_required_skills) * 5
        strengths.append(
            f"Matched {len(matched_required_skills)} required skills: "
            + ", ".join(matched_required_skills)
        )

    if missing_required_skills:
        concerns.append(
            f"Missing required skills: "
            + ", ".join(missing_required_skills)
        )

    score = max(0, min(100, score))

    if score >= 80:
        recommendation = Recommendation.APPLY
    elif score >= 60:
        recommendation = Recommendation.CONSIDER
    else:
        recommendation = Recommendation.PASS

    return FitAnalysis(
        overall_score=score,
        recommendation=recommendation,
        strengths=strengths,
        concerns=concerns,
        notes=notes,
        matched_required_skills=matched_required_skills,
        missing_required_skills=missing_required_skills,
        matched_preferred_skills=[],
    )