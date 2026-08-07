import pytest

from unittest.mock import Mock, patch

from src.database.repository import SaveJobResult
from src.models.candidate_profile import CandidateProfile
from src.services.job_service import JobService
from src.artifacts.analysis_artifacts import (
    save_fit_analysis,
    save_job_opening,
    save_resume_recommendation,
    save_tailored_resume,
)


def make_profile() -> CandidateProfile:
    return CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe",
        core_skills=["Python"],
    )

def test_analyze_url_rejects_empty_url() -> None:
    repository = Mock()
    service = JobService(repository)

    with pytest.raises(
        ValueError,
        match="Job URL cannot be empty",
    ):
        service.analyze_url(
            url="   ",
            profile=make_profile(),
        )

@patch("src.services.job_service.parse_job_opening")
@patch("src.services.job_service.get_job_artifact_directory")
def test_analyze_skips_duplicate_without_reprocess(
    mock_get_artifact_directory,
    mock_parse_job_opening,
    tmp_path,
) -> None:
    repository = Mock()

    repository.save_original_job.return_value = (
        SaveJobResult(
            job_id=17,
            created=False,
            duplicate_reason="source_url",
        )
    )

    artifact_directory = tmp_path / "000017"

    mock_get_artifact_directory.return_value = (
        artifact_directory
    )

    service = JobService(repository)

    result = service.analyze(
        source_name="sample.txt",
        original_text="Original job text",
        parser_text="Parser job text",
        profile=make_profile(),
        source="url",
        source_url="https://example.com/job/17",
        reprocess=False,
    )

    assert result.job_id == 17
    assert result.skipped is True
    assert result.job_opening is None

    mock_parse_job_opening.assert_not_called()
    repository.update_parsed_job.assert_not_called()
    repository.update_fit_analysis.assert_not_called()

@patch("src.services.job_service.save_tailored_resume")
@patch("src.services.job_service.save_resume_recommendation")
@patch("src.services.job_service.save_fit_analysis")
@patch("src.services.job_service.save_job_opening")
@patch("src.services.job_service.ResumeFormatter")
@patch("src.services.job_service.recommend_resume_changes")
@patch("src.services.job_service.score_job")
@patch("src.services.job_service.parse_job_opening")
@patch("src.services.job_service.write_original_job_artifact")
@patch("src.services.job_service.get_job_artifact_directory")
def test_analyze_reprocesses_duplicate_when_requested(
    mock_get_artifact_directory,
    mock_write_original,
    mock_parse,
    mock_score,
    mock_recommend,
    mock_formatter_class,
    mock_save_job,
    mock_save_fit,
    mock_save_recommendation,
    mock_save_resume,
    tmp_path,
) -> None:
    repository = Mock()

    repository.save_original_job.return_value = (
        SaveJobResult(
            job_id=17,
            created=False,
            duplicate_reason="source_url",
        )
    )

    artifact_directory = tmp_path / "000017"
    mock_get_artifact_directory.return_value = (
        artifact_directory
    )

    job_opening = Mock()
    fit_analysis = Mock()
    recommendation = Mock()

    mock_parse.return_value = job_opening
    mock_score.return_value = fit_analysis
    mock_recommend.return_value = recommendation

    formatter = Mock()
    formatter.format.return_value = "resume text"
    mock_formatter_class.return_value = formatter

    service = JobService(repository)

    result = service.analyze(
        source_name="sample.txt",
        original_text="Original job text",
        parser_text="Parser job text",
        profile=make_profile(),
        source="url",
        source_url="https://example.com/job/17",
        reprocess=True,
    )

    assert result.job_id == 17
    assert result.skipped is False
    assert result.job_opening is job_opening
    assert result.fit_analysis is fit_analysis

    mock_parse.assert_called_once_with(
        job_text="Parser job text",
        source_file="sample.txt",
    )

    repository.update_parsed_job.assert_called_once_with(
        job_id=17,
        job_opening=job_opening,
    )

    repository.update_fit_analysis.assert_called_once_with(
        job_id=17,
        fit_analysis=fit_analysis,
    )

@patch("src.services.job_service.build_parser_input")
@patch("src.services.job_service.fetch_job_description")
def test_analyze_url_builds_job_input(
    mock_fetch_job_description,
    mock_build_parser_input,
) -> None:
    repository = Mock()
    service = JobService(repository)

    fetched_job = Mock()
    fetched_job.visible_text = "Original job text"
    fetched_job.canonical_url = (
        "https://example.com/canonical-job"
    )
    fetched_job.requested_url = (
        "https://example.com/requested-job"
    )

    mock_fetch_job_description.return_value = fetched_job
    mock_build_parser_input.return_value = (
        "Enriched parser text"
    )

    expected_result = Mock()

    with patch.object(
        service,
        "analyze",
        return_value=expected_result,
    ) as mock_analyze:
        result = service.analyze_url(
            url="https://example.com/requested-job",
            profile=make_profile(),
            reprocess=True,
        )

    assert result is expected_result

    mock_analyze.assert_called_once_with(
        source_name="fetched_job.txt",
        original_text="Original job text",
        parser_text="Enriched parser text",
        profile=make_profile(),
        source="url",
        source_url=(
            "https://example.com/canonical-job"
        ),
        reprocess=True,
    )

from unittest.mock import Mock, patch

from src.database.save_job_result import SaveJobResult
from src.services.job_service import JobService


@patch("src.services.job_service.parse_job_opening")
@patch("src.services.job_service.write_original_job_artifact")
@patch("src.services.job_service.get_job_artifact_directory")
def test_process_job_text_stores_before_parsing(
    mock_get_job_artifact_directory,
    mock_write_original_job_artifact,
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

    repository.save_original_job.side_effect = (
        save_original_job
    )

    mock_parse_job_opening.side_effect = (
        record_parse
    )

    artifact_directory = (
        tmp_path / "000017"
    )

    original_path = (
        artifact_directory / "original_job.txt"
    )

    mock_get_job_artifact_directory.return_value = (
        artifact_directory
    )

    mock_write_original_job_artifact.return_value = (
        original_path
    )

    service = JobService(
        repository=repository,
    )

    (
        job_id,
        job_artifact_directory,
        job_opening,
    ) = service._process_job_text(
        original_text="Untouched original text",
        parser_text="Enriched parser text",
        source_file="sample.txt",
        source="file",
    )

    assert job_id == 17
    assert (
        job_artifact_directory
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