from pathlib import Path

import streamlit as st

from src.database.repository import SQLiteJobRepository
from src.services.job_service import JobService
from src.services.profile_service import ProfileService


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROFILE_PATH = (
    PROJECT_ROOT
    / "config"
    / "candidate_profile.json"
)


st.set_page_config(
    page_title="AI Career Manager",
    page_icon="💼",
    layout="centered",
)


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

profile_service = ProfileService()

repository = SQLiteJobRepository()

job_service = JobService(
    repository=repository,
)


# ---------------------------------------------------------
# Load Candidate Profile
# ---------------------------------------------------------

try:
    profile = profile_service.load(
        PROFILE_PATH
    )

except Exception as exc:
    st.error(
        f"Unable to load candidate profile: {exc}"
    )
    st.stop()


# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------

st.title("AI Career Manager")

st.write(
    "Analyze job opportunities and improve the candidate "
    "profile used for job-fit scoring."
)


# =========================================================
# JOB ANALYSIS
# =========================================================

st.header("Analyze Job")

job_url = st.text_input(
    "Job URL",
    key="job_url_input",
    placeholder=(
        "https://example.com/jobs/123"
    ),
)

reprocess = st.checkbox(
    "Reprocess if this job already exists",
    key="reprocess_job",
)

if st.button(
    "Analyze Job",
    type="primary",
    key="analyze_job",
):

    if not job_url.strip():
        st.warning(
            "Enter a job URL."
        )

    else:
        try:
            with st.spinner(
                "Fetching and analyzing job..."
            ):
                result = job_service.analyze_url(
                    url=job_url.strip(),
                    profile=profile,
                    reprocess=reprocess,
                )

            st.session_state[
                "job_analysis_result"
            ] = result

        except Exception as exc:
            st.error(
                f"Unable to analyze job: {exc}"
            )


# ---------------------------------------------------------
# Display Current Job Analysis
# ---------------------------------------------------------

result = st.session_state.get(
    "job_analysis_result"
)

if result is not None:

    st.divider()

    if result.skipped:

        st.info(
            f"Job {result.job_id} already exists. "
            "Enable reprocessing to analyze it again."
        )

    else:

        job = result.job_opening
        fit = result.fit_analysis

        if job is not None:

            st.subheader(
                job.title
                or "Untitled Job"
            )

            if job.company:
                st.write(
                    f"**Company:** {job.company}"
                )

            if job.location:
                st.write(
                    f"**Location:** {job.location}"
                )

            if job.remote_status:
                st.write(
                    "**Work arrangement:** "
                    f"{job.remote_status}"
                )

            if job.employment_type:
                st.write(
                    "**Employment type:** "
                    f"{job.employment_type}"
                )

        if fit is not None:

            st.metric(
                "Fit Score",
                fit.overall_score,
            )

            recommendation = (
                fit.recommendation
            )

            if hasattr(
                recommendation,
                "value",
            ):
                recommendation = (
                    recommendation.value
                )

            st.write(
                "**Recommendation:** "
                f"{recommendation}"
            )


        # -------------------------------------------------
        # Missing Skills
        # -------------------------------------------------

        missing_skills = getattr(
            fit,
            "missing_required_skills",
            [],
        )

        if missing_skills:

            st.markdown(
                "### Missing or Unmatched Skills"
            )

            st.write(
                "If you actually have experience with one "
                "of these skills, add it to your profile."
            )

            for index, skill in enumerate(
                missing_skills
            ):

                skill_col, add_col = (
                    st.columns(
                        [4, 1]
                    )
                )

                with skill_col:
                    st.write(skill)

                with add_col:

                    if st.button(
                        "Add",
                        key=(
                            "add_missing_skill_"
                            f"{index}"
                        ),
                    ):

                        try:
                            profile_service.add_skill(
                                profile,
                                skill,
                            )

                            profile_service.save(
                                profile=profile,
                                profile_path=(
                                    PROFILE_PATH
                                ),
                            )

                            st.success(
                                f"Added {skill} "
                                "to your profile."
                            )

                            st.rerun()

                        except ValueError as exc:
                            st.warning(
                                str(exc)
                            )

                        except Exception as exc:
                            st.error(
                                "Unable to update "
                                f"profile: {exc}"
                            )

        else:

            if fit is not None:
                st.success(
                    "No missing required skills "
                    "were reported."
                )


        # -------------------------------------------------
        # Generated Resume
        # -------------------------------------------------

        if result.resume_output_file:

            st.markdown(
                "### Generated Resume"
            )

            st.write(
                str(
                    result.resume_output_file
                )
            )


# =========================================================
# CANDIDATE PROFILE
# =========================================================

st.divider()

st.header("Candidate Profile")

st.write(
    f"**Name:** {profile.name}"
)

if profile.email:
    st.write(
        f"**Email:** {profile.email}"
    )


# ---------------------------------------------------------
# Core Skills
# ---------------------------------------------------------

st.markdown(
    "### Core Skills"
)

if profile.core_skills:

    for index, skill in enumerate(
        profile.core_skills
    ):

        skill_col, remove_col = (
            st.columns(
                [4, 1]
            )
        )

        with skill_col:
            st.write(
                skill
            )

        with remove_col:

            if st.button(
                "Remove",
                key=(
                    "remove_skill_"
                    f"{index}"
                ),
            ):

                try:
                    profile_service.remove_skill(
                        profile,
                        skill,
                    )

                    profile_service.save(
                        profile=profile,
                        profile_path=PROFILE_PATH,
                    )

                    st.rerun()

                except Exception as exc:
                    st.error(
                        "Unable to remove skill: "
                        f"{exc}"
                    )

else:

    st.info(
        "No core skills are currently recorded."
    )


# ---------------------------------------------------------
# Add One Skill
# ---------------------------------------------------------

st.markdown(
    "### Add Skill"
)

new_skill = st.text_input(
    "Enter a new skill:",
    key="new_skill_input",
    placeholder=(
        "Example: Playwright"
    ),
)

if st.button(
    "Add Skill",
    key="add_single_skill",
):

    try:
        profile_service.add_skill(
            profile,
            new_skill,
        )

        profile_service.save(
            profile=profile,
            profile_path=PROFILE_PATH,
        )

        st.success(
            f"Added skill: "
            f"{new_skill.strip()}"
        )

        st.rerun()

    except ValueError as exc:
        st.warning(
            str(exc)
        )

    except Exception as exc:
        st.error(
            f"Unable to save profile: {exc}"
        )


# ---------------------------------------------------------
# Add Multiple Skills
# ---------------------------------------------------------

st.markdown(
    "### Add Multiple Skills"
)

skills_text = st.text_input(
    "Enter skills separated by commas:",
    key="bulk_skill_input",
    placeholder=(
        "Example: Playwright, CI/CD, "
        "API testing"
    ),
)

if st.button(
    "Add Skills",
    key="bulk_add_skills",
):

    try:
        skills = [
            skill.strip()
            for skill
            in skills_text.split(",")
            if skill.strip()
        ]

        if not skills:
            raise ValueError(
                "Enter at least one skill."
            )

        for skill in skills:
            profile_service.add_skill(
                profile,
                skill,
            )

        profile_service.save(
            profile=profile,
            profile_path=PROFILE_PATH,
        )

        st.success(
            f"Processed {len(skills)} "
            "skill(s)."
        )

        st.rerun()

    except ValueError as exc:
        st.warning(
            str(exc)
        )

    except Exception as exc:
        st.error(
            f"Unable to save profile: {exc}"
        )