# Milestone 4 – Application Management

**Completion Date:** August 2026

Milestone Theme: From Job Analysis to Application Management

---

# Overview

Milestone 4 expanded AI Career Manager beyond analyzing job opportunities into
actively managing the job application process.

Milestone 3 established the application's persistent storage, service layer,
repository architecture, and initial Streamlit interface.

This milestone built on that foundation by introducing persistent application
tracking, application lifecycle management, activity history, follow-up
management, and historical job workflows.

AI Career Manager can now help manage what happens after an interesting job is
discovered.

---

# Major Accomplishments

## Application Tracking

Added persistent application records linked to analyzed jobs.

Applications can now maintain information including:

- Current application status
- Application date
- Next action
- Follow-up date
- Creation timestamp
- Update timestamp

An analyzed job can be converted into a tracked application without duplicating
the underlying job record.

---

## Application Lifecycle

Introduced explicit lifecycle states for tracked applications.

Current states include:

- `INTERESTED`
- `APPLIED`
- `INTERVIEWING`
- `OFFER`
- `REJECTED`
- `WITHDRAWN`
- `CLOSED`

Service-layer operations coordinate important lifecycle transitions rather than
requiring the user interface to manipulate persistence directly.

Examples include:

- Marking an application as submitted
- Beginning the interview process
- Recording an offer
- Recording a rejection
- Withdrawing from consideration
- Closing an application

The lifecycle intentionally remains flexible because real hiring processes do
not always follow a predictable sequence.

---

## Application Event History

Added a separate persistent event history for application activity.

Application status represents the application's current state, while events
preserve what happened over time.

Tracked activity can include events such as:

- Application submitted
- Interview scheduled
- Interview completed
- Offer received
- Rejection
- Withdrawal
- Application closed

Events include:

- Application identifier
- Event type
- Occurrence timestamp
- Optional notes
- Creation timestamp

Multiple events of the same type are supported.

For example, an application can contain several interview-scheduled and
interview-completed events without requiring additional application states.

---

## Status and Event Separation

A key architectural principle emerged during this milestone:

**Status is the best current summary. Events are the historical truth.**

This separation prevents the application lifecycle from becoming an excessively
complex state machine.

For example, an application may remain in `INTERVIEWING` while recording:

- First interview scheduled
- First interview completed
- Second interview scheduled
- Second interview completed
- Third interview scheduled

The current status remains simple while the event history preserves the complete
story.

---

## Transactional Lifecycle Operations

Application lifecycle operations that modify both application state and event
history now support shared database transactions.

This prevents partial updates where:

- Application status changes but the corresponding event is not recorded
- An event is recorded without the intended status change

Repository methods support shared SQLite connections when coordinated by the
service layer.

This strengthened consistency between current application state and historical
activity.

---

## Follow-Up Management

Added follow-up tracking for active applications.

Each application can now maintain:

- A next action
- A follow-up date

Example:

> Second interview completed. Follow up Friday if no response is received.

Follow-up information is persisted and can be updated as the hiring process
changes.

---

## Needs Attention

Added a Needs Attention workflow to identify applications requiring action.

Applications with due follow-ups are surfaced automatically.

Active statuses currently include:

- `INTERESTED`
- `APPLIED`
- `INTERVIEWING`
- `OFFER`

Terminal applications such as rejected, withdrawn, or closed applications are
excluded from the active follow-up queue.

This creates the foundation for a future career-management dashboard.

---

## Recent Activity

Added date-based application activity queries and UI presentation.

The application can now display activity for:

- Today
- Yesterday

Recent Activity combines application events with their associated job
information, allowing the user to quickly understand what happened across the
job search.

---

## Job History

Expanded persisted job history into an interactive workflow.

Stored jobs can now be selected individually rather than displayed as one large
list.

For each historical job, the application can display information such as:

- Job title
- Company
- Location
- Fit score
- Recommendation
- Application status

Historical jobs can also be converted into tracked applications.

---

## Application Actions from Job History

Job History now supports application management directly from the selected job.

Depending on the application's current state, available actions can include:

- Track Application
- Mark as Applied
- Start Interviewing
- Offer Received
- Rejected
- Withdraw
- Close Application

Terminal actions support optional notes so that the reason an application ended
can be preserved in its event history.

This allows information from company emails or other communications to remain
associated with the application.

---

## Manual Activity Recording

Added a general activity-entry workflow.

Users can select a tracked application, choose an event type, enter optional
notes, and record the activity.

This supports real hiring workflows without requiring a dedicated UI control for
every possible event.

Examples include:

- Scheduling another interview
- Completing an interview
- Recording hiring-team communication
- Preserving contextual notes

---

## Database Improvements

Expanded the SQLite schema to support application management and event history.

Database initialization now creates the required Milestone 4 structures for a
new database.

Additional query behavior supports:

- Application lookup by job
- Follow-up retrieval
- Chronological event history
- Date-range event queries
- Ordered job history

Database indexes support frequently used lookup and ordering patterns.

A fresh-database initialization test was performed successfully at milestone
completion.

---

## Streamlit User Interface

The Streamlit application now supports substantially more of the career
management workflow.

Current capabilities include:

- Analyze jobs
- Track interesting jobs as applications
- Advance applications through lifecycle states
- Record repeatable application events
- Add lifecycle notes
- Schedule follow-ups
- Display applications needing attention
- Display recent activity
- Browse historical jobs
- Reopen historical jobs
- Manage tracked applications
- Maintain candidate skills

The UI has successfully validated the underlying workflows, but its increasing
size also revealed the need for improved information architecture.

UI restructuring is intentionally deferred to Milestone 5.

---

## Testing

Automated testing continued to serve as the primary safety mechanism for
development.

Coverage now includes application behavior across:

- Repository persistence
- Application services
- Application lifecycle transitions
- Event recording
- Follow-up queries
- Active versus terminal application behavior
- Date-range activity queries
- Job persistence
- Duplicate detection
- Parsing
- Artifact generation
- URL acquisition
- Integration behavior

At Milestone 4 completion:

**165 automated tests pass.**

The complete test suite was executed successfully before milestone closeout.

A fresh SQLite database was also initialized successfully to verify that the
application does not depend on manually created Milestone 4 schema.

---

# Architectural Improvements

Major architectural improvements during Milestone 4 include:

- Persistent application entities
- Persistent application event history
- Separation of state from historical events
- Transactional service operations
- Shared repository database connections
- Follow-up query support
- Date-range activity retrieval
- Application-to-job relationships
- Historical job reopening
- Expanded lifecycle service methods
- Increased database indexing
- Improved end-to-end workflow coverage

The service and repository architecture established during Milestone 3 proved
capable of supporting these additions without major restructuring.

---

# Real-World Validation

Milestone 4 features were exercised against realistic job-search scenarios.

Examples included:

- Tracking an interesting job
- Marking the application as submitted
- Entering the interview process
- Recording multiple interview rounds
- Waiting for another interview after completing a previous one
- Scheduling follow-up actions
- Surfacing due applications under Needs Attention
- Recording company communication
- Rejecting an application
- Withdrawing from an application
- Closing an application
- Adding contextual notes explaining why an application ended

These workflows demonstrated that application management requires more
flexibility than a rigid linear state machine.

---

# Lessons Learned

Several important engineering and product lessons emerged during this
milestone.

## Status and history solve different problems.

A single application status cannot represent everything that happens during a
hiring process.

Status works well as a summary of the present.

Events work well as a record of the past.

Keeping them separate creates a simpler and more expressive system.

---

## Real hiring processes are messy.

Hiring workflows are not reliably linear.

An application may involve:

- Multiple interviews
- Repeated scheduling
- Long waiting periods
- Unexpected additional interview rounds
- Verbal and written offers
- Hiring pauses
- Company-side closures
- Candidate withdrawal
- Changes in direction after apparent progress

The software should record reality rather than force reality into an overly
rigid state machine.

---

## Flexible state transitions are valuable.

Users may occasionally move applications through states in unusual sequences.

The application should remain robust when this occurs.

Historical events provide context even when the current state alone cannot
explain the complete path taken by the application.

Future versions may provide warnings or guidance for unusual transitions, but
the system should avoid becoming fragile when users deviate from an expected
workflow.

---

## Follow-ups turn stored data into actionable data.

Persisting application history is useful.

Surfacing the applications that require attention is significantly more useful.

The Needs Attention workflow demonstrates the transition from passive record
keeping toward active career management.

---

## Real usage exposes UI architecture problems quickly.

The Streamlit interface was sufficient for validating Milestone 4 workflows.

As functionality increased, however, the single-page interface became
increasingly crowded.

This is useful product feedback rather than a failure of the current
implementation.

The working Milestone 4 UI provides concrete evidence for how the next
generation of navigation should be structured.

---

## Automated tests make incremental development practical.

Several regressions and implementation mistakes during the milestone were
identified immediately by tests.

Small service and repository tests made it possible to evolve the architecture
without losing confidence in previously completed behavior.

The milestone concluded with 165 passing automated tests.

---

# Statistics

Approximate project characteristics at the completion of Milestone 4:

- Persistent job history
- Persistent application tracking
- Persistent application event history
- Application lifecycle management
- Follow-up scheduling
- Needs Attention workflow
- Recent Activity workflow
- Interactive historical job management
- Transactional lifecycle operations
- SQLite query indexes
- Streamlit career-management interface
- 165 passing automated tests
- Successful fresh-database initialization
- Continued real-world use during an active job search

---

# Deliberate Deferrals

Several features were intentionally deferred rather than forced into Milestone
4.

## Richer Post-Offer Lifecycle

The current `OFFER` state does not fully describe the stages that may occur
between receiving an offer and actually beginning employment.

Future states may include:

- `ACCEPTED`
- `ONBOARDING`
- `HIRED`

These states require additional real-world usage and design before their exact
semantics are finalized.

In particular, accepting an offer does not necessarily mean that a job search
has ended.

---

## User Interface Redesign

The current Streamlit page now contains several distinct workflows.

Future navigation will likely separate concerns such as:

- Dashboard
- Jobs
- Applications
- Candidate Profile

The current interface will remain functional while Milestone 5 explores a more
scalable presentation architecture.

---

## Lifecycle User Experience

Future improvements may include:

- Better action grouping
- More compact lifecycle controls
- Improved note entry
- Application detail views
- Clearer event timelines
- Status-change guidance
- Warnings for unusual transitions without rigidly preventing them

The underlying Milestone 4 architecture is intended to support these
improvements without significant persistence-layer changes.

---

# Looking Ahead

Milestone 5 will focus on turning the growing career-management feature set into
a more cohesive product experience.

Likely areas of development include:

- UI and navigation redesign
- Dedicated application views
- Improved career dashboard
- Richer post-offer lifecycle modeling
- `ACCEPTED`, `ONBOARDING`, and `HIRED` semantics
- Better application timelines
- Recruiter and contact management
- Resume version history
- Skill evidence management
- Career analytics

Milestone 4 intentionally leaves room for these workflows to evolve based on
real usage.

---

# Summary

Milestone 4 transformed AI Career Manager from a system that primarily analyzes
job opportunities into one that can actively manage the application process.

The application now remembers not only which jobs were analyzed, but which jobs
became applications, what happened during those applications, what requires
attention next, and how each process ultimately progressed.

The most important architectural principle established during this milestone
is simple:

**Status is the best current summary. Events are the historical truth.**

Combined with persistent storage, service-layer coordination, transactional
updates, follow-up management, and comprehensive automated testing, this gives
AI Career Manager a strong foundation for increasingly sophisticated career
management workflows.

Milestone 5 can now focus on making those capabilities easier and more pleasant
to use.