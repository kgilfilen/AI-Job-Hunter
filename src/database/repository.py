"""SQLite repository for persisted job records."""

from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Dict, Optional, Union

from src.database.database import DATABASE_PATH, get_connection
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.database.save_job_result import SaveJobResult

PathLike = Union[str, Path]

def _validate_job_id(job_id: int) -> None:
    if job_id <= 0:
        raise ValueError("job_id must be greater than zero")

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
    ) -> SaveJobResult:
        """Save a job or return the existing duplicate record."""

        if not original_description.strip():
            raise ValueError("original_description cannot be empty")

        normalized_source_url = (
            source_url.strip()
            if source_url is not None and source_url.strip()
            else None
        )

        description_hash = sha256(
            original_description.encode("utf-8")
        ).hexdigest()

        if normalized_source_url is not None:
            existing_job = self.find_by_source_url(
                normalized_source_url
            )

            if existing_job is not None:
                return SaveJobResult(
                    job_id=int(existing_job["id"]),
                    created=False,
                    duplicate_reason="source_url",
                )

        existing_job = self.find_by_description_hash(
            description_hash
        )

        if existing_job is not None:
            return SaveJobResult(
                job_id=int(existing_job["id"]),
                created=False,
                duplicate_reason="description_hash",
            )

        timestamp = datetime.now(timezone.utc).isoformat()

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
                    normalized_source_url,
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

        return SaveJobResult(
            job_id=job_id,
            created=True,
        )

    def get_job(
        self,
        job_id: int,
    ) -> Optional[Dict[str, object]]:
        """Return one stored job, or None if the ID does not exist."""
        _validate_job_id(job_id)

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    title,
                    company,
                    location,
                    fit_score,
                    recommendation,
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

    def update_parsed_job(
        self,
        job_id: int,
        job_opening: JobOpening,
    ) -> None:
        """Update a stored job with parser results."""
        _validate_job_id(job_id)

        timestamp = datetime.now(timezone.utc).isoformat()

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                UPDATE jobs
                SET
                    title = ?,
                    company = ?,
                    location = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    job_opening.title,
                    job_opening.company,
                    job_opening.location,
                    timestamp,
                    job_id,
                ),
            )

        if cursor.rowcount == 0:
            raise ValueError(
                f"Job ID does not exist: {job_id}"
            )

    def update_fit_analysis(
        self,
        job_id: int,
        fit_analysis: FitAnalysis,
    ) -> None:
        """Update a stored job with fit-analysis results."""
        _validate_job_id(job_id)

        timestamp = datetime.now(timezone.utc).isoformat()

        recommendation = fit_analysis.recommendation

        if isinstance(recommendation, Enum):
            recommendation = recommendation.value

        if recommendation is not None:
            recommendation = str(recommendation)

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                UPDATE jobs
                SET
                    fit_score = ?,
                    recommendation = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    fit_analysis.overall_score,
                    recommendation,
                    timestamp,
                    job_id,
                ),
            )

        if cursor.rowcount == 0:
            raise ValueError(f"Job ID does not exist: {job_id}")


    def find_by_source_url(
        self,
        source_url: str,
    ) -> Optional[Dict[str, object]]:
        """Return the job with an exact source URL, if one exists."""

        normalized_url = source_url.strip()

        if not normalized_url:
            return None

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    title,
                    company,
                    location,
                    fit_score,
                    recommendation,
                    status,
                    created_at,
                    updated_at
                FROM jobs
                WHERE source_url = ?
                ORDER BY id
                LIMIT 1
                """,
                (normalized_url,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)


    def find_by_description_hash(
        self,
        description_hash: str,
    ) -> Optional[Dict[str, object]]:
        """Return the job with an exact description hash, if one exists."""

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    source,
                    source_url,
                    description_hash,
                    original_description,
                    title,
                    company,
                    location,
                    fit_score,
                    recommendation,
                    status,
                    created_at,
                    updated_at
                FROM jobs
                WHERE description_hash = ?
                ORDER BY id
                LIMIT 1
                """,
                (description_hash,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)