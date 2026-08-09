"""Tests for SQLite application-tracking persistence."""

import sqlite3

import pytest

from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository
from src.models.application_status import ApplicationStatus


@pytest.fixture
def database_path(tmp_path):
    """Return an initialized temporary database path."""

    path = tmp_path / "test.db"

    initialize_database(path)

    return path


@pytest.fixture
def job_id(database_path):
    """Create and return a persisted job ID."""

    repository = SQLiteJobRepository(database_path)

    result = repository.save_original_job(
        original_description="Example job description",
        source="test",
        source_url="https://example.com/jobs/1",
    )

    return result.job_id


@pytest.fixture
def repository(database_path):
    """Return an application repository using the temporary database."""

    return SQLiteApplicationRepository(database_path)


def test_create_application_defaults_to_interested(
    repository,
    job_id,
):
    application = repository.create_application(job_id)

    assert application.id > 0
    assert application.job_id == job_id
    assert application.status == ApplicationStatus.INTERESTED
    assert application.applied_at is None
    assert application.next_action is None
    assert application.follow_up_at is None
    assert application.notes is None
    assert application.created_at is not None
    assert application.updated_at is not None


def test_create_application_with_explicit_status(
    repository,
    job_id,
):
    application = repository.create_application(
        job_id,
        status=ApplicationStatus.APPLIED,
    )

    assert application.status == ApplicationStatus.APPLIED


def test_get_application_returns_saved_application(
    repository,
    job_id,
):
    created = repository.create_application(job_id)

    retrieved = repository.get_application(created.id)

    assert retrieved == created


def test_get_application_returns_none_when_missing(
    repository,
):
    assert repository.get_application(999) is None


def test_get_by_job_id_returns_application(
    repository,
    job_id,
):
    created = repository.create_application(job_id)

    retrieved = repository.get_by_job_id(job_id)

    assert retrieved == created


def test_get_by_job_id_returns_none_without_application(
    repository,
    job_id,
):
    assert repository.get_by_job_id(job_id) is None


def test_only_one_application_allowed_per_job(
    repository,
    job_id,
):
    repository.create_application(job_id)

    with pytest.raises(sqlite3.IntegrityError):
        repository.create_application(job_id)


def test_application_requires_existing_job(
    repository,
):
    with pytest.raises(sqlite3.IntegrityError):
        repository.create_application(999)


def test_update_application_updates_selected_fields(
    repository,
    job_id,
):
    application = repository.create_application(job_id)

    updated = repository.update_application(
        application.id,
        status=ApplicationStatus.APPLIED,
        applied_at="2026-08-08T20:00:00+00:00",
        next_action="Follow up with recruiter",
        follow_up_at="2026-08-15T15:00:00+00:00",
        notes="Applied through company website.",
    )

    assert updated.status == ApplicationStatus.APPLIED
    assert updated.applied_at == "2026-08-08T20:00:00+00:00"
    assert updated.next_action == "Follow up with recruiter"
    assert updated.follow_up_at == "2026-08-15T15:00:00+00:00"
    assert updated.notes == "Applied through company website."


def test_partial_update_preserves_other_fields(
    repository,
    job_id,
):
    application = repository.create_application(job_id)

    populated = repository.update_application(
        application.id,
        status=ApplicationStatus.APPLIED,
        applied_at="2026-08-08T20:00:00+00:00",
        next_action="Send follow-up email",
        follow_up_at="2026-08-15T15:00:00+00:00",
        notes="Initial application submitted.",
    )

    updated = repository.update_application(
        populated.id,
        next_action="Prepare for recruiter call",
    )

    assert updated.status == ApplicationStatus.APPLIED
    assert updated.applied_at == "2026-08-08T20:00:00+00:00"
    assert updated.next_action == "Prepare for recruiter call"
    assert updated.follow_up_at == "2026-08-15T15:00:00+00:00"
    assert updated.notes == "Initial application submitted."


def test_update_can_explicitly_clear_optional_field(
    repository,
    job_id,
):
    application = repository.create_application(job_id)

    populated = repository.update_application(
        application.id,
        notes="Temporary note",
    )

    assert populated.notes == "Temporary note"

    cleared = repository.update_application(
        application.id,
        notes=None,
    )

    assert cleared.notes is None


def test_update_missing_application_raises_value_error(
    repository,
):
    with pytest.raises(
        ValueError,
        match="Application ID does not exist",
    ):
        repository.update_application(
            999,
            status=ApplicationStatus.APPLIED,
        )


@pytest.mark.parametrize(
    "application_id",
    [
        0,
        -1,
    ],
)
def test_invalid_application_id_rejected(
    repository,
    application_id,
):
    with pytest.raises(
        ValueError,
        match="application_id must be greater than zero",
    ):
        repository.get_application(application_id)


@pytest.mark.parametrize(
    "job_id",
    [
        0,
        -1,
    ],
)
def test_invalid_job_id_rejected(
    repository,
    job_id,
):
    with pytest.raises(
        ValueError,
        match="job_id must be greater than zero",
    ):
        repository.create_application(job_id)