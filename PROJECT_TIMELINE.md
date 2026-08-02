# AI Career Manager Project Roadmap

**Last Updated:** July 30, 2026

## Vision

Build an AI-powered career platform that helps software engineers manage their careers by combining job discovery and evaluation, application tracking, a Professional Knowledge Base, AI-assisted document generation, interview preparation, and long-term career planning.

The first public module is **AI Job Hunter**.

Development sequencing is described in `docs/development_strategy.md`.

## Summary

Milestone 1: Analyze jobs.

Milestone 2: Present yourself professionally.

Milestone 3: Track your job search.

Milestone 4: Build your professional memory.

Milestone 5: Generate evidence-based résumés.

Milestone 6: Manage your career.

Milestone 7: Prepare for interviews.

Milestone 8: Integrate everything into a cohesive AI Career Manager.

# Milestone 1 – AI Job Hunter MVP

**Status:** ✅ Complete

**Completed:** June 30, 2026
**Post-MVP stabilization completed:** July 30, 2026

## Project Setup

* Create GitHub repository
* Python project structure
* Virtual environment
* Documentation
* Git workflow
* Dockerized development and test environment

## Data Models

* CandidateProfile
* JobOpening
* FitAnalysis
* JSON serialization
* Expanded candidate-profile fields
* Candidate profile loading and validation

## Parsing

* Job title
* Company
* Location
* Employment type
* Remote status
* Security clearance
* Required skills
* Preferred skills
* Responsibilities

## Scoring

* Required-skill matching
* Preferred-skill matching
* Explainable scoring
* Confidence values
* Candidate-profile-aware fit analysis
* Required-skill coverage penalties
* Consistency between fit scores and identified concerns

## Resume Intelligence

* Deterministic resume recommendation engine
* Skills-to-emphasize recommendations
* Experience-to-highlight recommendations
* Missing-keyword identification
* Resume concern identification
* Unit tests for resume recommendations
* Candidate-to-recommendation pipeline coverage
* Readable recommendation formatting
* End-to-end résumé-generation regression coverage

## Quality and Developer Operations

* Unit tests
* Integration tests
* Pytest integration markers
* Modular architecture
* Full regression testing
* API usage reporting utility
* Logical Git commits and feature-branch workflow
* Known-good tested application state

---

# Milestone 2 – Professional Identity

**Status:** ✅ Substantially Complete

**Sprint 2:** July 24–31, 2026

The major engineering work for this milestone is complete. Remaining résumé, LinkedIn, GitHub, and documentation work should be treated as milestone closeout and professional-profile polish.

## Resume

* Resume redesign
* AI Job Hunter project added
* Behavioral Coaching Platform added
* Complete Master Resume
* Create reusable tailored-resume template
* Perform final content and formatting review
* Confirm consistency with CandidateProfile

## LinkedIn

* Headline
* About section
* Current projects
* Charter updates
* Final polish
* Confirm consistency with résumé and GitHub

## GitHub

* Public AI Job Hunter repository
* AI Career Manager repository
* Initial tags
* Clean feature-branch merge workflow
* Improve public GitHub profile README
* Simplify public repositories for recruiter review
* Improve AI Job Hunter repository presentation
* Add screenshots or example output when available

## Milestone Closeout

* Merge remaining Milestone 2 work into `main`
* Run full regression suite
* Update README and roadmap
* Create a known-good Git tag
* Confirm that recruiter-facing materials tell a consistent story

---

# User Evaluation Period

**Status:** 🚧 In Progress

Use AI Job Hunter as a real user before beginning substantial new feature development.

## Goals

* Process real job descriptions
* Test excellent, moderate, weak, and clearly unsuitable matches
* Evaluate the usefulness of fit scores
* Evaluate résumé recommendations
* Identify awkward or repetitive workflow steps
* Record missing information and unexpected behavior
* Distinguish defects from feature requests
* Identify information the application should remember

## Evaluation Discipline

During user sessions:

* Record ideas instead of immediately implementing them
* Fix blocking defects when necessary
* Avoid speculative feature expansion
* Keep a temporary record of evaluated and applied jobs
* Note every occasion where the application should have remembered something

## Evaluation Notes

Maintain:

```text
docs/user_experience_notes.md
```

Use entries such as:

```markdown
## Observation

What happened during actual use?

## Impact

How did it affect the workflow or decision?

## Potential Improvement

What change might address it?

## Classification

Defect, usability issue, persistence need, or future feature.
```

---

# Milestone 3 – Job History and Application Tracking

**Status:** 📋 Planned

Milestone 3 will give AI Job Hunter persistent memory of jobs that have already been discovered, analyzed, recommended, rejected, or applied to.

The primary purpose is to prevent duplicate work and reduce the risk of applying to the same position more than once.

## Local Persistence

* Add a small SQLite database
* Keep database access behind a repository layer
* Create database initialization and migration support
* Store timestamps in a consistent format
* Keep database implementation separate from business logic
* Make local backup and restore straightforward

## Job Records

Store:

* Company
* Job title
* Location
* Remote status
* Employment type
* Source
* External job ID
* Original posting URL
* Raw job description
* Normalized job-description hash
* Parsed JobOpening data
* First-seen date
* Last-seen date
* Last-analysis date
* Posting status
* User notes

## Analysis Records

Store:

* Fit score
* Recommendation
* Matched required skills
* Missing required skills
* Matched preferred skills
* Strengths
* Concerns
* Recommendation notes
* Scoring-version information
* Analysis timestamp

## Application Status

Support an initial status workflow:

* NEW
* ANALYZED
* RECOMMENDED
* CONSIDERING
* APPLIED
* INTERVIEWING
* REJECTED
* WITHDRAWN
* DECLINED
* EXPIRED

Allow the user to record:

* Application date
* Résumé version used
* Cover letter used
* Recruiter or contact
* Follow-up date
* Interview dates
* Notes
* Outcome

## Duplicate Detection

Check for duplicates using:

1. External source and job ID
2. Exact or normalized posting URL
3. Normalized job-description hash
4. Company, title, and location similarity
5. Previously applied positions at the same company

When a possible duplicate is found, show:

* Previous analysis date
* Previous fit score
* Current application status
* Application date, when applicable
* Reason the posting was flagged

Duplicate detection should warn the user without permanently blocking legitimate applications to reposted or separately numbered positions.

## Repository Layer

Define clear persistence interfaces, such as:

```python
class JobRepository:
    def save_job(self, job):
        ...

    def get_job(self, job_id):
        ...

    def find_duplicates(self, job):
        ...

    def list_jobs(self, status=None):
        ...

    def update_status(self, job_id, status):
        ...
```

Initial implementation:

```python
class SQLiteJobRepository(JobRepository):
    ...
```

The application should be able to move to PostgreSQL later without changing scoring, parsing, recommendation, or formatting logic.

## Initial User Workflow

```text
Submit job URL or description
        ↓
Check for existing or similar job
        ↓
Parse and analyze new posting
        ↓
Save job and analysis
        ↓
Review recommendation
        ↓
Update application status
```

## Initial Interface

The first interface may remain command-line based.

Minimum useful commands or workflows:

* Add a job
* Analyze and save a job
* List recently analyzed jobs
* List recommended jobs
* List applied jobs
* Show one job and its history
* Change application status
* Add notes
* Warn about possible duplicates

## Milestone 3 Completion Criteria

Milestone 3 is complete when:

* An analyzed job persists between application runs
* Previous analyses can be retrieved
* Applied jobs are clearly identifiable
* Duplicate jobs produce a warning
* Application status can be updated
* The full test suite remains green
* Persistence logic has unit and integration coverage
* The database can be backed up and recreated reliably

---

# Milestone 4 – Professional Knowledge Base & Candidate Intelligence

**Status:** 📋 Planned

The Professional Knowledge Base becomes the source of truth for résumé generation, interview preparation, career analysis, and future AI assistance.

## Initial Structure

* Professional summary
* Career history
* Technical skills
* Major projects
* Interview stories
* Leadership examples
* Successes
* Failures and lessons learned
* Education
* Certifications

## Initial Implementation

* Create directory and Markdown structure
* Define a consistent entry format
* Add Charter/Spectrum experience
* Add prior QA and automation roles
* Add AI Job Hunter project
* Add Behavioral Coaching Platform project
* Add reusable accomplishment statements
* Add initial STAR stories
* Add evidence or source references for important professional claims

## Initial Target

Create 10–20 or more pages of structured Markdown.

## Added Sections (after User day feedback)

### Candidate Skills Inventory

* Canonical skills
* Skill aliases
* Related skills
* Years of experience
* Last used
* Evidence/projects
* Skill notes
* Confidence level

### Skill Normalization

* Normalize equivalent terminology
* Maintain alias dictionaries
* Distinguish aliases from related technologies
* Reuse normalized skills across parsing, scoring, and résumé generation

### Profile Advisor

* Aggregate recurring missing skills
* Recommend profile improvements
* Detect probable aliases
* Suggest learning priorities
* Help maintain an accurate Candidate Profile

## Completion Criteria

* Major positions and projects are represented
* Technical skills are connected to supporting experience
* Accomplishments can be retrieved by role, skill, and project
* STAR stories are available for common interview categories
* Content can support fact-based résumé generation
* Professional claims remain traceable to supporting evidence

---

# Milestone 5 – Resume Generator

**Status:** 🚧 Foundation Started

Foundational components were developed during Milestone 1. Complete résumé generation will use the Professional Knowledge Base as its source of truth.

## Completed Foundation

* Parse job descriptions
* Match candidate skills to job requirements
* Identify matched and missing skills
* Generate structured résumé recommendations
* Recommend skills to emphasize
* Recommend experience to highlight
* Identify missing keywords
* Identify possible candidate concerns
* Format recommendations as readable output
* Test recommendation and formatting behavior
* Exercise candidate-to-résumé output through regression tests

## Planned Features

* Select the best accomplishments from the Knowledge Base
* Rewrite the professional summary
* Tailor skills and experience sections
* Preserve factual accuracy during generation
* Generate a complete tailored résumé
* Associate generated résumés with job records
* Preserve application-document history
* Export Microsoft Word
* Export PDF

## Completion Criteria

* A complete résumé can be generated for a stored job
* Every major claim comes from the Professional Knowledge Base
* Generated documents remain associated with the job application
* The user can identify which résumé was submitted
* Word and PDF exports are usable for applications

---

# Milestone 6 – Career Dashboard

**Status:** 📋 Planned

Create a daily AI assistant for career-management work.

## Features

* Application tracker
* Recruiter tracker
* Interview tracker
* Follow-up reminders
* Skill-gap analysis
* Learning recommendations
* Daily activity summary
* LLM usage and cost visibility
* Job-search activity history
* Application statistics
* Recently analyzed and recommended jobs

The Career Dashboard should use the persistent job and application data created during Milestone 3.

---

# Milestone 7 – Interview Assistant

**Status:** 📋 Planned

Generate interview preparation directly from the user’s own professional experience and the requirements of a stored job opening.

## Features

* STAR stories
* Technical examples
* Behavioral questions
* Architecture discussions
* Project walkthroughs
* Mock interviews
* Job-specific interview preparation
* Interview notes
* Interview outcome tracking
* Preparation linked to application records

---

# Milestone 8 – AI Career Manager MVP

**Status:** 📋 Planned

Combine the major components into a single usable application.

## Major Modules

* Professional Knowledge Base
* Resume Generator
* AI Job Hunter
* Job History and Application Tracking
* Interview Assistant
* Career Dashboard

## MVP Outcomes

* Maintain one structured professional source of truth
* Analyze a job posting
* Evaluate candidate fit
* Recognize previously analyzed or applied-to jobs
* Generate a tailored résumé
* Preserve the résumé used for each application
* Generate interview preparation
* Track applications and follow-up work
* Maintain long-term professional and job-search history

---

# Future Ideas and Backlog

These ideas have been discussed but intentionally postponed until the core platform is complete.

## Job Discovery and Acquisition

* Saved job-search definitions
* Configurable job-source records
* LinkedIn saved-search links
* Job-alert email ingestion
* Browser extension or bookmarklet
* Company-career-page adapters
* Approved job-board API integrations
* Automated job-posting ingestion
* Scheduled source checks
* Posting-expiration detection

## Artificial Intelligence

* RAG search over the Professional Knowledge Base
* Local vector database
* Personal Digital Twin
* Long-term memory
* Career recommendations
* Machine-learning-assisted job ranking
* Feedback-based recommendation improvement
* Similar-job detection beyond deterministic matching

## Engineering

* Plugin architecture
* REST API
* Web interface
* Authentication
* Role-based access
* Multi-user support
* PostgreSQL support
* Background processing
* Data-retention and privacy controls
* Hosted deployment

## Career Features

* Cover-letter generation
* LinkedIn optimization
* Networking tracker
* Recruiter CRM
* Salary analytics
* Job-search analytics
* Offer comparison
* Long-term career planning

---

# Current Sprint

**Sprint 2:** July 24–31, 2026

**Status:** ✅ Substantially Complete

## Completed This Sprint

* Improve CandidateProfile
* Add candidate-profile pipeline coverage
* Add deterministic résumé recommendation engine
* Add résumé recommender unit tests
* Build résumé recommendation formatter
* Add formatted recommendations to the command-line workflow
* Add realistic formatter and workflow tests
* Add end-to-end résumé-generation regression coverage
* Organize integration tests with pytest markers
* Improve scoring consistency
* Add API usage reporting utility
* Dockerize development and testing
* Run final regression tests
* Merge `feature/improve_candidate_profile`
* Establish a clean résumé recommendation workflow

## Remaining Sprint Closeout

* Finish Master Resume
* Complete LinkedIn polish
* Improve GitHub profile for recruiter review
* Update README and development logs
* Merge remaining work into `main`
* Run final full regression suite
* Create a known-good release tag

## User Evaluation Work

* Use AI Job Hunter on real job postings
* Record user-experience observations
* Maintain a temporary application log
* Identify duplicate-job and persistence requirements
* Avoid beginning nonessential feature work during evaluation

## Next Milestone Preparation

* Define initial SQLite schema
* Define job and application statuses
* Define repository interfaces
* Identify duplicate-detection rules
* Decide which current objects will be persisted
* Design migration and test strategy

---

# Project Notes

This project began as AI Job Hunter, an application that analyzes software-engineering job postings and evaluates candidate fit.

The first MVP established structured job parsing, candidate modeling, explainable fit analysis, automated testing, LLM integration, and deterministic résumé recommendations.

## Post-MVP Development Added

* Dockerized and reproducible execution
* Improved candidate-profile modeling
* Organized unit and integration testing
* API usage reporting
* Structured résumé recommendations
* Readable résumé recommendation output
* End-to-end regression coverage
* Improved fit-scoring consistency
* A disciplined feature-branch and commit workflow

As the application began moving toward real use, another foundational requirement became clear: the system must remember jobs that have already been analyzed and applications that have already been submitted.

Without persistence, the user could repeat analysis, lose application history, or accidentally apply to the same position more than once.

For that reason, Job History and Application Tracking now precedes the Professional Knowledge Base in the roadmap.

The broader opportunity remains larger than job matching. AI Career Manager will organize an engineer’s complete professional history, connect that history to real job opportunities, generate fact-based application materials, support interviews, and preserve long-term career knowledge.

AI Job Hunter therefore becomes one tested, reusable module inside a larger AI-assisted career platform.

Development does not have to follow the milestones in perfectly sequential order. Small foundational pieces may be implemented early when they clarify the architecture or provide immediate practical value.

However:

* Persistent job history is the foundation for reliable application tracking.
* The Professional Knowledge Base is the foundation for reliable document generation.
* Both should exist before the full Career Dashboard and AI Career Manager MVP are completed.

---

# Architecture Principles

* Business logic should produce structured data objects.
* Formatting, presentation, and user-interface concerns should remain separate from business logic.
* Persistence should remain separate from domain and scoring logic.
* Database access should occur through repository interfaces.
* Deterministic processing should be preferred where an LLM is unnecessary.
* LLM calls should be isolated, testable, and cost-conscious.
* Professional facts should come from a maintained source of truth.
* Generated documents should remain traceable to supporting professional evidence.
* Job analyses and generated documents should remain traceable to the relevant job record.
* SQLite should be treated as a valid local database, not as a temporary hack.
* Future database migration should not require redesigning the core application.

---

# Guiding Principles

* Keep the architecture modular.
* Build reusable components before adding features.
* Maintain excellent documentation.
* Prefer maintainability over cleverness.
* Write tests alongside functionality.
* Separate unit tests from external-service integration tests.
* Use small, focused feature branches and commits.
* Monitor external API usage and cost.
* Use AI to accelerate engineering, not replace engineering judgment.
* Build tools that you personally use first.
* Capture feature ideas without immediately implementing them.
* Let real usage determine the next useful features.
* Prevent duplicate effort and preserve application history.
* Let the Professional Knowledge Base become the foundation for fact-based career assistance.
