from typing import Any, Dict

from models.job_opening import JobOpening

from parsers.title_parser import verify_job_title
from parsers.company_parser import verify_company_name
from parsers.location_parser import verify_job_location
from parsers.remote_status_parser import verify_job_remote_status
from parsers.employment_type_parser import verify_job_employment_type
from parsers.security_clearnance_parser import verify_job_security_clearance


def parser_metadata(result: Any) -> Dict[str, Any]:
    return {
        "confidence": getattr(result, "confidence", 0.0),
        "evidence": getattr(result, "evidence", None),
        "warning": getattr(result, "warning", None),
    }


def parse_job_opening(job_text: str, source_file: str) -> JobOpening:
    title_result = verify_job_title(job_text)
    company_result = verify_company_name(job_text)
    location_result = verify_job_location(job_text)
    remote_status_result = verify_job_remote_status(job_text)
    employment_type_result = verify_job_employment_type(job_text)
    security_clearance_result = verify_job_security_clearance(job_text)

    return JobOpening(
        source_file=source_file,

        title=title_result.title,
        company=company_result.name,
        location=location_result.location,

        remote_status=remote_status_result.status,
        employment_type=employment_type_result.employment_type,

        security_clearance_required=security_clearance_result.required,
        security_clearance_level=security_clearance_result.level,

        required_skills=[],
        preferred_skills=[],
        responsibilities=[],

        salary_range=None,
        notes=[],

        parser_metadata={
            "title": parser_metadata(title_result),
            "company": parser_metadata(company_result),
            "location": parser_metadata(location_result),
            "remote_status": parser_metadata(remote_status_result),
            "employment_type": parser_metadata(employment_type_result),
            "security_clearance": parser_metadata(security_clearance_result),
        },
    )
