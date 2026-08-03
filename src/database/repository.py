"""SQLite repository for persisted job records."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Dict, Optional, Union

from src.database.database import DATABASE_PATH, get_connection


PathLike = Union[str, Path]


class SQLiteJobRepository:
    """Store and retrieve jobs using SQLite."""

    def __init__(
        self,
        database_path: PathLike = DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

    def save_original_job(
        self,
        original_description: str,
        source: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> int:
        """Save the original job description and return its row ID."""

        if not original_description.strip():
            raise ValueError("original_description cannot be empty")

        timestamp = datetime.now(timezone.utc).isoformat()

        description_hash = sha256(
            original_description.encode("utf-8")
        ).hexdigest()

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO jobs (
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    "NEW",
                    timestamp,
                    timestamp,
                ),
            )

            job_id = cursor.lastrowid

        if job_id is None:
            raise RuntimeError(
                "SQLite did not return an ID for the saved job"
            )

        return job_id

    def get_job(
        self,
        job_id: int,
    ) -> Optional[Dict[str, object]]:
        """Return one stored job, or None if the ID does not exist."""

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    status,
                    created_at,
                    updated_at
                FROM jobs
                WHERE id = ?
                """,
                (job_id,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)