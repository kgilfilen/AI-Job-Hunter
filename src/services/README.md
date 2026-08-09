# Services

The `services` package coordinates higher-level application workflows.

Unlike the model, parser, scoring, and resume packages, services are responsible for connecting multiple components into complete operations. They provide the orchestration layer between input acquisition, persistence, parsing, analysis, recommendation generation, artifact creation, and profile management.

## Files

### `job_service.py`

Defines `JobService`, the primary orchestration service for acquiring and analyzing jobs.

It coordinates:

- web job acquisition
- parser-input formatting
- duplicate detection and persistence
- job parsing
- deterministic fit scoring
- resume recommendations
- tailored resume formatting
- analysis artifact generation

It also defines `JobAnalysisResult`, which packages the results and output paths from a complete analysis workflow.

### `profile_service.py`

Defines `ProfileService`, which manages loading, validating, modifying, backing up, and saving the candidate profile.

It provides a controlled boundary around profile persistence rather than requiring callers to manipulate the profile JSON directly.

## Job Analysis Workflow

`JobService` supports both URL-based and already-acquired job text.

The high-level flow is:

```text
Job URL or job text
        |
        v
   JobService
        |
        +--> acquire / validate input
        |
        +--> save original job
        |
        +--> duplicate check
        |
        +--> parse JobOpening
        |
        +--> persist parsed job
        |
        +--> score candidate fit
        |
        +--> persist fit analysis
        |
        +--> recommend resume changes
        |
        +--> format tailored resume
        |
        +--> save analysis artifacts
        |
        v
 JobAnalysisResult
```

This makes `JobService` the application-level coordinator for the job-analysis pipeline.

## `JobAnalysisResult`

`JobAnalysisResult` represents the outcome of one complete job-analysis request.

It contains:

- job ID
- artifact directory
- whether processing was skipped
- parsed `JobOpening`
- `FitAnalysis`
- `ResumeRecommendation`
- job-opening artifact path
- fit-analysis artifact path
- recommendation artifact path
- tailored-resume artifact path

When an already-stored job is detected and reprocessing was not requested, `skipped` is `True` and the analysis objects may be absent.

## URL Analysis

`JobService.analyze_url()` handles jobs supplied as URLs.

It:

1. validates that the URL is not empty,
2. fetches the job page,
3. verifies that visible job text was retrieved,
4. builds parser-ready input from the fetched page,
5. selects the canonical URL when available,
6. delegates the rest of the workflow to `analyze()`.

This keeps web acquisition separate from the main analysis pipeline while still presenting one service-level operation to callers.

## Text Analysis

`JobService.analyze()` accepts:

- source name
- original job text
- parser-ready text
- candidate profile
- source type
- optional source URL
- optional `reprocess` flag

The method validates both original and parser-ready text before continuing.

It then delegates storage and parsing to `_process_job_text()`.

If the job is not skipped, the service continues through scoring, persistence, resume recommendation, resume formatting, and artifact generation.

## Original Text vs. Parser Text

The service deliberately keeps two versions of job input:

```text
original_text
parser_text
```

`original_text` preserves the acquired source material.

`parser_text` is the version prepared for structured parsing.

This allows formatting or metadata enrichment for parser input without losing the original job description.

## Duplicate Handling

`_process_job_text()` first calls the repository to save the original job.

The repository result indicates whether the job was newly created.

If the job already exists and:

```text
reprocess = False
```

the service returns the existing job ID and artifact directory without repeating parsing and analysis.

If reprocessing is requested, the workflow continues.

This prevents unnecessary repeated AI parsing and duplicate artifacts during normal operation.

## Persistence Boundary

`JobService` uses `SQLiteJobRepository` rather than writing SQL directly.

The service currently persists:

- original job data
- parsed job information
- fit-analysis results

Database details remain the responsibility of the repository layer.

## Analysis and Resume Integration

After parsing, `JobService` calls the deterministic scorer:

```python
score_job(job_opening, profile)
```

It then generates resume-tailoring recommendations with:

```python
recommend_resume_changes(...)
```

Finally, `ResumeFormatter` combines the candidate, job, fit analysis, and recommendations into tailored resume text.

The service therefore coordinates these components without moving their domain logic into the service itself.

## Artifact Generation

For a successfully processed job, the service writes artifacts for:

- original job text
- parsed job opening
- fit analysis
- resume recommendation
- tailored resume

Artifact paths are returned in `JobAnalysisResult`.

This creates a durable, inspectable record of each stage of analysis.

## Profile Management

`ProfileService` provides the application-level interface for candidate-profile persistence.

### Loading

`load()` delegates JSON loading and nested dataclass construction to `load_candidate_profile()`.

### Validation

`validate()` currently verifies that the supplied object is a `CandidateProfile`.

The validation boundary exists even though current validation is intentionally minimal, allowing stronger profile rules to be added later without changing callers.

### Saving

`save()`:

1. validates the profile,
2. creates the destination directory if needed,
3. backs up an existing profile,
4. converts the dataclass structure to a dictionary,
5. writes formatted JSON to a temporary file,
6. atomically replaces the destination file.

Using a temporary file reduces the risk of leaving a partially written candidate profile if persistence is interrupted.

## Profile History

Before overwriting an existing profile, `ProfileService` creates a timestamped backup.

Backups are stored under:

```text
profile_history/
```

The timestamp uses UTC and is incorporated into the backup filename.

This preserves earlier candidate-profile states as the profile evolves.

## Skill Updates

`ProfileService` currently provides two convenience operations.

### `add_skill()`

- trims surrounding whitespace
- rejects an empty skill
- avoids exact duplicates
- adds the skill to `core_skills`

### `remove_skill()`

- trims surrounding whitespace
- removes exact matching entries from `core_skills`

These methods modify and return the supplied `CandidateProfile`.

Skill comparison here is currently case-sensitive after whitespace trimming.

## Architectural Role

The service layer answers questions such as:

> What sequence of components must run to analyze this job?

and:

> How should a profile be safely loaded, modified, and persisted?

It should not absorb the implementation details of those components.

For example:

```text
fetcher      -> retrieves job content
formatter    -> prepares or renders data
parser       -> extracts structured job facts
repository   -> persists data
scorer       -> calculates candidate fit
resume       -> recommends truthful resume emphasis
artifacts    -> writes analysis outputs
service      -> coordinates the workflow
```

This separation keeps orchestration visible without concentrating all application logic into one module.

## Current Limitations

The current service layer has several visible areas for future development:

- `ProfileService.validate()` currently performs type validation only.
- Profile skill add/remove operations use exact case-sensitive matching.
- Job-analysis steps execute sequentially.
- Failure handling is largely delegated to the underlying components.
- There is no transaction spanning the complete job-analysis workflow.
- A failure after some persistence or artifact operations may leave a partially completed analysis.
- `JobAnalysisResult` is a regular class rather than a dataclass.
- Application tracking and application-event history are not currently coordinated by these services.

The last point is relevant to a future daily activity view: recording actions such as applying, interviewing, following up, or withdrawing would naturally fit behind a service boundary rather than requiring the UI or CLI to update database records directly.
