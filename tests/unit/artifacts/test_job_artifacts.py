"""Unit tests for job artifact organization."""

import json
import pytest

from src.artifacts.job_artifacts import (
    get_job_artifact_directory,
    write_original_job_artifact,
)
from src.models.job_opening import JobOpening
from src.artifacts.analysis_artifacts import _write_json


def test_get_job_artifact_directory_uses_zero_padded_job_id(
    tmp_path,
) -> None:
    directory = get_job_artifact_directory(
        job_id=17,
        artifact_root=tmp_path,
    )

    assert directory == tmp_path / "000017"
    assert directory.is_dir()


def test_get_job_artifact_directory_rejects_invalid_job_id(
    tmp_path,
) -> None:
    with pytest.raises(
        ValueError,
        match="job_id must be greater than zero",
    ):
        get_job_artifact_directory(
            job_id=0,
            artifact_root=tmp_path,
        )


def test_write_original_job_artifact_preserves_exact_text(
    tmp_path,
) -> None:
    job_text = "Original job description\nwith exact spacing.\n"

    output_path = write_original_job_artifact(
        job_id=42,
        job_text=job_text,
        artifact_root=tmp_path,
    )

    assert output_path == tmp_path / "000042" / "original_job.txt"
    assert output_path.read_text(encoding="utf-8") == job_text
    
def test_write_json_includes_company(tmp_path) -> None:
    job = JobOpening(
        source_file="applied_systems_sdet.txt",
        title="Software Development Engineer in Test",
        company="Applied Systems",
        location="Remote",
        remote_status="Remote",
        employment_type="Full-time",
        security_clearance_required=False,
        security_clearance_level=None,
    )

    output_file = tmp_path / "job.json"

    _write_json(
        output_file=output_file,
        value=job,
    )

    saved = json.loads(output_file.read_text(encoding="utf-8"))

    assert saved["company"] == "Applied Systems"

