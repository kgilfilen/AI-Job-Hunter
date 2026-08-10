"""Service for application tracking and activity history."""

from datetime import date, datetime, time, timedelta, timezone, tzinfo
from typing import Optional

from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)
from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.models.application import Application
from src.models.application_status import ApplicationStatus
from src.constants import ApplicationEventType
from src.models.application_event import ApplicationEvent

class ApplicationService:
    """Coordinate application state and application history."""

    def __init__(
        self,
        application_repository: SQLiteApplicationRepository,
        event_repository: SQLiteApplicationEventRepository,
    ) -> None:
        self.application_repository = application_repository
        self.event_repository = event_repository

    def mark_applied(
        self,
        application_id: int,
        *,
        applied_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Mark an application as submitted and record the event."""

        if applied_at is None:
            applied_at = datetime.now(timezone.utc).isoformat()

        application = self.application_repository.update_application(
            application_id,
            status=ApplicationStatus.APPLIED,
            applied_at=applied_at,
        )

        self.event_repository.create_event(
            application_id,
            ApplicationEventType.APPLICATION_SUBMITTED.value,
            occurred_at=applied_at,
            notes=notes,
        )

        return application

    def record_activity(
        self,
        application_id: int,
        event_type: ApplicationEventType,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> ApplicationEvent:
        """Record an application activity that does not change current state."""

        if occurred_at is None:
            occurred_at = datetime.now(timezone.utc).isoformat()

        return self.event_repository.create_event(
            application_id,
            event_type.value,
            occurred_at=occurred_at,
            notes=notes,
        )

    def get_activity_for_date(
        self,
        activity_date: date,
        *,
        timezone_info: tzinfo = timezone.utc,
    ) -> list[ApplicationEvent]:
        """Return application activity for one calendar date."""

        start_local = datetime.combine(
            activity_date,
            time.min,
            tzinfo=timezone_info,
        )

        end_local = start_local + timedelta(days=1)

        start_at = start_local.astimezone(
            timezone.utc
        ).isoformat()

        end_at = end_local.astimezone(
            timezone.utc
        ).isoformat()

        return self.event_repository.list_events_between(
            start_at,
            end_at,
        )