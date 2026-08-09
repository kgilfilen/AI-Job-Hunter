# UI

The `ui` package contains the interactive user interface for the AI Career Manager.

The current implementation uses Streamlit and provides a lightweight front end over the service layer. It does not implement job-analysis logic itself; instead, it calls `JobService` and `ProfileService` and presents their results to the user.

## `streamlit_app.py`

This file defines the current Streamlit application.

Its primary responsibilities are:

- load the candidate profile
- accept a job URL for analysis
- optionally reprocess an existing job
- display parsed job information
- display fit score and recommendation
- show missing required skills
- allow verified missing skills to be added to the profile
- display the generated resume artifact path
- display and edit core candidate skills

## Application Startup

The UI configures the Streamlit page and creates the main service objects:

```text
ProfileService
SQLiteJobRepository
JobService
```

The candidate profile is loaded from:

```text
config/candidate_profile.json
```

If the profile cannot be loaded, the application displays an error and stops.

## Job Analysis Workflow

The main job-analysis interaction begins with a job URL.

The user can also select:

```text
Reprocess if this job already exists
```

When `Analyze Job` is pressed, the UI delegates to:

```python
job_service.analyze_url(...)
```

The returned `JobAnalysisResult` is stored in Streamlit session state so it remains available during reruns.

The UI therefore acts as a presentation layer over the service workflow rather than duplicating acquisition, parsing, scoring, or artifact logic.

## Existing-Job Behavior

If the service reports that the job already exists and was skipped, the UI displays the existing job ID and tells the user that reprocessing can be enabled.

This reflects duplicate handling implemented in the service/repository layers.

## Job Result Display

For a successfully analyzed job, the UI currently displays:

- job title
- company
- location
- work arrangement
- employment type
- fit score
- recommendation

The recommendation may be an enum, so the UI converts it to its `.value` when necessary before displaying it.

## Missing Skills Review

The UI displays `missing_required_skills` from the `FitAnalysis`.

Each missing skill is shown with an `Add` button.

The interface explicitly tells the user:

> If you actually have experience with one of these skills, add it to your profile.

This creates an important human-verification boundary.

The scoring system may identify a skill as missing because it is absent from the structured candidate profile. The UI does not assume that means the candidate lacks the experience. Instead, the user decides whether the skill is genuinely part of their background.

When the user confirms a skill:

1. `ProfileService.add_skill()` updates the profile.
2. `ProfileService.save()` persists it.
3. Streamlit reruns the interface.

This is a useful feedback loop between job analysis and profile improvement.

## Generated Resume

When a tailored resume artifact was produced, the UI displays its file path.

The current interface does not render or download the resume contents directly.

## Candidate Profile View

The second major area of the UI displays the candidate profile.

It currently shows:

- candidate name
- candidate email
- core skills

The UI is therefore not yet a full candidate-profile editor. It focuses primarily on skill maintenance.

## Removing Skills

Every existing core skill is displayed with a `Remove` button.

Removing a skill:

1. calls `ProfileService.remove_skill()`,
2. saves the updated profile,
3. reruns the Streamlit application.

## Adding One Skill

The user can manually enter one skill and add it to the candidate profile.

Input validation and persistence are delegated to `ProfileService`.

## Adding Multiple Skills

The UI also supports comma-separated bulk entry.

For example:

```text
Playwright, CI/CD, API testing
```

The UI:

1. splits the text on commas,
2. trims each skill,
3. rejects an empty list,
4. adds each skill through `ProfileService`,
5. saves the profile once after processing the collection.

## Session State

The current job-analysis result is stored under:

```text
job_analysis_result
```

in Streamlit session state.

This allows the result to survive the reruns triggered by Streamlit interactions such as adding or removing profile skills.

## Architectural Role

The UI layer answers:

> How does the user interact with the application's capabilities?

It should not answer:

> How is the job parsed, scored, stored, or analyzed?

Those responsibilities remain behind the service layer.

The current dependency direction is:

```text
Streamlit UI
    |
    +--> ProfileService
    |
    +--> JobService
             |
             +--> repository
             +--> fetcher
             +--> parser
             +--> scorer
             +--> resume recommender
             +--> artifact writers
```

This keeps the interface relatively thin and makes it possible to add another interface later—such as a CLI, web API, or desktop application—without moving the core workflow out of the service layer.

## Current Limitations

The Streamlit interface is intentionally small and functional.

Current limitations include:

- only URL-based job analysis is exposed in the UI
- job history is not displayed
- application status is not displayed or editable
- application activity history is not yet available
- there is no today/yesterday activity review
- resume contents are not displayed directly
- the full candidate profile is not editable
- preferred skills, target titles, experience, education, certifications, and preferences are not currently managed here
- job-analysis results are not presented as a historical list
- errors are displayed directly from caught exceptions
- the entire interface currently resides in one Streamlit file

## Natural Next UI Features

Several future features fit naturally into this layer once supporting services and persistence exist.

### Recent Job Activity

A useful view would show jobs analyzed or updated today and yesterday.

### Application Tracking

The UI could allow the user to self-report actions such as:

```text
Applied
Interview scheduled
Interview completed
Followed up
Offer received
Rejected
Withdrawn
```

Because applications are submitted outside the AI Career Manager, these actions would be explicitly user-recorded rather than inferred.

### Application History

Once application events are stored, the UI could present a chronological activity view showing:

- job
- company
- event
- event time
- current application status
- next action
- follow-up date

This would provide a daily job-search journal without requiring the application to submit jobs on the user's behalf.

### Richer Resume Review

The generated tailored resume could eventually be displayed directly in the interface, with links or controls for viewing its supporting fit analysis and recommendations.

## Growth Direction

As the UI expands, it may become useful to split `streamlit_app.py` into smaller components or pages.

For now, keeping the interface in a single file is reasonable because the available workflows are still small and tightly related.

The important architectural constraint is to keep business logic behind the service layer so UI growth does not create a second implementation of the application workflow.
