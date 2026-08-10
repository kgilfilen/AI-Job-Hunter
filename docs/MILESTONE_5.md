# Milestone 5 — Multi-Career Profiles and Career Planning

**Status:** Proposed
**Defined:** August 2026

## Milestone Theme

Milestone 5 expands the AI Career Manager from primarily managing an active job search into representing **multiple possible career directions for one person**.

The central product question is:

> **Given who I am now, and where I might want to go, what opportunities are realistic, and what should I do next?**

Milestone 5 should begin making that question explicit in the product architecture.

---

# 1. Why This Milestone Exists

The current candidate model largely assumes:

```text
One Candidate
      ↓
One CandidateProfile
      ↓
One Career Direction
```

That assumption is too restrictive.

A person may simultaneously be:

* established in one career
* qualified for another career
* transitioning toward a third
* exploring additional possibilities

Career direction is therefore not identical to personal identity.

The Career Manager should eventually represent:

```text
One Candidate
      ↓
Shared History
      ↓
Multiple Career Profiles
```

---

# 2. Career Profiles

A career profile represents a particular career direction.

Examples might include:

```text
Candidate
├── Software / QA
├── Culinary
└── Construction
```

These are not separate users.

They are different professional views of the same person.

Each profile may have its own:

* target titles
* target industries
* relevant skills
* preferred skills
* work preferences
* career-specific summary
* resume emphasis
* selected experience
* skill gaps
* readiness level

---

# 3. Shared Candidate Record

Information that describes the person rather than a particular career should not have to be duplicated across profiles.

A possible conceptual structure is:

```text
Candidate
│
├── Identity
│   ├── name
│   ├── email
│   ├── phone
│   ├── location
│   ├── LinkedIn
│   └── other contact information
│
├── Master History
│   ├── employment
│   ├── education
│   ├── certifications
│   ├── projects
│   └── skills/evidence
│
└── Career Profiles
    ├── Profile A
    ├── Profile B
    └── Profile C
```

The exact model should be designed during Milestone 5 rather than assumed now.

---

# 4. Profiles Must Remain Truthful

Multiple profiles should not create multiple fictional versions of the candidate.

The underlying evidence remains shared.

A career profile selects and emphasizes relevant evidence.

For example:

```text
Master History
├── Restaurant leadership
├── Construction projects
├── Software engineering
├── Education
└── Certifications
```

A software resume might emphasize software engineering and transferable leadership.

A culinary resume might emphasize restaurant experience.

A construction profile might emphasize hands-on project experience.

None of these profiles should invent experience that does not exist in the master record.

This extends the resume truthfulness principle already present in the project:

> **Emphasize selectively. Never fabricate.**

---

# 5. Aspirational Career Profiles

A career profile does not need to represent an already-established career.

Profiles should eventually support career possibilities at different maturity levels.

Conceptually:

```text
EXPLORING
    ↓
PREPARING
    ↓
OPPORTUNITY READY
    ↓
TRANSITIONING
    ↓
ESTABLISHED
```

These names are placeholders, not final enums.

The important requirement is that the system distinguish between:

> "I have done this professionally for twenty years."

and:

> "I am seriously considering this and have begun preparing."

Both can be valid career profiles, but the evidence and recommendations should differ.

---

# 6. Evidence

A career profile should become stronger as evidence accumulates.

Evidence may include:

* professional experience
* education
* coursework
* projects
* certifications
* licenses
* assessments
* portfolios
* volunteer experience
* internships
* transferable experience from another career

Eventually the system should be able to distinguish between:

```text
Skill claimed
```

and:

```text
Skill supported by evidence
```

This may become an important foundation for candidate intelligence.

---

# 7. Students and Early-Career Users

Milestone 5 should avoid assuming that users already have substantial professional histories.

A student may begin with:

```text
Student
├── Career Profile A — Exploring
├── Career Profile B — Exploring
└── Career Profile C — Exploring
```

Over several years:

```text
Coursework
    +
Projects
    +
Activities
    +
Summer Work
    +
Internships
        ↓
Increasing Career Evidence
```

The Career Manager could therefore become useful before the user's first professional job search.

Internships should be treated as meaningful opportunities, not simply smaller full-time jobs.

A student-facing profile might ask:

* What internships am I competitive for now?
* What should I learn before next summer?
* Which projects would strengthen this profile?
* What requirements repeatedly appear in internships?
* What evidence am I missing?
* How close am I to entry-level readiness?

---

# 8. Career Changers

Career changers present a different problem.

They often have substantial evidence, but much of it comes from another field.

The Career Manager should eventually distinguish:

```text
Directly Relevant Experience
        +
Transferable Experience
        +
Missing Evidence
```

For example, leadership, troubleshooting, customer interaction, project ownership, training, quality control, process improvement, and operational responsibility may transfer between careers even when the domain changes.

The system should identify transferable strengths without pretending that adjacent experience is identical to direct experience.

---

# 9. Career Exploration

An exploratory career profile should allow the user to investigate a possible career without committing to it.

Instead of generic career advice, the system should eventually use real market evidence.

Conceptually:

```text
Candidate
    +
Possible Career
    +
Representative Real Jobs
           ↓
Requirements Analysis
           ↓
Current Strengths
Transferable Strengths
Recurring Gaps
Preparation Requirements
           ↓
Career Viability
```

This could answer questions such as:

> How realistic is this career for me?

> What would I need to learn?

> Which requirements appear repeatedly?

> How much of my existing experience transfers?

> What entry point would be realistic?

> What should I do first if I want to explore this seriously?

This capability should build on the existing job parser, deterministic scoring, and future Profile Advisor rather than creating an unrelated career-recommendation engine.

---

# 10. Career-Aware Job Analysis

The current flow is approximately:

```text
CandidateProfile
      +
JobOpening
      ↓
FitAnalysis
```

Milestone 5 should move toward:

```text
Candidate
      +
Selected CareerProfile
      +
JobOpening
      ↓
Career-Specific FitAnalysis
```

A job should be evaluated against the relevant career profile rather than every skill the candidate has ever acquired.

This prevents irrelevant experience from polluting fit calculations.

---

# 11. Profile Selection

Initially, profile selection should probably remain explicit.

For example:

```text
Analyze using:

[ Software / QA ]
[ Culinary ]
[ Construction ]
```

Automatic profile inference may eventually be useful, but it should not be required for the first implementation.

A future system could infer:

> "This appears to be a culinary opportunity. Analyze using the Culinary profile?"

Explicit confirmation would preserve user control.

---

# 12. Career-Aware Resume Generation

Resume generation should use:

```text
Master Candidate Evidence
          +
Selected Career Profile
          +
Specific Job
          ↓
Tailored Resume
```

The selected profile determines which evidence is relevant.

The job determines which parts of that relevant evidence deserve emphasis.

This creates two levels of tailoring:

```text
Person
 ↓
Career-specific representation
 ↓
Job-specific representation
```

Truthfulness remains enforced at both levels.

---

# 13. Profile Advisor Across Careers

The Profile Advisor concept becomes more powerful with multiple career profiles.

Missing skills should be aggregated within the relevant career.

For example:

```text
Software / QA Profile

20 attractive jobs analyzed

Recurring gaps:
Playwright       8
Kubernetes       6
AWS              5
Performance Test 4
```

Another career profile should maintain its own market intelligence.

This allows the system to answer:

> What investment would make this particular career profile stronger?

Eventually, comparisons between career paths may also become possible.

---

# 14. Possible Career Comparison

This is likely beyond the first Milestone 5 implementation, but the architecture should not prevent it.

A future user might compare:

```text
Career A
Current readiness: High
Major gaps: 2
Entry opportunities: Strong

Career B
Current readiness: Moderate
Major gaps: 5
Transferable experience: Strong

Career C
Current readiness: Low
Preparation required: Significant
Personal interest: High
```

The system should not pretend that career choice can be reduced to one numerical score.

Compensation, interest, location, training time, lifestyle, opportunity availability, risk, and personal values may all matter.

Career comparison should therefore remain decision support rather than automated life decision-making.

---

# 15. Potential Users

Milestone 5 should be designed generally enough to support several user types.

### Established professionals

Manage an active career and job search.

### Multi-skilled professionals

Have more than one credible career direction.

### Career changers

Want to move from established experience into another field.

### Career explorers

Want evidence about possible future careers.

### Students

Build career evidence through education, projects, and internships.

### Returning workers

Reassess older experience against current market expectations.

The architecture should not encode assumptions specific to any one of these groups.

---

# 16. Proposed Implementation Sequence

Milestone 5 should be incremental.

## Phase 1 — Candidate/Career Separation

Refactor the current candidate model so personal identity/history and career-specific targeting can be separated without breaking existing functionality.

Existing single-profile behavior should continue to work.

## Phase 2 — Multiple Career Profiles

Allow a candidate to define more than one career profile.

Support:

* profile name
* target titles
* relevant skills
* career-specific preferences
* profile status/maturity if appropriate

## Phase 3 — Profile Selection

Allow CLI/UI workflows to choose which career profile is being used.

## Phase 4 — Career-Aware Scoring

Fit scoring should operate against the selected career profile.

Existing deterministic scoring principles should remain.

## Phase 5 — Career-Aware Resume Generation

Resume recommendations and formatting should use the selected career profile while drawing truthful evidence from the master candidate record.

## Phase 6 — Aspirational Profiles

Allow profiles that represent careers being explored or prepared for rather than established professional histories.

## Phase 7 — Career Intelligence

Aggregate job-market evidence by career profile.

Begin answering:

> What am I repeatedly missing?

> What should I build next?

> How ready am I for this direction?

The exact boundary between Milestone 5 and later milestones should be determined as implementation proceeds.

---

# 17. What Milestone 5 Should Not Become

Milestone 5 should not attempt to solve every career-planning problem immediately.

In particular, avoid prematurely building:

* a universal career aptitude test
* psychological personality matching
* automated declarations of the user's "best" career
* large occupation taxonomies before they are needed
* complex career-ranking algorithms
* speculative salary prediction
* AI-generated fictional candidate evidence
* automatic educational plans without supporting market evidence

The project should continue following the pattern that has worked so far:

> Build the smallest useful capability, use it, observe what becomes necessary, and generalize when evidence supports the abstraction.

---

# 18. Architectural Principles to Preserve

Milestone 5 should retain several principles established earlier in the project.

### Probabilistic interpretation, deterministic rules

Use AI where interpretation is genuinely valuable.

Keep explicit business logic deterministic where practical.

### Evidence before claims

Career profiles and resumes must be grounded in actual candidate evidence.

### Preserve source information

Do not destroy underlying candidate history when creating career-specific views.

### Incremental migration

The existing Career Manager should continue working while the candidate architecture evolves.

### Real market feedback

Whenever practical, evaluate career readiness against actual job and internship requirements rather than generic assumptions about occupations.

### User agency

The system provides evidence and recommendations.

The user makes career decisions.

---

# 19. Success Criteria

Milestone 5 will be successful when the Career Manager can represent one person with multiple meaningful career directions without mixing those directions together.

At minimum, the system should be able to:

* maintain shared candidate information
* maintain multiple career profiles
* select a career profile for analysis
* score jobs against the selected profile
* generate truthful career-appropriate resume recommendations
* preserve existing application-management functionality
* represent at least one established and one aspirational career profile

The design should also make student and career-transition use cases possible without requiring a separate architecture.

---

# 20. Product Direction

Milestone 5 represents an important transition in the project's identity.

Earlier versions primarily answered:

> Is this job good for me?

The emerging Career Manager should increasingly answer:

> **Given who I am now, and where I might want to go, what opportunities are realistic, and what should I do next?**

That question should guide Milestone 5 design decisions.

The goal is not merely to help someone get the next job.

The longer-term opportunity is to help a person understand, build, and navigate the careers that are realistically available to them.
