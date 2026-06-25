import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class SecurityClearanceResult:
    required: bool
    level: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_job_security_clearance(job_text: str) -> SecurityClearanceResult:
    prompt = f"""
You are extracting security clearance requirements from a job description.

Return ONLY valid JSON with these fields:
{{
"clearance_required": true,
"clearance_level": "Secret",
"confidence": 0.95,
"evidence": "Active Secret Security Clearance required",
"warning": null
}}

Field definitions:

* clearance_required: true or false
* clearance_level: one of:
    “Public Trust”
    “Confidential”
    “Secret”
    “Top Secret”
    “TS/SCI”
    “SCI”
    “Polygraph”
    “TS/SCI with Polygraph”
    “Other”
    null
* confidence: number from 0.0 to 1.0
* evidence: short quote from the job description supporting the decision
* warning: string or null

Rules:

* Do not invent a clearance requirement.
* If the posting explicitly states no clearance is required, set clearance_required to false.
* If no clearance information is present, set clearance_required to false and clearance_level to null.
* If multiple clearance levels are mentioned, choose the highest required level and explain in warning.
* If the posting says “ability to obtain clearance”, set clearance_required to true.
* Prefer exact terminology used in the posting.
* Return only valid JSON.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return SecurityClearanceResult(
        required=data.get("clearance_required", False),
        level=data.get("clearance_level"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )