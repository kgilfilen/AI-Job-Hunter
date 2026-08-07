#

## Artifacts

### Analysis_artifacts

#### Purpose

This module is responsible for persisting generated job-analysis artifacts to disk.

It does not perform analysis, scoring, parsing, or recommendation logic. Its job is to take already-created domain objects or text and write them into the per-job artifact directory in a consistent format.

In architectural terms:

JobService
   ↓
analysis_artifacts
   ↓
filesystem

It is an output/persistence utility for generated files.

#### Inputs and outputs

save_job_opening(job_opening, job_artifact_directory)

* Input: JobOpening dataclass
* Input: target artifact directory
* Output: Path to job.json
* Side effect: creates parent directory if needed through _write_json()
* File format: UTF-8, pretty-printed JSON

save_fit_analysis(fit_analysis, job_artifact_directory)

* Input: FitAnalysis dataclass
* Input: target artifact directory
* Output: Path to _fit.json
* Side effect: writes/overwrites fit-analysis artifact

save_resume_recommendation(recommendation, job_artifact_directory)

* Input: ResumeRecommendation dataclass
* Input: target artifact directory
* Output: Path to _resume_recommendation.json

save_tailored_resume(resume_text, job_artifact_directory)

* Input: rendered resume text
* Input: target artifact directory
* Output: Path to tailored_resume.md
* Side effect: explicitly creates the artifact directory if necessary
* File format: UTF-8 Markdown

_write_json(output_file, value)

* Input: output path
* Input: a dataclass-compatible object
* Output: None
* Side effect: creates parent directories and writes JSON
* Assumption: value must work with dataclasses.asdict()

make_json_safe(value)

* Input: nested Python value
* Output: equivalent value suitable for json.dumps()
* Handles:
Enum → .value
lists recursively
dictionaries recursively
* Leaves primitive or otherwise unchanged values untouched


#### Behavioral specifications:

* Artifact writers must return the exact path they wrote.
* JSON files must use UTF-8 encoding.
* JSON output must be formatted with four-space indentation.
* Parent directories must be created automatically for JSON artifacts.
* Tailored-resume directories must also be created automatically.
* Existing files at the target path are overwritten.
* Enum values anywhere inside nested lists/dictionaries must serialize using their underlying .value.
* Dataclass fields must be serialized recursively via asdict().
* Artifact generation must not mutate the domain objects supplied to it.
* This module must not contain business rules about whether an artifact should be created; callers decide that.

#### Current file contract

For one job artifact directory, the expected generated structure is:

``` bash
<job_artifact_directory>/
    job.json
    _fit.json
    _resume_recommendation.json
    tailored_resume.md
```

That naming convention is effectively part of the module’s external contract now. If another component expects _fit.json, changing it to fit_analysis.json would be a behavioral change, not just cleanup.

#### Error behavior

There is no custom exception handling, so filesystem and serialization errors propagate naturally.

Examples include:

* permission errors
* invalid/unwritable paths
* disk errors
* passing a non-dataclass object to _write_json()
* unsupported nested values that remain non-JSON-serializable after make_json_safe()

That is reasonable for this layer; higher-level services/UI can decide how to present those errors.

#### Good unit-test targets

The essential tests I’d want are:

* save_job_opening() writes job.json and returns its path.
* save_fit_analysis() writes _fit.json.
* save_resume_recommendation() writes _resume_recommendation.json.
* save_tailored_resume() creates directories and writes exact text.
* _write_json() creates missing parent directories.
* JSON serialization includes representative dataclass fields.
* make_json_safe() converts nested enums.
* Existing output files are overwritten successfully.

One subtle edge case worth testing is nested tuples or other collection types. make_json_safe() only recursively handles list and dict; if your dataclasses ever contain tuples, sets, Path, datetime, etc., serialization may fail. I would not change that until the models actually require it.

Overall, this module now has a very clean responsibility: convert completed analysis products into durable human- and machine-readable artifacts.