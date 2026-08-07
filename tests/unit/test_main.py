from unittest.mock import Mock, patch

from src.database.save_job_result import SaveJobResult
from src.main import display_job_result
from src.services.job_service import JobService


@patch("src.services.job_service.write_original_job_artifact")
@patch("src.services.job_service.get_job_artifact_directory")
@patch("src.services.job_service.parse_job_opening")
def test_process_job_text_stores_before_parsing(
    mock_parse_job_opening,
    mock_get_artifact_directory,
    mock_write_original_job_artifact,
    tmp_path,
) -> None:
    events = []

    repository = Mock()

    def save_original_job(**kwargs):
        events.append("stored")

        return SaveJobResult(
            job_id=17,
            created=True,
        )

    def record_parse(**kwargs):
        events.append("parsed")
        return Mock()

    repository.save_original_job.side_effect = (
        save_original_job
    )

    mock_parse_job_opening.side_effect = (
        record_parse
    )

    artifact_directory = (
        tmp_path / "000017"
    )

    mock_get_artifact_directory.return_value = (
        artifact_directory
    )

    service = JobService(
        repository=repository
    )

    (
        job_id,
        returned_artifact_directory,
        job_opening,
    ) = service._process_job_text(
        original_text="Untouched original text",
        parser_text="Enriched parser text",
        source_file="sample.txt",
        source="file",
    )

    assert job_id == 17
    assert (
        returned_artifact_directory
        == artifact_directory
    )
    assert job_opening is not None

    assert events == [
        "stored",
        "parsed",
    ]

    mock_parse_job_opening.assert_called_once_with(
        job_text="Enriched parser text",
        source_file="sample.txt",
    )

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