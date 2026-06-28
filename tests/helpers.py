from models.job_opening import JobOpening


def make_test_job(**overrides):
    defaults = {
        "source_file": "test.txt",
        "title": "SDET III",
        "company": "Example Company",
        "location": None,
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "salary_range": None,
        "remote_status": None,
        "employment_type": None,
        "security_clearance_required": False,
        "security_clearance_level": None,
        "notes": [],
        "parser_metadata": {},
    }

    defaults.update(overrides)

    return JobOpening(**defaults)