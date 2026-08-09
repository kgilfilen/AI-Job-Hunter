# Scoring

The `scoring` package evaluates how well a structured `JobOpening` matches a `CandidateProfile`.

The current implementation is deterministic: the same job and candidate profile produce the same score, strengths, concerns, matched skills, missing skills, and recommendation.

## Files

### `fit_scorer.py`

Contains the current fit-scoring implementation.

Its main entry point is:

```python
score_job(
    job: JobOpening,
    profile: CandidateProfile,
) -> FitAnalysis
```

The function evaluates several dimensions of fit and returns a structured `FitAnalysis`.

### `skill_matcher.py`

Currently empty.

The skill-normalization and matching logic is presently implemented inside `fit_scorer.py`. This file may provide a natural future home for that logic if skill matching becomes more sophisticated or reusable.

## Scoring Flow

```text
JobOpening
    |
    +--> title
    +--> remote status
    +--> clearance requirement
    +--> required skills
    +--> preferred skills
              |
              v
        deterministic rules
              ^
              |
CandidateProfile
    |
    +--> target titles
    +--> remote preference
    +--> clearance status
    +--> core skills
              |
              v
          FitAnalysis
              |
              +--> overall score
              +--> recommendation
              +--> strengths
              +--> concerns
              +--> matched skills
              +--> missing skills
```

## Starting Score

Every job begins with a neutral baseline score of:

```text
50
```

Adjustments are then applied for title alignment, work arrangement, security clearance, required skills, and preferred skills.

The final result is clamped to the range:

```text
0–100
```

## Title Match

The scorer compares the job title against the candidate's `target_titles`.

If one or more target titles occur within the job title, the longest matching target title is selected and the score receives:

```text
+15
```

The match is also recorded as a strength.

## Security Clearance

If the job requires a security clearance and the candidate profile does not indicate an active clearance, the score receives:

```text
-25
```

A corresponding concern is added to the analysis.

## Remote Preference

If the candidate has a remote-work preference and it matches the job's remote status, the score receives:

```text
+10
```

Flexible arrangements such as remote-or-hybrid can receive:

```text
+8
```

The matching work arrangement is recorded as a strength.

## Required Skills

Required skills receive the largest variable scoring adjustment.

The scorer compares the job's required skills against the candidate's `core_skills`.

The required-skill match ratio is calculated as:

```text
matched required skills
-----------------------
all required skills
```

That ratio is converted to an adjustment ranging approximately from:

```text
-20 to +20
```

using:

```python
round((required_match_ratio * 40) - 20)
```

This means:

```text
0% match   -> -20
50% match  ->   0
100% match -> +20
```

Matched required skills are recorded as strengths.

Missing required skills are recorded as concerns.

## Preferred Skills

Preferred skills are also compared against the candidate's `core_skills`.

Each matched preferred skill adds:

```text
+2
```

up to a maximum preferred-skill bonus of:

```text
+10
```

Matched preferred skills are recorded as strengths.

Missing preferred skills are preserved in the returned `FitAnalysis`, but they do not currently reduce the numerical score.

## Skill Normalization

Before comparison, selected skill aliases are normalized to canonical names.

Current examples include:

```text
REST APIs    -> REST API
RESTful API  -> REST API
py test      -> pytest
playwright   -> Playwright
selenium     -> Selenium
python       -> Python
```

Skill matching then uses set intersection and difference to identify matched and missing skills.

Unknown skills are stripped of surrounding whitespace but otherwise preserved.

## Recommendation Thresholds

After scoring, the numerical score is translated into one of three recommendations:

```text
80–100  -> Apply
60–79   -> Consider
0–59    -> Pass
```

The recommendation values come from the shared `Recommendation` enum.

## FitAnalysis Output

`score_job()` returns a `FitAnalysis` containing:

- overall score
- recommendation
- strengths
- concerns
- notes
- matched required skills
- missing required skills
- matched preferred skills
- missing preferred skills

This keeps the numerical score separate from the supporting explanation.

## Deterministic Design

The scoring layer does not call an AI model.

Its job is to answer:

> Given the structured facts already extracted from the job and candidate profile, how strong is the match according to explicit scoring rules?

This makes the scoring behavior:

- reproducible
- testable
- inspectable
- adjustable without changing parser behavior
- easier to explain to a user

The parser layer may use probabilistic AI extraction, but once a `JobOpening` reaches scoring, the score itself is produced by deterministic software.

## Current Limitations

The current scoring model is intentionally simple and transparent.

Notable limitations include:

- skill matching uses a small manually maintained normalization map
- semantic equivalents are not recognized unless explicitly mapped
- only `profile.core_skills` are used for required and preferred skill matching
- candidate experience history is not searched for additional skill evidence
- title matching is substring-based rather than semantic
- remote preference logic is based on string comparison
- no weighting is currently applied for years of experience
- industries, education, certifications, salary, relocation preference, and responsibilities do not currently affect the score
- all required skills are treated as equally important
- confidence metadata from AI parsers does not currently affect scoring

These limitations make future scoring improvements straightforward to identify while keeping the present behavior easy to understand and test.

## Possible Future Refactoring

If skill matching grows beyond the current normalization map and set comparison, `skill_matcher.py` is a natural place to move:

```text
SKILL_NORMALIZATION_MAP
normalize_skill()
match_skills()
```

That would keep `fit_scorer.py` focused on weighting and recommendation logic while allowing skill matching to evolve independently.

Until that separation is useful, keeping the current implementation together is also reasonable.
