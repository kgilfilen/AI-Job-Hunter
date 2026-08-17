# AI Career Manager — Shelf-Safe State

## Purpose of This Document

This document is the restart point for future development of AI Career Manager.

It is intentionally written so that development can stop for months or years
and later resume without depending on memory of the previous development cycle.

If returning to this project after a long absence, start here before changing
code.

---

# Current State

## Branch

Current development branch:

`milestone-5`

At the time of shelf-safe preparation, this branch was synchronized with its
remote branch before the final closeout changes were committed.

## Known-Good Test Baseline

Python/backend:

`171 passed`

Frontend:

`11 passed`

Frontend test command:

```bash
cd frontend
npx vitest run
```

Backend test command:

```bash
pytest
```

Both suites were completely green immediately before shelf-safe closeout.

---

# Current Deployment Status

The application is currently known-good for local development/use.

It has NOT yet been publicly deployed.

Local architecture:

```text
Browser
  ↓
Vite / React frontend
localhost:5173
  ↓
HTTP requests
  ↓
Uvicorn / FastAPI backend
127.0.0.1:8000
  ↓
Python services
  ↓
repositories
  ↓
SQLite
```

Public deployment remains a closeout/future task.

Do not assume that localhost URLs are suitable for production deployment.

---

# Starting the Product Locally

From the repository root, start the backend:

```bash
python3 -m uvicorn src.api.main:app --reload
```

Leave this terminal running.

In another terminal:

```bash
cd frontend
npm run dev
```

Vite should provide a URL similar to:

```text
http://localhost:5173/
```

Open that URL in a browser.

The FastAPI Swagger interface should be available at:

```text
http://127.0.0.1:8000/docs
```

---

# Known-Good Manual Smoke Test

The following workflow was manually verified immediately before shelf-safe
closeout:

1. Start Uvicorn.
2. Start the Vite frontend.
3. Open a fresh browser session at `http://localhost:5173/`.
4. Confirm real application data loads.
5. Select an application.
6. Confirm Application Details appear.
7. Confirm Activity History loads for the selected application.
8. Enter a status note.
9. Mark an application Withdrawn.
10. Confirm the application status updates immediately without browser refresh.
11. Confirm the new Withdrawn event appears immediately in Activity History.

This complete read/write path was verified against the real local database.

---

# Major Architecture

The application currently contains two separate web servers during development.

## Frontend

React + TypeScript, served by Vite.

Responsibilities include:

- rendering the browser UI;
- application state;
- forms and interaction;
- calling backend APIs;
- refreshing UI state after mutations.

Important frontend directory:

```text
frontend/src/
```

Important components currently include:

```text
components/
  NeedsAttention.tsx
  RecentActivity.tsx
  RecordActivity.tsx
  ApplicationList.tsx
```

`App.tsx` primarily coordinates application state and API calls.

## Backend

FastAPI application served by Uvicorn.

Important backend layers:

```text
FastAPI API
    ↓
services
    ↓
repositories
    ↓
SQLite
```

Business behavior should generally remain in services rather than being
duplicated in FastAPI routes or React.

---

# Working Application Management Features

The React frontend currently supports:

- Needs Attention display;
- Recent Activity display;
- recording application activity;
- tracked application list;
- selecting an application;
- application details;
- per-application activity history;
- lifecycle notes;
- Mark Rejected;
- Mark Withdrawn;
- Mark Closed;
- immediate frontend refresh after application mutations.

Application lifecycle operations update both current application status and
application-event history through the service layer.

---

# Career Profile Work Completed

Milestone 5 introduced the beginning of multi-career support.

The original `CandidateProfile` represented both:

- the person/shared evidence; and
- one career direction.

The model now also supports:

```python
CareerProfile
```

and:

```python
CandidateProfile.career_profiles
```

The current migration is intentionally backward-compatible.

Legacy single-profile fields still exist while the new structure is introduced.

Do NOT remove those legacy fields without tracing all remaining callers and
tests.

---

# Career Profile Loading

`profile_loader.py` now converts nested career-profile JSON objects into actual
`CareerProfile` dataclass instances.

This behavior is tested.

The current candidate JSON contains a first career profile:

```text
Software / QA
```

The loader supports multiple profiles.

---

# Career Profile Selection

`CandidateProfile` provides a lookup method similar to:

```python
get_career_profile(name)
```

Behavior:

- matching name → returns the corresponding `CareerProfile`;
- unknown name → returns `None`.

Both success and missing-profile behavior are tested.

---

# Career-Aware Scoring

`score_job()` now accepts an optional selected `CareerProfile`.

When a career profile is supplied, career-specific information comes from that
profile, including:

- target titles;
- core skills;
- remote preference.

Shared facts such as security-clearance status remain on `CandidateProfile`.

When no career profile is supplied, legacy behavior continues to work.

A test proves that the SAME candidate and SAME job can receive different fit
results when analyzed using different career profiles.

This is intentional and is a core Milestone 5 architectural change.

---

# Career-Aware Resume Recommendations

`recommend_resume_changes()` now also accepts the same optional selected
`CareerProfile`.

Career-specific skills are taken from the selected career profile when one is
provided.

Shared candidate facts remain sourced from `CandidateProfile`.

This keeps fit scoring and resume recommendations aligned to the same career
context.

---

# Production Career Profile Flow

The CLI now supports an optional argument:

```text
--career-profile "Software / QA"
```

The production path is:

```text
CLI
  ↓
load CandidateProfile
  ↓
get_career_profile(name)
  ↓
JobService.analyze(...)
  ↓
score_job(..., career_profile)
  ↓
recommend_resume_changes(..., career_profile)
```

If the requested profile does not exist, the application raises a clear
`ValueError`.

The valid-selection and invalid-selection orchestration paths are tested in
`test_main.py`.

Calling the workflow without `--career-profile` preserves legacy behavior.

---

# Important Design Decisions

## Shared candidate truth vs career-specific representation

The candidate's underlying evidence must remain truthful and shared.

Career profiles select and emphasize relevant evidence; they must not create
fictional versions of the candidate.

Conceptually:

```text
Candidate
├── identity
├── experience
├── education
├── certifications
├── shared facts
└── career profiles
    ├── Software / QA
    ├── ...
    └── ...
```

## Backward-compatible migration

The old single-profile representation has NOT been aggressively removed.

New capabilities were added first.

This was intentional so existing analysis workflows would continue working
during migration.

## Data down / events up in React

Frontend component design currently follows a simple React principle:

```text
data goes down
events go up
```

`App.tsx` owns major state/API behavior while child components primarily render
UI and send user actions back through callbacks.

## Functionality before styling

The current React interface is intentionally functionality-first.

Do not interpret plain appearance as unfinished business logic.

Visual styling/responsive design should be treated as a separate product pass.

---

# Known Limitations

## Deployment

The product is not yet publicly deployed.

A true operational shelf-safe release should eventually include a deployed
frontend/backend and production data-storage strategy.

## UI

The frontend is currently functional rather than polished.

One observed usability issue:

Selecting an application updates Application Details below the application
list, and the changed area may be below the visible browser viewport.

A user can therefore click an application and initially think nothing happened.

Possible future improvements include:

- application-detail navigation;
- scrolling selected details into view;
- responsive layout;
- deliberate visual styling.

## Fit scoring

Current deterministic fit scoring is useful but too literal in some cases.

A preserved Milestone 6 regression example:

An Automation Test Engineer position initially scored approximately 35.

After adding skills already represented by the user's actual background, the
score rose to approximately 53.

The system still recommended `Pass`, despite human review concluding the job
was worth pursuing.

Observed problems include:

- literal skill-name matching;
- semantically related skills treated as independent;
- insufficient distinction between major domain gaps and minor tool gaps;
- downstream resume advice treating an imperfect fit score as authoritative.

Do NOT simply inflate scores.

Future scoring work should improve representation, semantic normalization, and
weighting while preserving truthful evidence.

---

# Intentionally Deferred Work

The following ideas are NOT unfinished code.

They are deferred product directions:

- deeper multi-career profile UI;
- established vs aspirational career maturity;
- career-profile market intelligence;
- semantic skill matching improvements;
- scoring calibration;
- Profile Advisor;
- richer lifecycle controls;
- final React visual design;
- responsive/mobile styling;
- public deployment:

        INTENTIONALLY DEFERRED — local operation is sufficient for current use.

- agent-assisted job-board discovery;
- saved/automated job searches.

Do not assume all of these belong in the next product cycle.

Real usage should determine priority.

---

# Shelf-Safe Rule

Before beginning another Career Manager development cycle:

Do NOT immediately start coding.

First:

1. Read this document.
2. Read `README.md`.
3. Pull the current repository.
4. Check branch/tag/known-good commit.
5. Install dependencies if needed.
6. Run:

   ```bash
   pytest
   ```

7. Confirm the known-good Python baseline or understand dependency-driven
   changes.

8. Run:

   ```bash
   cd frontend
   npx vitest run
   ```

9. Start FastAPI and React.
10. Perform the manual smoke test above.
11. Use the product on several real jobs.
12. Review accumulated bugs/ideas.
13. Define a bounded next product cycle before modifying code.

---

# Most Natural Next Development Seams

If returning with no stronger product evidence, likely candidates include:

1. finish product deployment;
2. complete explicit career-profile selection in the main user-facing UI;
3. improve career-profile representation;
4. address semantic fit-scoring weaknesses using preserved regression cases;
5. polish React UI and responsive behavior.

These are candidates, not commitments.

---

# Definition of Shelf-Safe

This project is shelf-safe when:

- all intended current-cycle code is complete;
- Python tests are green;
- frontend tests are green;
- manual smoke test passes;
- repository is clean;
- current changes are committed;
- startup/testing instructions are accurate;
- known limitations are documented;
- future work is recorded rather than half-implemented;
- deployment state is explicitly known;
- a future developer does not need the original developer's memory to resume.

The engineering target is not literally zero minutes of reorientation.

The target is:

> **No dependency on human memory.**

A future development session should be able to reconstruct the state of the
project entirely from the repository.

---

# Shelf-Safe Baseline

Date prepared: August 2026

Backend tests:

```text
171 passed
```

Frontend tests:

```text
11 passed
```

Manual browser smoke test:

```text
PASSED
```

Local read/write application workflow:

```text
PASSED
```

Public deployment:

```text
NOT YET COMPLETE
```

Shelf-safe checkpoint commit:

4ab415c
