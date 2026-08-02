"""Normalize common job-title abbreviations."""

_TITLE_ALIASES = {
    "sr sdet": "Senior Software Development Engineer in Test",
    "senior sdet": "Senior Software Development Engineer in Test",
    "sdet": "Software Development Engineer in Test",
}


def normalize_job_title(title: str) -> str:
    """Return a canonical title when a known alias exists."""

    cleaned_title = " ".join(title.strip().split())
    normalized_key = cleaned_title.casefold()

    return _TITLE_ALIASES.get(normalized_key, cleaned_title)