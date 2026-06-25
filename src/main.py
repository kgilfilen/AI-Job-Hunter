import json
from dataclasses import asdict
from pathlib import Path

from parsers.job_opening_parser import parse_job_opening


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


def main():
    job_files = sorted(JOBS_DIR.glob("*.txt"))
    job_files = sorted(JOBS_DIR.glob("dev_II_cpp.txt"))

    for job_file in job_files:
        print(f"\n--- Processing {job_file.name} ---")

        job_text = job_file.read_text(encoding="utf-8")
        job_opening = parse_job_opening(
            job_text=job_text,
            source_file=job_file.name,
        )

        output_file = save_job_opening(job_file, job_opening)

        print(json.dumps(asdict(job_opening), indent=4))
        print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()
