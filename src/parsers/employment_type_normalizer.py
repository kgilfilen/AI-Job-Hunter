# src/parsers/employment_type_normalizer.py

import re
from typing import Optional


_EMPLOYMENT_TYPE_ALIASES = {
    "full time": "full-time",
    "fulltime": "full-time",
    "full-time": "full-time",
    "part time": "part-time",
    "parttime": "part-time",
    "part-time": "part-time",
    "contract": "contract",
    "contractor": "contract",
    "temporary": "temporary",
    "temp": "temporary",
    "intern": "internship",
    "internship": "internship",
}


def normalize_employment_type(
    employment_type: Optional[str],
) -> Optional[str]:
    """Normalize an extracted employment type to a canonical value."""

    if employment_type is None:
        return None

    normalized_key = re.sub(
        r"\s+",
        " ",
        employment_type.strip().casefold(),
    )

    return _EMPLOYMENT_TYPE_ALIASES.get(normalized_key, normalized_key)

def detect_employment_type(job_text: str) -> Optional[str]:
    """Detect explicit employment-type language in a job description."""

    normalized_text = re.sub(
        r"[-_/]",
        " ",
        job_text.casefold(),
    )
    normalized_text = re.sub(r"\s+", " ", normalized_text)

    patterns = (
        (r"\bfull\s*time\b", "full-time"),
        (r"\bpart\s*time\b", "part-time"),
        (r"\bcontract(?:or)?\b", "contract"),
        (r"\btemporary\b|\btemp\b", "temporary"),
        (r"\binternship\b|\bintern\b", "internship"),
    )

    for pattern, canonical_value in patterns:
        if re.search(pattern, normalized_text):
            return canonical_value

    return None
