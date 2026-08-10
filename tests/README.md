# Tests

The test suite verifies the AI Career Manager at two primary levels:

* **Unit tests** validate deterministic components and individual application boundaries in isolation.
* **Integration tests** validate workflows that cross component boundaries, including tests that use the live AI parser.

The suite also contains reusable helpers and representative job-description data used for parser regression and integration testing.

## Directory Structure

```text
tests/
├── conftest.py
├── helpers/
│   ├── helpers.py
│   └── job_test_data.py
├── integration/
│   ├── parsers/
│   │   └── test_job_opening_parser.py
│   ├── scoring/
│   │   └── test_fit_scorer.py
│   ├── test_job_opening_integration.py
│   └── test_resume_generation.py
├── test_data/
│   └── jobs/
│       └── ...
└── unit/
    ├── artifacts/
    ├── database/
    ├── fetchers/
    ├── formatters/
    ├── models/
    ├── parsers/
    ├── resume/
    ├── scoring/
    ├── services/
    ├── test_main.py
    └── test_profile_loader.py
```

## Unit Tests

Unit tests are located under:

```text
tests/unit/
```

They primarily exercise deterministic behavior without making live AI API calls.

The unit suite covers:

* job and application persistence
* duplicate-job detection
* job metadata extraction
* web-page acquisition behavior
* model construction and validation
* parser wrappers and deterministic parser utilities
* employment-type normalization
* deterministic fit scoring
* resume recommendations
* resume formatting
* generated job artifacts
* profile loading and persistence
* job and profile services
* selected CLI/application behavior

SQLite repository tests use isolated temporary databases created through pytest's `tmp_path` fixture. This allows real SQL constraints and persistence behavior to be tested without modifying the application's normal database.

For example, repository tests verify behavior such as:

* storing and retrieving jobs
* rejecting invalid data
* updating parsed job information
* deduplicating jobs by source URL and description hash
* creating and updating applications
* enforcing application foreign-key and uniqueness constraints

## Integration Tests

Integration tests are located under:

```text
tests/integration/
```

These tests verify that multiple application components work together correctly.

Important integration boundaries include:

```text
job description
      ↓
AI parser
      ↓
JobOpening
      ↓
deterministic scoring
      ↓
FitAnalysis
```

and:

```text
CandidateProfile
      +
JobOpening
      +
FitAnalysis
      ↓
resume recommendation
      ↓
resume formatter
      ↓
Markdown resume
```

Integration tests therefore focus on behavior across subsystem boundaries rather than repeating deterministic unit-test coverage.

## Live AI Tests

Tests that make real AI API calls are marked:

```python
@pytest.mark.live_ai
```

When every test in a module uses the live AI parser, the entire module may be marked:

```python
pytestmark = pytest.mark.live_ai
```

Live-AI tests are intentionally separated from ordinary deterministic tests because they have different characteristics:

* they require API access and credentials
* they incur API usage
* they are slower than deterministic tests
* their results may contain limited probabilistic variation
* they may be affected by rate limits or external service availability

Assertions in live-AI tests should therefore verify important structural or semantic behavior without unnecessarily depending on fragile wording.

## Reusing Live AI Results

Live AI calls should not be repeated when multiple tests can examine the same parsed result.

Module-scoped pytest fixtures are used for this purpose:

```python
@pytest.fixture(scope="module")
def job_opening():
    return parse_job_opening_file(...)
```

The first test that requires the fixture causes the job to be parsed. Pytest then reuses that result for other tests in the same module.

Fixtures may also depend on other fixtures:

```python
@pytest.fixture(scope="module")
def fit_analysis(job_opening, profile):
    return score_job(job_opening, profile)
```

This approach reduces:

* API usage
* test execution time
* rate-limit exposure
* unnecessary probabilistic variation between related assertions

Live API calls should generally occur during fixture or test execution rather than at module import time.

## Test Data

Representative job descriptions are stored under:

```text
tests/test_data/jobs/
```

These files provide stable inputs for parser regression and integration testing.

They represent different job-description characteristics, including:

* different employers and job titles
* explicit employment types
* security-clearance requirements
* remote-work information
* company information inferred from job-description evidence

Shared test-data paths and loading behavior are provided by:

```text
tests/helpers/job_test_data.py
```

Keeping representative job descriptions in source control allows parser behavior to be evaluated repeatedly against known inputs.

## Test Helpers

Reusable test construction belongs under:

```text
tests/helpers/
```

For example, `make_test_job()` creates a valid baseline `JobOpening` and allows individual tests to override only the fields relevant to the behavior being tested.

This keeps tests concise while avoiding repeated model-construction boilerplate.

Helpers should simplify setup without hiding the behavior being tested.

## Running Tests

Run the complete test suite:

```bash
python3 -m pytest
```

Run only unit tests:

```bash
python3 -m pytest tests/unit
```

Run integration tests:

```bash
python3 -m pytest tests/integration
```

Run only live-AI tests:

```bash
python3 -m pytest -m live_ai
```

Exclude live-AI tests:

```bash
python3 -m pytest -m "not live_ai"
```

Run a specific test module:

```bash
python3 -m pytest tests/unit/scoring/test_fit_scorer.py -v
```

## Smoke Tests

Selected high-value tests may be marked:

```python
@pytest.mark.smoke_test_this
```

These provide a small, fast way to exercise especially important behavior during development.

They can be run with:

```bash
python3 -m pytest -m smoke_test_this
```

A smoke marker does not replace broader unit or integration coverage. It identifies tests that are useful for a quick confidence check.

## Testing Philosophy

The project deliberately separates **probabilistic intelligence** from **deterministic application behavior**.

AI is used where interpretation is valuable, such as extracting structured information from natural-language job descriptions.

Once information has been converted into structured application models, deterministic Python code is preferred for operations such as:

* scoring
* persistence
* deduplication
* validation
* recommendation rules
* formatting
* workflow orchestration

The test suite reflects that architecture.

Deterministic behavior should generally have precise, repeatable unit tests. AI-backed behavior should be tested at carefully selected integration boundaries using representative inputs and assertions that tolerate irrelevant variation while protecting important application contracts.

The goal is not simply a large number of tests. The goal is confidence that deterministic rules remain deterministic, AI boundaries produce usable structured results, and the components work correctly together.

