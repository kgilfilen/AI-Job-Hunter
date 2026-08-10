# Source Package

The `src` package contains the implementation of the AI Career Manager.

Most functionality is organized into focused subpackages. The files directly under `src/` provide the command-line entry point, candidate-profile loading, and shared recommendation values.

## Top-Level Files

### `main.py`

Provides the command-line entry point for job analysis and resume tailoring.

Supported job-input modes are mutually exclusive:

```text
--file      Process one local job-description text file
--examples  Process all .txt files in examples/jobs
--url       Fetch and process one job-description URL
```

Additional options are:

```text
--profile    Select the candidate profile JSON file
--reprocess  Reprocess a job that already exists
```

The default profile is `config/candidate_profile.json`.

### CLI Workflow

```text
CLI arguments
      |
      v
initialize database
      |
      v
load candidate profile
      |
      v
build JobInput object(s)
      |
      v
JobService.analyze()
      |
      v
display results
```

`main.py` delegates the core workflow to `JobService` rather than implementing parsing, scoring, persistence, and resume recommendation itself.

For a successfully analyzed job, the CLI displays the parsed job opening, fit analysis, resume recommendation, database job ID, and generated artifact paths.

If an existing job is skipped, the CLI reports its ID and explains that `--reprocess` can regenerate its analysis and artifacts.

### Job Input Handling

`get_job_inputs()` converts each supported input source into a `JobInput` containing:

```text
source_name
original_text
parser_text
source
source_url
```

For local and example files, original and parser text are currently identical.

For URLs, the page is fetched, visible text is preserved as the original source, `build_parser_input()` creates parser-ready text, and the canonical URL is retained when available.

### Running the CLI

```bash
python3 -m src.main --file path/to/job.txt
```

```bash
python3 -m src.main --examples
```

```bash
python3 -m src.main --url "https://example.com/job"
```

```bash
python3 -m src.main --profile path/to/profile.json --file path/to/job.txt
```

```bash
python3 -m src.main --reprocess --file path/to/job.txt
```

---

### `profile_loader.py`

Provides:

```python
load_candidate_profile(profile_path)
```

The loader reads candidate-profile JSON and constructs a `CandidateProfile`.

Nested collections are converted into their domain dataclasses:

```text
experience      -> Experience
education       -> Education
certifications  -> Certification
```

If the profile file does not exist, the loader raises `FileNotFoundError`.

Higher-level profile loading and persistence are handled by `ProfileService`.

---

### `constants.py`

Defines the shared `Recommendation` enum used by fit scoring:

```text
APPLY     -> "Apply"
CONSIDER  -> "Consider"
PASS      -> "Pass"
```

It also defines `VALID_RECOMMENDATIONS`, containing the three supported values.

## Package Structure

```text
src/
|
+-- main.py              CLI entry point
+-- profile_loader.py    candidate-profile JSON loading
+-- constants.py         shared recommendation values
|
+-- artifacts/           generated analysis artifacts
+-- database/            SQLite persistence and repositories
+-- fetchers/             external job acquisition
+-- formatters/           parser input and resume formatting
+-- models/               domain data structures
+-- parsers/              structured job extraction
+-- resume/               resume-tailoring recommendations
+-- scoring/              deterministic fit scoring
+-- services/             application workflow orchestration
+-- ui/                   interactive Streamlit interface
```

Each substantial subpackage can maintain its own `README.md` for implementation-specific architecture and behavior.

## Architectural Flow

```text
Job source
    |
    v
fetch / load
    |
    v
parser preparation
    |
    v
JobOpening
    |
    v
deterministic scoring <---- CandidateProfile
    |
    v
FitAnalysis
    |
    v
resume recommendations
    |
    v
tailored resume
    |
    +--> SQLite persistence
    +--> analysis artifacts
    +--> CLI / Streamlit UI
```

The service layer coordinates this workflow while individual packages remain responsible for their own domain logic.

## CLI and UI

The project currently has two user-facing interfaces:

```text
src/main.py
    -> command-line interface

src/ui/streamlit_app.py
    -> interactive Streamlit interface
```

Both rely on the same service layer. Adding or changing a user interface should not require a second implementation of job parsing, scoring, persistence, or resume recommendation.

## Design Principle

The source tree intentionally separates deterministic software from probabilistic AI behavior.

AI-assisted interpretation is concentrated primarily in the parser layer, where natural-language job descriptions are converted into structured facts.

Once those facts exist, much of the remaining workflow—including fit scoring and current resume recommendation logic—is deterministic.

This separation makes the system more:

- testable
- explainable
- reproducible
- debuggable
- extensible

It also makes clear which results depend on AI interpretation and which are produced by explicit software rules.

## Documentation Map

Detailed documentation is kept close to the code it describes:

```text
models/README.md
    Domain-model responsibilities

parsers/README.md
    Parser architecture and data flow

parsers/PROMPTS.md
    AI prompt intent and output contracts

parsers/PARSER_CONTRACTS.md
    Parser behavioral contracts and failure behavior

resume/README.md
    Deterministic resume recommendation logic

scoring/README.md
    Fit-scoring rules and thresholds

services/README.md
    Application workflow orchestration

ui/README.md
    Streamlit interface and user workflows
```

Other source directories can follow the same pattern when directory-level documentation adds useful architectural context without merely duplicating the implementation.
