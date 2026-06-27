import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@dataclass
class ResponsibilitiesResult:
    responsibilities: List[str] = field(default_factory=list)
    confidence: float = 0.0
    evidence: Optional[str] = None
    warning: Optional[str] = None


def verify_responsibilities(job_text: str) -> ResponsibilitiesResult:
    prompt = f"""
You are extracting primary job responsibilities from a job description.

Normalize equivalent technologies whenever possible.

Return ONLY valid JSON with this format:

{{
  "responsibilities": [
    "Design automated test frameworks",
    "Develop Python test scripts",
    "Collaborate with developers",
    "Review test results"
  ],
  "confidence": 0.95,
  "evidence": "Responsibilities include designing automation frameworks and collaborating with engineering teams.",
  "warning": null
}}

Rules:

- Extract only the major job responsibilities.
- Write each responsibility as a concise action statement.
- Do not include qualifications or skills.
- Remove duplicate or overlapping responsibilities.
- Prefer verb phrases beginning with an action word such as:
    Design
    Develop
    Implement
    Build
    Test
    Maintain
    Analyze
    Collaborate
    Lead
    Support
- Limit the list to approximately 5–10 responsibilities.
- Do not invent responsibilities.
- Return only valid JSON.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return ResponsibilitiesResult(
        responsibilities=data.get("responsibilities", []),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )
