# Database Package

## Directory Overview

The **Database** package is responsible for persistent storage of job records
using SQLite.

It defines the database schema, establishes SQLite connections, initializes
required tables and indexes, and exposes repository operations used by higher
application layers.

The package deliberately separates:

- database configuration and schema management
- application-facing persistence operations

In architectural terms:

```text
JobService
    ↓
SQLiteJobRepository
    ↓
database.py
    ↓
SQLite
```

### Design Goals

- Preserve original job descriptions before processing.
- Provide deterministic duplicate detection.
- Keep SQL and SQLite-specific behavior outside business services.
- Maintain job analysis state across application runs.
- Allow the persistence implementation to evolve without changing callers.
- Support isolated temporary databases during testing.

### Modules

| Module | Responsibility |
|---------|----------------|
| `database.py` | Defines SQLite configuration, schema, indexes, connections, and initialization. |
| `repository.py` | Provides application-facing operations for storing, retrieving, deduplicating, and updating jobs. |
| `save_job_result.py` | Defines the result returned when storing a new or duplicate job. |

---

# database.py

## Purpose

This module defines the SQLite database configuration and initializes the
database objects required by AI Career Manager.

Its responsibilities are deliberately limited to:

- defining the default database location
- defining database schema
- defining database indexes
- creating database connections
- initializing required database objects

It does not contain job-processing, duplicate-detection, parsing, scoring, or
application workflow logic.

```text
SQLiteJobRepository
    ↓
database.py
    ↓
SQLite database
```

---

## Public Interface

This module exposes:

- `DATABASE_PATH`
- `get_connection()`
- `initialize_database()`

It also defines the SQL schema and indexes used to initialize the database.

---

## Inputs and Outputs

### `get_connection(database_path)`

- Input: optional string or `Path` identifying the SQLite database
- Default: `data/ai_career_manager.db`
- Output: configured `sqlite3.Connection`
- Side effect: creates the parent directory if necessary
- Configuration: rows are returned as `sqlite3.Row`

The `sqlite3.Row` configuration allows callers to access result columns by
column name and later convert rows into dictionaries.

---

### `initialize_database(database_path)`

- Input: optional string or `Path`
- Output: None
- Side effects:
  - creates the database file when necessary
  - creates the `jobs` table if it does not exist
  - creates the source-URL index
  - creates the description-hash index

Initialization is idempotent for the currently defined schema.

---

## Dependencies

This module depends on:

- `pathlib.Path`
- `sqlite3`
- Python path-like type definitions

It has no dependency on:

- application services
- AI
- parsers
- scoring
- candidate profiles
- Streamlit
- artifact generation

---

## Database Schema

The current `jobs` table stores:

| Column | Purpose |
|--------|---------|
| `id` | Database-generated job identifier |
| `source` | Origin of the job record |
| `source_url` | URL from which the job was obtained |
| `description_hash` | SHA-256 identity of the original description |
| `original_description` | Untouched original job text |
| `title` | Parsed job title |
| `company` | Parsed employer |
| `location` | Parsed job location |
| `fit_score` | Candidate/job fit score |
| `recommendation` | Fit recommendation |
| `status` | Current application/job state |
| `created_at` | Creation timestamp |
| `updated_at` | Most recent update timestamp |

The default status is:

```text
NEW
```

---

## Indexes

### `idx_jobs_source_url`

Indexes:

```text
jobs.source_url
```

This supports efficient duplicate lookup by source URL.

### `idx_jobs_description_hash`

Indexes:

```text
jobs.description_hash
```

This supports efficient duplicate lookup using the original job-description
hash.

These indexes improve lookup performance but are not currently defined as
unique constraints.

---

## Behavioral Specifications

- The default SQLite database is stored at `data/ai_career_manager.db`.
- Parent directories are created automatically before opening the database.
- Returned connections use `sqlite3.Row`.
- Database initialization may safely be called repeatedly.
- Initialization creates required tables and indexes when absent.
- Existing tables are not destroyed or recreated.
- SQLite transactions are managed through connection context managers.

---

## Invariants

The module guarantees:

- A configured database path can be opened without manually creating its parent directory.
- Every initialized database contains the `jobs` table.
- Required indexes exist after initialization.
- Existing job data is preserved when initialization runs again.
- Repository callers receive row objects that support named-column access.

---

## Current Database Contract

The persistence hierarchy currently consists of one primary table:

```text
SQLite Database
    ↓
jobs
```

The `jobs` table acts as the persistent identity and analysis record for each
job known to the application.

Future career-management tables may reference `jobs.id` as the persistent job
identifier.

---

## Error Behavior

There is no custom database exception translation.

SQLite and filesystem exceptions propagate naturally.

Examples include:

- filesystem permission failures
- invalid database locations
- SQLite operational errors
- malformed schema statements
- database corruption

Higher application layers are responsible for deciding how these failures are
presented to users.

---

## Good Unit-Test Targets

Essential tests include:

- `get_connection()` creates missing parent directories.
- Connections use `sqlite3.Row`.
- `initialize_database()` creates the `jobs` table.
- Required indexes are created.
- Initialization is idempotent.
- Initialization does not destroy existing records.
- A custom temporary database path works correctly.

---

## Possible Future Enhancements

Potential improvements include:

- Formal schema migrations
- Schema version tracking
- Additional career-management tables
- Foreign-key enforcement
- Database-level uniqueness constraints
- Connection configuration through application settings
- Backup and restore tooling

---

## Overall Responsibility

This module provides the low-level SQLite foundation for persistent application
data.

It defines **where the database lives and what fundamental database objects
exist**, but deliberately does not define application workflows or business
rules.

---

# repository.py

## Purpose

This module provides the application's job persistence repository.

`SQLiteJobRepository` hides SQLite implementation details from higher-level
services and exposes operations expressed in application terms.

Its responsibilities include:

- storing original job descriptions
- assigning persistent job identifiers
- detecting duplicate jobs
- retrieving stored jobs
- storing parsed job information
- storing fit-analysis results

```text
JobService
    ↓
SQLiteJobRepository
    ↓
database.py
    ↓
SQLite
```

---

## Public Interface

The principal public class is:

- `SQLiteJobRepository`

Its public operations are:

- `save_original_job()`
- `get_job()`
- `update_parsed_job()`
- `update_fit_analysis()`
- `find_by_source_url()`
- `find_by_description_hash()`

The module also contains the internal validation helper:

- `_validate_job_id()`

---

## Inputs and Outputs

### `SQLiteJobRepository(database_path)`

- Input: optional database path
- Default: application `DATABASE_PATH`
- Output: repository instance
- Side effects: none during construction

The path is retained by the repository and used when operations open database
connections.

---

### `save_original_job(original_description, source, source_url)`

- Input: untouched original job description
- Input: optional source identifier
- Input: optional source URL
- Output: `SaveJobResult`
- Side effect: may insert a new row into `jobs`

This operation also:

- normalizes blank URLs to `None`
- calculates the SHA-256 hash of the exact original description
- checks for an existing job with the same URL
- checks for an existing job with the same description hash
- assigns UTC creation and update timestamps

The original job description is persisted without modification.

---

### `get_job(job_id)`

- Input: positive job ID
- Output: dictionary containing the stored job
- Output: `None` when no matching job exists
- Side effects: none

The returned record includes both original input data and available parsed and
scored values.

---

### `update_parsed_job(job_id, job_opening)`

- Input: positive job ID
- Input: parsed `JobOpening`
- Output: None
- Side effect: updates:
  - title
  - company
  - location
  - updated timestamp

The original description and persistent identity are not replaced.

---

### `update_fit_analysis(job_id, fit_analysis)`

- Input: positive job ID
- Input: `FitAnalysis`
- Output: None
- Side effect: updates:
  - fit score
  - recommendation
  - updated timestamp

Enum recommendations are converted to their underlying value before storage.

---

### `find_by_source_url(source_url)`

- Input: source URL
- Output: matching job dictionary or `None`
- Side effects: none

Whitespace is removed from the beginning and end of the supplied URL.

A blank URL produces no match.

---

### `find_by_description_hash(description_hash)`

- Input: SHA-256 description hash
- Output: matching job dictionary or `None`
- Side effects: none

The comparison is exact.

---

## Dependencies

This module depends on:

- `datetime`
- `timezone`
- `Enum`
- `hashlib.sha256`
- `pathlib.Path`
- `database.get_connection()`
- `JobOpening`
- `FitAnalysis`
- `SaveJobResult`

It has no direct dependency on:

- Streamlit
- command-line handling
- web fetching
- AI prompting
- resume generation
- artifact generation

---

## Duplicate Detection

Duplicate detection occurs in two stages.

### Source URL Match

If a nonblank source URL is supplied, the repository first looks for an exact
matching stored URL.

```text
source URL
    ↓
existing match?
    ↓ yes
duplicate_reason = "source_url"
```

### Description Hash Match

If no URL match exists, the repository computes:

```text
SHA-256(original_description)
```

and looks for an identical hash.

```text
description
    ↓
SHA-256
    ↓
existing match?
    ↓ yes
duplicate_reason = "description_hash"
```

A job is inserted only when neither duplicate condition is found.

This allows the application to recognize both:

- repeated access to the same posting URL
- identical descriptions obtained from different URLs or sources

---

## Behavioral Specifications

- Empty original descriptions are rejected.
- Original descriptions are hashed exactly as supplied.
- Blank source URLs are stored as `None`.
- Source-URL duplicate detection occurs before description-hash detection.
- Duplicate jobs reuse the existing persistent job ID.
- Duplicate detection does not modify the existing record.
- New jobs begin with status `NEW`.
- Creation and update timestamps use timezone-aware UTC ISO-8601 values.
- Parsed job updates do not overwrite original descriptions.
- Fit-analysis updates do not overwrite parsed job fields.
- Nonexistent update targets raise an error.
- Job IDs must be positive integers.

---

## Invariants

The repository guarantees:

- Every newly created job receives a database-generated positive identifier.
- The untouched original job description remains associated with that ID.
- Every stored job has a SHA-256 description hash.
- Duplicate jobs return the existing job ID rather than creating a second logical record.
- `created_at` is established at insertion.
- `updated_at` changes when parsed or fit-analysis data is updated.
- Original job identity is preserved as analysis enriches the record.

---

## Current Persistence Lifecycle

A job record evolves incrementally:

```text
Original Job
    ↓
save_original_job()
    ↓
id
source
source_url
description_hash
original_description
status
timestamps
    ↓
update_parsed_job()
    ↓
title
company
location
    ↓
update_fit_analysis()
    ↓
fit_score
recommendation
```

The persistent record therefore grows as the job moves through the analysis
pipeline rather than being replaced at each stage.

---

## Error Behavior

The repository raises `ValueError` when:

- an original description is blank
- a job ID is zero or negative
- an update references an unknown job ID

It raises `RuntimeError` if SQLite successfully performs an insertion but does
not provide the inserted job ID.

SQLite and filesystem errors otherwise propagate naturally.

---

## Good Unit-Test Targets

Essential repository tests include:

- Saving and retrieving an original job
- Rejecting blank descriptions
- Rejecting non-positive job IDs
- Returning `None` for unknown valid IDs
- Updating parsed fields
- Rejecting parsed updates for unknown jobs
- Updating fit-analysis fields
- Rejecting fit updates for unknown jobs
- Normalizing blank URLs
- Detecting duplicate source URLs
- Detecting duplicate description hashes
- Creating separate records for different descriptions
- Preserving the original job description exactly
- Correctly storing Enum recommendations
- Updating timestamps after enrichment

Additional valuable tests include:

- URL duplicate detection takes precedence over description hash
- Unicode job descriptions produce stable hashes
- Repeated lookups do not modify records
- Custom temporary database paths work correctly

---

## Possible Future Enhancements

Potential improvements include:

- Repository methods for job history
- Job/application status transitions
- Listing and filtering jobs
- Application and interview repositories
- Typed persisted-record models instead of raw dictionaries
- Shared row-to-record conversion
- Transaction-level duplicate protection
- Database uniqueness constraints
- Pagination
- Archival
- Migration/version support

---

## Overall Responsibility

`SQLiteJobRepository` provides the persistence boundary between application
services and SQLite.

Its job is to answer questions such as:

- Has this job already been seen?
- What persistent ID represents it?
- What original description was saved?
- What parsed information has been learned?
- What fit analysis was recorded?

It deliberately does not decide:

- whether a job should be analyzed
- whether a duplicate should be reprocessed
- how a job should be scored
- what recommendation should be generated
- how results should be displayed

Those decisions belong to application services and presentation layers.

---

# save_job_result.py

## Purpose

This module defines the result returned when the repository attempts to persist
an original job.

`SaveJobResult` communicates two pieces of information to higher layers:

- which persistent job record represents the job
- whether that record was newly created or already existed

When the job already exists, the result may also explain why it was considered
a duplicate.

This provides a small, explicit contract between the repository and application
services.

```text
SQLiteJobRepository
        ↓
SaveJobResult
        ↓
JobService
```

---

## Public Interface

This module exposes one immutable dataclass:

- `SaveJobResult`

Its fields are:

- `job_id`
- `created`
- `duplicate_reason`

---

## Inputs and Outputs

### `SaveJobResult(job_id, created, duplicate_reason)`

#### `job_id`

- Type: `int`
- Purpose: identifies the persistent job record
- Expected value: positive SQLite job ID

The same field is returned whether the job was newly created or an existing
duplicate was found.

#### `created`

- Type: `bool`
- Purpose: indicates whether the repository inserted a new job record

Values:

```text
True
    A new persistent job record was created.

False
    An existing job record represents this job.
```

#### `duplicate_reason`

- Type: `Optional[str]`
- Default: `None`
- Purpose: identifies the duplicate-detection rule that matched an existing job

Current repository-generated values are:

```text
source_url
description_hash
```

For newly created jobs, the expected value is:

```text
None
```

---

## Dependencies

This module depends only on:

- `dataclasses.dataclass`
- `typing.Optional`

It has no dependency on:

- SQLite
- repositories
- services
- parsing
- scoring
- AI
- artifacts
- user interfaces

This makes the result object independent of the implementation that produces or
consumes it.

---

## Behavioral Specifications

- `SaveJobResult` is immutable.
- Every result contains a job ID.
- `created=True` represents successful creation of a new job record.
- `created=False` represents reuse of an existing job record.
- Duplicate reasons are optional.
- Repository duplicate detection currently uses `source_url` and
  `description_hash` as reason values.
- The object contains no persistence or application behavior.

---

## Invariants

The model is intended to maintain the following relationships:

```text
created = True
    →
duplicate_reason = None
```

and:

```text
created = False
    →
job_id identifies an existing record
```

When the repository knows why the record matched:

```text
created = False
    →
duplicate_reason identifies the matching rule
```

The dataclass itself does not currently enforce these relationships; they are
part of the repository/service contract.

---

## Current Result Contract

### Newly Created Job

Example:

```python
SaveJobResult(
    job_id=42,
    created=True,
)
```

represents:

```text
Job 42 was newly inserted.
```

### Duplicate by Source URL

```python
SaveJobResult(
    job_id=17,
    created=False,
    duplicate_reason="source_url",
)
```

represents:

```text
The supplied job matches existing job 17 by source URL.
```

### Duplicate by Description Hash

```python
SaveJobResult(
    job_id=17,
    created=False,
    duplicate_reason="description_hash",
)
```

represents:

```text
The supplied job matches existing job 17 by description content.
```

---

## Error Behavior

This module contains no runtime validation or custom error handling.

Python's dataclass constructor accepts any values matching normal Python calling
semantics.

Validation of job IDs and duplicate-state consistency currently belongs to the
code that constructs the object.

---

## Good Unit-Test Targets

Because this is a small immutable value object, extensive testing is not
necessary.

Useful tests include:

- Fields are assigned correctly.
- `duplicate_reason` defaults to `None`.
- Instances are immutable.
- Two instances with identical values compare equal.

The more important behavioral tests belong in `SQLiteJobRepository`, where the
conditions that produce each result are determined.

---

## Possible Future Enhancements

Potential improvements include:

- Replace `duplicate_reason` strings with an Enum.
- Validate that newly created jobs do not specify a duplicate reason.
- Validate that duplicate results contain a known reason.
- Rename or generalize the result if additional persistence outcomes are added.

An Enum could eventually make the duplicate contract more explicit:

```python
class DuplicateReason(Enum):
    SOURCE_URL = "source_url"
    DESCRIPTION_HASH = "description_hash"
```

This is not necessary while the number of duplicate reasons remains small.

---

## Overall Responsibility

`SaveJobResult` is a small immutable value object that communicates the result
of attempting to persist an original job.

It allows the repository to report persistence outcomes without forcing
application services to understand SQL or duplicate-detection implementation
details.

It deliberately contains no persistence logic, business logic, or presentation
logic.

---

# Package-Level Invariants

Across the Database package:

- SQLite implementation details remain isolated from service and UI layers.
- Original source material is preserved before analysis enrichment.
- Persistent job identity remains stable across processing stages.
- Duplicate detection is deterministic.
- Database operations do not contain presentation logic.
- Higher layers interact with persistence through repository operations rather
  than direct SQL.

---

# Architectural Boundary

The package belongs below the service layer:

```text
CLI / Streamlit
      ↓
Application Services
      ↓
Database Repository
      ↓
SQLite Configuration
      ↓
SQLite
```

Code outside the Database package should generally not need to know:

- table names
- SQL statements
- index names
- SQLite row behavior
- connection details

That separation allows the persistence implementation to evolve without
requiring corresponding changes throughout the application.