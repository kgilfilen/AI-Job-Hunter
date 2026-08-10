# Product Evolution: From AI Job Hunter to Career Manager

**Project start:** June 22, 2026
**Purpose of this document:** Preserve how our understanding of the product evolved during development, including the questions, discoveries, architectural decisions, and changes in perspective that shaped the system.

This is not intended to be a conventional changelog. It is an engineering case study in iterative product discovery.

---

## 1. Where We Started

The project began on June 22, 2026 with a relatively focused problem:

> Can AI help automate and improve the job-search process?

The immediate problem was practical. Job searching involves repeatedly finding job descriptions, reading them, deciding whether they are worth pursuing, determining how well the candidate fits, and adjusting application materials.

The first conception of the system was therefore essentially an **AI-assisted job hunter**.

At that point, the problem appeared approximately like this:

```text
Job Description
      ↓
AI Analysis
      ↓
Is this a good job for me?
```

That was useful, but development quickly exposed additional questions.

---

## 2. Job Descriptions Need Structure

Raw job descriptions are inconsistent natural-language documents.

Different employers describe the same concepts in different ways. Titles vary. Remote status may be explicit or implied. Employment type may appear in several formats. Skills may be scattered throughout the description. Security-clearance requirements require careful interpretation.

The system therefore needed to convert unstructured job descriptions into a consistent model.

```text
Raw Job Description
        ↓
Probabilistic AI Parsing
        ↓
Structured JobOpening
```

This became an important architectural boundary.

AI is useful for interpreting ambiguous human language. Once that interpretation has been converted into structured data, however, much of the remaining application behavior does not require AI.

This led to one of the project's central engineering principles:

> **Use probabilistic intelligence for interpretation and deterministic software for rules.**

---

## 3. Parsing Was Not Enough

Once jobs could be represented consistently, the next question became obvious:

> Is this job actually a good fit for the candidate?

Answering that required something the original design had not needed: a structured representation of the candidate.

The `CandidateProfile` emerged to describe such things as:

* target job titles
* skills
* experience
* education
* certifications
* remote-work preferences
* relocation preferences
* security-clearance status

Now the system had two structured sides:

```text
CandidateProfile + JobOpening
             ↓
         Fit Analysis
```

---

## 4. Scoring Should Be Deterministic

An important architectural decision followed.

AI could have been asked:

> "On a scale of 0–100, how good is this job for this candidate?"

That would have been easy to implement, but difficult to reason about and difficult to test.

Instead, fit scoring became deterministic.

Explicit rules determine the effects of such things as:

* title matches
* required-skill matches
* missing required skills
* preferred skills
* remote-work alignment
* security-clearance requirements

This produced repeatable behavior.

The AI interprets the job. Python evaluates the structured interpretation.

```text
Natural Language
      ↓
     AI
      ↓
Structured Facts
      ↓
Deterministic Rules
      ↓
Decision Support
```

This separation became increasingly important as the project grew.

---

## 5. A Fit Score Still Does Not Tell the Candidate What to Do

Once the system could say that a job was an APPLY, CONSIDER, or PASS opportunity, another limitation appeared.

Knowing that a job is attractive does not answer:

> How should I present myself for this particular opportunity?

This led to resume recommendations and resume tailoring.

The system needed to identify:

* skills worth emphasizing
* relevant experience worth highlighting
* useful job terminology
* missing requirements
* possible concerns

An important truthfulness rule emerged:

> **The system may emphasize real experience, but it must not invent experience.**

A missing job requirement should remain missing.

This principle became important enough to protect explicitly with automated tests.

---

## 6. Individual Job Analysis Was Too Temporary

Originally, processing a job was largely transactional:

```text
Job comes in
     ↓
Analyze it
     ↓
Produce artifacts
     ↓
Move to the next job
```

But real job searching is not transactional.

A candidate needs to remember:

* jobs previously examined
* jobs already applied to
* duplicate postings
* application dates
* current application status
* follow-up dates
* recruiter contacts
* interviews
* next actions

That realization led to SQLite persistence.

The system began changing from a **job analyzer** into a **job-search manager**.

---

## 7. Preserve the Original Before Interpreting It

Persistence produced another architectural insight.

The original job description is primary evidence. AI parsing is an interpretation of that evidence.

Therefore the system should save the original description before attempting AI parsing.

```text
Original Job
     ↓
Persist
     ↓
Parse
     ↓
Store Interpretation
```

This allows the system to recover from parser failures, reprocess jobs as parsing improves, audit interpretations, and preserve historical evidence even if the AI-derived representation changes.

The test suite explicitly protects this ordering.

---

## 8. Persistence Creates History

Once jobs and applications were persisted, another product possibility became visible.

The system could begin answering questions about the job search itself:

> What did I apply to today?

> What did I do yesterday?

> Which applications need attention?

> Who should I follow up with?

> What interviews are coming?

This suggested application tracking and eventually an application-event history rather than only storing the current state.

The emerging model became:

```text
Job
 ↓
Application
 ↓
Current State

Application
 ↓
Events
 ├── Applied
 ├── Followed up
 ├── Recruiter contact
 ├── Interview scheduled
 ├── Interview completed
 ├── Rejected
 └── Offer
```

This is an important shift.

The system is no longer merely analyzing opportunities. It is helping manage an ongoing process.

---

## 9. One Job at a Time Does Not Reveal the Market

Another insight emerged from repeated job analysis.

Suppose a candidate lacks a skill in one job. That may not matter.

But suppose that same missing skill appears in seven attractive jobs.

That is useful career intelligence.

This led to the idea of a **Profile Advisor** capable of aggregating evidence across opportunities.

Instead of only asking:

> What am I missing for this job?

the system can eventually ask:

> What am I repeatedly missing across the jobs I actually want?

That produces a new feedback loop:

```text
Candidate Profile
       ↓
Real Job Market
       ↓
Repeated Requirements
       ↓
Skill Gaps
       ↓
Learning / Experience Decisions
       ↓
Stronger Candidate Profile
```

The job-search system begins contributing to career development.

---

## 10. Milestone 4 Became an Architectural Review

As the codebase grew, Milestone 4 included deliberate architectural cleanup and documentation.

Source directories were reviewed and documented.

The test suite was examined as a system rather than merely as individual passing tests.

That review uncovered several useful lessons.

### Tests should mirror architectural boundaries

Deterministic normalization belongs in unit tests.

Live AI parsing belongs in integration tests.

Parser-to-scorer behavior is a meaningful integration boundary because it crosses from probabilistic interpretation into deterministic decision logic.

### A green test can still be broken

One resume-generation integration test was discovered to be effectively false-green: intended assertions were unreachable.

Passing test counts alone are therefore insufficient. Tests themselves require review.

### Expensive probabilistic calls should be shared deliberately

Several live-AI tests independently parsed the same job description.

Each test was individually reasonable, but the suite as a whole was unnecessarily:

* expensive
* slow
* exposed to rate limits
* exposed to additional probabilistic variation

Module-scoped pytest fixtures allowed one AI interpretation to be shared by several related assertions.

This became another engineering principle:

> **Treat probabilistic or externally expensive test boundaries differently from cheap deterministic functions.**

---

## 11. The Candidate Model Exposed a Bigger Assumption

The original `CandidateProfile` was built for one immediate user and one primary career direction.

Eventually a new question arose:

> What if one person is legitimately capable of pursuing several careers?

For example, one person might have meaningful backgrounds or abilities in:

* software engineering and testing
* culinary work
* construction

Putting every skill from every career into one profile would make scoring increasingly noisy.

This exposed an assumption hidden in the original model:

> One person does not necessarily equal one career profile.

---

## 12. Multiple Career Profiles

The next idea was to separate the person from the career-specific representation.

Conceptually:

```text
Candidate
├── Shared Identity and History
│   ├── contact information
│   ├── education
│   ├── employment
│   └── certifications
│
└── Career Profiles
    ├── Software / QA
    ├── Culinary
    └── Construction
```

Career profiles could independently contain:

* target roles
* relevant skills
* career-specific preferences
* resume emphasis
* selected experience
* career-specific scoring considerations

The candidate's underlying history remains truthful and shared.

The career profile determines which parts are relevant to a particular direction.

---

## 13. A Career Profile Does Not Have to Describe an Existing Career

The multiple-career discussion exposed an even deeper idea.

People do not only manage careers they already have.

They imagine careers.

A person may have:

* an established career
* a career they are actively transitioning toward
* a career they are preparing for
* a career they are merely exploring

Historical experience reinforced this.

A person may begin with education in one field and substantial experience in another, investigate an entirely different career, prepare for qualifying tests, discover that the opportunity is not competitive enough, and later discover another path that becomes a successful long-term career.

Those possibilities are not fake profiles.

They are **possible futures at different levels of maturity**.

This suggested that career profiles should eventually represent states such as:

```text
Exploring
    ↓
Preparing
    ↓
Competitive for Internships / Entry Opportunities
    ↓
Career Transition
    ↓
Established
```

The exact state model remains to be designed.

The important discovery is that a career profile represents **direction plus evidence**, not merely past employment.

---

## 14. Students Reveal the Long-Term Value

The same architecture naturally applies to students.

Consider a student entering college several years before beginning a full-time professional job search.

Initially the student may have several possible career profiles.

Over time, those profiles can accumulate evidence:

* coursework
* projects
* certifications
* clubs and activities
* volunteer work
* part-time employment
* internships
* professional experience

The Career Manager could therefore become useful well before graduation.

Instead of creating a resume from scratch during senior year, the student could spend several years building evidence toward possible careers.

The system might eventually help answer:

> Which internships strengthen this career direction?

> What requirements repeatedly appear in entry-level jobs?

> Which of those requirements have I already demonstrated?

> What should I try to accomplish next semester?

This transforms the system from a tool used during unemployment into something that can accompany a person through career development.

---

## 15. The Potential Users Expanded

The evolving architecture revealed several potential user groups.

### Established professional

Knows the career direction and wants help evaluating opportunities, tailoring applications, and managing the search.

### Career changer

Has substantial existing experience but wants to move into another field.

Needs help identifying transferable evidence and remaining gaps.

### Career explorer

Is considering several plausible futures and wants evidence about their realism.

### Student

Is accumulating the education, projects, internships, and early experience necessary to become competitive.

### Returning worker

Has prior experience but needs to determine how current market expectations compare with existing skills and what needs refreshing.

These users appear different, but they share a common underlying problem.

---

# 16. The Core Product Question

By August 2026, the original question:

> Can AI help automate my job search?

had evolved into something substantially broader:

> **Given who I am now, and where I might want to go, what opportunities are realistic, and what should I do next?**

This is the emerging core of the Career Manager.

The product therefore operates between three states:

```text
WHO I AM NOW
      ↓
WHERE I MIGHT GO
      ↓
WHAT I SHOULD DO NEXT
```

Jobs, internships, skills, education, applications, projects, and career profiles all provide evidence connecting those states.

---

# 17. Engineering Lessons From the Evolution

Several broader engineering lessons emerged from this process.

## Build for the problem you understand today

The original single-profile design was not necessarily a mistake.

It accurately modeled the problem understood at that stage.

Prematurely designing a generalized multi-career planning platform on June 22 would likely have produced unnecessary abstractions without enough evidence to design them well.

## Use working software to discover the next question

Many important requirements appeared only after the preceding capability existed.

Parsing revealed the need for scoring.

Scoring revealed the need for tailoring.

Analysis revealed the need for persistence.

Persistence revealed application management.

Repeated analysis revealed candidate intelligence.

Candidate modeling revealed multiple careers.

Multiple careers revealed aspirational profiles.

Aspirational profiles revealed students and long-term career planning.

The progression was not random feature accumulation. Each working capability exposed the next limitation.

## Preserve evidence separately from interpretation

Original job descriptions should survive changes in AI interpretation.

Candidate history should remain distinct from career-specific presentation.

Facts and interpretations have different lifecycles.

## Separate probabilistic and deterministic responsibilities

AI is valuable where ambiguity exists.

Deterministic software is preferable where explicit business rules exist.

This makes behavior easier to understand, test, reproduce, and change.

## Test architecture matters

A passing suite is not automatically a well-designed suite.

Tests should reflect architectural boundaries, and expensive probabilistic operations deserve deliberate lifecycle management.

## Do not generalize before the evidence exists—but recognize the abstraction when it appears

A system can begin specific and become general.

The goal is not to predict every future requirement.

The goal is to build clean enough boundaries that new evidence can reveal the next abstraction without requiring the entire system to be discarded.

---

# 18. Why Preserve This History?

Most software repositories preserve what the system became.

They rarely preserve **how the team learned what the system should become**.

That reasoning is valuable.

The evolution of the Career Manager demonstrates a practical engineering process:

```text
Build
  ↓
Use
  ↓
Observe limitations
  ↓
Ask better questions
  ↓
Identify the underlying abstraction
  ↓
Refactor deliberately
  ↓
Build again
```

The objective is not to avoid changing our minds.

The objective is to change our minds for good reasons, preserve what we learned, and allow the architecture to evolve with our understanding.

This document should therefore continue to record major changes in product understanding—not every implementation detail, but the moments when a new question materially changes what we believe the system is.
