import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class RemoteStatusResult:
    status: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_job_remote_status(job_text: str) -> RemoteStatusResult:
    prompt = f"""
You are extracting the official job remote status from a job description.

Return ONLY valid JSON with these fields:
- status: string or null
- confidence: number from 0.0 to 1.0
- evidence: short quote or phrase from the job description that supports the status
- warning: string or null

Allowed values:
- remote
- hybrid
- onsite
- remote or hybrid
- hybrid or remote
- flexible
- unknown

Rules:
- Do not infer remote just because no location is listed.
- Extract remote/hybrid/in-office status if present.
- Use null if no remote status is given.
- Do not invent a status.
- Prefer the exact status used in the posting.
- If multiple statuses appear, choose the most likely official posting status and explain in warning.
- If no status is clear, use null.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return RemoteStatusResult(
        status=data.get("status"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )

