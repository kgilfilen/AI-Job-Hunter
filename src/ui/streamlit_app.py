from pathlib import Path

import streamlit as st

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

st.title("AI Career Manager")
st.write(
    "Review and improve the candidate profile used "
    "for job-fit scoring."
)

profile_service = ProfileService()

try:
    profile = profile_service.load(
        PROFILE_PATH
    )
except Exception as exc:
    st.error(
        f"Unable to load candidate profile: {exc}"
    )
    st.stop()


st.subheader("Candidate Profile")

st.write(f"**Name:** {profile.name}")

if profile.email:
    st.write(f"**Email:** {profile.email}")


st.markdown("### Core Skills")

if profile.core_skills:
    for skill in profile.core_skills:
        st.write(f"• {skill}")
else:
    st.info(
        "No core skills are currently recorded."
    )


st.markdown("### Add Skill")

new_skill = st.text_input(
    "Enter a new skill:",
    key="new_skill_input",
    placeholder="Example: Playwright",
)

if st.button(
    "Add Skill",
    type="primary",
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
            f"Added skill: {new_skill.strip()}"
        )

        st.rerun()

    except ValueError as exc:
        st.warning(str(exc))

    except Exception as exc:
        st.error(
            f"Unable to save profile: {exc}"
        )


for index, skill in enumerate(
    profile.core_skills
):
    skill_col, remove_col = st.columns(
        [4, 1]
    )

    with skill_col:
        st.write(skill)

    with remove_col:
        if st.button(
            "Remove",
            key=f"remove_skill_{index}",
        ):
            profile_service.remove_skill(
                profile,
                skill,
            )

            profile_service.save(
                profile=profile,
                profile_path=PROFILE_PATH,
            )

            st.rerun()