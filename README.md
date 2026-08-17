# AI Career Manager

AI Career Manager is an AI-assisted career management application for analyzing
jobs, evaluating fit, tailoring resumes, and tracking job applications over
time.

Originally started as **AI Job Hunter** in June 2026, the project evolved from
a job-analysis and resume-tailoring tool into a persistent career management
platform.

The project combines AI-assisted workflows with conventional software
engineering practices including layered architecture, persistent storage,
automated testing, explicit domain models, and human review.

---

# Current Product

The application currently supports two related workflows:

## Job Analysis

- Job description ingestion from files and URLs
- Intelligent web-page extraction
- Structured AI-assisted job parsing
- Candidate/job fit scoring
- Resume-tailoring recommendations
- Tailored resume generation
- Persistent job history
- Duplicate detection using URL and SHA-256 hashing
- Career-specific job analysis using selectable career profiles

## Application Management

- Persistent application tracking
- Application lifecycle status
- Application history/events
- Needs Attention workflow
- Recent Activity
- Manual activity recording
- Per-application activity history
- Application status notes
- Rejected, Withdrawn, and Closed lifecycle operations
- Immediate browser updates after application changes

The application has been used with real job-search and application data.

---

# Purpose

Searching for software engineering jobs involves a surprising amount of
repetitive work.

AI Career Manager reduces that work while keeping the candidate in control of
career decisions and preserving truthful candidate evidence.

The application assists with:

- Reading and structuring job descriptions
- Comparing jobs against candidate career profiles
- Identifying strong and weak job matches
- Resume tailoring
- Application tracking
- Application lifecycle management
- Preserving job-search history
- Long-term career management

AI-generated analysis is advisory rather than authoritative.

Human judgment remains part of the workflow.

---

# Architecture

The application uses a layered architecture.

```text
                         Job File / URL
                              │
                              ▼
                     Fetch / Read Input
                              │
                              ▼
                       JobInput Model
                              │
                              ▼
                     Duplicate Detection
                              │
                              ▼
                       AI Job Parser
                              │
                              ▼
                      JobOpening Model
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Career-Aware              Persistent Job
           Fit Scoring                  Storage
                 │
                 ▼
       Resume Recommendation
                 │
                 ▼
       Tailored Resume Output


                    Browser / React
                           │
                           ▼
                     FastAPI API
                           │
                           ▼
                    Service Layer
                           │
                           ▼
                    Repositories
                           │
                           ▼
                        SQLite
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
           Jobs                    Applications
                                      │
                                      ▼
                              Application Events
```

The application intentionally separates:

- User interface
- HTTP/API concerns
- Business services
- Persistence
- Domain models
- AI parsing
- Fit scoring
- Resume recommendations
- Artifact generation

Business behavior should generally live in services rather than being
duplicated in API routes or UI components.

---

# Technology Stack

Current technologies include:

- Python 3
- FastAPI
- Uvicorn
- React
- TypeScript
- Vite
- SQLite
- OpenAI API
- BeautifulSoup
- Pytest
- Vitest
- Docker
- Git

The repository also contains earlier Streamlit UI work. The current application
management interface is React + FastAPI.

---

# Career Profiles

AI Career Manager is evolving from a single-career candidate model toward a
multi-career architecture.

A candidate has shared facts and evidence such as:

- Identity
- Experience
- Education
- Certifications
- Security-clearance status

Career-specific representation can then be stored in `CareerProfile` objects,
including:

- Target titles
- Core skills
- Preferred skills
- Remote preference

Conceptually:

```text
Candidate
├── shared identity and evidence
├── experience
├── education
├── certifications
└── career profiles
    ├── Software / QA
    ├── ...
    └── ...
```

Job scoring and resume recommendations can receive an explicitly selected
career profile.

The CLI supports:

```bash
--career-profile "Software / QA"
```

The migration remains intentionally backward-compatible. Legacy single-profile
fields still exist and should not be removed without tracing their remaining
callers.

---

# Application Lifecycle

Applications maintain both:

1. current application state; and
2. historical application events.

This allows the application to answer both:

> What state is this application in now?

and:

> What happened to this application over time?

Lifecycle history can include events such as:

- Application submitted
- Follow-up sent
- Recruiter contact
- Interview scheduled
- Interview completed
- Thank-you sent
- Rejected
- Offer received
- Offer accepted
- Offer declined
- Hired
- Application closed
- Withdrawn

Application status changes and corresponding historical events are handled
through the service layer.

---

# Real-World Validation

AI Career Manager has been used throughout a real software-engineering job
search.

The application has been used to:

- Analyze real job descriptions
- Eliminate poor-fit positions
- Identify opportunities worth pursuing
- Record legitimate candidate skills and experience
- Re-analyze opportunities after profile improvements
- Track actual applications
- Record application lifecycle changes
- Preserve application history

Real usage has also exposed weaknesses in deterministic fit scoring.

For example, literal skill matching can undervalue strong opportunities when
related skills use different terminology.

Those cases are preserved as future regression examples rather than being
addressed by simply inflating scores.

---

# Testing

The project uses automated testing extensively.

Current automated coverage includes:

- Unit tests
- Integration tests
- Repository tests
- Service tests
- Parser tests
- URL fetcher tests
- Regression tests
- React component/application tests

## Known-Good Shelf-Safe Baseline

At the August 2026 shelf-safe checkpoint:

```text
Python/backend: 171 passed
Frontend:        11 passed
```

Run the complete Python suite from the repository root:

```bash
pytest
```

Run the frontend suite:

```bash
cd frontend
npx vitest run
```

The shelf-safe checkpoint also includes a successful manual browser smoke test
against real local application data.

---

# Repository Structure

```text
src/
    api/            FastAPI endpoints
    artifacts/      Artifact generation
    database/       SQLite persistence
    fetchers/       Job acquisition
    formatters/     Resume and output formatting
    models/         Domain models
    parsers/        AI parsing
    resume/         Resume recommendations
    scoring/        Candidate fit scoring
    services/       Business logic
    ui/             Earlier Streamlit interface

frontend/
    src/
        components/ React UI components

tests/
examples/
outputs/
config/
docs/
```

For the current development state and exact instructions for resuming
development after an extended break, read:

**`SHELF_SAFE.md`**

That document is the authoritative restart point for future development cycles.

---

# Running the Web Application Locally

The current application-management interface uses separate backend and frontend
development servers.

## Backend

From the repository root:

```bash
python3 -m uvicorn src.api.main:app --reload
```

FastAPI runs at:

```text
http://127.0.0.1:8000
```

Swagger/OpenAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend

In another terminal:

```bash
cd frontend
npm run dev
```

Vite normally serves the application at:

```text
http://localhost:5173/
```

Both servers must be running for the local React application to work normally.

---

# Running Job Analysis

Analyze example jobs:

```bash
python src/main.py --examples
```

Analyze a local job description:

```bash
python src/main.py --file example_job.txt
```

Analyze a job directly from a URL:

```bash
python src/main.py --url https://...
```

Analyze using a specific career profile:

```bash
python src/main.py \
    --file example_job.txt \
    --career-profile "Software / QA"
```

The earlier Streamlit interface can still be launched with:

```bash
streamlit run src/ui/streamlit_app.py
```

It should not be confused with the current React application-management UI.

---

# Docker

The project includes Docker support.

Build:

```bash
docker build -t ai-career-manager .
```

Run:

```bash
docker run --rm --env-file .env ai-career-manager
```

Run the Python test suite:

```bash
docker run --rm ai-career-manager pytest
```

Docker configuration may need to be revisited when the React/FastAPI product is
prepared for public deployment.

---

# Current Deployment State

The current release is known-good for local operation.

It is **not yet publicly deployed**.

The current local architecture uses:

- Vite/React at `localhost:5173`
- FastAPI/Uvicorn at `127.0.0.1:8000`
- SQLite persistence

A future production deployment will require explicit decisions about frontend
hosting, backend hosting, persistent production storage, configuration,
security, and backup/recovery.

See `SHELF_SAFE.md` for the exact known-good local baseline.

---

# Engineering Philosophy

Large language models are excellent at understanding unstructured information
and accelerating repetitive engineering work.

Software engineers remain responsible for:

- Architecture
- Truthfulness
- Validation
- Testing
- Debugging
- Maintainability
- Operational safety
- Long-term ownership

The application has therefore been developed incrementally through:

- Small architectural changes
- Frequent execution
- Continuous automated testing
- Real-world use
- Human review
- Incremental refactoring

The goal is not merely to produce working software.

The goal is to understand the software well enough to maintain it, extend it,
debug it, explain it, and safely return to it after a long absence.

**AI should reduce repetitive work—not engineering discipline.**

---

# Shelf-Safe Development

AI Career Manager is also being used to develop and test a project-management
pattern called **Shelf-Safe Development**.

The idea is that a software product does not need to remain under continuous
development.

At the end of a product cycle, the project should be deliberately placed into
a state where:

- the current product works;
- automated tests establish a known-good baseline;
- persistent data is understood and protected;
- startup and testing instructions are accurate;
- known limitations are recorded;
- unfinished experiments are not left ambiguously connected;
- architectural decisions are documented;
- the next development cycle can begin without depending on human memory.

The engineering target is:

> **No dependency on human memory.**

A shelf-safe product may remain untouched while other products are developed,
then be resumed months or years later.

See **`SHELF_SAFE.md`** before beginning another development cycle.

---

# Future Product Cycles

Potential future directions include:

- Public deployment
- Explicit career-profile selection in the web UI
- Additional career profiles
- Semantic skill normalization
- Fit-score calibration
- Career-profile market intelligence
- Profile Advisor
- Resume version history
- Cover letter workflows
- Interview preparation
- Career analytics
- Saved job searches
- Agent-assisted job discovery
- Additional application lifecycle workflows
- React visual design and responsive layout

These are candidates for future product cycles rather than commitments.

Real-world use should determine which work is valuable enough to build next.

---

# Security

Sensitive information should never be committed to source control.

Examples include:

- API keys
- Authentication secrets
- Personal resumes
- Production databases
- Real application history

Local and production data should be treated as persistent user data rather than
disposable development artifacts.

---

# Resuming Development

If this project has been inactive for any meaningful period:

**Do not start by changing code.**

Start with:

**`SHELF_SAFE.md`**

It records:

- the known-good test baseline;
- startup instructions;
- manual smoke-test procedure;
- current architecture;
- completed milestone work;
- important design decisions;
- known limitations;
- intentionally deferred work;
- likely next development seams.

The repository, not developer memory, should contain enough context to restart
development safely.

---

# Author

**Kenny Gilfilen**

Colorado, USA
