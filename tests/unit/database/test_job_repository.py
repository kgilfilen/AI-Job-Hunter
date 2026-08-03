"""Unit tests for SQLiteJobRepository."""
import pytest
from typing import Callable
from unittest.mock import Mock, call, patch

from src.main import _store_original_job, process_job_text
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository
from src.models.job_opening import JobOpening



@pytest.fixture
def repository(tmp_path):
    """Return a repository backed by an isolated temporary database."""

    database_path = tmp_path / "test.db"

    initialize_database(database_path)

    return SQLiteJobRepository(database_path)


def test_save_and_retrieve_original_job(repository) -> None:
    description = """
    Senior Software Development Engineer in Test

    Build and maintain automated tests for web and API systems.
    """

    job_id = repository.save_original_job(
        original_description=description,
        source="manual",
        source_url=None,
    )

    stored_job = repository.get_job(job_id)

    assert stored_job is not None
    assert stored_job["id"] == job_id
    assert stored_job["source"] == "manual"
    assert stored_job["source_url"] is None
    assert stored_job["original_description"] == description
    assert stored_job["status"] == "NEW"
    assert stored_job["description_hash"]


def test_get_job_returns_none_for_unknown_id(repository) -> None:
    assert repository.get_job(999999) is None


def test_save_original_job_rejects_empty_description(repository) -> None:
    with pytest.raises(
        ValueError,
        match="original_description cannot be empty",
    ):
        repository.save_original_job(
            original_description="   ",
            source="manual",
        )

def test_store_original_job_passes_untouched_text_to_repository(
    capsys,
) -> None:
    repository = Mock()
    repository.save_original_job.return_value = 42

    job_text = "Original job text\nwith exact formatting.\n"

    job_id = _store_original_job(
        repository=repository,
        job_text=job_text,
        source="url",
        source_url="https://example.com/jobs/42",
    )

    assert job_id == 42

    repository.save_original_job.assert_called_once_with(
        original_description=job_text,
        source="url",
        source_url="https://example.com/jobs/42",
    )

    captured = capsys.readouterr()

    assert "Stored original job as database ID 42" in captured.out

def test_original_job_is_stored_before_parsing() -> None:
    events = []

    repository = Mock()

    def save_job(**kwargs):
        events.append("stored")
        return 7

    def parse_job(**kwargs):
        events.append("parsed")
        return Mock()

    repository.save_original_job.side_effect = save_job

    job_text = "Complete original description"

    job_id = repository.save_original_job(
        original_description=job_text,
        source="manual",
        source_url=None,
    )

    parsed_job = parse_job(
        job_text=job_text,
        source_file="manual_job.txt",
    )

    assert job_id == 7
    assert parsed_job is not None
    assert events == ["stored", "parsed"]


def test_update_parsed_job(repository) -> None:
    description = "Original job description."

    job_id = repository.save_original_job(
        original_description=description,
        source="manual",
    )

    job_opening = JobOpening(
        source_file="sample.txt",
        title="Senior SDET",
        company="Applied Systems",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=[],
        preferred_skills=[],
        responsibilities=[],
        salary_range=None,
        notes=[],
        parser_metadata={},
    )

    repository.update_parsed_job(
        job_id=job_id,
        job_opening=job_opening,
    )

    stored = repository.get_job(job_id)

    assert stored["title"] == "Senior SDET"
    assert stored["company"] == "Applied Systems"
    assert stored["location"] == "Remote"

def test_update_parsed_job_rejects_unknown_job(
    tmp_path,
) -> None:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)

    repository = SQLiteJobRepository(database_path)

    job_opening = JobOpening(
        source_file="sample.txt",
        title="Senior SDET",
        company="Applied Systems",
        location="Remote",
        remote_status="remote",
        employment_type="full-time",
        security_clearance_required=False,
        security_clearance_level=None,
        required_skills=[],
        preferred_skills=[],
        responsibilities=[],
        salary_range=None,
        notes=[],
        parser_metadata={},
    )

    with pytest.raises(
        ValueError,
        match="Job ID does not exist: 999999",
    ):
        repository.update_parsed_job(
            job_id=999999,
            job_opening=job_opening,
        )