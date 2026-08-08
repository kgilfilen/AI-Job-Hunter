# Formatters Package

## Directory Overview

The **Formatters** package is responsible for converting structured application
data into textual representations used by downstream components.

It currently serves two distinct formatting roles:

* preparing fetched web-page evidence for job parsing
* rendering candidate information into a tailored Markdown resume

The package does not fetch web pages, invoke AI models, score candidates, persist
data, or manage application history.

### Design Goals

* Separate text presentation from domain logic.
* Produce deterministic output from structured inputs.
* Preserve source facts while changing ordering and emphasis where appropriate.
* Prepare clear, structured evidence for downstream AI parsing.
* Prevent resume formatting from inventing candidate skills or experience.
* Keep rendering concerns isolated from persistence and business workflows.

### Modules

| Module                  | Responsibility                                                               |
| ----------------------- | ---------------------------------------------------------------------------- |
| `job_page_formatter.py` | Converts a `FetchedJobPage` into structured text for downstream job parsing. |
| `resume_formatter.py`   | Converts candidate and job data into a tailored Markdown resume.             |

---

# job_page_formatter.py

## Purpose

This module converts a `FetchedJobPage` into a structured text representation
that can be supplied to the downstream job parser.

It combines several kinds of evidence:

* requested URL
* canonical URL
* page title
* structured JSON-LD job metadata
* general page metadata
* visible page text

Conceptually:

```text
FetchedJobPage
    ↓
job_page_formatter
    ↓
structured parser input
    ↓
job parser / AI interpretation
```

The formatter does not interpret the job posting itself.

Its responsibility is to organize available evidence into a stable,
human-readable format before probabilistic parsing occurs.

---

## Public Interface

The module exposes one public function:

* `build_parser_input()`

---

## Inputs and Outputs

### `build_parser_input(page)`

* Input: `FetchedJobPage`
* Output: formatted string
* Side effects: none

The function combines available page evidence into a single text document.

The resulting structure begins with:

```text
JOB PAGE EVIDENCE

Requested URL: ...
```

Optional sections are included only when relevant data exists.

---

## Output Structure

A typical formatted result may contain:

```text
JOB PAGE EVIDENCE

Requested URL: ...
Canonical URL: ...

Page Title:
...

Structured Job Metadata:
Title: ...
Company: ...
Location: ...
Employment Type: ...
Salary: ...
Date Posted: ...
Valid Through: ...

Page Metadata:
description: ...
og:description: ...
og:site_name: ...
og:title: ...

Visible Page Text:
------------------
...
```

The exact optional sections depend on what was available in the fetched page.

---

## Structured Job Metadata

The formatter currently recognizes the following fields from
`page.job_metadata`:

* title
* company
* location
* employment type
* salary
* date posted
* valid-through date

The entire section is omitted if all structured values are `None`.

Individual missing fields are also omitted.

---

## Salary Formatting

Salary information is assembled from:

* salary currency
* salary value
* salary interval

For example:

```text
USD 120000–140000 per YEAR
```

The salary field is included only when a salary value exists.

Currency and interval are optional.

This module does not calculate salary values. It only renders metadata already
extracted elsewhere.

---

## Page Metadata

General HTML metadata is emitted under:

```text
Page Metadata:
```

Metadata keys are sorted before output.

Values containing only whitespace are ignored.

Sorting provides deterministic output even if the original dictionary order
changes.

---

## Visible Page Text

Visible page text is always appended under:

```text
Visible Page Text:
------------------
```

The formatter assumes that HTML cleanup and visible-text extraction have already
been performed by the Fetchers package.

It does not perform additional HTML parsing.

---

## Dependencies

This module depends on:

* Python typing support
* `FetchedJobPage`

It indirectly consumes:

* `JobMetadata`
* page metadata
* visible text

through the `FetchedJobPage` domain object.

It has no dependency on:

* HTTP requests
* BeautifulSoup
* AI clients
* candidate profiles
* scoring
* resume generation
* repositories
* SQLite
* Streamlit

---

## Behavioral Specifications

* Requested URL is always included.
* Canonical URL is included only when present.
* Page title is included only when present.
* Structured-job metadata is included only when at least one field exists.
* Missing structured fields are omitted.
* Salary is rendered only when a salary value exists.
* Currency precedes the salary value when available.
* Salary interval follows the salary value when available.
* General page metadata keys are sorted.
* Blank metadata values are ignored.
* Visible page text is always included.
* Output sections are separated using blank lines.
* Inputs are not modified.

---

## Invariants

The module aims to guarantee:

* deterministic section ordering
* deterministic metadata ordering
* preservation of source evidence
* no interpretation of job requirements
* no network or persistence side effects
* no mutation of `FetchedJobPage`

---

## Error Behavior

The formatter assumes that the supplied object conforms to the
`FetchedJobPage` contract.

Unexpected object structures or invalid field types may raise ordinary Python
errors.

No errors are deliberately suppressed.

---

## Good Unit-Test Targets

* requested URL always included
* canonical URL included when available
* canonical URL omitted when absent
* page title formatting
* structured metadata section included when data exists
* structured metadata section omitted when empty
* individual missing metadata fields omitted
* salary with currency
* salary without currency
* salary with interval
* page metadata keys sorted
* blank metadata values excluded
* visible page text included
* deterministic complete output

---

## Possible Future Enhancements

* Explicit section-size limits for unusually large web pages.
* Additional structured metadata fields.
* Separate trusted structured evidence from lower-confidence page metadata.
* More explicit delimiters for downstream parsing.
* Diagnostic information about evidence sources.
* Versioning of the parser-input text contract.

---

## Overall Responsibility

`job_page_formatter.py` creates the textual boundary between deterministic web
extraction and downstream probabilistic job parsing.

It does not decide what the evidence means.

It organizes the evidence so that the parser can make that decision from a
consistent representation.

---

# resume_formatter.py

## Purpose

This module renders a candidate profile as a tailored Markdown resume.

Its central rule is that tailoring may change **ordering and emphasis**, but it
must not invent candidate qualifications.

The formatter therefore uses resume recommendations to highlight relevant
existing information while treating the `CandidateProfile` as the factual
source of truth.

Conceptually:

```text
CandidateProfile
JobOpening
ResumeRecommendation
FitAnalysis
        ↓
ResumeFormatter
        ↓
tailored Markdown resume
```

The formatter is deterministic.

The recommendation layer may use probabilistic intelligence to determine what
should receive emphasis, but the formatter controls how that recommendation is
applied to the candidate's existing facts.

---

## Public Interface

The primary public interface is:

```python
ResumeFormatter.format()
```

All remaining methods are formatting and normalization helpers internal to the
class.

---

## Inputs and Outputs

### `ResumeFormatter.format(candidate, job, analysis, recommendations)`

Inputs:

* `CandidateProfile`
* `JobOpening`
* `FitAnalysis`
* `ResumeRecommendation`

Output:

* Markdown resume as a string

Side effects:

* none

The returned text:

* is Markdown
* ends with exactly one newline
* contains only sections supported by available candidate data

The current implementation receives `FitAnalysis` as part of the formatter
contract but does not directly use its contents.

---

## Resume Structure

The formatter may produce:

```text
# Candidate Name

contact information

## Professional Summary

...

## Core Skills

- skill
- skill

## Professional Experience

### Job Title
Company
Location | Dates

- accomplishment
- accomplishment

## Education

- **Degree** — Institution | Location | Date

## Certifications

- **Certification** — Organization | Date
```

Sections with no relevant source data are omitted.

---

## Header

The header may contain:

* candidate name
* email
* phone
* location
* LinkedIn
* GitHub

Only non-empty values are included.

The candidate name is rendered as a Markdown H1.

Contact values are currently placed on separate lines.

---

## Professional Summary

The formatter starts with the candidate's existing summary when one is
available.

It may then add job-specific context.

Recommended skills are compared against skills already present in the candidate
profile.

When both a target job title and verified matching skills exist, the formatter
adds a sentence similar to:

```text
Relevant strengths for the <job title> role include <skills>.
```

At most five matching skills are used in that sentence.

If a job title exists but no recommended skills match the candidate profile, the
formatter may instead add:

```text
Seeking to apply this experience to the <job title> role.
```

This behavior changes presentation but does not add unsupported candidate
qualifications.

---

## Core Skills

The formatter renders candidate core skills under:

```text
## Core Skills
```

Skills listed in `recommendations.skills_to_emphasize` are moved toward the
beginning when those skills already exist in the candidate's core-skills list.

Remaining candidate skills retain their original relative order.

Recommended skills that are not present in the candidate profile are not added.

Duplicate skills are removed using normalized comparison.

---

## Professional Experience

Candidate experience entries remain in their existing order.

Within each experience entry, however, highlights may be reordered.

Highlights containing recommended emphasis terms are placed before remaining
highlights.

The highlight text itself is not rewritten.

This preserves factual content while making relevant evidence easier to see.

---

## Highlight Matching

Recommended skill terms are normalized before comparison.

A highlight is considered emphasized when a normalized recommendation term
occurs within the normalized highlight text.

For example, a recommendation for:

```text
automation
```

may prioritize a candidate highlight containing:

```text
Built automation infrastructure for regression testing.
```

Matching affects order only.

It does not modify the bullet text.

---

## Education

Education entries include:

* degree
* optional field of study
* institution
* location
* graduation date

Available detail values are joined using:

```text
 |
```

The degree is rendered in Markdown bold.

---

## Certifications

Certification entries may include:

* certification name
* issuing organization
* issue date
* expiration date

Expiration information is appended when available.

Missing optional values are omitted.

---

## Text Normalization

The formatter uses normalization for comparison and deduplication.

Normalization:

* converts text to lowercase
* strips surrounding whitespace
* collapses repeated whitespace

This allows values such as:

```text
Python
python
 PYTHON
```

to be treated as equivalent for matching purposes.

The original candidate spelling is preserved in rendered output.

---

## Duplicate Handling

`_unique_preserving_order()` removes normalized duplicates while preserving the
first original representation encountered.

This is used when determining matched and prioritized skills.

---

## Detail Joining

`_join_details()`:

* accepts optional string values
* removes empty values
* strips whitespace
* joins remaining values with `|`

This provides consistent formatting across education, experience, and
certification information.

---

## Dependencies

This module depends on:

* `CandidateProfile`
* `Experience`
* `Education`
* `Certification`
* `JobOpening`
* `FitAnalysis`
* `ResumeRecommendation`

It has no direct dependency on:

* AI clients
* HTTP requests
* web fetching
* database repositories
* artifact persistence
* Streamlit

---

## Behavioral Specifications

* Candidate facts are treated as authoritative.
* Recommended skills are never added unless they already exist in candidate
  skills.
* Candidate experience bullet text is not rewritten.
* Recommendations may alter ordering and emphasis.
* Core skills matching is case-insensitive.
* Duplicate skills are removed using normalized comparison.
* Candidate skill spelling is preserved in output.
* Experience entries retain their original order.
* Recommended-skill experience highlights are placed first.
* Empty sections are omitted.
* Optional detail values are omitted rather than rendered as placeholders.
* The final resume ends with one newline.
* Input domain objects are not modified.

---

## Invariants

The module aims to guarantee:

* no fabricated candidate skills
* no fabricated candidate experience
* no rewriting of factual experience highlights
* deterministic output for the same inputs
* stable section ordering
* stable relative ordering when no recommendation changes priority
* preservation of original candidate display text
* independence from persistence and UI layers

---

## Error Behavior

The formatter assumes valid domain objects.

Unexpected field types or malformed model data may raise ordinary Python errors.

The formatter does not catch or suppress formatting errors.

Missing optional candidate information normally causes the affected section or
value to be omitted rather than producing an exception.

---

## Good Unit-Test Targets

### Complete Resume

* expected section order
* Markdown formatting
* final newline
* deterministic output

### Header

* complete contact information
* partial contact information
* missing name
* missing all contact information

### Summary

* candidate summary retained
* matching recommended skills added
* maximum five skills added to summary
* job title with no skill matches
* missing job title
* missing candidate summary

### Skills

* recommended existing skills moved first
* unsupported recommended skills ignored
* case-insensitive matching
* duplicate skill removal
* remaining skill order preserved

### Experience

* experience order preserved
* matching highlights prioritized
* nonmatching highlights retain order
* experience bullet text unchanged
* location/date detail formatting
* empty highlight lists

### Education

* degree with field of study
* degree without field of study
* partial detail information
* multiple education entries

### Certifications

* complete certification
* certification without expiration
* certification with expiration
* missing optional organization/date values

### Utilities

* whitespace normalization
* case normalization
* detail joining
* order-preserving deduplication
* empty term handling

---

## Possible Future Enhancements

* Decide whether `FitAnalysis` should directly influence formatting or be removed
  from the formatter contract.
* More sophisticated but still factual experience prioritization.
* Configurable resume section ordering.
* Alternative Markdown or plain-text layouts.
* Multiple resume templates.
* ATS-specific rendering.
* Controlled line or page-length targets.
* Explicit resume-format versioning.
* Separate presentation templates from prioritization logic.

---

## Package Architectural Boundary

The Formatters package sits between structured domain data and textual
representations.

For job parsing:

```text
deterministic fetched evidence
        ↓
job_page_formatter
        ↓
structured prompt input
        ↓
probabilistic interpretation
```

For resume generation:

```text
probabilistic recommendation
        +
verified CandidateProfile
        ↓
deterministic ResumeFormatter
        ↓
tailored resume
```

This distinction is important.

AI may recommend that a skill or accomplishment deserves greater emphasis.

The formatter decides how to apply that recommendation according to explicit
rules while preventing unsupported facts from entering the resume.

---

## Overall Responsibility

The Formatters package turns structured internal data into stable textual
representations.

`job_page_formatter.py` prepares page evidence for downstream parsing.

`resume_formatter.py` renders a tailored resume from verified candidate data and
resume recommendations.

Both modules are intentionally deterministic and contain no network,
persistence, or AI-client behavior.
