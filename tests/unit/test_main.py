import pytest
from unittest.mock import Mock, patch

from src.database.save_job_result import SaveJobResult
from src.main import display_job_result, main
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

def test_main_passes_selected_career_profile_to_job_service() -> None:
    args = Mock()
    args.profile = "candidate_profile.json"
    args.career_profile = "Software / QA"
    args.reprocess = False

    career_profile = Mock()
    career_profile.name = "Software / QA"

    profile = Mock()
    profile.get_career_profile.return_value = career_profile

    job_input = Mock()
    job_input.source_name = "test-job.txt"
    job_input.original_text = "Original job text"
    job_input.parser_text = "Parser job text"
    job_input.source = "test"
    job_input.source_url = None

    analysis_result = Mock()
    analysis_result.skipped = True
    analysis_result.job_id = 1

    with (
        patch("src.main.initialize_database"),
        patch("src.main.parse_arguments", return_value=args),
        patch("src.main.ProfileService") as profile_service_class,
        patch("src.main.JobService") as job_service_class,
        patch("src.main.get_job_inputs", return_value=[job_input]),
        patch("src.main.display_job_result"),
    ):
        profile_service_class.return_value.load.return_value = profile
        job_service_class.return_value.analyze.return_value = analysis_result

        main()

        profile.get_career_profile.assert_called_once_with(
            "Software / QA"
        )

        job_service_class.return_value.analyze.assert_called_once_with(
            source_name="test-job.txt",
            original_text="Original job text",
            parser_text="Parser job text",
            profile=profile,
            career_profile=career_profile,
            source="test",
            source_url=None,
            reprocess=False,
        )

def test_main_raises_for_unknown_career_profile() -> None:
    args = Mock()
    args.profile = "candidate_profile.json"
    args.career_profile = "Culinary"
    args.reprocess = False

    profile = Mock()
    profile.get_career_profile.return_value = None

    with (
        patch("src.main.initialize_database"),
        patch("src.main.parse_arguments", return_value=args),
        patch("src.main.ProfileService") as profile_service_class,
    ):
        profile_service_class.return_value.load.return_value = profile

        with pytest.raises(
            ValueError,
            match="Career profile not found: Culinary",
        ):
            main()