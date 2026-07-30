"""Model for resume-tailoring recommendations."""

from dataclasses import dataclass, field


@dataclass
class ResumeRecommendation:
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