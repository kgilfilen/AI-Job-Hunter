"""
Resume formatter.

Converts a candidate profile, job opening, and fit analysis
into a tailored Markdown resume.
"""

from src.models.job_opening import JobOpening
from src.models.fit_analysis import FitAnalysis
from src.models.candidate_profile import CandidateProfile


class ResumeFormatter:
    """Formats a tailored resume."""

    def format(
        self,
        candidate: CandidateProfile,
        job: JobOpening,
        analysis: FitAnalysis,
    ) -> str:
        """Return a Markdown resume."""

        lines = []

        # Header
        lines.append(f"# {candidate.name}")
        lines.append("")
        lines.append(candidate.email)
        lines.append(candidate.phone)
        lines.append(candidate.location)
        lines.append("")

        # Professional Summary
        lines.append("## Professional Summary")
        lines.append(candidate.summary)
        lines.append("")

        # Core Skills
        lines.append("## Core Skills")

        for skill in candidate.core_skills:
            lines.append(f"- {skill}")

        lines.append("")

        # Professional Experience
        lines.append("## Professional Experience")

        for experience in candidate.experience:

            lines.append(f"### {experience.title}")
            lines.append(experience.company)
            lines.append(experience.dates)
            lines.append("")

            for bullet in experience.highlights:
                lines.append(f"- {bullet}")

            lines.append("")

        # Education
        lines.append("## Education")

        for school in candidate.education:
            lines.append(f"- {school}")

        lines.append("")

        # Certifications
        if candidate.certifications:

            lines.append("## Certifications")

            for cert in candidate.certifications:
                lines.append(f"- {cert}")

            lines.append("")

        return "\n".join(lines)
