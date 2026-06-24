import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class JobTitleResult:
    title: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_job_title(job_text: str) -> JobTitleResult:
    prompt = f"""
You are extracting the official job title from a job description.

Return ONLY valid JSON with these fields:
- title: string or null
- confidence: number from 0.0 to 1.0
- evidence: short quote or phrase from the job description that supports the title
- warning: string or null

Rules:
- Do not invent a title.
- Prefer the exact title used in the posting.
- If multiple titles appear, choose the most likely official posting title and explain in warning.
- If no title is clear, use null.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return JobTitleResult(
        title=data.get("title"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )
