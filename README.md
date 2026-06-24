# AI Job Hunter
AI Job Hunter is a Python-based application that automates portions of the job search process, including job description analysis, resume tailoring, cover letter generation, application tracking, and future machine learning-based job ranking.
The project was conceived on June 22, 2026, with the goal of delivering a production-ready MVP by June 30, 2026.

## Purpose
Searching for jobs often involves repetitive work:

* Reading job descriptions
* Identifying required skills
* Comparing jobs against a resume
* Tailoring resumes
* Writing cover letters
* Tracking applications

AI Job Hunter automates much of this workflow while maintaining human review and approval.

## Features
Current Features

* Job description parsing
* Structured job object generation
* Resume strategy recommendations
* Cover letter draft generation
* Application tracking
* Role-based access control
* Public demo mode
* REST API

Planned Features

* Automated job discovery
* Resume tailoring
* Interview question generation
* Job recommendation engine
* Machine learning ranking models
* Application success analytics
* Agent-assisted application workflow

## Architecture
```text
Job Description
       |
       v
Job Parser
       |
       v
Structured Job Object
       |
       +-------> Resume Strategy
       |
       +-------> Cover Letter Generator
       |
       +-------> Application Tracker
       |
       +-------> Future ML Scoring
```

## Technology Stack

* Python
* FastAPI
* SQLite
* OpenAI API
* Okta Authentication
* GitHub Actions
* Pytest

## Security
Sensitive information is never committed to source control.
Examples include:

* API keys
* Authentication secrets
* Production databases
* Personal resumes
* Real job application history

Configuration is managed through environment variables.

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
tests/
examples/
docs/

README.md
LICENSE
requirements.txt
```

## Running Locally
```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn src.main:app --reload
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


