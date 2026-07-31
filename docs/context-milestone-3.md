# AI Career Manager
## Context for Next Conversation

**Date:** July 30, 2026

---

# Current Status

Milestone 2 ("Professional Identity") is complete.

Completed work includes:

- Candidate Profile JSON model
- Candidate Profile loader
- Improved fit scoring
- Resume recommendation engine
- Markdown resume generation
- GitHub recommendation support
- LinkedIn recommendation support
- Education rendering
- Regression test suite
- Integration tests
- Docker support
- Stable parser/scorer architecture

All tests are currently passing.

The local Git repository has been cleaned up and old feature branches removed.

---

# Project Philosophy

We are intentionally building this as a professional software project.

Goals:

- clean architecture
- incremental milestones
- strong automated testing
- Git feature-branch workflow
- production-quality code
- user-driven development

We prefer adding functionality only after using the software enough to understand what is genuinely useful.

---

# Milestone 3

Milestone 3 has changed from the original roadmap.

Instead of a Professional Knowledge Base, the next milestone will be:

# Job History & Application Tracking

Primary goals:

- Store every processed job
- Prevent duplicate applications
- Preserve original job descriptions
- Track application status
- Support interview preparation months later

---

# Core Design Decision

Every job processed by AI Career Manager should be stored immediately.

Workflow:

Receive Job Description

↓

Store Original Job Description

↓

Duplicate Detection

↓

Parse

↓

Score

↓

Generate Resume Recommendations

↓

Update Stored Record

This ensures the original posting is never lost, even if parsing or AI processing fails.

---

# SQLite

SQLite will be introduced during this milestone.

Initial tables will likely include:

Job

Fields (approximate):

- id
- company
- title
- source
- source_url
- external_job_id
- full_job_description
- parsed_job_data
- fit_score
- recommendation
- status
- date_found
- date_applied
- notes

Additional tables can be added later if needed.

---

# Job Status Values

Current proposal:

- NEW
- RECOMMENDED
- DECLINED
- APPLIED
- INTERVIEWING
- OFFER
- REJECTED
- WITHDRAWN
- EXPIRED

These may evolve during implementation.

---

# User-Day Objectives

Before writing much new code, spend time using the application.

Process multiple real job descriptions.

Evaluate:

- parser quality
- fit scoring
- recommendation quality
- generated resume usefulness

Record observations under four headings:

BUG

CONFUSING

SLOW

IDEA

Do not immediately implement every idea.

Collect observations first.

---

# Important Discovery

The application should retain the complete original job description.

Reasons:

- interview preparation
- compare reposted jobs
- historical reference
- regenerate resumes later
- generate interview questions later

This became one of the major design decisions from the user evaluation.

---

# Test Data

Keep several job descriptions in the repository strictly for automated testing.

Real job searches should not live in the repository.

Real jobs belong in SQLite.

---

# Future Vision

After Milestone 3 the application should support workflows like:

Import Job

↓

Analyze

↓

Recommend Resume

↓

Apply

↓

Track Progress

↓

Prepare For Interview

↓

Record Outcome

This moves AI Career Manager beyond a parser into a true job-search assistant.

---

# Development Style

Continue using:

- feature branches
- pull requests
- automated tests
- small milestones
- frequent commits

Maintain production-quality code throughout.

---

# Immediate Next Task

Create the Milestone 3 feature branch.

Design the SQLite schema.

Implement job persistence before additional AI features.

Then begin importing and tracking real jobs.