# AI Career Manager
## Workflow Overview (End of Milestone 3)

**Status:** Milestone 3 (Job History & Application Tracking) is functionally complete.
This document summarizes the current architecture, workflows, and the direction of the next milestone.

---

# Current System Workflow

```
             +----------------+
             | User Input     |
             +----------------+
                     |
     +---------------+----------------+
     |                                |
   --file                        --url
     |                                |
 Read file                  Fetch web page
     |                                |
     |                  Extract:
     |                  - Visible text
     |                  - Page title
     |                  - Canonical URL
     |                  - OpenGraph metadata
     |                                |
     +---------------+----------------+
                     |
          Build JobInput object
                     |
      +--------------+---------------+
      |                              |
 original_text               parser_text
 (preserved forever)     (metadata + text)
      |                              |
      |                              |
      +--------------+---------------+
                     |
           Duplicate Detection
                     |
          +----------+----------+
          |                     |
        New Job             Existing Job
          |                     |
          |             --reprocess?
          |              /         \
          |            no           yes
          |            |             |
          |        Stop here     Continue
          |                       processing
          |
          +-------------------------------+
                                          |
                             Store original job
                               in SQLite
                                          |
                         Save original_job.txt
                                          |
                                  Parse JobOpening
                                          |
                          Update parsed fields
                           in database
                                          |
                               Score candidate fit
                                          |
                         Update fit analysis
                            in database
                                          |
                      Generate recommendations
                                          |
                       Generate tailored resume
                                          |
                           Save artifacts
```

---

# Current Persistent Data

Every job now has a permanent database record.

The database currently stores:

- Unique Job ID
- Original job description
- Source (file, URL, examples)
- Source URL
- Description hash
- Parser results
    - title
    - company
    - location
- Fit analysis
    - score
    - recommendation
- Created timestamp
- Updated timestamp

---

# Artifact Directory

Every processed job has its own permanent directory.

Example:

```
outputs/jobs/000123/
```

Contents:

```
original_job.txt
job.json
fit.json
resume_recommendation.json
tailored_resume.md
```

Nothing is overwritten by subsequent jobs.

---

# Duplicate Detection

Duplicate detection currently works using:

- Source URL
- Description hash

Behavior:

New Job

```
Store
Parse
Score
Generate artifacts
```

Duplicate

```
Stop immediately
```

unless

```
--reprocess
```

is specified.

Reprocessing regenerates all parser outputs and resume artifacts while reusing the existing Job ID.

---

# Current URL Processing

Current fetch pipeline:

```
URL
    ↓
Download page
    ↓
Extract

    Requested URL
    Canonical URL
    Page Title
    OpenGraph metadata
    Visible text

    ↓

Build parser input

    ↓

LLM Parser
```

The original page text is preserved exactly.

The parser receives an enriched version containing page metadata.

---

# Current Architecture

The project is now separated into distinct responsibilities.

```
Fetchers
    Retrieve job pages

Formatters
    Prepare parser input
    Generate resumes

Parsers
    Extract structured information

Models
    JobOpening
    FitAnalysis
    ResumeRecommendation
    CandidateProfile
    JobInput
    FetchedJobPage

Database
    SQLite repository
    Duplicate detection
    Persistence

Artifacts
    Permanent outputs
```

Each layer has focused responsibilities and is independently testable.

---

# Testing

Current automated coverage includes:

- Parser unit tests
- Integration parser tests
- URL fetcher tests
- Repository tests
- Database tests
- Resume recommendation tests
- Duplicate detection tests
- Workflow tests
- Regression tests for difficult job descriptions

Current status:

```
66 unit tests
68 total tests
```

(All passing.)

---

# Next Milestone

## Smarter Job Acquisition

The next milestone focuses on improving the quality of extracted job information rather than adding infrastructure.

Current:

```
Visible Text
```

Next:

```
Visible Text

+

Page Title

+

OpenGraph Metadata

+

JSON-LD

+

Structured ATS Metadata
```

---

# JSON-LD Support

Many modern ATS systems publish structured JobPosting data.

Example:

```json
{
    "@type": "JobPosting",

    "title": "...",

    "hiringOrganization": {
        "name": "Applied Systems"
    },

    "employmentType": "FULL_TIME",

    "jobLocation": "...",

    "datePosted": "...",

    "validThrough": "..."
}
```

This information is often more accurate than visible page text.

---

# Provenance Tracking

Long-term objective:

Every extracted field records its origin.

Example:

```
Company

Value:
Applied Systems

Source:
JSON-LD

Confidence:
0.99
```

Instead of storing only values, AI Career Manager will know why it believes each value is correct.

---

# Future Vision

Eventually the workflow becomes:

```
Find Jobs

↓

Acquire

↓

Normalize

↓

Store Permanently

↓

Detect Duplicates

↓

Extract Rich Metadata

↓

LLM Parsing

↓

Fit Analysis

↓

Resume Generation

↓

Application Tracking

↓

Application History

↓

Skill Gap Analysis

↓

Career Recommendations
```

The long-term goal is to transform AI Career Manager from a parser into a complete personal career management system that remembers every opportunity, continuously improves candidate matching, and provides increasingly intelligent guidance throughout the job search.