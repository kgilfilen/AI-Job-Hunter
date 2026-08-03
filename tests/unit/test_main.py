from unittest.mock import Mock, patch

from src.main import process_job_text

@patch("src.main.parse_job_opening")
def test_process_job_text_stores_before_parsing(
    mock_parse_job_opening,
    tmp_path,
) -> None:
    events = []

    repository = Mock()

    def save_original_job(**kwargs):
        events.append("stored")
        return 17

    def record_parse(**kwargs):
        events.append("parsed")
        return Mock()

    repository.save_original_job.side_effect = save_original_job
    mock_parse_job_opening.side_effect = record_parse

    artifact_directory = tmp_path / "000017"
    original_path = artifact_directory / "original_job.txt"

    with patch(
        "src.main.get_job_artifact_directory",
        return_value=artifact_directory,
    ), patch(
        "src.main.write_original_job_artifact",
        return_value=original_path,
    ):
        (
            job_id,
            job_artifact_directory,
            job_opening,
        ) = process_job_text(
            job_text="Untouched original text",
            source_file="sample.txt",
            repository=repository,
            source="file",
        )

    assert job_id == 17
    assert job_artifact_directory == artifact_directory
    assert job_opening is not None
    assert events == ["stored", "parsed"]

    mock_parse_job_opening.assert_called_once_with(
        job_text="Untouched original text",
        source_file="sample.txt",
    )