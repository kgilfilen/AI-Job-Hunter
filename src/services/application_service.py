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
from src.database.database import get_connection

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

        with get_connection(
            self.application_repository.database_path
        ) as connection:
            application = (
                self.application_repository.update_application(
                    application_id,
                    status=ApplicationStatus.APPLIED,
                    applied_at=applied_at,
                    connection=connection,
                )
            )

            self.event_repository.create_event(
                application_id,
                ApplicationEventType.APPLICATION_SUBMITTED.value,
                occurred_at=applied_at,
                notes=notes,
                connection=connection,
            )

        return application

    def mark_interviewing(
        self,
        application_id: int,
    ) -> Application:
        """Mark an application as being in the interview process."""

        return self.application_repository.update_application(
            application_id,
            status=ApplicationStatus.INTERVIEWING,
        )


    def mark_offer(
        self,
        application_id: int,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Mark an application as having received an offer."""

        return self._update_status_with_event(
            application_id=application_id,
            status=ApplicationStatus.OFFER,
            event_type=ApplicationEventType.OFFER_RECEIVED,
            occurred_at=occurred_at,
            notes=notes,
        )


    def mark_rejected(
        self,
        application_id: int,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Mark an application as rejected."""

        return self._update_status_with_event(
            application_id=application_id,
            status=ApplicationStatus.REJECTED,
            event_type=ApplicationEventType.REJECTED,
            occurred_at=occurred_at,
            notes=notes,
        )


    def mark_withdrawn(
        self,
        application_id: int,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Mark an application as withdrawn."""

        return self._update_status_with_event(
            application_id=application_id,
            status=ApplicationStatus.WITHDRAWN,
            event_type=ApplicationEventType.WITHDRAWN,
            occurred_at=occurred_at,
            notes=notes,
        )

    def mark_closed(
        self,
        application_id: int,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Close an application that is no longer active."""

        return self._update_status_with_event(
            application_id=application_id,
            status=ApplicationStatus.CLOSED,
            event_type=ApplicationEventType.CLOSED,
            occurred_at=occurred_at,
            notes=notes,
        )

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

    def get_applications_needing_attention(
        self,
        due_at: str,
    ) -> list[Application]:
        """Return active applications with follow-ups due by the given time."""

        active_statuses = {
            ApplicationStatus.INTERESTED,
            ApplicationStatus.APPLIED,
            ApplicationStatus.INTERVIEWING,
            ApplicationStatus.OFFER,
        }

        applications = (
            self.application_repository.list_follow_ups_due(
                due_at
            )
        )

        return [
            application
            for application in applications
            if application.status in active_statuses
        ]

    def _update_status_with_event(
        self,
        application_id: int,
        status: ApplicationStatus,
        event_type: ApplicationEventType,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        """Update application state and record its history atomically."""

        if occurred_at is None:
            occurred_at = datetime.now(timezone.utc).isoformat()

        with get_connection(
            self.application_repository.database_path
        ) as connection:
            application = (
                self.application_repository.update_application(
                    application_id,
                    status=status,
                    connection=connection,
                )
            )

            self.event_repository.create_event(
                application_id,
                event_type.value,
                occurred_at=occurred_at,
                notes=notes,
                connection=connection,
            )

        return application