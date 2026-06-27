import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@dataclass
class RequiredSkillsResult:
    required_skills: List[str] = field(default_factory=list)
    confidence: float = 0.0
    evidence: Optional[str] = None
    warning: Optional[str] = None


def verify_required_skills(job_text: str) -> RequiredSkillsResult:
    prompt = f"""
You are extracting required skills from a job description.

Normalize equivalent technologies whenever possible.

Return ONLY valid JSON with these fields:

{{
  "required_skills": [
    "Python",
    "pytest",
    "REST APIs"
  ],
  "confidence": 0.95,
  "evidence": "Required qualifications include Python, pytest, and REST API testing",
  "warning": null
}}

Rules:
- Extract only skills that appear required or strongly expected.
- Include programming languages, frameworks, tools, platforms, testing skills, domain skills, and methodologies.
- Do not include soft skills unless they are clearly listed as required.
- Do not invent skills.
- Prefer concise normalized names, such as "Python" instead of "strong Python programming experience".
- If no required skills are clear, return an empty list.
- Return only valid JSON.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return RequiredSkillsResult(
        required_skills=data.get("required_skills", []),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )
