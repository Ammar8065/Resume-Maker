import streamlit as st


def render_ats_score(score_data):
    overall = score_data["overall_score"]
    breakdown = score_data["breakdown"]

    # Color based on score
    if overall >= 80:
        color = "#28a745"
        label = "Excellent"
    elif overall >= 60:
        color = "#ffc107"
        label = "Good"
    elif overall >= 40:
        color = "#fd7e14"
        label = "Needs Work"
    else:
        color = "#dc3545"
        label = "Poor"

    # Big score display
    st.markdown(
        f"""
        <div style="text-align:center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border-radius: 12px; margin-bottom: 16px;">
            <div style="font-size: 48px; font-weight: bold; color: {color};">{overall}</div>
            <div style="font-size: 16px; color: {color}; font-weight: 600;">{label}</div>
            <div style="font-size: 12px; color: #aaa; margin-top: 4px;">ATS Compatibility Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Breakdown
    cols = st.columns(4)
    sections = [
        ("Keyword Match", breakdown["keyword_match"]),
        ("Sections", breakdown["section_completeness"]),
        ("Formatting", breakdown["formatting"]),
        ("Content", breakdown["content_quality"]),
    ]

    for col, (name, data) in zip(cols, sections):
        score = data["score"]
        weight = data["weight"]
        if score >= 80:
            s_color = "#28a745"
        elif score >= 60:
            s_color = "#ffc107"
        else:
            s_color = "#dc3545"

        col.markdown(
            f"""
            <div style="text-align:center; padding: 10px; background: #0e1117;
                        border: 1px solid #333; border-radius: 8px;">
                <div style="font-size: 24px; font-weight: bold; color: {s_color};">{score}</div>
                <div style="font-size: 11px; color: #ccc;">{name}</div>
                <div style="font-size: 10px; color: #666;">{weight}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Detailed breakdown in expanders
    st.markdown("")

    # Keywords
    kw = breakdown["keyword_match"]
    with st.expander(f"Keyword Analysis ({len(kw['matched'])} matched, {len(kw['missing'])} missing)"):
        if kw["matched"]:
            matched_tags = " ".join(
                [f'<span style="background:#28a74533;color:#28a745;padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{k}</span>' for k in kw["matched"][:30]]
            )
            st.markdown(f"**Matched:** {matched_tags}", unsafe_allow_html=True)
        if kw["missing"]:
            missing_tags = " ".join(
                [f'<span style="background:#dc354533;color:#dc3545;padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{k}</span>' for k in kw["missing"][:20]]
            )
            st.markdown(f"**Missing:** {missing_tags}", unsafe_allow_html=True)

    # Content suggestions
    content = breakdown["content_quality"]
    if content["suggestions"]:
        with st.expander("Content Improvement Suggestions"):
            for suggestion in content["suggestions"]:
                st.markdown(f"- {suggestion}")

    # LLM suggestions
    return overall
