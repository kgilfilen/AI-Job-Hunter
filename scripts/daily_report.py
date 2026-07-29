"""Generate a lightweight daily development report.

This script makes no OpenAI API calls.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path


def run_git_command(*args: str) -> str:
    """Run a Git command and return its output."""

    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Unavailable"


def get_working_tree_status() -> str:
    status = run_git_command("status", "--short")
    return status if status else "Clean"


def build_report(
    usage_cost: float | None,
    requests: int | None,
    notes: str | None,
) -> str:
    today = date.today().isoformat()

    branch = run_git_command("branch", "--show-current")
    last_commit = run_git_command(
        "log",
        "-1",
        "--pretty=format:%h %s",
    )
    working_tree = get_working_tree_status()

    usage_cost_text = (
        f"${usage_cost:.2f}"
        if usage_cost is not None
        else "Not entered"
    )
    requests_text = (
        str(requests)
        if requests is not None
        else "Not entered"
    )
    notes_text = notes or "None"

    return f"""AI Job Hunter — Daily Report
================================

Date: {today}

OpenAI Usage — Previous Day
---------------------------
Cost: {usage_cost_text}
Requests: {requests_text}

Repository
----------
Branch: {branch}
Last commit: {last_commit}

Working tree:
{working_tree}

Development Notes
-----------------
{notes_text}
"""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a daily AI Job Hunter report."
    )
    parser.add_argument(
        "--usage-cost",
        type=float,
        help="Previous day's OpenAI API cost in dollars.",
    )
    parser.add_argument(
        "--requests",
        type=int,
        help="Previous day's number of OpenAI requests.",
    )
    parser.add_argument(
        "--notes",
        help="Brief development notes.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    report = build_report(
        usage_cost=args.usage_cost,
        requests=args.requests,
        notes=args.notes,
    )

    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
