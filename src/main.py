import argparse
import json

from dataclasses import asdict
from enum import Enum
from pathlib import Path

from src.fetchers.web_fetcher import fetch_job_description
from src.formatters.resume_formatter import ResumeFormatter
from src.models.candidate_profile import CandidateProfile
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import ResumeRecommendation
from src.parsers.job_opening_parser import parse_job_opening
from src.profile_loader import load_candidate_profile
from src.resume.resume_recommender import recommend_resume_changes
from src.scoring.fit_scorer import score_job


JOBS_DIR = Path("examples/jobs")
OUTPUT_DIR = Path("examples/output")


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
    output_key: Path,
    job_opening: JobOpening,
) -> Path:
    """Save a parsed job opening as JSON."""
    output_file = OUTPUT_DIR / f"{output_key.stem}.json"

    _write_json(
        output_file=output_file,
        value=job_opening,
    )

    return output_file


def save_fit_analysis(
    output_key: Path,
    fit_analysis: FitAnalysis,
) -> Path:
    """Save a fit analysis as JSON."""
    output_file = OUTPUT_DIR / f"{output_key.stem}_fit.json"

    _write_json(
        output_file=output_file,
        value=fit_analysis,
    )

    return output_file


def save_resume_recommendation(
    output_key: Path,
    recommendation: ResumeRecommendation,
) -> Path:
    """Save resume-tailoring recommendations as JSON."""
    output_file = (
        OUTPUT_DIR
        / f"{output_key.stem}_resume_recommendation.json"
    )

    _write_json(
        output_file=output_file,
        value=recommendation,
    )

    return output_file


def save_tailored_resume(
    output_key: Path,
    resume_text: str,
) -> Path:
    """Save a tailored resume as Markdown."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        OUTPUT_DIR
        / f"{output_key.stem}_tailored_resume.md"
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
    """Serialize a dataclass value to a formatted JSON file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_dict = make_json_safe(asdict(value))

    output_file.write_text(
        json.dumps(safe_dict, indent=4),
        encoding="utf-8",
    )


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
) -> list[tuple[str, str]]:
    """Load job-description text from the selected input source."""
    if args.file is not None:
        if not args.file.exists():
            raise FileNotFoundError(
                f"Job-description file does not exist: {args.file}"
            )

        if not args.file.is_file():
            raise ValueError(
                f"Job-description path is not a file: {args.file}"
            )

        job_text = args.file.read_text(
            encoding="utf-8"
        ).strip()

        if not job_text:
            raise ValueError(
                f"Job-description file is empty: {args.file}"
            )

        return [(args.file.name, job_text)]

    if args.url is not None:
        job_text = fetch_job_description(args.url).strip()

        if not job_text:
            raise ValueError(
                f"Fetched job description is empty: {args.url}"
            )

        return [("fetched_job.txt", job_text)]

    job_files = sorted(JOBS_DIR.glob("*.txt"))

    if not job_files:
        raise FileNotFoundError(
            f"No job-description files found in {JOBS_DIR}"
        )

    job_inputs: list[tuple[str, str]] = []

    for job_file in job_files:
        job_text = job_file.read_text(
            encoding="utf-8"
        ).strip()

        if not job_text:
            raise ValueError(
                f"Job-description file is empty: {job_file}"
            )

        job_inputs.append(
            (job_file.name, job_text)
        )

    return job_inputs


def process_job(
    source_name: str,
    job_text: str,
    profile: CandidateProfile,
) -> None:
    """Process one job description and save all generated artifacts."""
    print(f"\n--- Processing {source_name} ---")

    if not job_text:
        raise ValueError(
            f"Job description is empty: {source_name}"
        )

    job_opening = parse_job_opening(
        job_text=job_text,
        source_file=source_name,
    )

    fit_analysis = score_job(
        job_opening,
        profile,
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

    output_key = Path(source_name)

    job_output_file = save_job_opening(
        output_key,
        job_opening,
    )

    fit_output_file = save_fit_analysis(
        output_key,
        fit_analysis,
    )

    recommendation_output_file = save_resume_recommendation(
        output_key,
        recommendation,
    )

    resume_output_file = save_tailored_resume(
        output_key,
        resume_text,
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
    print(f"Saved: {job_output_file}")
    print(f"Saved: {fit_output_file}")
    print(f"Saved: {recommendation_output_file}")
    print(f"Saved: {resume_output_file}")


def main() -> None:
    """Run the job-analysis and resume-tailoring workflow."""
    args = parse_arguments()

    profile = load_candidate_profile(
        args.profile
    )

    job_inputs = get_job_inputs(args)

    for source_name, job_text in job_inputs:
        process_job(
            source_name=source_name,
            job_text=job_text,
            profile=profile,
        )


if __name__ == "__main__":
    main()
