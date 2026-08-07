"""Unit tests for SQLiteJobRepository."""
import pytest

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

    result = repository.save_original_job(
        original_description=description,
        source="manual",
        source_url=None,
    )
    job_id = result.job_id

    assert result.created is True

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

    
def test_update_parsed_job(repository) -> None:
    description = "Original job description."

    result = repository.save_original_job(
        original_description=description,
        source="manual",
    )
    job_id = result.job_id

    assert result.created is True

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

def test_same_source_url_returns_existing_job(
    repository,
) -> None:
    first = repository.save_original_job(
        original_description="First description",
        source="url",
        source_url="https://example.com/jobs/123",
    )

    second = repository.save_original_job(
        original_description="Updated or different page text",
        source="url",
        source_url="https://example.com/jobs/123",
    )

    assert first.created is True
    assert second.created is False
    assert second.job_id == first.job_id
    assert second.duplicate_reason == "source_url"

def test_same_description_hash_returns_existing_job(
    repository,
) -> None:
    description = "Identical complete job description."

    first = repository.save_original_job(
        original_description=description,
        source="url",
        source_url="https://example.com/jobs/one",
    )

    second = repository.save_original_job(
        original_description=description,
        source="url",
        source_url="https://another.example/jobs/two",
    )

    assert first.created is True
    assert second.created is False
    assert second.job_id == first.job_id
    assert second.duplicate_reason == "description_hash"

def test_different_descriptions_create_different_jobs(
    repository,
) -> None:
    first = repository.save_original_job(
        original_description="First job description.",
        source="manual",
    )

    second = repository.save_original_job(
        original_description="Second job description.",
        source="manual",
    )

    assert first.created is True
    assert second.created is True
    assert second.job_id != first.job_id

def test_blank_source_url_is_stored_as_none(
    repository,
) -> None:
    result = repository.save_original_job(
        original_description="A unique job description.",
        source="manual",
        source_url="   ",
    )

    stored = repository.get_job(result.job_id)

    assert stored is not None
    assert stored["source_url"] is None

