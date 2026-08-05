"""Unit tests for structured job metadata extraction."""

from src.models.job_metadata import JobMetadata
from src.fetchers.job_metadata_extractor import (
    extract_job_metadata,
    find_job_posting,
    extract_json_ld,
)


def test_extract_json_ld_returns_single_dictionary() -> None:
    html = """
    <html>
        <head>
            <script type="application/ld+json">
                {
                    "@context": "https://schema.org",
                    "@type": "JobPosting",
                    "title": "Senior QA Engineer"
                }
            </script>
        </head>
    </html>
    """

    blocks = extract_json_ld(html)

    assert blocks == [
        {
            "@context": "https://schema.org",
            "@type": "JobPosting",
            "title": "Senior QA Engineer",
        }
    ]


def test_extract_json_ld_returns_multiple_dictionaries() -> None:
    html = """
    <html>
        <head>
            <script type="application/ld+json">
                {
                    "@type": "Organization",
                    "name": "Applied Systems"
                }
            </script>

            <script type="application/ld+json">
                {
                    "@type": "JobPosting",
                    "title": "Software Development Engineer in Test"
                }
            </script>
        </head>
    </html>
    """

    blocks = extract_json_ld(html)

    assert len(blocks) == 2

    assert blocks[0]["@type"] == "Organization"
    assert blocks[0]["name"] == "Applied Systems"

    assert blocks[1]["@type"] == "JobPosting"
    assert blocks[1]["title"] == (
        "Software Development Engineer in Test"
    )


def test_extract_json_ld_ignores_malformed_json() -> None:
    html = """
    <html>
        <head>
            <script type="application/ld+json">
                {
                    "@type": "JobPosting",
                    "title": "Broken JSON",
                }
            </script>
        </head>
    </html>
    """

    blocks = extract_json_ld(html)

    assert blocks == []

def test_find_job_posting_returns_matching_block() -> None:
    blocks = [
        {
            "@type": "Organization",
            "name": "Applied Systems",
        },
        {
            "@type": "JobPosting",
            "title": "Senior QA Engineer",
        },
    ]

    result = find_job_posting(blocks)

    assert result == {
        "@type": "JobPosting",
        "title": "Senior QA Engineer",
    }


def test_find_job_posting_supports_graph() -> None:
    blocks = [
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "name": "Applied Systems",
                },
                {
                    "@type": "JobPosting",
                    "title": "Senior QA Engineer",
                },
            ],
        }
    ]

    result = find_job_posting(blocks)

    assert result is not None
    assert result["title"] == "Senior QA Engineer"


def test_extract_job_metadata_from_job_posting() -> None:
    blocks = [
        {
            "@type": "JobPosting",
            "title": "Senior QA Engineer",
            "employmentType": "FULL_TIME",
            "datePosted": "2026-08-01",
            "validThrough": "2026-09-01",
            "hiringOrganization": {
                "@type": "Organization",
                "name": "Applied Systems",
            },
            "jobLocation": {
                "@type": "Place",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Denver",
                    "addressRegion": "CO",
                    "addressCountry": "US",
                },
            },
        }
    ]

    metadata = extract_job_metadata(blocks)

    assert metadata == JobMetadata(
        title="Senior QA Engineer",
        company="Applied Systems",
        location="Denver, CO, US",
        employment_type="FULL_TIME",
        date_posted="2026-08-01",
        valid_through="2026-09-01",
    )


def test_extract_job_metadata_returns_empty_model_without_job() -> None:
    metadata = extract_job_metadata(
        [
            {
                "@type": "Organization",
                "name": "Applied Systems",
            }
        ]
    )

    assert metadata == JobMetadata()