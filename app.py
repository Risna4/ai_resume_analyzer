import streamlit as st

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import calculate_match_scores, find_missing_skills
from roadmap_generator import generate_roadmap


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume and find suitable job roles "
    "based on your skills."
)


# ==================================================
# RESUME UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)


# ==================================================
# PROCESS UPLOADED RESUME
# ==================================================

if uploaded_file is not None:

    # ==================================================
    # FILE SIZE VALIDATION
    # ==================================================

    max_file_size = 5 * 1024 * 1024  # 5 MB

    if uploaded_file.size > max_file_size:

        st.error(
            "File size is too large. "
            "Please upload a resume smaller than 5 MB."
        )

        st.stop()

    # ==================================================
    # DISPLAY UPLOADED FILE
    # ==================================================

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    # ==================================================
    # EXTRACT TEXT FROM RESUME
    # ==================================================

    resume_text = extract_resume_text(
        uploaded_file
    )


    # ==================================================
    # CHECK WHETHER TEXT WAS EXTRACTED
    # ==================================================

    if not resume_text.strip():

        st.error(
            "Could not extract text from the resume."
        )

    else:

        # ==================================================
        # CLEAN RESUME TEXT
        # ==================================================

        cleaned_text = clean_text(
            resume_text
        )


        # ==================================================
        # EXTRACT SKILLS
        # ==================================================

        skills = extract_skills(
            cleaned_text
        )

        st.subheader(
            "🔎 Extracted Skills"
        )

        if skills:

            st.write(
                ", ".join(skills)
            )

        else:

            st.warning(
                "No known skills were detected."
            )


        # ==================================================
        # JOB ROLE MATCHING
        # ==================================================

        st.subheader(
            "🎯 Job Role Recommendations"
        )

        results = calculate_match_scores(
            cleaned_text
        )

        # Round match scores
        results["score"] = results[
            "score"
        ].round(2)


        # ==================================================
        # TOP 3 JOB ROLES
        # ==================================================

        st.write(
            "### 🏆 Top 3 Recommended Roles"
        )

        top_roles = results.head(3)

        for index, row in top_roles.iterrows():

            st.write(
                f"**{index + 1}. {row['role']}**"
            )

            score = min(
                int(row["score"]),
                100
            )

            st.progress(
                score
            )

            st.write(
                f"Match Score: **{row['score']}%**"
            )


        # ==================================================
        # MATCH SCORE CHART
        # ==================================================

        st.subheader(
            "📊 Match Scores for All Roles"
        )

        chart_data = results[
            ["role", "score"]
        ].set_index("role")

        st.bar_chart(
            chart_data
        )


        # ==================================================
        # DETAILED MATCH SCORES
        # ==================================================

        st.subheader(
            "📋 Detailed Match Scores"
        )

        st.dataframe(
            results[
                ["role", "score"]
            ],
            use_container_width=True
        )


        # ==================================================
        # TARGET ROLE
        # ==================================================

        st.subheader(
            "🎯 Select Target Role"
        )

        selected_role = st.selectbox(
            "Choose a role for skill-gap analysis:",
            results["role"].tolist()
        )


        # ==================================================
        # GET SELECTED JOB
        # ==================================================

        selected_job = results[
            results["role"] == selected_role
        ].iloc[0]


        # ==================================================
        # REQUIRED SKILLS FOR SELECTED ROLE
        # ==================================================

        required_skills = [
            skill.strip()
            for skill in selected_job[
                "skills"
            ].split(",")
        ]


        # ==================================================
        # SKILLS FOUND FOR SELECTED ROLE
        # ==================================================

        st.subheader(
            "✅ Skills Found"
        )

        found_for_role = []

        for skill in required_skills:

            if skill.lower() in [
                s.lower()
                for s in skills
            ]:

                found_for_role.append(
                    skill
                )


        if found_for_role:

            for skill in found_for_role:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.info(
                "No required skills for this role "
                "were detected in the resume."
            )


        # ==================================================
        # MISSING SKILLS
        # ==================================================

        missing_skills = find_missing_skills(
            skills,
            required_skills
        )

        st.subheader(
            "❌ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"❌ {skill}"
                )

        else:

            st.success(
                "No missing skills found from "
                "the selected skill list."
            )


        # ==================================================
        # LEARNING ROADMAP
        # ==================================================

        st.subheader(
            "📚 Learning Roadmap"
        )

        roadmap = generate_roadmap(
            missing_skills
        )

        if roadmap:

            for i, (skill, explanation) in enumerate(
                roadmap,
                start=1
            ):

                st.write(
                    f"### Step {i}: {skill}"
                )

                st.write(
                    explanation
                )

        else:

            st.success(
                "You already have the listed skills "
                "for this role!"
            )


        # ==================================================
        # DOWNLOAD ANALYSIS REPORT
        # ==================================================

        st.subheader(
            "📥 Download Analysis Report"
        )

        report = ""

        report += "AI RESUME ANALYZER - ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"

        # Resume information
        report += f"Resume: {uploaded_file.name}\n\n"


        # ==================================================
        # EXTRACTED SKILLS IN REPORT
        # ==================================================

        report += "EXTRACTED SKILLS\n"
        report += "-" * 30 + "\n"

        if skills:

            report += (
                ", ".join(skills)
                + "\n\n"
            )

        else:

            report += (
                "No known skills were detected.\n\n"
            )


        # ==================================================
        # TOP 3 RECOMMENDED ROLES IN REPORT
        # ==================================================

        report += "TOP 3 RECOMMENDED JOB ROLES\n"
        report += "-" * 30 + "\n"

        for i, (_, row) in enumerate(
            top_roles.iterrows(),
            start=1
        ):

            report += (
                f"{i}. {row['role']} - "
                f"{row['score']}% match\n"
            )

        report += "\n"


        # ==================================================
        # SELECTED TARGET ROLE IN REPORT
        # ==================================================

        report += "SELECTED TARGET ROLE\n"
        report += "-" * 30 + "\n"

        report += (
            f"{selected_role}\n\n"
        )


        # ==================================================
        # SKILLS FOUND IN REPORT
        # ==================================================

        report += "SKILLS FOUND FOR TARGET ROLE\n"
        report += "-" * 30 + "\n"

        if found_for_role:

            for skill in found_for_role:

                report += (
                    f"✓ {skill}\n"
                )

        else:

            report += (
                "No required skills detected.\n"
            )

        report += "\n"


        # ==================================================
        # MISSING SKILLS IN REPORT
        # ==================================================

        report += "MISSING SKILLS\n"
        report += "-" * 30 + "\n"

        if missing_skills:

            for skill in missing_skills:

                report += (
                    f"✗ {skill}\n"
                )

        else:

            report += (
                "No missing skills found.\n"
            )

        report += "\n"


        # ==================================================
        # LEARNING ROADMAP IN REPORT
        # ==================================================

        report += "LEARNING ROADMAP\n"
        report += "-" * 30 + "\n"

        if roadmap:

            for i, (skill, explanation) in enumerate(
                roadmap,
                start=1
            ):

                report += (
                    f"Step {i}: {skill}\n"
                )

                report += (
                    f"{explanation}\n\n"
                )

        else:

            report += (
                "No additional learning steps required "
                "from the selected skill list.\n"
            )


        # ==================================================
        # REPORT DISCLAIMER
        # ==================================================

        report += "\n"
        report += "NOTE\n"
        report += "-" * 30 + "\n"

        report += (
            "Match scores are estimates based on the "
            "skills and job-role data used by this system.\n"
        )

        report += (
            "Missing a keyword does not necessarily mean "
            "the candidate lacks the actual skill.\n"
        )


        # ==================================================
        # DOWNLOAD BUTTON
        # ==================================================

        st.download_button(
            label="📄 Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )


        # ==================================================
        # VIEW EXTRACTED RESUME
        # ==================================================

        with st.expander(
            "📄 View Extracted Resume Text"
        ):

            st.text(
                resume_text
            )