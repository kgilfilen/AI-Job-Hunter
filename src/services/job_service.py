"""Application service for job acquisition and analysis."""

from pathlib import Path
from typing import Optional

from src.artifacts.job_artifacts import (
    get_job_artifact_directory,
    write_original_job_artifact,
)
from src.database.repository import SQLiteJobRepository
from src.fetchers.web_fetcher import fetch_job_description
from src.formatters.job_page_formatter import build_parser_input
from src.formatters.resume_formatter import ResumeFormatter
from src.models.candidate_profile import CandidateProfile
from src.models.fit_analysis import FitAnalysis
from src.models.job_opening import JobOpening
from src.models.resume_recommendation import ResumeRecommendation
from src.parsers.job_opening_parser import parse_job_opening
from src.resume.resume_recommender import recommend_resume_changes
from src.scoring.fit_scorer import score_job

from src.artifacts.analysis_artifacts import (
    save_fit_analysis,
    save_job_opening,
    save_resume_recommendation,
    save_tailored_resume,
)

class JobAnalysisResult:
    """Result returned by a complete job-analysis workflow."""

    def __init__(
        self,
        job_id: int,
        artifact_directory: Path,
        skipped: bool,
        job_opening: Optional[JobOpening] = None,
        fit_analysis: Optional[FitAnalysis] = None,
        recommendation: Optional[
            ResumeRecommendation
        ] = None,
        job_output_file: Optional[Path] = None,
        fit_output_file: Optional[Path] = None,
        recommendation_output_file: Optional[
            Path
        ] = None,
        resume_output_file: Optional[Path] = None,
    ) -> None:
        self.job_id = job_id
        self.artifact_directory = artifact_directory
        self.skipped = skipped
        self.job_opening = job_opening
        self.fit_analysis = fit_analysis
        self.recommendation = recommendation
        self.job_output_file = job_output_file
        self.fit_output_file = fit_output_file
        self.recommendation_output_file = (
            recommendation_output_file
        )
        self.resume_output_file = resume_output_file


class JobService:
    """Coordinate job acquisition, parsing, scoring, and artifacts."""

    def __init__(
        self,
        repository: SQLiteJobRepository,
    ) -> None:
        self.repository = repository

    def analyze_url(
        self,
        url: str,
        profile: CandidateProfile,
        reprocess: bool = False,
    ) -> JobAnalysisResult:
        """Fetch and analyze one job URL."""

        normalized_url = url.strip()

        if not normalized_url:
            raise ValueError(
                "Job URL cannot be empty."
            )

        fetched_job = fetch_job_description(
            normalized_url
        )

        original_text = (
            fetched_job.visible_text.strip()
        )

        if not original_text:
            raise ValueError(
                "Fetched job description is empty: "
                f"{normalized_url}"
            )

        parser_text = build_parser_input(
            fetched_job
        )

        source_url = (
            fetched_job.canonical_url
            or fetched_job.requested_url
        )

        return self.analyze(
            source_name="fetched_job.txt",
            original_text=original_text,
            parser_text=parser_text,
            profile=profile,
            source="url",
            source_url=source_url,
            reprocess=reprocess,
        )

    def analyze(
        self,
        source_name: str,
        original_text: str,
        parser_text: str,
        profile: CandidateProfile,
        source: str,
        source_url: Optional[str] = None,
        reprocess: bool = False,
    ) -> JobAnalysisResult:
        """Process one job and return its analysis."""

        if not original_text:
            raise ValueError(
                f"Job description is empty: {source_name}"
            )

        if not parser_text:
            raise ValueError(
                f"Parser input is empty: {source_name}"
            )

        (
            job_id,
            artifact_directory,
            job_opening,
        ) = self._process_job_text(
            original_text=original_text,
            parser_text=parser_text,
            source_file=source_name,
            source=source,
            source_url=source_url,
            reprocess=reprocess,
        )

        if job_opening is None:
            return JobAnalysisResult(
                job_id=job_id,
                artifact_directory=artifact_directory,
                skipped=True,
            )

        fit_analysis = score_job(
            job_opening,
            profile,
        )

        self.repository.update_fit_analysis(
            job_id=job_id,
            fit_analysis=fit_analysis,
        )

        recommendation = recommend_resume_changes(
            job=job_opening,
            fit_analysis=fit_analysis,
            candidate=profile,
        )

        resume_text = ResumeFormatter().format(
            candidate=profile,
            job=job_opening,
            analysis=fit_analysis,
            recommendations=recommendation,
        )

        job_output_file = save_job_opening(
            job_opening=job_opening,
            job_artifact_directory=artifact_directory,
        )

        fit_output_file = save_fit_analysis(
            fit_analysis=fit_analysis,
            job_artifact_directory=artifact_directory,
        )

        recommendation_output_file = (
            save_resume_recommendation(
                recommendation=recommendation,
                job_artifact_directory=(
                    artifact_directory
                ),
            )
        )

        resume_output_file = save_tailored_resume(
            resume_text=resume_text,
            job_artifact_directory=artifact_directory,
        )

        return JobAnalysisResult(
            job_id=job_id,
            artifact_directory=artifact_directory,
            skipped=False,
            job_opening=job_opening,
            fit_analysis=fit_analysis,
            recommendation=recommendation,
            job_output_file=job_output_file,
            fit_output_file=fit_output_file,
            recommendation_output_file=(
                recommendation_output_file
            ),
            resume_output_file=resume_output_file,
        )


    def _process_job_text(
        self,
        original_text: str,
        parser_text: str,
        source_file: str,
        source: str,
        source_url: Optional[str] = None,
        reprocess: bool = False,
    ) -> tuple[
        int,
        Path,
        Optional[JobOpening],
    ]:
        """Store and parse unless an existing job is skipped."""

        save_result = self.repository.save_original_job(
            original_description=original_text,
            source=source,
            source_url=source_url,
        )

        job_id = save_result.job_id

        artifact_directory = (
            get_job_artifact_directory(
                job_id
            )
        )

        if (
            not save_result.created
            and not reprocess
        ):
            return (
                job_id,
                artifact_directory,
                None,
            )

        write_original_job_artifact(
            job_id=job_id,
            job_text=original_text,
        )

        job_opening = parse_job_opening(
            job_text=parser_text,
            source_file=source_file,
        )

        self.repository.update_parsed_job(
            job_id=job_id,
            job_opening=job_opening,
        )

        return (
            job_id,
            artifact_directory,
            job_opening,
        )

