import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class LocationResult:
    location: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_job_location(job_text: str) -> LocationResult:
    prompt = f"""
You are extracting the official job location from a job description.

Return ONLY valid JSON with these fields:
- location: string or null
- confidence: number from 0.0 to 1.0
- evidence: short quote or phrase from the job description that supports the location
- warning: string or null

Rules:
- Extract city/state/country if present.
- If remote/hybrid is stated separately, do not treat that as location.
- Use null if no physical location is given.
- Do not invent a location.
- Prefer the exact location used in the posting.
- If multiple locations appear, choose the most likely official posting location and explain in warning.
- If no location is clear, use null.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return LocationResult(
        location=data.get("location"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )

