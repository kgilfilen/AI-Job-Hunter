from dataclasses import dataclass

@dataclass
class JobOpening:
    company: str | None
    title: str | None
    location: str | None

    required_skills: list[str]
    preferred_skills: list[str]

    responsibilities: list[str]

    salary_range: str | None
    remote_status: str | None

    notes: list[str]