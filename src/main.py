import argparse
import json

from dataclasses import asdict
from enum import Enum
from pathlib import Path

from src.parsers.job_opening_parser import parse_job_opening
from src.models.candidate_profile import CandidateProfile
from src.scoring.fit_scorer import score_job
from src.models.fit_analysis import FitAnalysis
from src.fetchers.web_fetcher import fetch_job_description
from src.profile_loader import load_candidate_profile


JOBS_DIR = Path("examples/jobs")
OUTPUT_DIR = Path("examples/output")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse and score one or more job descriptions."
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


def save_job_opening(job_file: Path, job_opening) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}.json"
    safe_dict = make_json_safe(asdict(job_opening))

    output_file.write_text(
        json.dumps(safe_dict, indent=4),
        encoding="utf-8",
    )

    return output_file


def save_fit_analysis(
    job_file: Path,
    fit_analysis: FitAnalysis,
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}_fit.json"
    safe_dict = make_json_safe(asdict(fit_analysis))

    output_file.write_text(
        json.dumps(safe_dict, indent=4),
        encoding="utf-8",
    )

    return output_file


def make_json_safe(value):
    if isinstance(value, Enum):
        return value.value

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            make_json_safe(key): make_json_safe(val)
            for key, val in value.items()
        }

    return value


def build_candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Kenny Gilfilen",
        target_titles=[
            "SDET",
            "Software Development Engineer in Test",
            "QA Automation Engineer",
            "Test Automation Engineer",
            "Quality Engineer",
        ],
        core_skills=[
            "Python",
            "pytest",
            "Playwright",
            "Selenium",
            "API testing",
            "test automation",
        ],
        remote_preference="remote",
        has_security_clearance=False,
        willing_to_relocate=False,
    )


def get_job_inputs(args: argparse.Namespace) -> list[tuple[str, str]]:
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
        job_text = fetch_job_description(args.url)

        return [("fetched_job.txt", job_text)]

    job_files = sorted(JOBS_DIR.glob("*.txt"))

    if not job_files:
        raise FileNotFoundError(
            f"No job-description files found in {JOBS_DIR}"
        )

    return [
        (
            job_file.name,
            job_file.read_text(
                encoding="utf-8"
            ).strip(),
        )
        for job_file in job_files
    ]

def process_job(
    source_name: str,
    job_text: str,
    profile: CandidateProfile,
) -> None:
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

    output_key = Path(source_name)

    print("\033[1mFit Analysis:\033[0m")
    print(
        json.dumps(
            make_json_safe(asdict(fit_analysis)),
            indent=4,
        )
    )

    output_fit_file = save_fit_analysis(
        output_key,
        fit_analysis,
    )

    output_file = save_job_opening(
        output_key,
        job_opening,
    )

    print("\033[1mJob Opening:\033[0m")
    print(
        json.dumps(
            make_json_safe(asdict(job_opening)),
            indent=4,
        )
    )

    print(f"Saved: {output_file}")
    print(f"Saved: {output_fit_file}")


def main() -> None:
    args = parse_arguments()
    profile = load_candidate_profile(args.profile)
    job_inputs = get_job_inputs(args)

    for source_name, job_text in job_inputs:
        process_job(
            source_name,
            job_text,
            profile,
        )


if __name__ == "__main__":
    main()