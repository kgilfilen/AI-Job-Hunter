# AI Job Hunter - Project Timeline

## Day 1 – Project Foundation

* Created the initial repository structure.
* Established the project vision: use AI to analyze job descriptions rather than simply search for jobs.
* Configured the Python development environment.
* Connected the project to Git and GitHub.
* Created the initial README and architecture documentation.

## Day 2 – LLM Parsing

* Integrated the OpenAI API.
* Built the first LLM parser for extracting job titles.
* Expanded the design into multiple specialized parsers rather than one large prompt.
* Added parsers for:
    * Company
    * Location
    * Employment Type
    * Remote Status
    * Security Clearance
* Standardized parser outputs to include:
    * Extracted value
    * Confidence
    * Evidence
    * Warning

## Day 3 – Domain Models and Scoring

* Introduced the JobOpening domain model.
* Consolidated parser results into a single object.
* Added JSON persistence.
* Created:
    * CandidateProfile
    * FitAnalysis
* Built the first rule-based scoring engine.
* Introduced recommendation enums (Apply, Consider, Pass).
* Separated factual job information from candidate-specific fit analysis.

## Day 4 – Testing and Skill Extraction

* Established separate unit and integration test suites.
* Added automated tests for:
    * Domain models
    * Rule-based scoring
    * Recommendation validation
    * Default values
* Added parsers for:
    * Required Skills
    * Preferred Skills
    * Responsibilities
* Improved parser prompts through iterative testing using real job descriptions.
* Began designing the project as a future machine learning dataset by preserving structured features extracted from job postings.

## Current Status

The application currently performs the following pipeline:

Job Description

↓

LLM Feature Extraction

↓

JobOpening

↓

Rule-Based Fit Scoring

↓

FitAnalysis

↓

Structured JSON Output

## Planned Next Milestones

* Improve skill-based scoring.
* Normalize equivalent technology names.
* Build resume strategy generation.
* Add LLM-assisted scoring.
* Collect a larger dataset for future machine learning experiments.
* Develop ranking models using historical job data and application outcomes.

