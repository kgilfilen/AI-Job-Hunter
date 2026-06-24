

def test_job_opening_has_title():
    job = JobOpening(title="Software Engineer")
    assert job.title is not None