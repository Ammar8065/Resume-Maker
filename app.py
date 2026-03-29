import streamlit as st
from ui.main_page import render_main_page
from ui.profile_page import render_profile_page
from ui.dashboard import render_dashboard

st.set_page_config(
    page_title="Resume Maker",
    page_icon="📄",
    layout="wide",
)

generator = st.Page(render_main_page, title="Resume Generator", icon="📄", default=True)
profile = st.Page(render_profile_page, title="Edit Profile", icon="✏️")
dashboard = st.Page(render_dashboard, title="Dashboard", icon="📊")

nav = st.navigation([generator, profile, dashboard])
nav.run()
