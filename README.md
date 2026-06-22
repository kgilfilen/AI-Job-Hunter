# AI Job Hunter
AI Job Hunter is a Python-based application that automates portions of the job search process, including job description analysis, resume tailoring, cover letter generation, application tracking, and future machine learning-based job ranking.
The project was conceived on June 22, 2026, with the goal of delivering a production-ready MVP by June 30, 2026.

# Purpose
Searching for jobs often involves repetitive work:
* Reading job descriptions
* Identifying required skills
* Comparing jobs against a resume
* Tailoring resumes
* Writing cover letters
* Tracking applications
AI Job Hunter automates much of this workflow while maintaining human review and approval.

# Features
Current Features
* Job description parsing
* Structured job object generation
* Resume strategy recommendations
* Cover letter draft generation
* Application tracking
* Role-based access control
* Public demo mode
* REST API
# Planned Features
* Automated job discovery
* Resume tailoring
* Interview question generation
* Job recommendation engine
* Machine learning ranking models
* Application success analytics
* Agent-assisted application workflow

# Architecture
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

# Technology Stack
* Python
* FastAPI
* SQLite
* OpenAI API
* Okta Authentication
* GitHub Actions
* Pytest

# Security
Sensitive information is never committed to source control.
Examples include:
* API keys
* Authentication secrets
* Production databases
* Personal resumes
* Real job application history
Configuration is managed through environment variables.

# User Roles
Guest
* Access demo data
* View sample job analyses
* Explore application functionality
Admin
* Analyze real job descriptions
* Generate tailored resumes
* Generate cover letters
* Manage application history

# Repository Structure
src/
tests/
examples/
docs/

README.md
LICENSE
requirements.txt

# Running Locally
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn src.main:app --reload

# Future Machine Learning Integration
This project intentionally separates business logic from scoring logic.
Current releases use transparent rule-based scoring.
Future releases may include:
* Interview probability prediction
* Resume-job similarity scoring
* Job clustering
* Application outcome prediction
* Recommendation systems

# Disclaimer
This project is intended as a personal productivity and portfolio project. Generated resumes and cover letters should always be reviewed before submission.

# Author
Kenny Gilfilen Colorado, USA

