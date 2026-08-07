import argparse
import json

from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Optional

from src.fetchers.web_fetcher import fetch_job_description
from src.formatters.resume_formatter import ResumeFormatter
from src.formatters.job_page_formatter import build_parser_input
from src.models.candidate_profile import CandidateProfile
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import ResumeRecommendation
from src.models.job_input import JobInput
from src.parsers.job_opening_parser import parse_job_opening
from src.profile_loader import load_candidate_profile
from src.services.profile_service import ProfileService
from src.resume.resume_recommender import recommend_resume_changes
from src.scoring.fit_scorer import score_job
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository
from src.artifacts.job_artifacts import write_original_job_artifact
from src.artifacts.job_artifacts import get_job_artifact_directory
from src.database.save_job_result import SaveJobResult


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
    input_group = parser.add_mutually_exclusive_group(required=True)

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


def save_job_opening(
    job_opening: JobOpening,
    job_artifact_directory: Path,
) -> Path:
    """Save the parsed job opening as JSON."""

    output_file = job_artifact_directory / "job.json"

    _write_json(
        output_file=output_file,
        value=job_opening,
    )

    return output_file
    
def save_fit_analysis(
    fit_analysis: FitAnalysis,
    job_artifact_directory: Path,
) -> Path:
    """Save the fit analysis as JSON."""

    output_file = job_artifact_directory / "fit_analysis.json"

    _write_json(
        output_file=output_file,
        value=fit_analysis,
    )

    return output_file


def save_resume_recommendation(
    recommendation: ResumeRecommendation,
    job_artifact_directory: Path,
) -> Path:
    """Save resume-tailoring recommendations as JSON."""

    output_file = (
        job_artifact_directory
        / "resume_recommendation.json"
    )

    _write_json(
        output_file=output_file,
        value=recommendation,
    )

    return output_file



def save_tailored_resume(
    resume_text: str,
    job_artifact_directory: Path,
) -> Path:
    """Save the tailored resume as Markdown."""

    output_file = (
        job_artifact_directory
        / "tailored_resume.md"
    )

    output_file.write_text(
        resume_text,
        encoding="utf-8",
    )

    return output_file

def _write_json(
    output_file: Path,
    value: object,
) -> None:
    """Serialize a dataclass value to formatted JSON."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_dict = make_json_safe(asdict(value))

    output_file.write_text(
        json.dumps(safe_dict, indent=4),
        encoding="utf-8",
    )

def _store_original_job(
    repository: SQLiteJobRepository,
    job_text: str,
    source: str,
    source_url: Optional[str] = None,
) -> SaveJobResult:
    """Persist untouched job text or identify an existing job."""

    result = repository.save_original_job(
        original_description=job_text,
        source=source,
        source_url=source_url,
    )

    if result.created:
        print(
            f"Created job record {result.job_id}."
        )
    else:
        reason_labels = {
            "source_url": "same source URL",
            "description_hash": "identical job description",
        }

        reason = reason_labels.get(
            result.duplicate_reason,
            "existing job",
        )

        print(
            f"Duplicate found: job {result.job_id} "
            f"matched by {reason}."
        )

    return result

def make_json_safe(value: object) -> object:
    """Convert enums and nested collections into JSON-safe values."""
    if isinstance(value, Enum):
        return value.value

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    return value


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

        original_text = fetched_job.visible_text.strip()

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

def process_job(
    source_name: str,
    original_text: str,
    parser_text: str,
    profile: CandidateProfile,
    repository: SQLiteJobRepository,
    source: str,
    source_url: Optional[str] = None,
    reprocess: bool = False,
) -> None:
    """Process one job and save all generated artifacts."""

    print(f"\n--- Processing {source_name} ---")

    if not original_text:
        raise ValueError(
            f"Job description is empty: {source_name}"
        )

    if not parser_text:
        raise ValueError(
            f"Parser input is empty: {source_name}"
        )

    (
        job_id,
        job_artifact_directory,
        job_opening,
    ) = process_job_text(
        original_text=original_text,
        parser_text=parser_text,
        source_file=source_name,
        repository=repository,
        source=source,
        source_url=source_url,
        reprocess=reprocess,
    )

    if job_opening is None:
        return

    fit_analysis = score_job(
        job_opening,
        profile,
    )

    repository.update_fit_analysis(
        job_id=job_id,
        fit_analysis=fit_analysis,
    )

    recommendation = recommend_resume_changes(
        job=job_opening,
        fit_analysis=fit_analysis,
        candidate=profile,
    )

    resume_text = ResumeFormatter().format(
        candidate=profile,
        job=job_opening,
        analysis=fit_analysis,
        recommendations=recommendation,
    )

    job_output_file = save_job_opening(
        job_opening=job_opening,
        job_artifact_directory=job_artifact_directory,
    )

    fit_output_file = save_fit_analysis(
        fit_analysis=fit_analysis,
        job_artifact_directory=job_artifact_directory,
    )

    recommendation_output_file = save_resume_recommendation(
        recommendation=recommendation,
        job_artifact_directory=job_artifact_directory,
    )

    resume_output_file = save_tailored_resume(
        resume_text=resume_text,
        job_artifact_directory=job_artifact_directory,
    )

    print("\033[1mJob Opening:\033[0m")
    print(
        json.dumps(
            make_json_safe(asdict(job_opening)),
            indent=4,
        )
    )

    print("\033[1mFit Analysis:\033[0m")
    print(
        json.dumps(
            make_json_safe(asdict(fit_analysis)),
            indent=4,
        )
    )

    print("\033[1mResume Recommendation:\033[0m")
    print(
        json.dumps(
            make_json_safe(asdict(recommendation)),
            indent=4,
        )
    )

    print("\033[1mGenerated Files:\033[0m")
    print(f"Database job ID: {job_id}")
    print(f"Saved: {job_output_file}")
    print(f"Saved: {fit_output_file}")
    print(f"Saved: {recommendation_output_file}")
    print(f"Saved: {resume_output_file}")

def process_job_text(
    original_text: str,
    parser_text: str,
    source_file: str,
    repository: SQLiteJobRepository,
    source: str,
    source_url: Optional[str] = None,
    reprocess: bool = False,
) -> tuple[int, Path, Optional[JobOpening]]:
    """Store original input and parse it unless it is a skipped duplicate."""

    save_result = _store_original_job(
        repository=repository,
        job_text=original_text,
        source=source,
        source_url=source_url,
    )

    job_id = save_result.job_id

    job_artifact_directory = get_job_artifact_directory(
        job_id
    )

    if not save_result.created and not reprocess:
        print(
            f"Skipping job {job_id}. "
            "Use --reprocess to regenerate its analysis "
            "and artifacts."
        )

        return (
            job_id,
            job_artifact_directory,
            None,
        )

    if not save_result.created:
        print(f"Reprocessing existing job {job_id}.")

    original_artifact_path = write_original_job_artifact(
        job_id=job_id,
        job_text=original_text,
    )

    print(
        "Saved original job artifact to "
        f"{original_artifact_path}"
    )

    job_opening = parse_job_opening(
        job_text=parser_text,
        source_file=source_file,
    )

    repository.update_parsed_job(
        job_id=job_id,
        job_opening=job_opening,
    )

    return (
        job_id,
        job_artifact_directory,
        job_opening,
    )
    
    
def main() -> None:
    """Run the job-analysis and resume-tailoring workflow."""
    initialize_database()
    job_repository = SQLiteJobRepository()
    args = parse_arguments()

    profile_service = ProfileService()

    profile = profile_service.load(
        args.profile,
    )

    job_inputs = get_job_inputs(args)

    for job_input in job_inputs:
        process_job(
            source_name=job_input.source_name,
            original_text=job_input.original_text,
            parser_text=job_input.parser_text,
            profile=profile,
            repository=job_repository,
            source=job_input.source,
            source_url=job_input.source_url,
            reprocess=args.reprocess,
        )
if __name__ == "__main__":
    main()
