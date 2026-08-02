Notes:

in the principle of separating facts from interpretation, we keep job opening scores in the job_opening_fit.json file. 

The job title test looked for "SDET III" in the candidate profile...for now I added that to the profile. Later I will consider making that comparison more fuzzy.

Nine integration tests passed, great start. Working on unit tests next.



## Security Clearance vs. Background Checks

AI Career Manager treats security clearances and background checks as separate concepts.

### Security Clearance

Represents eligibility to access classified government information.

Examples:

- Confidential
- Secret
- Top Secret
- TS/SCI

Security clearances may be active, expired, or never held.

### Background Check

Represents employer hiring requirements that are independent of security clearances.

Examples:

- Criminal background check
- Employment verification
- Education verification
- Drug screening
- Credit check

Many software engineers undergo numerous background checks without ever holding a government security clearance.

The application should therefore model these independently for both candidate profiles and job requirements.

Public Trust is modeled separately from security clearances because it represents a federal suitability determination rather than access to classified information.

## Observation

A Michigan Licensed Math Substitute Teacher position scored higher than several software QA positions that I considered better matches.

## Impact

The current scoring algorithm emphasizes generic skill overlap but does not sufficiently consider career domain or professional trajectory.

## Potential Improvement

Introduce career-domain classification and domain-aware scoring. Evaluate whether "career plausibility" should be a separate component of the overall fit score.

## Classification

Scoring enhancement