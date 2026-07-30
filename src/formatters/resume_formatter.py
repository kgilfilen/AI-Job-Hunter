"""
Resume formatter.

Converts a candidate profile, job opening, fit analysis, and resume
recommendations into a tailored Markdown resume.
"""

from typing import Optional

from src.models.candidate_profile import (
    CandidateProfile,
    Certification,
    Education,
    Experience,
)
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import ResumeRecommendation


class ResumeFormatter:
    """Format a candidate profile as a tailored Markdown resume."""

    def format(
        self,
        candidate: CandidateProfile,
        job: JobOpening,
        analysis: FitAnalysis,
        recommendations: ResumeRecommendation,
    ) -> str:
        """Return a tailored Markdown resume.

        Recommendations influence the ordering and emphasis of existing
        candidate information. The formatter does not add skills or experience
        that are not already present in the candidate profile.
        """
        lines: list[str] = []

        self._add_header(lines, candidate)
        self._add_professional_summary(
            lines=lines,
            candidate=candidate,
            job=job,
            recommendations=recommendations,
        )
        self._add_core_skills(
            lines=lines,
            candidate=candidate,
            recommendations=recommendations,
        )
        self._add_professional_experience(
            lines=lines,
            candidate=candidate,
            recommendations=recommendations,
        )
        self._add_education(lines, candidate)
        self._add_certifications(lines, candidate)

        return "\n".join(lines).rstrip() + "\n"

    def _add_header(
        self,
        lines: list[str],
        candidate: CandidateProfile,
    ) -> None:
        """Add candidate name and contact information."""
        if candidate.name:
            lines.append(f"# {candidate.name}")
            lines.append("")

        contact_values = [
            value
            for value in (
                candidate.email,
                candidate.phone,
                candidate.location,
                candidate.linkedin,
                candidate.github,
            )
            if value
        ]

        lines.extend(contact_values)

        if candidate.name or contact_values:
            lines.append("")

    def _add_professional_summary(
        self,
        lines: list[str],
        candidate: CandidateProfile,
        job: JobOpening,
        recommendations: ResumeRecommendation,
    ) -> None:
        """Add a targeted professional summary."""
        summary_parts: list[str] = []

        if candidate.summary:
            summary_parts.append(candidate.summary.strip())

        matched_skills = self._candidate_matching_skills(
            candidate=candidate,
            recommended_skills=recommendations.skills_to_emphasize,
        )

        if job.title and matched_skills:
            top_skills = ", ".join(matched_skills[:5])
            summary_parts.append(
                f"Relevant strengths for the {job.title} role include "
                f"{top_skills}."
            )
        elif job.title:
            summary_parts.append(
                f"Seeking to apply this experience to the {job.title} role."
            )

        if not summary_parts:
            return

        lines.append("## Professional Summary")
        lines.append(" ".join(summary_parts))
        lines.append("")

    def _add_core_skills(
        self,
        lines: list[str],
        candidate: CandidateProfile,
        recommendations: ResumeRecommendation,
    ) -> None:
        """Add core skills with recommended matches listed first."""
        if not candidate.core_skills:
            return

        lines.append("## Core Skills")

        ordered_skills = self._prioritize_skills(
            candidate_skills=list(candidate.core_skills),
            recommended_skills=recommendations.skills_to_emphasize,
        )

        for skill in ordered_skills:
            lines.append(f"- {skill}")

        lines.append("")

    def _add_professional_experience(
        self,
        lines: list[str],
        candidate: CandidateProfile,
        recommendations: ResumeRecommendation,
    ) -> None:
        """Add professional experience without altering factual content."""
        if not candidate.experience:
            return

        lines.append("## Professional Experience")

        emphasis_terms = self._normalize_terms(
            recommendations.skills_to_emphasize
        )

        for experience in candidate.experience:
            self._add_experience(
                lines=lines,
                experience=experience,
                emphasis_terms=emphasis_terms,
            )

    def _add_experience(
        self,
        lines: list[str],
        experience: Experience,
        emphasis_terms: set[str],
    ) -> None:
        """Add one professional experience entry."""
        lines.append(f"### {experience.title}")
        lines.append(experience.company)

        details = self._join_details(
            experience.location,
            experience.dates,
        )

        if details:
            lines.append(details)

        if experience.highlights:
            lines.append("")

            ordered_highlights = self._prioritize_highlights(
                highlights=list(experience.highlights),
                emphasis_terms=emphasis_terms,
            )

            for bullet in ordered_highlights:
                lines.append(f"- {bullet}")

        lines.append("")

    def _add_education(
        self,
        lines: list[str],
        candidate: CandidateProfile,
    ) -> None:
        """Add education entries."""
        if not candidate.education:
            return

        lines.append("## Education")

        for education in candidate.education:
            lines.append(self._format_education(education))

        lines.append("")

    def _format_education(
        self,
        education: Education,
    ) -> str:
        """Format one education entry."""
        degree_text = education.degree

        if education.field_of_study:
            degree_text = (
                f"{degree_text}, {education.field_of_study}"
            )

        details = self._join_details(
            education.institution,
            education.location,
            education.graduation_date,
        )

        if details:
            return f"- **{degree_text}** — {details}"

        return f"- **{degree_text}**"

    def _add_certifications(
        self,
        lines: list[str],
        candidate: CandidateProfile,
    ) -> None:
        """Add certifications when available."""
        if not candidate.certifications:
            return

        lines.append("## Certifications")

        for certification in candidate.certifications:
            lines.append(
                self._format_certification(certification)
            )

        lines.append("")

    def _format_certification(
        self,
        certification: Certification,
    ) -> str:
        """Format one certification entry."""
        details = self._join_details(
            certification.issuing_organization,
            certification.issue_date,
        )

        expiration_text = ""

        if certification.expiration_date:
            expiration_text = (
                f"; expires {certification.expiration_date}"
            )

        if details:
            return (
                f"- **{certification.name}** — "
                f"{details}{expiration_text}"
            )

        return (
            f"- **{certification.name}**"
            f"{expiration_text}"
        )

    def _candidate_matching_skills(
        self,
        candidate: CandidateProfile,
        recommended_skills: list[str],
    ) -> list[str]:
        """Return recommended skills that exist in the candidate profile."""
        all_candidate_skills = (
            list(candidate.core_skills)
            + list(candidate.preferred_skills)
        )

        candidate_lookup = {
            self._normalize(skill): skill
            for skill in all_candidate_skills
        }

        matches: list[str] = []

        for skill in recommended_skills:
            normalized = self._normalize(skill)

            if normalized in candidate_lookup:
                matches.append(candidate_lookup[normalized])

        return self._unique_preserving_order(matches)

    def _prioritize_skills(
        self,
        candidate_skills: list[str],
        recommended_skills: list[str],
    ) -> list[str]:
        """Place recommended candidate skills before remaining skills."""
        candidate_lookup = {
            self._normalize(skill): skill
            for skill in candidate_skills
        }

        prioritized: list[str] = []

        for skill in recommended_skills:
            normalized = self._normalize(skill)

            if normalized in candidate_lookup:
                prioritized.append(candidate_lookup[normalized])

        prioritized_normalized = {
            self._normalize(skill)
            for skill in prioritized
        }

        remaining = [
            skill
            for skill in candidate_skills
            if self._normalize(skill) not in prioritized_normalized
        ]

        return self._unique_preserving_order(
            prioritized + remaining
        )

    def _prioritize_highlights(
        self,
        highlights: list[str],
        emphasis_terms: set[str],
    ) -> list[str]:
        """Place highlights containing recommended skills first."""
        emphasized: list[str] = []
        remaining: list[str] = []

        for highlight in highlights:
            normalized_highlight = self._normalize(highlight)

            if any(
                term in normalized_highlight
                for term in emphasis_terms
            ):
                emphasized.append(highlight)
            else:
                remaining.append(highlight)

        return emphasized + remaining

    def _normalize_terms(
        self,
        values: list[str],
    ) -> set[str]:
        """Normalize non-empty terms for text matching."""
        return {
            normalized
            for value in values
            if (normalized := self._normalize(value))
        }

    def _join_details(
        self,
        *values: Optional[str],
    ) -> str:
        """Join non-empty résumé details with a separator."""
        return " | ".join(
            value.strip()
            for value in values
            if value and value.strip()
        )

    def _normalize(self, value: str) -> str:
        """Normalize text for case-insensitive comparisons."""
        return " ".join(value.lower().strip().split())

    def _unique_preserving_order(
        self,
        values: list[str],
    ) -> list[str]:
        """Remove duplicates while preserving their original order."""
        seen: set[str] = set()
        result: list[str] = []

        for value in values:
            normalized = self._normalize(value)

            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(value)

        return result