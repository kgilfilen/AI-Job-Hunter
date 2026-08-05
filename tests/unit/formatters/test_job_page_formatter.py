"""Unit tests for fetched job-page formatting."""

from src.formatters.job_page_formatter import (
    build_parser_input,
)
from src.models.fetched_job_page import FetchedJobPage
from src.models.job_metadata import JobMetadata


def test_build_parser_input_includes_page_evidence() -> None:
    page = FetchedJobPage(
        requested_url=(
            "https://jobs.example.com/posting/123"
        ),
        canonical_url=(
            "https://example.com/careers/123"
        ),
        page_title=(
            "Senior SDET | Applied Systems"
        ),
        metadata={
            "og:site_name": "Applied Systems",
            "og:title": "Senior SDET",
            "description": (
                "Join Applied Systems as a Senior SDET."
            ),
        },
        visible_text=(
            "Software Development Engineer in Test\n"
            "Build automated Playwright tests."
        ),
    )

    parser_input = build_parser_input(page)

    assert (
        "Requested URL: "
        "https://jobs.example.com/posting/123"
        in parser_input
    )

    assert (
        "Canonical URL: "
        "https://example.com/careers/123"
        in parser_input
    )

    assert (
        "Senior SDET | Applied Systems"
        in parser_input
    )

    assert (
        "og:site_name: Applied Systems"
        in parser_input
    )

    assert (
        "Join Applied Systems as a Senior SDET."
        in parser_input
    )

    assert (
        "Build automated Playwright tests."
        in parser_input
    )


def test_build_parser_input_handles_missing_optional_data() -> None:
    page = FetchedJobPage(
        requested_url="https://example.com/job",
        visible_text="A complete job description.",
    )

    parser_input = build_parser_input(page)

    assert (
        "Requested URL: https://example.com/job"
        in parser_input
    )
    assert "A complete job description." in parser_input
    assert "Canonical URL:" not in parser_input
    assert "Page Title:" not in parser_input
    assert "Page Metadata:" not in parser_input


def test_build_parser_input_sorts_metadata_keys() -> None:
    page = FetchedJobPage(
        requested_url="https://example.com/job",
        visible_text="Job text",
        metadata={
            "og:title": "Senior SDET",
            "description": "Description",
        },
    )

    parser_input = build_parser_input(page)

    description_position = parser_input.index(
        "description: Description"
    )
    title_position = parser_input.index(
        "og:title: Senior SDET"
    )

    assert description_position < title_position

def test_build_parser_input_includes_structured_job_metadata() -> None:
    page = FetchedJobPage(
        requested_url="https://example.com/jobs/123",
        visible_text="Full visible job description.",
        job_metadata=JobMetadata(
            title="Senior QA Engineer",
            company="Applied Systems",
            location="Denver, CO, US",
            employment_type="FULL_TIME",
            date_posted="2026-08-01",
            valid_through="2026-09-01",
        ),
    )

    parser_input = build_parser_input(page)

    assert "Structured Job Metadata:" in parser_input
    assert "Title: Senior QA Engineer" in parser_input
    assert "Company: Applied Systems" in parser_input
    assert "Location: Denver, CO, US" in parser_input
    assert "Employment Type: FULL_TIME" in parser_input
    assert "Date Posted: 2026-08-01" in parser_input
    assert "Valid Through: 2026-09-01" in parser_input

def test_build_parser_input_omits_empty_structured_metadata() -> None:
    page = FetchedJobPage(
        requested_url="https://example.com/job",
        visible_text="Job description.",
    )

    parser_input = build_parser_input(page)

    assert "Structured Job Metadata:" not in parser_input