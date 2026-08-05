"""SQLite database configuration and initialization."""

from pathlib import Path
import sqlite3
from typing import Union


DATABASE_PATH = Path("data/ai_career_manager.db")

PathLike = Union[str, Path]


JOBS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    source TEXT,
    source_url TEXT,

    description_hash TEXT NOT NULL,
    original_description TEXT NOT NULL,

    title TEXT,
    company TEXT,
    location TEXT,

    fit_score INTEGER,
    recommendation TEXT,

    status TEXT NOT NULL DEFAULT 'NEW',

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
"""

JOBS_SOURCE_URL_INDEX = """
CREATE INDEX IF NOT EXISTS idx_jobs_source_url
ON jobs (source_url)
"""

JOBS_DESCRIPTION_HASH_INDEX = """
CREATE INDEX IF NOT EXISTS idx_jobs_description_hash
ON jobs (description_hash)
"""


def get_connection(
    database_path: PathLike = DATABASE_PATH,
) -> sqlite3.Connection:
    """Return a connection to the configured SQLite database."""

    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database(
    database_path: PathLike = DATABASE_PATH,
) -> None:
    """Create database tables when they do not already exist."""

    with get_connection(database_path) as connection:
        connection.execute(JOBS_TABLE_SCHEMA)
        connection.execute(JOBS_SOURCE_URL_INDEX)
        connection.execute(JOBS_DESCRIPTION_HASH_INDEX)