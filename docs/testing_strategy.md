# Testing Strategy

AI Career Manager uses a layered testing strategy based on the testing pyramid.

The goal is not simply to maximize test count or code coverage. Tests exist to protect important behavior, architectural boundaries, integrations, and AI-assisted workflows.

## Testing Pyramid

```text
                 Manual / Exploratory
              -------------------------
                    End-to-End
              -------------------------
              AI Validation Scenarios
              -------------------------
                  Integration Tests
              -------------------------
                     Unit Tests
```

The lower layers contain the largest number of tests because they are faster, more deterministic, and easier to diagnose.

## Unit Tests

Unit tests form the foundation of the test suite.

They verify individual functions, classes, and business rules in isolation.

Examples include:

* Job parsing helpers
* Candidate profile updates
* Duplicate detection
* Repository behavior
* Metadata extraction
* Salary extraction
* Job scoring logic
* Service-layer decisions
* Artifact generation
* Input validation

Unit tests should normally be:

* Fast
* Deterministic
* Independent
* Free of network access
* Free of real AI API calls
* Easy to diagnose when they fail

The unit suite is intended to run continuously during development.

## Integration Tests

Integration tests verify important interactions between components.

These tests focus on architectural seams rather than repeating all unit-level cases.

Important integrations include:

```text
Web Fetcher
→ Metadata Extraction
→ Parser Input Builder
```

```text
JobService
→ Repository
→ Parser
→ Scorer
→ Artifact Generation
```

```text
ProfileService
→ CandidateProfile
→ Persistent Storage
```

Integration tests should confirm that independently tested components exchange data correctly and preserve expected behavior when combined.

## AI Validation Scenarios

Large language models introduce behavior that cannot always be tested effectively with ordinary deterministic assertions.

A response can be syntactically valid while still being semantically wrong.

For this reason, AI Career Manager maintains validation scenarios based on representative job descriptions.

Examples include verifying that the system correctly identifies:

* Job title
* Employer
* Location
* Employment type
* Required skills
* Security-clearance requirements
* Remote-work expectations

These scenarios are especially important when changing:

* AI models
* Prompts
* Parser instructions
* Metadata enrichment
* Structured evidence supplied to the model

AI validation tests may be slower and may incur API cost, so they are kept separate from the normal developer unit-test loop.

## End-to-End Tests

End-to-end tests verify complete user workflows.

Examples include:

```text
Job URL
→ Fetch
→ Parse
→ Persist
→ Score
→ Generate Recommendations
→ Generate Resume
```

and:

```text
Candidate Profile
→ Add Skill
→ Validate
→ Save
→ Reload
```

End-to-end tests are intentionally fewer than unit or integration tests.

Their purpose is to verify that the system as a whole can accomplish important user tasks.

## Manual and Exploratory Testing

Automated testing cannot fully evaluate user experience.

Manual testing is used for:

* Streamlit workflows
* Visual presentation
* Error messages
* Unexpected job-page formats
* Real-world recruiting websites
* Ambiguous job descriptions
* New user workflows

Exploratory testing is also used to discover cases that should later become automated regression tests.

When a meaningful defect is discovered manually, a regression test should be added whenever practical.

## Live AI Tests

Tests that make real OpenAI API calls are marked:

```text
live_ai
```

These tests are deliberately excluded from the normal fast development loop when appropriate because they:

* Require network access
* Cost money
* Take significantly longer
* May exhibit some nondeterminism

Fast development tests can be run with:

```bash
python3 -m pytest -m "not live_ai"
```

Full validation can be run with:

```bash
python3 -m pytest
```

## Test Reports

Pytest generates JUnit XML results:

```text
test-results/pytest-results.xml
```

The report represents the latest test execution and is intended for future CI integration.

Generated test reports are not committed to source control.

## Testing Philosophy

AI reduces the cost of writing and maintaining tests, but it does not replace engineering judgment.

The important questions remain:

* What behavior must be protected?
* What failures would matter to a user?
* What architectural contracts must remain stable?
* What assumptions are we making about external systems?
* What AI behavior requires validation rather than deterministic testing?

AI can accelerate fixture creation, mocks, repetitive cases, and test scaffolding.

The engineer remains responsible for deciding whether the tests are meaningful.

A guiding principle for this project is:

> Use AI to reduce the cost of engineering discipline, not the amount of engineering discipline.

## Regression Testing

Every defect that exposes an important previously untested behavior should be considered for a regression test.

The preferred workflow is:

```text
Discover defect
→ Understand root cause
→ Add or improve automated test
→ Fix defect
→ Run focused tests
→ Run regression suite
```

This prevents the same class of failure from quietly returning later.

## Test Review

Periodically, the project undergoes a deliberate test review.

For each significant module, the review produces:

1. A short list of essential tests.
2. A broader list of edge cases and lower-priority unit tests.
3. A list of integration scenarios across component boundaries.
4. Candidate AI validation scenarios.
5. Manual or exploratory workflows that cannot yet be automated effectively.

The objective is not exhaustive testing of every possible implementation detail.

The objective is strong protection of important behavior with a fast, understandable, maintainable test suite.
