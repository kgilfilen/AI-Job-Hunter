# AI Career Manager Project Roadmap

Last Updated: July 28, 2026

## Vision

Build an AI-powered career platform that helps software engineers manage their careers by combining a Professional Knowledge Base, AI-assisted document generation, job matching, interview preparation, and long-term career planning.
The first public module is AI Job Hunter.

### Development Sequencing is described in docs/development_strategy.md

## Milestone 1 – AI Job Hunter MVP

Status: ✅ Complete

Completed: June 30, 2026

Post-MVP stabilization updated: July 28, 2026

### Project Setup
* Create GitHub repository
* Python project structure
* Virtual environment
* Documentation
* Git workflow
* Dockerized development and test environment

### Data Models

* CandidateProfile
* JobOpening
* FitAnalysis
* JSON serialization
* Expanded candidate-profile fields
* Candidate profile loading and validation

### Parsing

* Job title
* Company
* Location
* Employment type
* Remote status
* Security clearance
* Required skills
* Preferred skills
* Responsibilities

### Scoring

* Required skill matching
* Preferred skill matching
* Explainable scoring
* Confidence values
* Candidate-profile-aware fit analysis

### Resume Intelligence

* Deterministic resume recommendation engine
* Skills-to-emphasize recommendations
* Experience-to-highlight recommendations
* Missing-keyword identification
* Resume concern identification
* Unit tests for resume recommendations
* Candidate-to-recommendation pipeline coverage

### Quality and Developer Operations

* Unit tests
* Integration tests
* Pytest integration markers
* Modular architecture
* Full regression testing
* API usage reporting utility
* Logical Git commits and feature-branch workflow


## Milestone 2 – Professional Identity

Status: 🚧 In Progress

Sprint 2: July 24–31, 2026

### Resume

* Resume redesign
* AI Job Hunter project added
* Behavioral Coaching Platform added
* Complete Master Resume
* Create reusable tailored-resume template
* Perform final content and formatting review

### LinkedIn

* Headline
* About section
* Current projects
* Charter updates
* Final polish
* Confirm consistency with résumé and GitHub

### GitHub

* Public AI Job Hunter repository
* AI Career Manager repository
* Initial tags
* Clean feature-branch merge workflow
* Improve public GitHub profile README
* Simplify public repositories for recruiter review
* Improve AI Job Hunter repository presentation
* Add screenshots or example output when available

## Milestone 3 – Professional Knowledge Base

Status: 📋 Planned

The Professional Knowledge Base becomes the source of truth for résumé generation, interview preparation, career analysis, and future AI assistance.

### Initial Structure

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

### Initial Implementation

* Create directory and Markdown structure
* Define a consistent entry format
* Add Charter/Spectrum experience
* Add prior QA and automation roles
* Add AI Job Hunter project
* Add Behavioral Coaching Platform project
* Add reusable accomplishment statements
* Add initial STAR stories

### Initial Target:10–20+ pages of structured Markdown.

## Milestone 4 – Resume Generator

Status: 🚧 Foundation Started

Some foundational components are being developed before the full Professional Knowledge Base is complete. Full résumé generation will depend on the Knowledge Base as its source of truth.

### Completed Foundation

* Parse job description
* Match candidate skills to job requirements
* Identify matched and missing skills
* Generate structured resume recommendations
* Recommend skills to emphasize
* Recommend experience to highlight
* Identify missing keywords
* Identify possible candidate concerns
* Test recommendation behavior

### Current Development

* Format recommendations as readable terminal output
* Integrate formatted recommendations into the application workflow
* Add realistic end-to-end examples

### Planned Features

* Select the best accomplishments from the Knowledge Base
* Rewrite the professional summary
* Tailor skills and experience sections
* Preserve factual accuracy during generation
* Generate a complete tailored résumé
* Export Microsoft Word
* Export PDF

## Milestone 5 – Career Dashboard

Status: 📋 Planned

Create a daily AI assistant for career management.

### Features

* Application tracker
* Recruiter tracker
* Interview tracker
* Follow-up reminders
* Skill-gap analysis
* Learning recommendations
* Daily activity summary
* LLM usage and cost visibility

## Milestone 6 – Interview Assistant

Status: 📋 Planned

Generate interview preparation directly from the user’s own professional experience.
Features

* STAR stories
* Technical examples
* Behavioral questions
* Architecture discussions
* Project walkthroughs
* Mock interviews
* Job-specific interview preparation

## Milestone 7 – AI Career Manager MVP

Status: 📋 Planned

Combine the major components into a single usable application.

### Major Modules

* Professional Knowledge Base
* Resume Generator
* AI Job Hunter
* Interview Assistant
* Career Dashboard

### MVP Outcomes

* Maintain one structured professional source of truth
* Analyze a job posting
* Evaluate candidate fit
* Generate a tailored résumé
* Generate interview preparation
* Track applications and follow-up work

## Future Ideas and Backlog

These ideas have been discussed but intentionally postponed until the core platform is complete.

### Artificial Intelligence

* RAG search over the Professional Knowledge Base
* Local vector database
* Personal Digital Twin
* Long-term memory
* Career recommendations
* Machine-learning-assisted job ranking
* Feedback-based recommendation improvement

### Engineering

* Plugin architecture
* REST API
* Web interface
* Authentication
* Role-based access
* Multi-user support
* Automated job-posting ingestion
* Data-retention and privacy controls

### Career Features

* Cover-letter generation
* LinkedIn optimization
* Networking tracker
* Recruiter CRM
* Salary analytics
* Application-document history
* Job-search analytics


# Current Sprint

Sprint 2: July 24–31, 2026

### Completed This Sprint

* Improve CandidateProfile
* Add candidate-profile pipeline coverage
* Add deterministic resume recommendation engine
* Add resume recommender unit tests
* Organize integration tests with pytest markers
* Add API usage reporting utility
* Dockerize development and testing
* Run final regression tests
* Merge feature/improve_candidate_profile
* Create a clean branch for resume recommendation output

### High Priority

* Build resume recommendation formatter
* Add formatted recommendations to the command-line workflow
* Finish Master Resume
* Build Professional Knowledge Base skeleton
* Improve GitHub profile for recruiter review
* Keep roadmap, README, and development logs current

### Medium Priority

* Add realistic formatter and workflow tests
* Complete LinkedIn polish
* Design the connection between the Knowledge Base and Resume Generator
* Improve GitHub Project organization
* Document AI Job Hunter architecture and data flow

### Low Priority

* UI design
* Career Dashboard architecture
* Digital Twin features
* RAG implementation

## Project Notes

This project began as AI Job Hunter, an application that analyzes software-engineering job postings and evaluates candidate fit.

The first MVP established structured job parsing, candidate modeling, explainable fit analysis, automated testing, and LLM integration.

#### Post-MVP development added:

* Dockerized and reproducible execution
* Improved candidate-profile modeling
* Organized unit and integration testing
* API usage reporting
* Structured résumé recommendations
* A disciplined feature-branch and commit workflow

As development progressed, we recognized that the larger opportunity was not simply matching candidates with jobs. It was organizing an engineer’s complete professional history into a reusable and maintainable knowledge base.

That insight led to the broader vision of AI Career Manager, where the Professional Knowledge Base becomes the central source of truth.

#### From that foundation, the system will eventually generate:

* Tailored résumés
* Cover letters
* Interview preparation
* Career recommendations
* Learning plans
* Application tracking
* Long-term professional memory

AI Job Hunter therefore becomes one tested, reusable module inside a larger AI-assisted career platform.

Development does not have to follow the milestones in a perfectly sequential order. Small foundational pieces may be implemented early when they clarify the architecture or provide immediate practical value. However, the Professional Knowledge Base remains the foundation for reliable, fact-based document generation.

## Architecture Principles

* Business logic should produce structured data objects.
* Formatting, presentation, and user-interface concerns should remain separate from business logic.
* Deterministic processing should be preferred where an LLM is unnecessary.
* LLM calls should be isolated, testable, and cost-conscious.
* Professional facts should come from a maintained source of truth.
* Generated documents should remain traceable to supporting professional evidence.

## Guiding Principles

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
* Let the Professional Knowledge Base become the foundation for everything else.
