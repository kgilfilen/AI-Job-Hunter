"""SQLite repository for application-history events."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from src.database.database import DATABASE_PATH, get_connection
from src.models.application_event import ApplicationEvent


PathLike = Union[str, Path]


def _validate_application_id(application_id: int) -> None:
    """Validate a persisted application identifier."""
    if application_id <= 0:
        raise ValueError(
            "application_id must be greater than zero"
        )


class SQLiteApplicationEventRepository:
    """Store and retrieve historical events for applications."""

    def __init__(
        self,
        database_path: PathLike = DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

    def create_event(
        self,
        application_id: int,
        event_type: str,
        *,
        occurred_at: Optional[str] = None,
        notes: Optional[str] = None,    ) -> ApplicationEvent:
        """Record an event for an application."""

        _validate_application_id(application_id)

        event_type = event_type.strip()

        if not event_type:
            raise ValueError("event_type must not be empty")

        timestamp = datetime.now(timezone.utc).isoformat()

        if occurred_at is None:
            occurred_at = timestamp

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO application_events (
                    application_id,
                    event_type,
                    occurred_at,
                    notes,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    application_id,
                    event_type,
                    occurred_at,
                    notes,
                    timestamp,
                ),
            )

            event_id = cursor.lastrowid

        if event_id is None:
            raise RuntimeError(
                "SQLite did not return an ID for the application event"
            )

        return ApplicationEvent(
            id=event_id,
            application_id=application_id,
            event_type=event_type,
            occurred_at=occurred_at,
            notes=notes,
            created_at=timestamp,
        )

    def list_events(
        self,
        application_id: int,
    ) -> list[ApplicationEvent]:
        """Return application events in chronological order."""

        _validate_application_id(application_id)

        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    application_id,
                    event_type,
                    occurred_at,
                    notes,
                    created_at
                FROM application_events
                WHERE application_id = ?
                ORDER BY occurred_at ASC, id ASC
                """,
                (application_id,),
            ).fetchall()

        return [
            self._row_to_event(row)
            for row in rows
        ]

    def list_events_between(
        self,
        start_at: str,
        end_at: str,
    ) -> list[ApplicationEvent]:
        """Return events occurring within a half-open time range."""

        rows = []

        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    application_id,
                    event_type,
                    occurred_at,
                    notes,
                    created_at
                FROM application_events
                WHERE occurred_at >= ?
                  AND occurred_at < ?
                ORDER BY occurred_at ASC, id ASC
                """,
                (
                    start_at,
                    end_at,
                ),
            ).fetchall()

        return [
            self._row_to_event(row)
            for row in rows
        ]

    @staticmethod
    def _row_to_event(row) -> ApplicationEvent:
        """Convert a SQLite row into an ApplicationEvent."""

        return ApplicationEvent(
            id=int(row["id"]),
            application_id=int(row["application_id"]),
            event_type=row["event_type"],
            occurred_at=row["occurred_at"],
            notes=row["notes"],
            created_at=row["created_at"],
        )