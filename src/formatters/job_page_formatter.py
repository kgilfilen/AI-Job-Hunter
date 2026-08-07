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

    job_metadata = page.job_metadata

    salary_text = None

    if job_metadata.salary is not None:
        salary_parts = []

        if job_metadata.salary_currency:
            salary_parts.append(
                job_metadata.salary_currency
            )

        salary_parts.append(
            job_metadata.salary
        )

        salary_text = " ".join(
            salary_parts
        )

        if job_metadata.salary_interval:
            salary_text += (
                f" per {job_metadata.salary_interval}"
            )

    structured_values = {
        "Title": job_metadata.title,
        "Company": job_metadata.company,
        "Location": job_metadata.location,
        "Employment Type": job_metadata.employment_type,
        "Salary": salary_text,
        "Date Posted": job_metadata.date_posted,
        "Valid Through": job_metadata.valid_through,
    }

    if any(
        value is not None
        for value in structured_values.values()
    ):
        sections.extend(
            [
                "",
                "Structured Job Metadata:",
            ]
        )

        for key, value in structured_values.items():
            if value is not None:
                sections.append(
                    f"{key}: {value}"
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