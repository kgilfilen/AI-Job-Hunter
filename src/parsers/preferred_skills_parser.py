import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@dataclass
class PreferredSkillsResult:
    preferred_skills: List[str] = field(default_factory=list)
    confidence: float = 0.0
    evidence: Optional[str] = None
    warning: Optional[str] = None


def verify_preferred_skills(job_text: str) -> PreferredSkillsResult:
    prompt = f"""
You are extracting preferred skills from a job description.

Normalize equivalent technologies whenever possible.

Return ONLY valid JSON with this format:

{{
  "preferred_skills": [
    "AWS",
    "Kubernetes",
    "C#"
  ],
  "confidence": 0.95,
  "evidence": "Experience with AWS and Kubernetes is preferred.",
  "warning": null
}}

Rules:

- Extract only skills that are explicitly preferred, desired, nice-to-have, a plus, beneficial, or equivalent wording.
- Do NOT include required skills.
- Include programming languages, frameworks, cloud platforms, databases, testing tools, operating systems, methodologies, and domain knowledge.
- Normalize names (e.g. "Amazon Web Services" -> "AWS").
- Do not invent skills.
- If no preferred skills are listed, return an empty list.
- Return only valid JSON.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return PreferredSkillsResult(
        preferred_skills=data.get("preferred_skills", []),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )
