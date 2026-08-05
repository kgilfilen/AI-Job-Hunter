"""Extract structured metadata from job-posting HTML."""

import json

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from src.models.job_metadata import JobMetadata


def extract_json_ld(
    html: str,
) -> List[Dict[str, Any]]:
    """Return valid JSON-LD dictionaries found in HTML."""

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    blocks: List[Dict[str, Any]] = []

    script_tags = soup.find_all(
        "script",
        attrs={"type": "application/ld+json"},
    )

    for script_tag in script_tags:
        raw_json = script_tag.string

        if raw_json is None:
            raw_json = script_tag.get_text()

        raw_json = raw_json.strip()

        if not raw_json:
            continue

        try:
            value = json.loads(raw_json)
        except json.JSONDecodeError:
            continue

        if isinstance(value, dict):
            blocks.append(value)

    return blocks

def find_job_posting(
    blocks: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Return the first JSON-LD JobPosting object."""

    for block in blocks:
        if block.get("@type") == "JobPosting":
            return block

        graph = block.get("@graph")

        if isinstance(graph, list):
            for item in graph:
                if (
                    isinstance(item, dict)
                    and item.get("@type") == "JobPosting"
                ):
                    return item

    return None


def extract_job_metadata(
    blocks: List[Dict[str, Any]],
) -> JobMetadata:
    """Extract normalized job facts from JSON-LD blocks."""

    job_posting = find_job_posting(blocks)

    if job_posting is None:
        return JobMetadata()

    hiring_organization = job_posting.get(
        "hiringOrganization"
    )

    company = None

    if isinstance(hiring_organization, dict):
        company_value = hiring_organization.get("name")

        if isinstance(company_value, str):
            company = company_value.strip() or None

    return JobMetadata(
        title=_clean_string(
            job_posting.get("title")
        ),
        company=company,
        location=_extract_location(job_posting),
        employment_type=_clean_string(
            job_posting.get("employmentType")
        ),
        date_posted=_clean_string(
            job_posting.get("datePosted")
        ),
        valid_through=_clean_string(
            job_posting.get("validThrough")
        ),
    )


def _clean_string(
    value: object,
) -> Optional[str]:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    return value.strip() or None


def _extract_location(
    job_posting: Dict[str, Any],
) -> Optional[str]:
    """Extract a readable location from JobPosting JSON-LD."""

    job_location = job_posting.get("jobLocation")

    if isinstance(job_location, list):
        if not job_location:
            return None

        job_location = job_location[0]

    if not isinstance(job_location, dict):
        return None

    address = job_location.get("address")

    if not isinstance(address, dict):
        return None

    parts = [
        _clean_string(address.get("addressLocality")),
        _clean_string(address.get("addressRegion")),
        _clean_string(address.get("addressCountry")),
    ]

    return ", ".join(
        part
        for part in parts
        if part is not None
    ) or None