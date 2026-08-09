# Resume

The `resume` package generates deterministic resume-tailoring recommendations from structured job and candidate data.

Unlike the parser layer, this package does not call an AI model. It works from existing `JobOpening`, `FitAnalysis`, and `CandidateProfile` data and produces a `ResumeRecommendation`.

Its central rule is:

> Recommend emphasis and positioning, but do not invent experience.

## `resume_recommender.py`

The main entry point is:

```python
recommend_resume_changes(
    job: JobOpening,
    fit_analysis: FitAnalysis,
    candidate: CandidateProfile,
) -> ResumeRecommendation
```

The function compares the job's required and preferred skills with the skills represented in the candidate profile, then builds structured recommendations for tailoring a resume.

## Inputs

The recommender uses three structured inputs.

### `JobOpening`

Provides job-specific information such as:

- title
- required skills
- preferred skills
- remote status
- security-clearance requirements

### `FitAnalysis`

Provides the broader candidate/job assessment, including:

- overall fit score
- concerns identified during fit analysis

### `CandidateProfile`

Provides candidate information used by the recommender, including:

- core skills
- preferred skills
- security-clearance status

The current implementation collects candidate skills from `core_skills` and `preferred_skills`.

## Output

The function returns a `ResumeRecommendation`.

Current recommendation categories are:

- `summary_changes`
- `skills_to_emphasize`
- `experience_to_highlight`
- `keywords_to_add`
- `keywords_missing`
- `possible_concerns`

## Recommendation Flow

```text
JobOpening
    |
    | required skills
    | preferred skills
    v
Skill comparison <------ CandidateProfile
    |
    +--> matched skills
    |
    +--> missing skills
    |
    v
ResumeRecommendation
    |
    +--> summary changes
    +--> skills to emphasize
    +--> keywords to add
    +--> missing keywords
    +--> experience areas to highlight
    +--> possible concerns
          ^
          |
      FitAnalysis
```

## Skill Matching

The recommender performs case-insensitive, whitespace-normalized skill comparison.

For example, values that differ only by capitalization or extra whitespace compare as the same skill.

Matched required and preferred skills are combined into:

```text
skills_to_emphasize
```

Those same matched skills are also copied into:

```text
keywords_to_add
```

Missing required and preferred skills are combined into:

```text
keywords_missing
```

Duplicate values are removed while preserving their original order.

## Summary Recommendations

The recommender may suggest changes to the professional summary based on the job.

Current behavior includes:

- aligning the summary with the target job title without changing the candidate's actual title
- placing the strongest matching skills near the top
- mentioning successful remote collaboration when the job is remote

These are positioning recommendations rather than generated claims about experience.

## Experience Recommendations

Matched skills are grouped into broader experience categories.

Current categories include:

- Python automation
- browser and UI automation
- API testing and service integration
- CI/CD and automated delivery
- containerized testing
- cloud-based testing and infrastructure
- performance and load testing
- AI, machine-learning, or LLM integration
- technical leadership and framework ownership

When one or more matched skills fall into a category, the recommender suggests highlighting measurable accomplishments involving that area.

For example, matching `Python` or `pytest` can produce a recommendation to highlight measurable Python automation accomplishments.

The recommender does not create those accomplishments. It only identifies areas of existing experience that may deserve stronger emphasis.

## Concerns

The recommender also records issues that should not be hidden or exaggerated.

### Missing Required Skills

When required skills are missing, it explicitly advises against claiming them.

Instead, the recommendation is to address gaps through:

- adjacent experience
- transferable skills
- current learning

### Security Clearance

If the job requires a security clearance and the candidate profile does not indicate one, that requirement is added as a concern.

### Existing Fit Concerns

Concerns already identified by `FitAnalysis` are carried forward into the resume recommendation.

### Low Fit Score

When the overall fit score is below 60, the recommender warns that resume tailoring may not be worth the effort without first reconsidering the application.

## Deterministic Design

`resume_recommender.py` is intentionally deterministic.

Given the same:

```text
JobOpening
CandidateProfile
FitAnalysis
```

it should produce the same recommendation output.

This makes the recommender straightforward to unit test and keeps resume guidance grounded in known candidate data.

The package does not independently interpret the original job description and does not call an AI model.

## Truthfulness Boundary

A central design constraint is that the recommender must not turn a job requirement into a candidate claim.

For example:

```text
Job requires Kubernetes
Candidate profile does not contain Kubernetes
```

should result in a missing-keyword or concern indication, not a recommendation to add Kubernetes as candidate experience.

Similarly, experience recommendations are phrased as areas to highlight only when related skills already appear in the candidate profile.

This boundary helps keep resume tailoring useful without creating unsupported qualifications.

## Current Limitations

The current implementation intentionally uses relatively simple matching and recommendation rules.

Notable limitations include:

- skill matching is based on normalized exact strings rather than aliases or semantic similarity
- candidate skills are currently drawn only from `core_skills` and `preferred_skills`
- experience history is not searched directly for additional skill evidence
- category detection uses keyword matching against the combined matched-skill text
- recommendations do not yet identify specific candidate experience entries or accomplishments to use
- the recommender does not generate a rewritten resume

These limitations leave room for later expansion while keeping the current behavior predictable and testable.

## Architectural Boundary

The resume package answers:

> Given what we already know about this candidate and this job, what truthful parts of the resume should receive more or less emphasis?

It does not answer:

> What does the job posting say?

That belongs to the parser layer.

It also does not answer:

> How strong is the candidate/job match overall?

That belongs to fit analysis.

Keeping these responsibilities separate allows resume-tailoring logic to evolve without coupling it directly to job parsing or candidate-fit scoring.
