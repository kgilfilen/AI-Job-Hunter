# Development Philosophy

## Primary Goal

Build a production-quality AI-assisted career platform while
demonstrating modern software engineering practices.

## Layered Development

Layer 1
AI Job Hunter foundation

Layer 2
Professional Knowledge Base

Layer 3
Resume Generation

Layer 4
Interview Assistant

Layer 5
Career Dashboard

Layer 6
Advanced AI Features

# Decision Rules

When deciding what to build next:

1. Finish the current layer.
2. Prefer reusable components.
3. Keep deterministic logic separate from LLM logic.
4. Write tests with new functionality.
5. Keep documentation current.
6. Park ideas that do not support the current layer.

# Parking Lot

Ideas are intentionally postponed.

Postponed does not mean rejected.

The project grows by completing layers rather than
adding partially finished features.



# Daily Development Workflow

Each development session should begin with a brief status update, given to the AI tool and created by the developer, specifically to keep the human being focused on a smart timeline, not drifting with the current. We will remind AI of our plans for the sprint, and our plans for today. Things can go SO FAST using AI that a human being can drift pretty far away from sprint goals in a short time. The next sprint can be changed if we need, but we should not drastically change this one, if possible. Certainly not by accident. 

The goal is to spend very little time planning and nearly all available
time building.

## Morning Check-in

Current branch:

Current milestone:

Current task:

Anything blocked?

What changed since yesterday?

How much development time is available today?

### Example:

branch: feature/resume-recommendations-output

milestone: Milestone 2 – Professional Identity

task: resume formatter

blockers: None

Changed since yesterday? Nothing

How much dev time today: 4 hours

## End of Session

Run tests.

Update documentation if needed.

Commit logical changes.

Push if appropriate.

Merge completed feature branches.

Record progress in the development log.

Identify the next starting task.

### Example: 

Next Start:

Resume Formatter

Expected time: 1-2 hours

Definition of done:

- formatter implemented
- tests written and run
- CLI output updated
- regression tests pass
- commit



## Developer Responsibilities

- current git branch

- current project status

- available dev time

- other daily priorities (meetings and interviews and appointments)

- test results

- merge status

- blockers
