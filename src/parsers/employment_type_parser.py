import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class EmploymentTypeResult:
    employment_type: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_job_employment_type(job_text: str) -> EmploymentTypeResult:
    prompt = f"""
You are extracting the official job employment type from a job description.

Return ONLY valid JSON with these fields:
- employment_type: string or null
- confidence: number from 0.0 to 1.0
- evidence: short quote or phrase from the job description that supports the employment type
- warning: string or null

Allowed values:
- full-time
- part-time
- contract
- contract_to_hire
- temporary
- internship
- unknown

Rules:
- Do not infer employment type just because no location is listed.
- Extract employment type if present.
- Use null if no employment type is given.
- Do not invent a type.
- Prefer the exact type used in the posting.
- If multiple types appear, choose the most likely official posting type and explain in warning.
- If no type is clear, use null.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return EmploymentTypeResult(
        employment_type=data.get("employment_type"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )