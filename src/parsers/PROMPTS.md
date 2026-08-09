# Parser Prompts

The AI Career Manager uses focused prompts to extract structured information from unstructured job descriptions.

Each AI-assisted parser is responsible for one field or category rather than asking a single large prompt to interpret the entire posting. This makes prompt behavior easier to test, inspect, refine, and troubleshoot.

The prompts currently use the OpenAI Responses API and request structured JSON output.

## Common Prompt Pattern

Most parser prompts follow the same general structure:

```text
1. Define the extraction task.
2. Define the required JSON fields.
3. Define allowed values or output format.
4. State rules that constrain interpretation.
5. Include the complete job description.
```

Most result objects include:

```text
value or values
confidence
evidence
warning
```

This structure preserves not only the extracted result but also information about how certain the parser is and what source text supports the result.

---

## Job Title Prompt

**File:** `title_parser.py`

**Purpose:** Extract the official title of the posted position.

**Output fields:**

```json
{
  "title": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Do not invent a job title.
- Prefer the exact title used in the posting.
- If multiple titles appear, choose the most likely official posting title.
- Record ambiguity in `warning`.
- Return `null` when no title is clear.

The full job description is passed to the model after these instructions.

---

## Company Name Prompt

**File:** `company_parser.py`

**Purpose:** Identify the actual hiring company.

**Output fields:**

```json
{
  "name": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Extract the hiring company rather than a vendor, recruiter, product, or client unless clearly stated.
- If the posting refers only to "our client," return `null` and add a warning.
- Prefer explicit metadata such as Company, Employer, Business Unit, Division, Organization, Client, or Hiring Company.
- Prefer explicit metadata over inferred names from narrative text.
- Do not mistake a division for the company when a parent organization is also identified.
- When labeled metadata is absent, inspect legal statements, careers URLs, recruiting email domains, office references, and repeated brand references.
- Prefer the most specific supported full company name.
- Do not invent a company.

This is one of the more detailed prompts because job postings often contain multiple organization names.

---

## Location Prompt

**File:** `location_parser.py`

**Purpose:** Extract the physical job location.

**Output fields:**

```json
{
  "location": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Extract city, state, and country when available.
- Do not treat remote or hybrid status as a physical location.
- Use `null` if no physical location is present.
- Do not invent a location.
- If multiple locations appear, select the most likely official posting location and describe ambiguity in `warning`.

---

## Remote Status Prompt

**File:** `remote_status_parser.py`

**Purpose:** Determine whether the position is remote, hybrid, onsite, or another supported arrangement.

**Output fields:**

```json
{
  "status": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Allowed values include:**

```text
remote
hybrid
onsite
remote or hybrid
hybrid or remote
flexible
unknown
```

**Important rules:**

- Do not infer remote status from the absence of a location.
- Extract remote, hybrid, or in-office language only when supported by the posting.
- Use `null` when the posting does not specify a status.
- Do not invent a status.
- Record ambiguity in `warning` when multiple arrangements are mentioned.

---

## Employment Type Prompt

**File:** `employment_type_parser.py`

**Purpose:** Extract the employment arrangement.

**Output fields:**

```json
{
  "employment_type": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Allowed values include:**

```text
full-time
part-time
contract
contract_to_hire
temporary
internship
unknown
```

**Important rules:**

- Extract the employment type only when present.
- Use `null` if it is not given.
- Do not invent a type.
- Prefer the exact posting language.
- If several employment types appear, choose the most likely official value and record the ambiguity.

After AI extraction, the value is passed through deterministic normalization. If no value is extracted, deterministic text detection can provide a fallback.

---

## Security Clearance Prompt

**File:** `security_clearance_parser.py`

**Purpose:** Determine whether a security clearance is required and, when possible, identify its level.

**Output fields:**

```json
{
  "clearance_required": true,
  "clearance_level": "string or null",
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Supported clearance concepts include:**

```text
Public Trust
Confidential
Secret
Top Secret
TS/SCI
SCI
Polygraph
TS/SCI with Polygraph
Other
null
```

**Important rules:**

- Do not invent a clearance requirement.
- Explicit statements that no clearance is required produce `false`.
- Absence of clearance information also produces `false` with a `null` level.
- "Ability to obtain clearance" is treated as a clearance requirement.
- If multiple levels appear, choose the highest required level and explain the ambiguity.
- Prefer terminology used in the posting.

---

## Required Skills Prompt

**File:** `required_skills_parser.py`

**Purpose:** Extract technical and domain skills that are required or strongly expected.

**Output fields:**

```json
{
  "required_skills": [],
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Extract only required or strongly expected skills.
- Include programming languages, frameworks, tools, platforms, testing skills, domain skills, and methodologies.
- Do not include soft skills unless they are clearly required.
- Normalize skill names where practical.
- Prefer concise names such as `Python` rather than copying a full qualification sentence.
- Do not invent skills.
- Return an empty list when required skills are not clear.

---

## Preferred Skills Prompt

**File:** `preferred_skills_parser.py`

**Purpose:** Extract skills that are desirable but not mandatory.

**Output fields:**

```json
{
  "preferred_skills": [],
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Extract only skills described as preferred, desired, nice-to-have, beneficial, a plus, or equivalent language.
- Do not include required skills.
- Include languages, frameworks, cloud platforms, databases, testing tools, operating systems, methodologies, and domain knowledge.
- Normalize equivalent technology names when practical.
- Do not invent skills.
- Return an empty list if no preferred skills are present.

Keeping required and preferred skills separate allows later fit analysis to weigh them differently.

---

## Responsibilities Prompt

**File:** `responsibilities_parser.py`

**Purpose:** Extract the major responsibilities of the position.

**Output fields:**

```json
{
  "responsibilities": [],
  "confidence": 0.0,
  "evidence": "supporting phrase or null",
  "warning": "string or null"
}
```

**Important rules:**

- Extract only major job responsibilities.
- Write each responsibility as a concise action statement.
- Do not include qualifications or skills.
- Remove duplicate or overlapping responsibilities.
- Prefer action-oriented verb phrases such as:
  - Design
  - Develop
  - Implement
  - Build
  - Test
  - Maintain
  - Analyze
  - Collaborate
  - Lead
  - Support
- Limit the result to approximately 5–10 responsibilities.
- Do not invent responsibilities.

---

## Prompt Design Principles

The current prompts follow several recurring design principles.

### Narrow Responsibility

Each prompt answers one specific question. This reduces ambiguity and makes failures easier to diagnose.

### Structured Output

Prompts request valid JSON rather than prose so the returned data can be converted directly into typed result objects.

### Evidence Preservation

Where possible, the model returns source evidence supporting the extracted value.

This helps distinguish an extraction grounded in the posting from an unsupported inference.

### Explicit Uncertainty

Each result carries a confidence value and may include a warning.

The system therefore does not assume that every AI-produced field is equally reliable.

### Anti-Hallucination Rules

Prompts repeatedly instruct the model not to invent missing information.

When a value cannot be established from the posting, the preferred result is `null`, `false`, or an empty list depending on the field.

### Normalization

Some prompts instruct the model to normalize equivalent terms, particularly skills.

Selected fields also receive deterministic normalization after AI extraction.

## Maintenance

When changing a parser prompt:

1. Keep its output contract compatible with the corresponding result dataclass.
2. Update parser tests for any intentional behavior change.
3. Preserve evidence, confidence, and warning information where applicable.
4. Prefer explicit rules over relying on unstated model behavior.
5. Add deterministic handling when a rule can be implemented reliably without AI.
6. Update this document when the prompt contract or major extraction rules change.

The source files remain the authoritative implementation. This document describes the intent and contract of the prompts so their behavior can be understood without reading every prompt string in the Python code.
