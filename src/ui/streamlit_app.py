from pathlib import Path
from datetime import datetime, timedelta, timezone

import streamlit as st

from src.database.repository import SQLiteJobRepository
from src.database.database import initialize_database
from src.services.job_service import JobService
from src.services.profile_service import ProfileService
from src.models.application_status import ApplicationStatus

from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)
from src.services.application_service import ApplicationService

from src.constants import ApplicationEventType

"""
Usage: python3 -m streamlit run src/ui/streamlit_app.py
"""

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

initialize_database()

repository = SQLiteJobRepository()

job_service = JobService(
    repository=repository,
)

application_repository = SQLiteApplicationRepository()

application_event_repository = (
    SQLiteApplicationEventRepository()
)

application_service = ApplicationService(
    application_repository=application_repository,
    event_repository=application_event_repository,
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

        application = application_repository.get_by_job_id(
            result.job_id
        )

        if application is None:
            if st.button(
                "Track Application",
                key=f"track_application_{result.job_id}",
            ):
                try:
                    application_repository.create_application(
                        result.job_id
                    )

                    st.success(
                        "Application tracking started."
                    )

                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Unable to track application: {exc}"
                    )

        else:
            st.info(
                f"Tracking application — "
                f"{application.status.value}"
            )

            if application.status == ApplicationStatus.INTERESTED:
                if st.button(
                    "Mark as Applied",
                    key=f"mark_applied_{application.id}",
                ):
                    try:
                        application_service.mark_applied(
                            application.id
                        )

                        st.success(
                            "Application marked as applied."
                        )

                        st.rerun()

                    except Exception as exc:
                        st.error(
                            f"Unable to mark application as applied: {exc}"
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
# APPLICATION MANAGEMENT
# =========================================================

st.divider()

st.header("Needs Attention")

due_at = datetime.now(timezone.utc).isoformat()

applications_needing_attention = (
    application_service.get_applications_needing_attention(
        due_at
    )
)

if not applications_needing_attention:
    st.info("No application follow-ups are currently due.")

else:
    for application in applications_needing_attention:
        job = repository.get_job(application.job_id)

        if job is None:
            job_title = f"Job {application.job_id}"
            company = None
        else:
            job_title = (
                job.get("title")
                or f"Job {application.job_id}"
            )
            company = job.get("company")

        st.subheader(job_title)

        if company:
            st.write(f"**Company:** {company}")

        st.write(
            f"**Status:** {application.status.value}"
        )

        if application.next_action:
            st.write(
                f"**Next action:** {application.next_action}"
            )

        if application.follow_up_at:
            st.write(
                f"**Follow up:** {application.follow_up_at}"
            )

        st.divider()


# ---------------------------------------------------------
# Recent Application Activity
# ---------------------------------------------------------

st.subheader("Recent Activity")

local_timezone = datetime.now().astimezone().tzinfo
today = datetime.now().astimezone().date()
yesterday = today - timedelta(days=1)

today_events = application_service.get_activity_for_date(
    today,
    timezone_info=local_timezone,
)

yesterday_events = application_service.get_activity_for_date(
    yesterday,
    timezone_info=local_timezone,
)


def display_application_events(
    label,
    events,
):
    """Display application events with associated job information."""

    st.markdown(f"### {label}")

    if not events:
        st.write("No application activity.")
        return

    for event in events:
        application = application_repository.get_application(
            event.application_id
        )

        if application is None:
            st.write(
                f"**{event.event_type}** — "
                f"Application {event.application_id}"
            )
            continue

        job = repository.get_job(application.job_id)

        if job is None:
            job_title = f"Job {application.job_id}"
            company = None
        else:
            job_title = (
                job.get("title")
                or f"Job {application.job_id}"
            )
            company = job.get("company")

        st.write(f"**{event.event_type}**")

        if company:
            st.write(
                f"{job_title} — {company}"
            )
        else:
            st.write(job_title)

        if event.notes:
            st.write(event.notes)

        st.caption(event.occurred_at)


display_application_events(
    "Today",
    today_events,
)

display_application_events(
    "Yesterday",
    yesterday_events,
)

# ---------------------------------------------------------
# Record Application Activity
# ---------------------------------------------------------

st.subheader("Record Activity")

tracked_applications = application_repository.list_applications()

if not tracked_applications:
    st.info("No tracked applications are available yet.")

else:
    application_labels = {}

    for application in tracked_applications:
        job = repository.get_job(application.job_id)

        if job is None:
            label = f"Job {application.job_id}"
        else:
            title = (
                job.get("title")
                or f"Job {application.job_id}"
            )
            company = job.get("company")

            if company:
                label = f"{title} — {company}"
            else:
                label = title

        application_labels[application.id] = label

    selected_application_id = st.selectbox(
        "Application",
        options=list(application_labels.keys()),
        format_func=lambda application_id: (
            application_labels[application_id]
        ),
    )

    selected_event_type = st.selectbox(
        "Activity",
        options=list(ApplicationEventType),
        format_func=lambda event_type: event_type.value,
    )

    activity_notes = st.text_area(
        "Notes",
        placeholder=(
            "Example: Second interview completed. "
            "Waiting for hiring-team response."
        ),
    )

    if st.button("Submit Activity"):
        application_service.record_activity(
            selected_application_id,
            selected_event_type,
            notes=activity_notes.strip() or None,
        )

        st.success("Application activity recorded.")
        st.rerun()

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