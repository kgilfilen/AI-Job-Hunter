# AI Career Manager

AI Career Manager is a Python-based application that preserves, analyzes, and manages job opportunities throughout the hiring process. It automates job acquisition, AI-assisted job analysis, resume tailoring, fit scoring, and long-term application tracking.

The project began on June 22, 2026, as "AI Job Hunter" and has evolved into a persistent career management system rather than simply a resume tailoring tool.

This project is not about replacing engineers, but accelerating them.

## Purpose
Searching for jobs often involves repetitive work, much of which I HATE:

* Reading job descriptions
* Identifying required skills
* Comparing jobs against a resume
* Tailoring resumes
* Writing cover letters
* Tracking applications

AI Job Hunter automates much of this workflow while maintaining human review and approval.

## Features

Current Features

* Import jobs from local files or URLs
* Intelligent web page extraction
* AI-powered job description parsing
* Structured JobOpening model generation
* Resume fit scoring
* Resume recommendation generation
* Tailored resume generation (Markdown)
* Permanent SQLite job history
* Duplicate detection using URL and SHA-256 hashing
* Artifact generation for every imported job
* Safe reprocessing of existing jobs
* Comprehensive unit and integration test suite
* Docker-based reproducible development environment

Planned Features

* JSON-LD and ATS metadata extraction 

     * Enhanced metadata extraction from modern recruiting platforms -- AI Career Manager extracts structured job information (such as company, title, employment type, and location) from recruiting platforms like Greenhouse, Lever, Workday, and other modern ATS systems to improve parsing accuracy.)
* Interview preparation assistant
* Application status and interview tracking
* Resume version history
* Cover letter generation
* Web interface
* Machine learning ranking models
* AI agent-assisted job search workflow

## Current Status

Completed

* AI parser
* Resume fit scoring
* Resume recommendations
* Persistent SQLite database
* Duplicate detection
* URL acquisition pipeline
* Artifact management
* Comprehensive automated testing
* Docker support

In Progress

* Rich metadata extraction
* Application workflow
* Interview preparation

Future

* Web UI
* GitHub Actions CI
* ML-assisted recommendation engine
### TODO:

* resume tailoring
* web interface
* github actions

## Architecture
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
```

## Technology Stack

* Python 3.x
* FastAPI
* SQLite
* OpenAI API
* Okta Authentication
* GitHub Actions
* Pytest
* Docker

## Persistent Job History

Every imported job receives a permanent database record.

Each job stores:

* Original job description
* Source URL (when applicable)
* Description hash
* Parsed job information
* Resume fit analysis
* Resume recommendations
* Artifact directory
* Creation and update timestamps

Duplicate jobs are detected using:

* Source URL
* SHA-256 hash of the original job description

Existing jobs may be intentionally regenerated using:

```bash
python3 -m src.main --reprocess
```

## Testing

The project is developed test-first whenever practical.

Current automated coverage includes:

* Unit tests
* Integration tests
* Regression tests
* Repository tests
* Parser tests
* URL fetcher tests

Test reports are automatically generated in JUnit XML format for future CI integration.

## Security
Sensitive information is never committed to source control.
Examples include:

* API keys
* Authentication secrets
* Production databases
* Personal resumes
* Real job application history

Configuration is managed through environment variables.

## Docker Support

The project is fully reproducible using docker. Everyone executes in an identical env, which eliminates "works on my machine".
The AI Job Hunter can be built, tested, and executed entirely within Docker, providing a reproducible dev environment.

### Build & Run

```bash
docker build -t ai-job-hunter .
```

### Run
``` bash
docker run --rm ai-job-hunter 

docker run --rm --env-file .env ai-job-hunter 

docker run --rm ai-job-hunter pytest -v

docker run --rm --env-file .env ai-job-hunter pytest -v
```
### Complete Docker Check
``` bash
./scripts/docker-check.sh
```

## User Roles
Guest

* Access demo data
* View sample job analyses
* Explore application functionality

Admin

* Analyze real job descriptions
* Generate tailored resumes
* Generate cover letters
* Manage application history

Developer

* TBD

## Repository Structure
```text
src/
    artifacts/
    database/
    fetchers/
    formatters/
    models/
    parsers/
    resume/
    scoring/

tests/

examples/

outputs/

config/

docs/
```

## Running Locally
```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn src.main:app --reload
```

## Running from Docker
```bash
docker run -rm --env-file .env ai-job-hunter
```

## Future Machine Learning Integration
This project intentionally separates business logic from scoring logic.

Current releases use transparent rule-based scoring.

Future releases may include:

* Interview probability prediction
* Resume-job similarity scoring
* Job clustering
* Application outcome prediction
* Recommendation systems

## Engineering Philosophy 

Where Do Engineers Often Go Wrong When Using AI?

One of the biggest mistakes engineers make when using AI is allowing the AI to generate large amounts of code that they never truly understand.

When I write software manually, I build a mental model of the application as it comes into existence. I know the paths through the code because I created them. I run the software frequently, add print statements, inspect variables, and watch the program execute. Over time, I develop an intuition for the system. I can often predict what the code will do before I run it because I have experienced each part of it being built.

And I carefully add minimal comments, because in 6 months I will have created 14 other apps, and completely forgotten about this one.

AI changes that process.

An engineer can ask for an entire module, class, or application and receive hundreds of lines of code in seconds. The code may be correct, but if it is accepted without inspection, testing, and observation, the engineer never develops a complete understanding of how it works. The code exists, but it is not yet part of the engineer’s mental model.

For this project, I deliberately used AI differently.

Rather than asking AI to build the entire system, I broke the project into small pieces:

* Repository structure
* Data models
* Parsers
* API integration
* Authentication
* Testing
* User interface

Each component was reviewed, modified, executed, and validated before moving to the next. I frequently run the code, inspect intermediate results, and verify that execution follows the expected path. AI helps accelerate development, but it does not replace engineering discipline.

My goal is not simply to produce working software. My goal is to understand the software well enough to maintain it, extend it, debug it, and explain it to another engineer months later.

This project was created with AI assistance, but it was engineered intentionally. I know what is in the codebase because I experienced it being built.

## Why This Project Matters

One of the most interesting aspects of this project is not the Python code, the API integration, or the user interface. It is the ability to extract meaning from unstructured text.

Well, now it is preserving and managing knowledge throughout a job search.

A simple example is identifying the correct job title from a job description.

At first glance, this appears to be a small problem. In practice, it is remarkably difficult. Job descriptions come from different companies, industries, and recruiting systems. Titles may appear multiple times, be abbreviated, be embedded in marketing language, or be surrounded by unrelated information.

Historically, solving this problem required large amounts of custom software, complex parsing logic, rules engines, keyword databases, and extensive maintenance. Even then, results were often inconsistent.

Today, a large language model can perform this task reliably across a variety of formats. During the development of this project, five significantly different job descriptions were analyzed and the correct job title was identified in each case.

The Python code required to make this happen is relatively small. The intelligence required to understand the text is not.

This project intentionally combines both capabilities:

* Large language models provide the ability to understand and extract meaning from text.
* Software engineering provides the structure, testing, validation, security, persistence, and user experience required to turn that capability into a useful application.

The goal of this project is not to demonstrate that AI can write software. The goal is to demonstrate how modern software engineering can leverage AI to solve problems that were previously expensive, complex, or impractical to automate.

As the project evolves, the focus remains the same: use AI where understanding is required, and use engineering discipline everywhere else.

## Disclaimer
This project is intended as a personal productivity and portfolio project. Generated resumes and cover letters should always be reviewed before submission.

## Author
Kenny Gilfilen  
Colorado, USA


