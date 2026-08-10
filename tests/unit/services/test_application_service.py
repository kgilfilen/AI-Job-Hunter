"""Tests for application workflow orchestration."""

from datetime import date, timezone
import pytest

from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)
from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.database.database import initialize_database
from src.database.repository import SQLiteJobRepository
from src.models.application_status import ApplicationStatus
from src.services.application_service import ApplicationService
from src.constants import ApplicationEventType

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
def application_repository(database_path):
    """Return an application repository."""
    return SQLiteApplicationRepository(database_path)


@pytest.fixture
def event_repository(database_path):
    """Return an application-event repository."""
    return SQLiteApplicationEventRepository(database_path)


@pytest.fixture
def service(
    application_repository,
    event_repository,
):
    """Return an application service."""
    return ApplicationService(
        application_repository=application_repository,
        event_repository=event_repository,
    )


def test_mark_applied_updates_current_application_state(
    service,
    application_repository,
    application_id,
):
    applied_at = "2026-08-10T18:00:00+00:00"

    service.mark_applied(
        application_id,
        applied_at=applied_at,
    )

    application = application_repository.get_application(
        application_id
    )

    assert application is not None
    assert application.status == ApplicationStatus.APPLIED
    assert application.applied_at == applied_at


def test_mark_applied_records_application_event(
    service,
    event_repository,
    application_id,
):
    applied_at = "2026-08-10T18:00:00+00:00"

    service.mark_applied(
        application_id,
        applied_at=applied_at,
        notes="Applied through company website.",
    )

    events = event_repository.list_events(
        application_id
    )

    assert len(events) == 1

    event = events[0]

    assert event.event_type == "Application submitted"
    assert event.occurred_at == applied_at
    assert event.notes == "Applied through company website."

def test_record_activity_records_event(
    service,
    event_repository,
    application_id,
):
    occurred_at = "2026-08-10T19:00:00+00:00"

    service.record_activity(
        application_id,
        ApplicationEventType.RECRUITER_CONTACT,
        occurred_at=occurred_at,
        notes="Recruiter called.",
    )

    events = event_repository.list_events(application_id)

    assert len(events) == 1
    assert (
        events[0].event_type
        == ApplicationEventType.RECRUITER_CONTACT.value
    )
    assert events[0].occurred_at == occurred_at
    assert events[0].notes == "Recruiter called."

def test_get_activity_for_date(
    service,
    event_repository,
    application_id,
):
    event_repository.create_event(
        application_id,
        ApplicationEventType.APPLICATION_SUBMITTED.value,
        occurred_at="2026-08-10T10:00:00+00:00",
    )

    event_repository.create_event(
        application_id,
        ApplicationEventType.FOLLOW_UP_SENT.value,
        occurred_at="2026-08-11T10:00:00+00:00",
    )

    events = service.get_activity_for_date(
        date(2026, 8, 10),
        timezone_info=timezone.utc,
    )

    assert len(events) == 1
    assert (
        events[0].event_type
        == ApplicationEventType.APPLICATION_SUBMITTED.value
    )