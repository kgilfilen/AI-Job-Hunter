# Models

The `models` package defines the core data structures used by the AI Career Manager.

These classes represent the information that moves between the deterministic parts of the application—file and web input, parsing, persistence, application tracking—and the AI-assisted analysis layer. Keeping these structures explicit makes the system easier to test, validate, serialize, and extend.

## Model Overview

### `application.py`

Defines `Application`, the domain model for tracking candidate activity associated with a stored job.

It links an application record to a job by `job_id` and stores:

- application status
- applied date
- next action
- follow-up date
- notes
- created and updated timestamps

The status value is represented by `ApplicationStatus`.

---

### `application_status.py`

Defines the `ApplicationStatus` enum used by application-tracking workflows.

Current lifecycle values are:

- `INTERESTED`
- `APPLIED`
- `INTERVIEWING`
- `OFFER`
- `REJECTED`
- `WITHDRAWN`
- `CLOSED`

Using an enum keeps application states consistent across the application rather than relying on arbitrary strings.

---

### `candidate_profile.py`

Defines the candidate's professional profile and its supporting data structures.

Supporting models include:

- `Experience`
- `Education`
- `Certification`

`CandidateProfile` contains identity and contact information, target roles, skills, industries, certifications, experience, education, work preferences, clearance information, relocation preference, and notes.

This model provides the structured candidate context used when evaluating jobs and generating recommendations.

---

### `fit_analysis.py`

Defines `FitAnalysis`, the structured result of comparing a candidate with a job opening.

It contains:

- overall fit score
- recommendation
- strengths
- concerns
- notes
- matched required skills
- missing required skills
- matched preferred skills
- missing preferred skills

This separates the result of fit analysis from both the candidate and job models.

---

### `fetched_job_page.py`

Defines `FetchedJobPage`, which represents the information captured while retrieving a job posting from the web.

It stores:

- requested URL
- visible page text
- page title
- canonical URL
- general page metadata
- structured `JobMetadata`

This model preserves the boundary between raw web retrieval and later job parsing.

---

### `job_input.py`

Defines the immutable `JobInput` model used when processing one job.

It preserves both:

- `original_text` — the original job description
- `parser_text` — the text prepared for parsing

It also records the source name, source type, and optional source URL.

Keeping original and parser-ready text separate allows normalization or preprocessing without losing the source material.

---

### `job_metadata.py`

Defines `JobMetadata`, containing structured facts that can be discovered before AI parsing.

Current fields include:

- title
- company
- location
- employment type
- date posted
- valid-through date
- salary
- salary currency
- salary interval

This allows deterministic metadata extraction to supplement or reduce dependence on AI parsing.

---

### `job_opening.py`

Defines `JobOpening`, the normalized representation of a parsed job posting.

It contains:

- source file
- title
- company
- location
- remote status
- employment type
- security-clearance requirements
- required skills
- preferred skills
- responsibilities
- salary range
- notes
- parser metadata

`JobOpening` is one of the central domain models in the application. Parsers convert job-description input into this structure so later workflows can operate on consistent data.

---

### `profile_update.py`

Defines the `ProfileService` interface for candidate-profile operations.

The service currently specifies:

- `load()`
- `save()`
- `validate()`

The methods are placeholders representing the expected boundary for loading, validating, and persisting a `CandidateProfile`.

---

### `resume_recommendation.py`

Defines `ResumeRecommendation`, which represents suggested changes for tailoring a resume to a specific job.

Recommendation categories include:

- summary changes
- skills to emphasize
- experience to highlight
- keywords to add
- missing keywords
- possible concerns

The `has_recommendations` property provides a simple way to determine whether any recommendation content was generated.

## How the Models Fit Together

A typical job-processing flow looks like this:

```text
Job source
    |
    v
JobInput
    |
    +----------------------+
    |                      |
    v                      v
FetchedJobPage        JobMetadata
    |                      |
    +----------+-----------+
               |
               v
          JobOpening
               |
       +-------+-------+
       |               |
       v               v
CandidateProfile   FitAnalysis
       |               |
       +-------+-------+
               |
               v
   ResumeRecommendation

Stored Job
    |
    v
Application
    |
    v
ApplicationStatus
```

Not every workflow uses every model. For example, a local text file may produce a `JobInput` without requiring `FetchedJobPage`, while web-based input can use both the fetched-page and metadata models before producing a `JobOpening`.

## Design Principles

The model layer intentionally contains mostly simple dataclasses and enums.

Models should primarily describe data, not perform orchestration, database access, web requests, or AI calls. Those responsibilities belong in services, parsers, repositories, and workflow code.

This separation provides several benefits:

- predictable interfaces between components
- straightforward unit testing
- easier serialization and persistence
- clearer boundaries between deterministic processing and AI-assisted analysis
- simpler future extension of the application

As the AI Career Manager grows, new model fields or model classes can be added without requiring the higher-level workflow to depend directly on parser, database, or API implementation details.
