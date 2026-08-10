from unittest.mock import Mock, patch

from src.database.save_job_result import SaveJobResult
from src.main import display_job_result
from src.services.job_service import JobService


def test_display_job_result_shows_skipped_job(
    capsys,
) -> None:
    result = Mock()

    result.job_id = 17
    result.skipped = True

    display_job_result(
        result
    )

    captured = capsys.readouterr()

    assert (
        "Skipping job 17."
        in captured.out
    )

    assert (
        "--reprocess"
        in captured.out
    )