"""Tests for SQLite application-event persistence."""

import sqlite3

import pytest

from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)
from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository


@pytest.fixture
def database_path(tmp_path):
    """Return an initialized temporary database path."""

    path = tmp_path / "test.db"
    initialize_database(path)

    return path


@pytest.fixture
def application_id(database_path):
    """Create and return a persisted application ID."""

    job_repository = SQLiteJobRepository(database_path)

    job_result = job_repository.save_original_job(
        original_description="Example job description",
        source="test",
        source_url="https://example.com/jobs/1",
    )

    application_repository = SQLiteApplicationRepository(
        database_path
    )

    application = application_repository.create_application(
        job_result.job_id
    )

    return application.id


@pytest.fixture
def repository(database_path):
    """Return an application-event repository."""

    return SQLiteApplicationEventRepository(database_path)


def test_create_event(
    repository,
    application_id,
):
    event = repository.create_event(
        application_id,
        "APPLICATION_SUBMITTED",
        occurred_at="2026-08-10T15:00:00+00:00",
        notes="Applied through company website.",
    )

    assert event.id > 0
    assert event.application_id == application_id
    assert event.event_type == "APPLICATION_SUBMITTED"
    assert event.occurred_at == "2026-08-10T15:00:00+00:00"
    assert event.notes == "Applied through company website."
    assert event.created_at is not None


def test_create_event_defaults_occurred_at(
    repository,
    application_id,
):
    event = repository.create_event(
        application_id,
        "RECRUITER_CONTACT",
    )

    assert event.occurred_at is not None
    assert event.created_at is not None


def test_list_events_returns_application_history(
    repository,
    application_id,
):
    first = repository.create_event(
        application_id,
        "APPLICATION_SUBMITTED",
        occurred_at="2026-08-10T15:00:00+00:00",
    )

    second = repository.create_event(
        application_id,
        "FOLLOW_UP_SENT",
        occurred_at="2026-08-11T15:00:00+00:00",
    )

    events = repository.list_events(application_id)

    assert events == [first, second]


def test_list_events_returns_empty_list(
    repository,
    application_id,
):
    events = repository.list_events(application_id)

    assert events == []


def test_events_are_ordered_by_occurred_at(
    repository,
    application_id,
):
    later = repository.create_event(
        application_id,
        "FOLLOW_UP_SENT",
        occurred_at="2026-08-12T15:00:00+00:00",
    )

    earlier = repository.create_event(
        application_id,
        "APPLICATION_SUBMITTED",
        occurred_at="2026-08-10T15:00:00+00:00",
    )

    events = repository.list_events(application_id)

    assert events == [earlier, later]


def test_event_requires_existing_application(
    repository,
):
    with pytest.raises(sqlite3.IntegrityError):
        repository.create_event(
            999,
            "APPLICATION_SUBMITTED",
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
        repository.list_events(application_id)


@pytest.mark.parametrize(
    "event_type",
    [
        "",
        "   ",
    ],
)
def test_empty_event_type_rejected(
    repository,
    application_id,
    event_type,
):
    with pytest.raises(
        ValueError,
        match="event_type must not be empty",
    ):
        repository.create_event(
            application_id,
            event_type,
        )

def test_list_events_between_returns_events_in_range(
    repository,
    application_id,
):
    repository.create_event(
        application_id,
        "Application submitted",
        occurred_at="2026-08-10T10:00:00+00:00",
    )

    repository.create_event(
        application_id,
        "Follow-up sent",
        occurred_at="2026-08-10T15:00:00+00:00",
    )

    events = repository.list_events_between(
        "2026-08-10T00:00:00+00:00",
        "2026-08-11T00:00:00+00:00",
    )

    assert len(events) == 2


def test_list_events_between_excludes_events_outside_range(
    repository,
    application_id,
):
    repository.create_event(
        application_id,
        "Earlier event",
        occurred_at="2026-08-09T23:59:59+00:00",
    )

    repository.create_event(
        application_id,
        "Inside range",
        occurred_at="2026-08-10T12:00:00+00:00",
    )

    repository.create_event(
        application_id,
        "Later event",
        occurred_at="2026-08-11T00:00:00+00:00",
    )

    events = repository.list_events_between(
        "2026-08-10T00:00:00+00:00",
        "2026-08-11T00:00:00+00:00",
    )

    assert len(events) == 1
    assert events[0].event_type == "Inside range"


def test_list_events_between_orders_events_chronologically(
    repository,
    application_id,
):
    later = repository.create_event(
        application_id,
        "Later event",
        occurred_at="2026-08-10T18:00:00+00:00",
    )

    earlier = repository.create_event(
        application_id,
        "Earlier event",
        occurred_at="2026-08-10T09:00:00+00:00",
    )

    events = repository.list_events_between(
        "2026-08-10T00:00:00+00:00",
        "2026-08-11T00:00:00+00:00",
    )

    assert events == [earlier, later]