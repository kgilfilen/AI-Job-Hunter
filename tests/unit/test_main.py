from unittest.mock import Mock, patch

from src.main import process_job_text
from src.database.save_job_result import SaveJobResult

@patch("src.main.parse_job_opening")
def test_process_job_text_stores_before_parsing(
    mock_parse_job_opening,
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
            original_text="Untouched original text",
            parser_text="Enriched parser text",
            source_file="sample.txt",
            repository=repository,
            source="file",
        )

    assert job_id == 17
    assert job_artifact_directory == artifact_directory
    assert job_opening is not None
    assert events == ["stored", "parsed"]

    mock_parse_job_opening.assert_called_once_with(
        job_text="Enriched parser text",
        source_file="sample.txt",
    )

@patch("src.main.parse_job_opening")
def test_process_job_text_skips_duplicate_without_reprocess(
    mock_parse_job_opening,
    tmp_path,
    capsys,
) -> None:
    repository = Mock()
    repository.save_original_job.return_value = SaveJobResult(
        job_id=17,
        created=False,
        duplicate_reason="source_url",
    )

    artifact_directory = tmp_path / "000017"

    with patch(
        "src.main.get_job_artifact_directory",
        return_value=artifact_directory,
    ), patch(
        "src.main.write_original_job_artifact",
    ) as mock_write_original:
        (
            job_id,
            job_artifact_directory,
            job_opening,
        ) = process_job_text(
            original_text="Original text",
            parser_text="Enriched parser text",
            source_file="sample.txt",
            repository=repository,
            source="url",
            source_url="https://example.com/jobs/17",
            reprocess=False,
        )

    captured = capsys.readouterr()

    assert job_id == 17
    assert job_artifact_directory == artifact_directory
    assert job_opening is None

    assert (
        "Duplicate found: job 17 matched by same source URL."
        in captured.out
    )
    assert (
        "Skipping job 17. "
        "Use --reprocess to regenerate its analysis and artifacts."
        in captured.out
    )

    mock_parse_job_opening.assert_not_called()
    mock_write_original.assert_not_called()
    repository.update_parsed_job.assert_not_called()


@patch("src.main.parse_job_opening")
def test_process_job_text_reprocesses_duplicate_when_requested(
    mock_parse_job_opening,
    tmp_path,
    capsys,
) -> None:
    repository = Mock()
    repository.save_original_job.return_value = SaveJobResult(
        job_id=17,
        created=False,
        duplicate_reason="source_url",
    )

    parsed_job = Mock()
    mock_parse_job_opening.return_value = parsed_job

    artifact_directory = tmp_path / "000017"
    original_path = artifact_directory / "original_job.txt"

    with patch(
        "src.main.get_job_artifact_directory",
        return_value=artifact_directory,
    ), patch(
        "src.main.write_original_job_artifact",
        return_value=original_path,
    ) as mock_write_original:
        (
            job_id,
            job_artifact_directory,
            job_opening,
        ) = process_job_text(
            original_text="Original text",
            parser_text="Enriched parser text",
            source_file="sample.txt",
            repository=repository,
            source="url",
            source_url="https://example.com/jobs/17",
            reprocess=True,
        )

    captured = capsys.readouterr()

    assert job_id == 17
    assert job_artifact_directory == artifact_directory
    assert job_opening is parsed_job

    assert (
        "Duplicate found: job 17 matched by same source URL."
        in captured.out
    )
    assert "Reprocessing existing job 17." in captured.out
    assert "Skipping job 17." not in captured.out

    mock_write_original.assert_called_once_with(
        job_id=17,
        job_text="Original text",
    )

    mock_parse_job_opening.assert_called_once_with(
        job_text="Enriched parser text",
        source_file="sample.txt",
    )

    repository.update_parsed_job.assert_called_once_with(
        job_id=17,
        job_opening=parsed_job,
    )