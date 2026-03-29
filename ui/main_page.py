import streamlit as st
from config.settings import MODELS, get_api_key_error_message, get_api_key_for_model
from services.llm_service import tailor_resume
from services.ats_scorer import compute_ats_score, extract_keywords
from services.pdf_generator import generate_resume_pdf
from services.profile_manager import load_profile, validate_profile
from services.usage_logger import log_usage
from ui.components import render_ats_score


def render_main_page():
    st.title("Resume Maker")
    st.caption("Paste a job description, pick a model, and get a tailored ATS-optimized resume PDF.")

    if "profile" not in st.session_state:
        st.session_state.profile = load_profile()

    # ---- Model Selection ----
    model_name = st.selectbox(
        "Model",
        options=list(MODELS.keys()),
        key="model_select",
    )

    # ---- Job Description Input ----
    st.markdown("### Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        height=250,
        key="jd_input",
        label_visibility="collapsed",
        placeholder="Paste the full job description here...",
    )

    # ---- Generate Button ----
    generate = st.button("Generate Tailored Resume", type="primary", use_container_width=True)

    if generate:
        api_key = get_api_key_for_model(model_name)
        if not api_key:
            st.error(get_api_key_error_message(model_name))
            return
        if not job_description.strip():
            st.error("Please paste a job description.")
            return

        profile = st.session_state.get("profile", {})
        issues = validate_profile(profile)
        if issues:
            st.warning("Profile issues: " + "; ".join(issues) + ". Results may be limited.")

        # Generate
        with st.spinner("Analyzing job description and tailoring your resume..."):
            try:
                tailored_data = tailor_resume(api_key, model_name, job_description, profile)
                st.session_state.tailored_data = tailored_data
            except Exception as e:
                st.error(f"LLM Error: {e}")
                return

        with st.spinner("Computing ATS score..."):
            ats_score = compute_ats_score(job_description, tailored_data)
            st.session_state.ats_score = ats_score

        with st.spinner("Generating PDF..."):
            try:
                personal_info = profile.get("personal_info", {})
                pdf_bytes = generate_resume_pdf(tailored_data, personal_info)
                st.session_state.pdf_bytes = pdf_bytes
            except Exception as e:
                st.error(f"PDF Error: {e}")
                return

        # --- Logging usage ---
        # Try to extract a JD title (first non-empty line or first 100 chars)
        jd_title = next((line.strip() for line in job_description.splitlines() if line.strip()), job_description[:100])
        # Extract skills from the JD
        skills = extract_keywords(job_description)
        log_usage(jd_title, skills)

        st.success("Resume generated!")

    # ---- Display Results ----
    if "ats_score" in st.session_state and st.session_state.ats_score:
        st.markdown("---")
        st.markdown("### ATS Score")
        render_ats_score(st.session_state.ats_score)

    if "tailored_data" in st.session_state and st.session_state.tailored_data:
        tailored = st.session_state.tailored_data

        kw_analysis = tailored.get("keyword_analysis", {})
        if kw_analysis.get("suggestions"):
            st.markdown("### AI Suggestions")
            st.info(kw_analysis["suggestions"])

    if "pdf_bytes" in st.session_state and st.session_state.pdf_bytes:
        st.markdown("---")
        st.download_button(
            label="Download Resume PDF",
            data=st.session_state.pdf_bytes,
            file_name="tailored_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
