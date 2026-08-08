# AI Career Manager

AI Career Manager is an AI-assisted software engineering project that automates
job analysis, resume tailoring, fit scoring, and long-term career management.

Rather than replacing engineering judgment, the application uses large language
models to accelerate repetitive work while preserving software engineering
discipline through clean architecture, automated testing, and human review.

Originally started as **AI Job Hunter** in June 2026, the project has evolved
into a persistent career management platform rather than simply a resume
tailoring tool.

---

# Highlights

Current capabilities include:

- AI-powered job description analysis
- Intelligent web page extraction
- Structured job parsing
- Resume fit scoring
- Resume recommendation generation
- Tailored resume generation
- Persistent SQLite job history
- Duplicate detection using URL and SHA-256 hashing
- Streamlit user interface
- Comprehensive unit and integration testing
- Docker-based reproducible development environment

---

# Purpose

Searching for software engineering jobs involves a surprising amount of
repetitive work.

AI Career Manager automates much of that workflow while keeping the engineer in
control of every decision.

The application assists with:

- Reading job descriptions
- Extracting requirements
- Comparing jobs against a candidate profile
- Resume tailoring
- Fit scoring
- Application tracking
- Long-term career management

---

# Architecture

```text
                Job File
                    │
                or URL
                    │
          Fetch / Read Input
                    │
          Build JobInput Model
                    │
          Duplicate Detection
                    │
        Store Original Job
             (SQLite)
                    │
          Parse Job Description
                    │
       Structured JobOpening
                    │
         Resume Fit Analysis
                    │
    Resume Recommendation Engine
                    │
     Tailored Resume Generator
                    │
      Persistent Artifacts
                    │
          Career History
```

The application intentionally separates:

- User interface
- Business services
- Persistence
- AI parsing
- Scoring
- Artifact generation

This architecture keeps each module focused on a single responsibility and
makes the system easier to test and extend.

---

# Technology Stack

Current technologies:

- Python 3
- SQLite
- OpenAI API
- Streamlit
- BeautifulSoup
- Pytest
- Docker

Planned additions:

- GitHub Actions
- Machine-learning recommendation models
- Additional AI agents
- Expanded web interface

---

# Real-World Validation

AI Career Manager has been used throughout my own software engineering job
search.

Every job I considered was analyzed before I invested time reading the complete
description.

The application helped me:

- Quickly eliminate poor-fit positions.
- Identify strong opportunities worth pursuing.
- Improve my candidate profile by recording legitimate skills and experience.
- Re-analyze opportunities after profile improvements.
- Maintain a permanent history of analyzed jobs.

The result has been less time spent evaluating unsuitable positions and greater
confidence in the jobs I choose to pursue.

---

# Testing

The project is developed using a test-first approach whenever practical.

Current automated coverage includes:

- Unit tests
- Integration tests
- Repository tests
- Parser tests
- URL fetcher tests
- Regression tests

The application architecture intentionally separates business logic from the
user interface, making most functionality straightforward to test.

---

# Repository Structure

```text
src/
    artifacts/      Artifact generation
    database/       SQLite persistence
    fetchers/       Job acquisition
    formatters/     Resume and output formatting
    models/         Domain models
    parsers/        AI parsing
    resume/         Resume recommendation
    scoring/        Candidate fit scoring
    services/       Business logic
    ui/             Streamlit user interface

tests/
examples/
outputs/
config/
docs/
```

Each package contains engineering documentation describing:

- Purpose
- Public interface
- Dependencies
- Behavioral specifications
- Invariants
- Testing strategy
- Future enhancements

---

# Running the Project

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

Launch the Streamlit interface:

```bash
streamlit run src/ui/streamlit_app.py
```

---

# Docker

The project is fully reproducible using Docker.

```bash
docker build -t ai-career-manager .
```

Run the application:

```bash
docker run --rm --env-file .env ai-career-manager
```

Run the test suite:

```bash
docker run --rm ai-career-manager pytest
```

---

# Engineering Philosophy

Large language models are excellent at understanding unstructured information.

Software engineers are responsible for architecture, validation, testing,
maintainability, and long-term ownership.

This project intentionally combines those strengths.

Rather than allowing AI to generate an application in one step, every feature
was developed incrementally:

- Small architectural changes
- Frequent execution
- Continuous testing
- Human review
- Incremental refactoring

The goal is not simply to produce working software.

The goal is to understand the software well enough to maintain it, extend it,
debug it, and explain it to another engineer months later.

**AI should reduce repetitive work—not engineering discipline.**

---

# Future Roadmap

Planned capabilities include:

- Application tracking
- Interview tracking
- Resume version history
- Cover letter generation
- AI interview preparation
- Machine-learning ranking
- Career analytics dashboard
- Multi-user support

---

# Security

Sensitive information is never committed to source control.

Examples include:

- API keys
- Authentication secrets
- Personal resumes
- Production databases
- Real application history

---

# Author

**Kenny Gilfilen**

Colorado, USA