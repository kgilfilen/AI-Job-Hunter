import argparse
import json

from dataclasses import asdict
from pathlib import Path

from src.artifacts.analysis_artifacts import (
    make_json_safe,
)
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository
from src.fetchers.web_fetcher import fetch_job_description
from src.formatters.job_page_formatter import build_parser_input
from src.models.job_input import JobInput
from src.services.job_service import (
    JobAnalysisResult,
    JobService,
)
from src.services.profile_service import ProfileService


JOBS_DIR = Path("examples/jobs")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Parse and score one or more job descriptions, then generate "
            "resume-tailoring recommendations and a Markdown resume."
        )
    )

    parser.add_argument(
        "--profile",
        default="config/candidate_profile.json",
        help="Path to the candidate profile JSON file.",
    )

    parser.add_argument(
        "--reprocess",
        action="store_true",
        help="Reprocess an existing job if it already exists.",
    )

    input_group = parser.add_mutually_exclusive_group(
        required=True
    )

    input_group.add_argument(
        "--file",
        type=Path,
        help="Path to a job-description text file.",
    )

    input_group.add_argument(
        "--examples",
        action="store_true",
        help="Process all .txt files in examples/jobs.",
    )

    input_group.add_argument(
        "--url",
        type=str,
        help="URL of a job description to fetch and process.",
    )

    return parser.parse_args()


def get_job_inputs(
    args: argparse.Namespace,
) -> list[JobInput]:
    """Load original and parser-ready job input."""

    if args.file is not None:
        if not args.file.exists():
            raise FileNotFoundError(
                "Job-description file does not exist: "
                f"{args.file}"
            )

        if not args.file.is_file():
            raise ValueError(
                "Job-description path is not a file: "
                f"{args.file}"
            )

        job_text = args.file.read_text(
            encoding="utf-8"
        ).strip()

        if not job_text:
            raise ValueError(
                f"Job-description file is empty: {args.file}"
            )

        return [
            JobInput(
                source_name=args.file.name,
                original_text=job_text,
                parser_text=job_text,
                source="file",
                source_url=None,
            )
        ]

    if args.url is not None:
        fetched_job = fetch_job_description(
            args.url
        )

        original_text = (
            fetched_job.visible_text.strip()
        )

        if not original_text:
            raise ValueError(
                "Fetched job description is empty: "
                f"{args.url}"
            )

        parser_text = build_parser_input(
            fetched_job
        )

        source_url = (
            fetched_job.canonical_url
            or fetched_job.requested_url
        )

        return [
            JobInput(
                source_name="fetched_job.txt",
                original_text=original_text,
                parser_text=parser_text,
                source="url",
                source_url=source_url,
            )
        ]

    job_files = sorted(
        JOBS_DIR.glob("*.txt")
    )

    if not job_files:
        raise FileNotFoundError(
            f"No job-description files found in {JOBS_DIR}"
        )

    job_inputs: list[JobInput] = []

    for job_file in job_files:
        job_text = job_file.read_text(
            encoding="utf-8"
        ).strip()

        if not job_text:
            raise ValueError(
                f"Job-description file is empty: {job_file}"
            )

        job_inputs.append(
            JobInput(
                source_name=job_file.name,
                original_text=job_text,
                parser_text=job_text,
                source="example",
                source_url=None,
            )
        )

    return job_inputs


def display_job_result(
    result: JobAnalysisResult,
) -> None:
    """Display a job-analysis result in the CLI."""

    if result.skipped:
        print(
            f"Skipping job {result.job_id}. "
            "Use --reprocess to regenerate its "
            "analysis and artifacts."
        )
        return

    print("\033[1mJob Opening:\033[0m")
    print(
        json.dumps(
            make_json_safe(
                asdict(result.job_opening)
            ),
            indent=4,
        )
    )

    print("\033[1mFit Analysis:\033[0m")
    print(
        json.dumps(
            make_json_safe(
                asdict(result.fit_analysis)
            ),
            indent=4,
        )
    )

    print(
        "\033[1mResume Recommendation:\033[0m"
    )
    print(
        json.dumps(
            make_json_safe(
                asdict(result.recommendation)
            ),
            indent=4,
        )
    )

    print("\033[1mGenerated Files:\033[0m")
    print(
        f"Database job ID: {result.job_id}"
    )
    print(
        f"Saved: {result.job_output_file}"
    )
    print(
        f"Saved: {result.fit_output_file}"
    )
    print(
        "Saved: "
        f"{result.recommendation_output_file}"
    )
    print(
        f"Saved: {result.resume_output_file}"
    )


def main() -> None:
    """Run the job-analysis and resume-tailoring workflow."""

    initialize_database()

    args = parse_arguments()

    repository = SQLiteJobRepository()

    profile_service = ProfileService()
    profile = profile_service.load(
        args.profile
    )

    job_service = JobService(
        repository=repository
    )

    job_inputs = get_job_inputs(
        args
    )

    for job_input in job_inputs:
        print(
            f"\n--- Processing "
            f"{job_input.source_name} ---"
        )

        result = job_service.analyze(
            source_name=job_input.source_name,
            original_text=job_input.original_text,
            parser_text=job_input.parser_text,
            profile=profile,
            source=job_input.source,
            source_url=job_input.source_url,
            reprocess=args.reprocess,
        )

        display_job_result(
            result
        )


if __name__ == "__main__":
    main()