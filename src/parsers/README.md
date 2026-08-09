# Parsers

The `parsers` package converts unstructured job-description text into the structured data used by the AI Career Manager.

The package uses a hybrid approach:

- AI-assisted parsers interpret job-description language and return structured results with confidence, evidence, and warnings.
- Deterministic normalizers standardize selected values and provide rule-based fallback behavior.
- `job_opening_parser.py` orchestrates the individual parsers and assembles the final `JobOpening` model.

This keeps extraction responsibilities small and explicit while giving the rest of the application a consistent representation of each job.

## Parsing Flow

```text
Job description text
        |
        v
+----------------------------+
| Individual field parsers   |
|                            |
| title                      |
| company                    |
| location                   |
| remote status              |
| employment type            |
| security clearance         |
| required skills            |
| preferred skills           |
| responsibilities           |
+----------------------------+
        |
        v
Normalization / fallback
        |
        v
JobOpening
        |
        +--> parser metadata
             confidence
             evidence
             warning
```

Each AI-assisted parser is responsible for one concern rather than asking one large prompt to interpret the entire posting. This makes parser behavior easier to test, inspect, refine, and troubleshoot independently.

## Parser Orchestration

### `job_opening_parser.py`

This is the main coordinator for the parsing subsystem.

`parse_job_opening()` sends the job text through the field-specific parsers for:

- title
- company
- location
- remote status
- employment type
- security clearance
- required skills
- preferred skills
- responsibilities

The results are assembled into a `JobOpening`.

The parser also preserves metadata from each extraction result:

- `confidence`
- `evidence`
- `warning`

This provides traceability into how individual values were derived instead of retaining only the final parsed value.

For employment type, the orchestrator first normalizes the AI-extracted value. If no employment type was extracted, it falls back to deterministic detection from the source text.

`parse_job_opening_file()` is a convenience wrapper that reads a job-description file and passes its contents to `parse_job_opening()`.

## Field Parsers

### `title_parser.py`

Extracts the official job title.

Returns a `JobTitleResult` containing:

- title
- confidence
- supporting evidence
- optional warning

The prompt emphasizes using the title actually present in the posting and avoiding invented values.

---

### `company_parser.py`

Extracts the hiring company name.

Returns a `CompanyNameResult`.

The parser includes additional rules for ambiguous postings, including recruiter or vendor language, client references, divisions, business units, legal statements, career URLs, email domains, and repeated brand references.

Its goal is to identify the actual hiring company when the posting provides enough evidence, while returning `None` when the employer cannot be established reliably.

---

### `location_parser.py`

Extracts the physical job location.

Returns a `LocationResult`.

The parser distinguishes physical location from remote or hybrid work status and avoids inventing a location when none is supplied.

---

### `remote_status_parser.py`

Extracts the work-location arrangement.

Returns a `RemoteStatusResult`.

Recognized concepts include:

- remote
- hybrid
- onsite
- combinations of remote and hybrid
- flexible arrangements

Remote status is intentionally separate from physical location.

---

### `employment_type_parser.py`

Uses AI-assisted extraction to identify the employment arrangement.

Returns an `EmploymentTypeResult`.

Expected categories include:

- full-time
- part-time
- contract
- contract-to-hire
- temporary
- internship

The extracted result is subsequently passed through deterministic normalization by the main parser.

---

### `security_clearance_parser.py`

Extracts security-clearance requirements.

Returns a `SecurityClearanceResult` containing:

- whether clearance is required
- clearance level
- confidence
- evidence
- warning

The parser recognizes common clearance levels such as Public Trust, Secret, Top Secret, TS/SCI, and polygraph-related requirements. Language requiring the candidate to be able to obtain a clearance is treated as a clearance requirement.

---

### `required_skills_parser.py`

Extracts skills that the posting presents as required or strongly expected.

Returns a `RequiredSkillsResult`.

The parser can identify technical tools, languages, frameworks, platforms, testing skills, domain knowledge, and methodologies. It is instructed to produce concise normalized skill names rather than copying qualification sentences directly.

---

### `preferred_skills_parser.py`

Extracts skills described as preferred, desired, beneficial, nice-to-have, or equivalent.

Returns a `PreferredSkillsResult`.

Required and preferred skills are deliberately parsed separately so downstream fit analysis can distinguish between mandatory qualifications and secondary advantages.

---

### `responsibilities_parser.py`

Extracts the primary responsibilities of the position.

Returns a `ResponsibilitiesResult`.

Responsibilities are reduced to concise action statements, duplicate or overlapping items are removed, and qualifications are excluded. The parser targets approximately 5–10 major responsibilities rather than reproducing the complete job description.

## Deterministic Normalization

### `employment_type_normalizer.py`

Provides deterministic normalization and fallback detection for employment type.

`normalize_employment_type()` maps common variations to canonical values, for example:

```text
full time   -> full-time
fulltime    -> full-time
contractor  -> contract
temp        -> temporary
intern      -> internship
```

`detect_employment_type()` searches the source job text for explicit employment-type language using regular expressions.

This creates a useful hybrid boundary: AI can interpret the posting first, while straightforward textual patterns can be handled deterministically when the AI result is absent.

---

### `job_title_normalizer.py`

Provides deterministic normalization for known job-title aliases.

For example:

```text
Sr SDET     -> Senior Software Development Engineer in Test
Senior SDET -> Senior Software Development Engineer in Test
SDET        -> Software Development Engineer in Test
```

Unknown titles are cleaned of unnecessary whitespace and otherwise preserved.

This normalizer is currently independent of the main `parse_job_opening()` orchestration and can be used where canonical job titles are needed.

## Result Pattern

Most AI-assisted field parsers follow the same basic contract:

```text
parsed value(s)
confidence
evidence
warning
```

This pattern is important because AI output is probabilistic. The application does not need to treat every extracted field as equally certain.

`job_opening_parser.py` carries this information forward in `JobOpening.parser_metadata`, allowing later code, tests, debugging tools, or user-facing features to inspect the basis and confidence of an extraction.

## Architectural Boundary

The parser layer is responsible for answering:

> What structured facts can be extracted from this job description?

It is not responsible for answering:

> Is this a good job for this candidate?

That second question belongs to the analysis layer, where the resulting `JobOpening` can be compared with `CandidateProfile`.

Keeping those responsibilities separate means the same parsed job can later support fit scoring, resume tailoring, application tracking, reporting, and other workflows without reparsing the original posting.

## Design Direction

The current parser architecture deliberately combines probabilistic intelligence with deterministic software.

AI-assisted parsing is useful where job postings contain inconsistent wording, ambiguous structure, or information scattered throughout natural-language text. Deterministic code is preferable where values can be normalized or recognized reliably with explicit rules.

As the project evolves, additional deterministic extraction can be added where patterns prove stable, while AI parsing can remain focused on fields that genuinely require language interpretation.
