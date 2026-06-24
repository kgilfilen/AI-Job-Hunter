import json
from pathlib import Path

from parsers.title_parser import verify_job_title
from parsers.company_parser import verify_company_name
from parsers.location_parser import verify_job_location
from parsers.remote_status_parser import verify_job_remote_status
from parsers.employment_type_parser import verify_job_employment_type
from parsers.security_clearnance_parser import verify_job_security_clearance


JOBS_DIR = Path("examples/jobs")
OUTPUT_DIR = Path("examples/output")


def parser_metadata(result):
    return {
        "confidence": result.confidence,
        "evidence": result.evidence,
        "warning": result.warning,
    }


def build_job_opening(job_file: Path) -> dict:
    job_text = job_file.read_text(encoding="utf-8")

    title_result = verify_job_title(job_text)
    company_result = verify_company_name(job_text)
    location_result = verify_job_location(job_text)
    remote_status_result = verify_job_remote_status(job_text)
    employment_type_result = verify_job_employment_type(job_text)
    security_clearance_result = verify_job_security_clearance(job_text)

    return {
        "source_file": job_file.name,
        "title": title_result.title,
        "company": company_result.name,
        "location": location_result.location,
        "remote_status": remote_status_result.status,
        "employment_type": employment_type_result.employment_type,
        "security_clearance": {
            "required": security_clearance_result.required,
            "level": security_clearance_result.level,
        },
        "parser_metadata": {
            "title": parser_metadata(title_result),
            "company": parser_metadata(company_result),
            "location": parser_metadata(location_result),
            "remote_status": parser_metadata(remote_status_result),
            "employment_type": parser_metadata(employment_type_result),
            "security_clearance": parser_metadata(security_clearance_result),
        },
    }


def save_job_opening(job_file: Path, job_opening: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{job_file.stem}.json"

    output_file.write_text(
        json.dumps(job_opening, indent=4),
        encoding="utf-8",
    )

    return output_file


def main():
    job_files = sorted(JOBS_DIR.glob("*.txt"))
    for job_file in job_files:
        print(f"\n--- Processing {job_file.name} ---")

        job_opening = build_job_opening(job_file)
        output_file = save_job_opening(job_file, job_opening)

        print(json.dumps(job_opening, indent=4))
        print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()