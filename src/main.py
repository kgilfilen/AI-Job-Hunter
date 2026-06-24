from pathlib import Path
from parsers.title_parser import verify_job_title


def main():
    job_files = Path("examples/jobs").glob("*.txt")

    for job_file in job_files:
        print(f"\n--- {job_file.name} ---")
        job_text = job_file.read_text(encoding="utf-8")

        result = verify_job_title(job_text)

        print(f"Title: {result.title}")
        print(f"Confidence: {result.confidence}")
        print(f"Evidence: {result.evidence}")
        print(f"Warning: {result.warning}")


if __name__ == "__main__":
    main()