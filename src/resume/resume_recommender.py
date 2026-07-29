"""Generate resume-tailoring recommendations for a job opening."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

# Adjust these imports if your model files use different paths.
from src.models.candidate_profile import CandidateProfile
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening


@dataclass
class ResumeRecommendations:
    """Recommended changes for tailoring a resume to a job opening."""

    summary_changes: list[str] = field(default_factory=list)
    skills_to_emphasize: list[str] = field(default_factory=list)
    experience_to_highlight: list[str] = field(default_factory=list)
    keywords_to_add: list[str] = field(default_factory=list)
    keywords_missing: list[str] = field(default_factory=list)
    possible_concerns: list[str] = field(default_factory=list)

    @property
    def has_recommendations(self) -> bool:
        """Return True when at least one recommendation was generated."""
        return any(
            (
                self.summary_changes,
                self.skills_to_emphasize,
                self.experience_to_highlight,
                self.keywords_to_add,
                self.keywords_missing,
                self.possible_concerns,
            )
        )


def recommend_resume_changes(
    job: JobOpening,
    fit_analysis: FitAnalysis,
    candidate: CandidateProfile,
) -> ResumeRecommendations:
    """Create resume recommendations from a job and candidate profile.

    The recommender does not invent experience. It only recommends emphasizing
    skills that appear in both the job requirements and candidate profile, and
    identifies job requirements that are not represented in the profile.
    """
    required_skills = _normalize_collection(
        getattr(job, "required_skills", [])
    )
    preferred_skills = _normalize_collection(
        getattr(job, "preferred_skills", [])
    )
    candidate_skills = _candidate_skills(candidate)

    matched_required = _find_matches(required_skills, candidate_skills)
    matched_preferred = _find_matches(preferred_skills, candidate_skills)

    missing_required = _find_missing(required_skills, candidate_skills)
    missing_preferred = _find_missing(preferred_skills, candidate_skills)

    recommendations = ResumeRecommendations()

    recommendations.skills_to_emphasize = _unique_preserving_order(
        matched_required + matched_preferred
    )

    recommendations.keywords_to_add = list(
        recommendations.skills_to_emphasize
    )

    recommendations.keywords_missing = _unique_preserving_order(
        missing_required + missing_preferred
    )

    recommendations.summary_changes = _build_summary_changes(
        job=job,
        matched_skills=recommendations.skills_to_emphasize,
    )

    recommendations.experience_to_highlight = (
        _build_experience_recommendations(
            recommendations.skills_to_emphasize
        )
    )

    recommendations.possible_concerns = _build_concerns(
        job=job,
        fit_analysis=fit_analysis,
        candidate=candidate,
        missing_required=missing_required,
    )

    return recommendations


def _candidate_skills(candidate: CandidateProfile) -> list[str]:
    """Collect all skills represented in the candidate profile."""
    return _unique_preserving_order(
        _normalize_collection(candidate.core_skills)
        + _normalize_collection(candidate.preferred_skills)
    )

def _normalize_collection(values: object) -> list[str]:
    """Convert a string or iterable of values into cleaned strings."""
    if values is None:
        return []

    if isinstance(values, str):
        values = [values]

    if not isinstance(values, Iterable):
        return []

    normalized: list[str] = []

    for value in values:
        text = str(value).strip()
        if text:
            normalized.append(text)

    return normalized


def _find_matches(
    job_skills: list[str],
    candidate_skills: list[str],
) -> list[str]:
    """Return job skills represented in the candidate profile."""
    candidate_normalized = {
        _normalize_skill(skill) for skill in candidate_skills
    }

    return [
        skill
        for skill in job_skills
        if _normalize_skill(skill) in candidate_normalized
    ]


def _find_missing(
    job_skills: list[str],
    candidate_skills: list[str],
) -> list[str]:
    """Return job skills not represented in the candidate profile."""
    candidate_normalized = {
        _normalize_skill(skill) for skill in candidate_skills
    }

    return [
        skill
        for skill in job_skills
        if _normalize_skill(skill) not in candidate_normalized
    ]


def _normalize_skill(skill: str) -> str:
    """Normalize a skill for case-insensitive comparison."""
    return " ".join(skill.lower().strip().split())


def _build_summary_changes(
    job: JobOpening,
    matched_skills: list[str],
) -> list[str]:
    """Build recommendations for the resume summary."""
    recommendations: list[str] = []

    title = getattr(job, "title", None)

    if title:
        recommendations.append(
            f"Align the professional summary with the "
            f"{title} role without changing your actual title."
        )

    if matched_skills:
        top_skills = ", ".join(matched_skills[:5])
        recommendations.append(
            f"Include the strongest matching skills near the top: "
            f"{top_skills}."
        )

    remote_status = str(
        getattr(job, "remote_status", "")
    ).strip().lower()

    if "remote" in remote_status:
        recommendations.append(
            "Mention successful remote collaboration and independent delivery."
        )

    return recommendations


def _build_experience_recommendations(
    matched_skills: list[str],
) -> list[str]:
    """Suggest experience areas to emphasize based on matched skills."""
    recommendations: list[str] = []

    skill_text = " ".join(matched_skills).lower()

    categories = {
        "Python automation work": (
            "python",
            "pytest",
            "robot framework",
        ),
        "browser and UI automation": (
            "selenium",
            "playwright",
            "cypress",
        ),
        "API testing and service integration": (
            "api",
            "postman",
            "rest",
        ),
        "CI/CD and automated delivery": (
            "ci/cd",
            "jenkins",
            "gitlab",
            "azure devops",
            "github actions",
        ),
        "containerized testing and reproducible environments": (
            "docker",
            "kubernetes",
        ),
        "cloud-based testing and infrastructure": (
            "aws",
            "azure",
            "gcp",
            "cloud",
        ),
        "performance and load testing": (
            "jmeter",
            "locust",
            "performance testing",
            "load testing",
        ),
        "AI, machine-learning, or LLM integration projects": (
            "machine learning",
            "ml",
            "ai",
            "llm",
            "openai",
        ),
        "technical leadership and framework ownership": (
            "leadership",
            "lead",
            "mentoring",
            "architecture",
        ),
    }

    for recommendation, keywords in categories.items():
        if any(keyword in skill_text for keyword in keywords):
            recommendations.append(
                f"Highlight measurable accomplishments involving "
                f"{recommendation}."
            )

    return recommendations

def _build_concerns(
    job: JobOpening,
    fit_analysis: FitAnalysis,
    candidate: CandidateProfile,
    missing_required: list[str],
) -> list[str]:
    """Identify issues that may need careful resume treatment."""
    concerns: list[str] = []

    if missing_required:
        concerns.append(
            "Do not claim missing required skills. Address them through "
            "adjacent experience, transferable skills, or current learning."
        )

    if (
        job.security_clearance_required
        and not candidate.has_security_clearance
    ):
        clearance_level = (
            job.security_clearance_level or "unspecified clearance"
        )
        concerns.append(
            f"The role requires {clearance_level}. The candidate profile "
            f"does not indicate an active security clearance."
        )

    for concern in _normalize_collection(fit_analysis.concerns):
        concerns.append(concern)

    if fit_analysis.overall_score < 60:
        concerns.append(
            "The fit score is below 60. Tailoring may help, but review whether "
            "this application is worth the time before rewriting the resume."
        )

    return _unique_preserving_order(concerns)


def _unique_preserving_order(values: list[str]) -> list[str]:
    """Remove duplicates while preserving their original order."""
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        key = value.lower().strip()

        if key and key not in seen:
            seen.add(key)
            result.append(value)

    return result