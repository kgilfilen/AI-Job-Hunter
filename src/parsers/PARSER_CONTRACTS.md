# Parser Contracts

This document defines the expected behavioral contracts for the `parsers` package.

The goal is to make parser behavior predictable for downstream code and tests, especially when source text is incomplete, ambiguous, or interpreted with uncertainty.

The Python source remains the authoritative implementation. This document describes the intended contract represented by the current code.

## Scope

The parser layer is responsible for converting job-description text into structured job facts.

It is not responsible for:

- candidate-specific fit decisions
- resume recommendations
- application tracking
- database persistence
- web retrieval
- user-interface behavior

Those responsibilities belong to other layers of the application.

## Common AI Parser Result Pattern

Most AI-assisted parsers return a dataclass containing:

```text
parsed value or values
confidence
evidence
warning
```

Examples include:

- `JobTitleResult`
- `CompanyNameResult`
- `LocationResult`
- `RemoteStatusResult`
- `EmploymentTypeResult`
- `SecurityClearanceResult`
- `RequiredSkillsResult`
- `PreferredSkillsResult`
- `ResponsibilitiesResult`

### `confidence`

`confidence` is a floating-point value intended to represent the parser's confidence in the extraction.

Current parser code defaults missing confidence values to `0.0`.

Downstream code should not assume that all parsed fields have equal reliability.

### `evidence`

`evidence` contains supporting text or a short phrase from the job description when available.

Its purpose is traceability: downstream code or a user can inspect why a value was extracted.

### `warning`

`warning` is optional explanatory information for ambiguity or unusual conditions.

Examples include:

- multiple possible values
- unclear company identity
- conflicting information in a posting

A missing warning does not necessarily imply perfect certainty.

## Missing Information

Parsers should not invent values that are not supported by the job description.

The representation of missing information depends on the field type.

### Scalar Optional Fields

Use `None` when a scalar value cannot be established.

Examples:

```text
title = None
company = None
location = None
remote status = None
employment type = None
clearance level = None
```

### Collection Fields

Use an empty list when no qualifying items are found.

Examples:

```text
required_skills = []
preferred_skills = []
responsibilities = []
```

### Boolean Clearance Requirement

The security-clearance parser currently uses:

```text
required = False
level = None
```

when no clearance requirement is present.

This means the current model does not distinguish between:

```text
"No clearance is required."
```

and:

```text
"The posting says nothing about clearance."
```

Both produce `required = False`.

If that distinction becomes important later, the contract or model should be expanded explicitly rather than inferred downstream.

## Ambiguous Information

When several plausible values appear, the AI parser is generally instructed to:

1. choose the most likely official value,
2. preserve supporting evidence,
3. describe ambiguity in `warning`.

For fields where the prompt does not support a reliable choice, returning `None` is preferable to inventing a value.

Downstream code should therefore treat a warning as meaningful parser metadata rather than as an error by itself.

## Parser Metadata Preservation

`job_opening_parser.py` converts each parser result into metadata containing:

```text
confidence
evidence
warning
```

and stores that information in `JobOpening.parser_metadata`.

The current metadata keys are:

```text
title
company
location
remote_status
employment_type
security_clearance
required_skills
preferred_skills
responsibilities
```

This allows the final `JobOpening` to retain traceability after the individual result objects are no longer available.

## JobOpening Assembly Contract

`parse_job_opening(job_text, source_file)` currently performs the following sequence:

```text
verify title
verify company
verify location
verify remote status
verify employment type
verify security clearance
verify required skills
verify preferred skills
verify responsibilities
normalize employment type
apply employment-type fallback if needed
construct JobOpening
```

The resulting `JobOpening` contains the extracted values plus parser metadata.

Current parser assembly does not populate:

```text
salary_range
notes
```

Those fields are currently initialized as:

```text
salary_range = None
notes = []
```

## Deterministic Normalization

Some extracted values are subject to deterministic normalization.

### Employment Type

The AI parser first extracts employment type.

The result is passed to:

```python
normalize_employment_type()
```

Common variants are converted to canonical values such as:

```text
full time   -> full-time
fulltime    -> full-time
part time   -> part-time
contractor  -> contract
temp        -> temporary
intern      -> internship
```

If the normalized AI result is `None`, the parser uses:

```python
detect_employment_type(job_text)
```

to search the source text deterministically.

Employment type is currently the only field in `parse_job_opening()` with this explicit deterministic fallback.

### Job Title

`job_title_normalizer.py` defines deterministic normalization for selected aliases such as SDET titles.

However, the current `parse_job_opening()` flow does not invoke `normalize_job_title()`.

Therefore, downstream code should not assume that titles returned by `parse_job_opening()` have passed through the title normalizer.

## AI Output Contract

The AI-assisted parsers request valid JSON and then pass the returned text directly to `json.loads()`.

The current implementation expects the model response to:

1. be valid JSON,
2. contain fields compatible with the parser's result dataclass,
3. provide values that can be converted to the expected Python types.

For example, confidence is converted with:

```python
float(data.get("confidence", 0.0))
```

## Current Failure Behavior

The parser layer currently does not define a shared recovery mechanism for malformed AI responses.

If the OpenAI request fails, the returned text is invalid JSON, or a returned value cannot be converted as expected, the individual parser may raise an exception.

There is currently no shared parser exception type, retry policy, JSON-repair step, or default fallback result for these failures.

This is an important distinction:

```text
Missing information in a valid parsing result
```

is handled by `None`, `False`, or `[]`.

But:

```text
Failure to obtain or decode a valid AI result
```

is not currently converted into one of those normal missing-value states.

Downstream callers should therefore not assume that `parse_job_opening()` always returns a `JobOpening`.

## File Parsing Contract

`parse_job_opening_file(path)`:

1. reads the file as UTF-8 text,
2. passes the complete contents to `parse_job_opening()`,
3. uses `path.name` as `source_file`.

File-reading errors are not currently caught inside this function.

## Parser Independence

Each field parser is intended to answer a narrowly scoped extraction question.

For example:

```text
title_parser.py             -> What is the job title?
company_parser.py           -> What company is hiring?
location_parser.py          -> What is the physical location?
required_skills_parser.py   -> Which skills are required?
```

A parser should not perform candidate-specific reasoning.

For example, `required_skills_parser.py` should determine which skills the employer requires, not whether the candidate possesses those skills.

That comparison belongs in later analysis.

## Deterministic vs. Probabilistic Behavior

The parser package intentionally contains both deterministic and probabilistic components.

### Probabilistic

AI-assisted parsers handle natural-language interpretation where postings may be inconsistent, ambiguous, or poorly structured.

### Deterministic

Normalizers and rule-based detection handle transformations that can be implemented reliably with explicit software rules.

The preferred direction is:

```text
Use deterministic logic when the rule is stable and explicit.
Use AI when interpretation of natural language is genuinely required.
```

Adding deterministic behavior should not silently change the meaning of an existing parser field. Changes should be covered by tests and reflected in the parser documentation.

## Contract Changes

A parser contract should be considered changed when any of the following changes:

- result dataclass fields
- expected value types
- allowed categorical values
- missing-value behavior
- normalization behavior
- deterministic fallback behavior
- parser metadata structure
- exception or retry behavior
- major prompt interpretation rules

When a parser contract changes:

1. update the implementation,
2. update or add tests,
3. update `PROMPTS.md` when prompt behavior changes,
4. update this document when downstream expectations change.

## Current Known Contract Limitations

The current parser implementation has several intentionally visible limitations:

- AI response failures are not handled through a shared recovery mechanism.
- Security-clearance absence and an explicit "no clearance required" statement both map to `required = False`.
- Employment type has deterministic fallback behavior, while other parsed fields generally do not.
- The job-title normalizer exists but is not currently part of the main `parse_job_opening()` pipeline.
- Salary extraction is not currently implemented by the main parser.
- Parser metadata records confidence, evidence, and warnings but does not currently enforce thresholds or alter behavior based on confidence.

These are not necessarily defects. They identify places where future behavior should be added deliberately rather than assumed.
