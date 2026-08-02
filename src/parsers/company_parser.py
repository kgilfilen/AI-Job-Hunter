import json
import os
from dataclasses import dataclass
from openai import OpenAI
from typing import Optional


@dataclass
class CompanyNameResult:
    name: Optional[str]
    confidence: float
    evidence: Optional[str]
    warning: Optional[str] = None


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def verify_company_name(job_text: str) -> CompanyNameResult:
    prompt = f"""
You are extracting the official company name from a job description.

Return ONLY valid JSON with these fields:
- name: string or null
- confidence: number from 0.0 to 1.0
- evidence: short quote or phrase from the job description that supports the name
- warning: string or null

Rules:
- Extract the hiring company, not a vendor, recruiter, product, or client unless clearly stated.
- If the posting says “our client,” set company to null and add a warning.
- Do not invent a name.
- Prefer the exact name used in the posting.
- If multiple names appear, choose the most likely official posting name and explain in warning.
- If no name is clear, use null.
- When identifying the company, inspect explicitly labeled fields such as:
        - Company
        - Employer
        - Business Unit
        - Division
        - Organization
        - Client
        - Hiring Company

    Prefer explicitly labeled metadata over inferred company names from narrative text.
    Do not treat a division as the company when a parent business unit is also provided.
- When the company is not given in a labeled field, inspect the entire posting for:
        - full employer names in EEO or legal statements
        - official careers URLs
        - recruiting email domains
        - phrases such as "<Company> office" or "join Team <Brand>"
        - repeated brand references

        Prefer the most specific full legal or brand name supported by multiple clues.
        Do not return a shortened brand name when the full company name appears elsewhere.

JOB DESCRIPTION:
{job_text}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    data = json.loads(response.output_text)

    return CompanyNameResult(
        name=data.get("name"),
        confidence=float(data.get("confidence", 0.0)),
        evidence=data.get("evidence"),
        warning=data.get("warning"),
    )

