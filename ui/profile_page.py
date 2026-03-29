import streamlit as st
from services.profile_manager import load_profile, save_profile


def render_profile_page():
    st.title("Edit Profile")
    st.caption("Update your skills, experience, projects, and certifications. These are used to generate tailored resumes.")

    if "profile" not in st.session_state:
        st.session_state.profile = load_profile()

    profile = st.session_state.profile

    # ---- Personal Info ----
    st.subheader("Personal Information")
    info = profile.get("personal_info", {})
    col1, col2 = st.columns(2)
    with col1:
        info["full_name"] = st.text_input("Full Name", value=info.get("full_name", ""), key="pi_name")
        info["email"] = st.text_input("Email", value=info.get("email", ""), key="pi_email")
        info["phone"] = st.text_input("Phone", value=info.get("phone", ""), key="pi_phone")
        info["location"] = st.text_input("Location", value=info.get("location", ""), key="pi_location")
    with col2:
        info["linkedin"] = st.text_input("LinkedIn", value=info.get("linkedin", ""), key="pi_linkedin")
        info["github"] = st.text_input("GitHub", value=info.get("github", ""), key="pi_github")
        info["portfolio"] = st.text_input("Portfolio", value=info.get("portfolio", ""), key="pi_portfolio")
    profile["personal_info"] = info

    st.divider()

    # ---- Summary ----
    st.subheader("Professional Summary")
    profile["summary"] = st.text_area(
        "Summary (will be tailored per job)",
        value=profile.get("summary", ""),
        height=100,
        key="pi_summary",
        label_visibility="collapsed",
    )

    st.divider()

    # ---- Skills ----
    st.subheader("Skills")
    skills = profile.get("skills", {"technical": [], "tools": [], "soft": []})
    col1, col2, col3 = st.columns(3)
    with col1:
        skills["technical"] = [
            s.strip()
            for s in st.text_area(
                "Technical Skills (comma-separated)",
                value=", ".join(skills.get("technical", [])),
                key="sk_tech",
            ).split(",")
            if s.strip()
        ]
    with col2:
        skills["tools"] = [
            s.strip()
            for s in st.text_area(
                "Tools & Technologies (comma-separated)",
                value=", ".join(skills.get("tools", [])),
                key="sk_tools",
            ).split(",")
            if s.strip()
        ]
    with col3:
        skills["soft"] = [
            s.strip()
            for s in st.text_area(
                "Soft Skills (comma-separated)",
                value=", ".join(skills.get("soft", [])),
                key="sk_soft",
            ).split(",")
            if s.strip()
        ]
    profile["skills"] = skills

    st.divider()

    # ---- Experience ----
    st.subheader("Work Experience")
    experience = profile.get("experience", [])

    for i, exp in enumerate(experience):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                exp["title"] = st.text_input("Job Title", value=exp.get("title", ""), key=f"exp_title_{i}")
                exp["company"] = st.text_input("Company", value=exp.get("company", ""), key=f"exp_company_{i}")
            with col2:
                exp["location"] = st.text_input("Location", value=exp.get("location", ""), key=f"exp_loc_{i}")
                c1, c2 = st.columns(2)
                with c1:
                    exp["start_date"] = st.text_input("Start Date", value=exp.get("start_date", ""), key=f"exp_start_{i}")
                with c2:
                    exp["end_date"] = st.text_input("End Date", value=exp.get("end_date", ""), key=f"exp_end_{i}")
            with col3:
                st.markdown("")
                st.markdown("")
                if st.button("Remove", key=f"exp_remove_{i}", type="secondary"):
                    experience.pop(i)
                    st.rerun()

            bullets_text = st.text_area(
                "Achievements (one per line)",
                value="\n".join(exp.get("bullets", [])),
                height=120,
                key=f"exp_bullets_{i}",
            )
            exp["bullets"] = [b.strip() for b in bullets_text.split("\n") if b.strip()]

    if st.button("+ Add Experience", key="exp_add"):
        experience.append({
            "title": "", "company": "", "location": "",
            "start_date": "", "end_date": "", "bullets": [],
        })
        st.rerun()
    profile["experience"] = experience

    st.divider()

    # ---- Education ----
    st.subheader("Education")
    education = profile.get("education", [])

    for i, edu in enumerate(education):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                edu["degree"] = st.text_input("Degree", value=edu.get("degree", ""), key=f"edu_deg_{i}")
                edu["institution"] = st.text_input("Institution", value=edu.get("institution", ""), key=f"edu_inst_{i}")
            with col2:
                edu["graduation_date"] = st.text_input("Graduation Date", value=edu.get("graduation_date", ""), key=f"edu_grad_{i}")
                edu["gpa"] = st.text_input("GPA (optional)", value=edu.get("gpa", ""), key=f"edu_gpa_{i}")
            with col3:
                st.markdown("")
                st.markdown("")
                if st.button("Remove", key=f"edu_remove_{i}", type="secondary"):
                    education.pop(i)
                    st.rerun()

            highlights_text = st.text_area(
                "Highlights (one per line)",
                value="\n".join(edu.get("highlights", [])),
                height=80,
                key=f"edu_hl_{i}",
            )
            edu["highlights"] = [h.strip() for h in highlights_text.split("\n") if h.strip()]

    if st.button("+ Add Education", key="edu_add"):
        education.append({
            "degree": "", "institution": "", "graduation_date": "",
            "gpa": "", "highlights": [],
        })
        st.rerun()
    profile["education"] = education

    st.divider()

    # ---- Projects ----
    st.subheader("Projects")
    projects = profile.get("projects", [])

    for i, proj in enumerate(projects):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                proj["name"] = st.text_input("Project Name", value=proj.get("name", ""), key=f"proj_name_{i}")
                proj["description"] = st.text_input("Description", value=proj.get("description", ""), key=f"proj_desc_{i}")
            with col2:
                proj["technologies"] = [
                    t.strip()
                    for t in st.text_input(
                        "Technologies (comma-separated)",
                        value=", ".join(proj.get("technologies", [])),
                        key=f"proj_tech_{i}",
                    ).split(",")
                    if t.strip()
                ]
                proj["url"] = st.text_input("URL (optional)", value=proj.get("url", ""), key=f"proj_url_{i}")
            with col3:
                st.markdown("")
                st.markdown("")
                if st.button("Remove", key=f"proj_remove_{i}", type="secondary"):
                    projects.pop(i)
                    st.rerun()

            bullets_text = st.text_area(
                "Key Points (one per line)",
                value="\n".join(proj.get("bullets", [])),
                height=80,
                key=f"proj_bullets_{i}",
            )
            proj["bullets"] = [b.strip() for b in bullets_text.split("\n") if b.strip()]

    if st.button("+ Add Project", key="proj_add"):
        projects.append({
            "name": "", "description": "", "technologies": [],
            "url": "", "bullets": [],
        })
        st.rerun()
    profile["projects"] = projects

    st.divider()

    # ---- Certifications ----
    st.subheader("Certifications")
    certs = profile.get("certifications", [])

    for i, cert in enumerate(certs):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                cert["name"] = st.text_input("Certification Name", value=cert.get("name", ""), key=f"cert_name_{i}")
                cert["issuer"] = st.text_input("Issuer", value=cert.get("issuer", ""), key=f"cert_issuer_{i}")
            with col2:
                cert["date"] = st.text_input("Date", value=cert.get("date", ""), key=f"cert_date_{i}")
                cert["credential_id"] = st.text_input("Credential ID (optional)", value=cert.get("credential_id", ""), key=f"cert_id_{i}")
            with col3:
                st.markdown("")
                st.markdown("")
                if st.button("Remove", key=f"cert_remove_{i}", type="secondary"):
                    certs.pop(i)
                    st.rerun()

    if st.button("+ Add Certification", key="cert_add"):
        certs.append({"name": "", "issuer": "", "date": "", "credential_id": ""})
        st.rerun()
    profile["certifications"] = certs

    # ---- Save Button ----
    st.divider()
    if st.button("Save Profile", type="primary", use_container_width=True):
        save_profile(profile)
        st.session_state.profile = profile
        st.success("Profile saved!")
