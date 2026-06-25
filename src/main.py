import json
from dataclasses import asdict
from pathlib import Path

from parsers.job_opening_parser import parse_job_opening
from models.candidate_profile import CandidateProfile
from scoring.fit_scorer import score_job


JOBS_DIR = Path("examples/jobs")
OUTPUT_DIR = Path("examples/output")


def save_job_opening(job_file: Path, job_opening) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}.json"

    output_file.write_text(
        json.dumps(asdict(job_opening), indent=4),
        encoding="utf-8",
    )

    return output_file

def save_fit_analysis(job_file: Path, fit_analysis: FitAnalysis) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}_fit.json"

    output_file.write_text(
        json.dumps(asdict(fit_analysis), indent=4),
        encoding="utf-8",
    )

    return output_file

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
        print(json.dumps(asdict(fit_analysis), indent=4))
        output_fit_file = save_fit_analysis(job_file, fit_analysis)

        output_file = save_job_opening(job_file, job_opening)

        print(json.dumps(asdict(job_opening), indent=4))
        print(f"Saved: {output_file}")
        print(f"Saved: {output_fit_file}")


if __name__ == "__main__":
    main()
