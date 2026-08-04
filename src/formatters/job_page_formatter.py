"""Format fetched job-page evidence for downstream parsing."""

from typing import List

from src.models.fetched_job_page import FetchedJobPage


def build_parser_input(page: FetchedJobPage) -> str:
    """Combine page metadata and visible text into parser input."""

    sections: List[str] = [
        "JOB PAGE EVIDENCE",
        "",
        f"Requested URL: {page.requested_url}",
    ]

    if page.canonical_url:
        sections.append(
            f"Canonical URL: {page.canonical_url}"
        )

    if page.page_title:
        sections.extend(
            [
                "",
                "Page Title:",
                page.page_title,
            ]
        )

    if page.metadata:
        sections.extend(
            [
                "",
                "Page Metadata:",
            ]
        )

        for key in sorted(page.metadata):
            value = page.metadata[key]

            if value.strip():
                sections.append(
                    f"{key}: {value}"
                )

    sections.extend(
        [
            "",
            "Visible Page Text:",
            "------------------",
            page.visible_text,
        ]
    )

    return "\n".join(sections)