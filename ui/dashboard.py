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
        import matplotlib.pyplot as plt
        skill_counts = Counter(all_skills)
        st.markdown("### Most Common Skills")
        top_skills = pd.Series(skill_counts).sort_values(ascending=False).head(15)
        fig, ax = plt.subplots(figsize=(8, 6))
        top_skills.sort_values().plot.barh(ax=ax, color="#4FC3F7")
        ax.set_xlabel("Count", fontsize=12)
        ax.set_ylabel("Skill", fontsize=12)
        ax.set_title("Most Common Skills", fontsize=16, weight="bold")
        ax.tick_params(axis='y', labelsize=11)
        ax.grid(axis='x', linestyle='--', alpha=0.6)
        st.pyplot(fig)

    # Recent JDs
    st.markdown("### Recent Job Descriptions")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(10)[["timestamp", "jd_title", "skills"]])
