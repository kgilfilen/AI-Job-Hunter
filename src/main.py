import json
from dataclasses import asdict
from pathlib import Path
from enum import Enum

from parsers.job_opening_parser import parse_job_opening
from models.candidate_profile import CandidateProfile
from scoring.fit_scorer import score_job
from models.fit_analysis import FitAnalysis



JOBS_DIR = Path("examples/jobs")
OUTPUT_DIR = Path("examples/output")


def save_job_opening(job_file: Path, job_opening) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}.json"

    safe_dict = make_json_safe(asdict(job_opening))

    output_file.write_text(
        json.dumps(safe_dict, indent=4),
        encoding="utf-8",
    )

    return output_file

def save_fit_analysis(job_file: Path, fit_analysis: FitAnalysis) -> Path:
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

def main():
    job_files = sorted(JOBS_DIR.glob("*.txt"))
    job_files = sorted(JOBS_DIR.glob("dev_II_cpp.txt"))

    profile = CandidateProfile(
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

    for job_file in job_files:
        print(f"\n--- Processing {job_file.name} ---")

        job_text = job_file.read_text(encoding="utf-8")
        job_opening = parse_job_opening(
            job_text=job_text,
            source_file=job_file.name,
        )
        fit_analysis = score_job(job_opening, profile)
        print("\033[1mFit Analysis:\033[0m")
        print(json.dumps(make_json_safe(asdict(fit_analysis)), indent=4))
        output_fit_file = save_fit_analysis(job_file, fit_analysis)

        output_file = save_job_opening(job_file, job_opening)

        print("\033[1mJob Opening:\033[0m")
        print(json.dumps(make_json_safe(asdict(job_opening)), indent=4))
        print(f"Saved: {output_file}")
        print(f"Saved: {output_fit_file}")


if __name__ == "__main__":
    main()
