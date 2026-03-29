import streamlit as st
import pandas as pd
import os
from collections import Counter

def render_dashboard():
    st.title("Usage Dashboard")
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "usage_log.csv")
    if not os.path.exists(log_path):
        st.info("No usage data yet.")
        return
    df = pd.read_csv(log_path)
    st.metric("Total Requests", len(df))
    st.metric("Unique JDs", df["jd_title"].nunique())

    # Most common skills
    all_skills = []
    for skills in df["skills"].dropna():
        all_skills.extend([s.strip() for s in str(skills).split(",") if s.strip()])
    if all_skills:
        skill_counts = Counter(all_skills)
        st.markdown("### Most Common Skills")
        st.bar_chart(pd.Series(skill_counts).sort_values(ascending=False).head(15))

    # Recent JDs
    st.markdown("### Recent Job Descriptions")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(10)[["timestamp", "jd_title", "skills"]])
