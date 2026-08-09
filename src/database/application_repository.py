"""SQLite repository for application-tracking records."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from src.database.database import (
    DATABASE_PATH,
    get_connection,
)
from src.models.application import Application
from src.models.application_status import ApplicationStatus


PathLike = Union[str, Path]

_UNSET = object()


def _validate_job_id(job_id: int) -> None:
    """Validate a persisted job identifier."""

    if job_id <= 0:
        raise ValueError("job_id must be greater than zero")


def _validate_application_id(application_id: int) -> None:
    """Validate a persisted application identifier."""

    if application_id <= 0:
        raise ValueError(
            "application_id must be greater than zero"
        )


class SQLiteApplicationRepository:
    """Store and retrieve application-tracking records using SQLite."""

    def __init__(
        self,
        database_path: PathLike = DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

    def create_application(
        self,
        job_id: int,
        status: ApplicationStatus = ApplicationStatus.INTERESTED,
    ) -> Application:
        """Create an application-tracking record for a stored job."""

        _validate_job_id(job_id)

        timestamp = datetime.now(timezone.utc).isoformat()

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO applications (
                    job_id,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    job_id,
                    status.value,
                    timestamp,
                    timestamp,
                ),
            )

            application_id = cursor.lastrowid

        if application_id is None:
            raise RuntimeError(
                "SQLite did not return an ID for the application"
            )

        application = self.get_application(application_id)

        if application is None:
            raise RuntimeError(
                "Application was created but could not be retrieved"
            )

        return application

    def get_application(
        self,
        application_id: int,
    ) -> Optional[Application]:
        """Return one application record, or None if it does not exist."""

        _validate_application_id(application_id)

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    job_id,
                    status,
                    applied_at,
                    next_action,
                    follow_up_at,
                    notes,
                    created_at,
                    updated_at
                FROM applications
                WHERE id = ?
                """,
                (application_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_application(row)

    def get_by_job_id(
        self,
        job_id: int,
    ) -> Optional[Application]:
        """Return the application record for a job, if one exists."""

        _validate_job_id(job_id)

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    job_id,
                    status,
                    applied_at,
                    next_action,
                    follow_up_at,
                    notes,
                    created_at,
                    updated_at
                FROM applications
                WHERE job_id = ?
                """,
                (job_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_application(row)

    def update_application(
        self,
        application_id: int,
        *,
        status: Optional[ApplicationStatus] = None,
        applied_at: object = _UNSET,
        next_action: object = _UNSET,
        follow_up_at: object = _UNSET,
        notes: object = _UNSET,
    ) -> Application:
        """Update selected application-tracking fields."""

        _validate_application_id(application_id)

        existing = self.get_application(application_id)

        if existing is None:
            raise ValueError(
                f"Application ID does not exist: {application_id}"
            )

        updated_status = (
            status
            if status is not None
            else existing.status
        )

        updated_applied_at = (
            existing.applied_at
            if applied_at is _UNSET
            else applied_at
        )

        updated_next_action = (
            existing.next_action
            if next_action is _UNSET
            else next_action
        )

        updated_follow_up_at = (
            existing.follow_up_at
            if follow_up_at is _UNSET
            else follow_up_at
        )

        updated_notes = (
            existing.notes
            if notes is _UNSET
            else notes
        )

        timestamp = datetime.now(timezone.utc).isoformat()

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                UPDATE applications
                SET
                    status = ?,
                    applied_at = ?,
                    next_action = ?,
                    follow_up_at = ?,
                    notes = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    updated_status.value,
                    updated_applied_at,
                    updated_next_action,
                    updated_follow_up_at,
                    updated_notes,
                    timestamp,
                    application_id,
                ),
            )

        updated = self.get_application(application_id)

        if updated is None:
            raise RuntimeError(
                "Application was updated but could not be retrieved"
            )

        return updated

    @staticmethod
    def _row_to_application(
        row,
    ) -> Application:
        """Convert a SQLite row into an Application."""

        return Application(
            id=int(row["id"]),
            job_id=int(row["job_id"]),
            status=ApplicationStatus(row["status"]),
            applied_at=row["applied_at"],
            next_action=row["next_action"],
            follow_up_at=row["follow_up_at"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )