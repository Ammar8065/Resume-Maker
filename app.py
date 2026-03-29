import streamlit as st

st.set_page_config(
    page_title="Resume Maker",
    page_icon="📄",
    layout="wide",
)

from ui.main_page import render_main_page
from ui.profile_page import render_profile_page

generator = st.Page(render_main_page, title="Resume Generator", icon="📄", default=True)
profile = st.Page(render_profile_page, title="Edit Profile", icon="✏️")

nav = st.navigation([generator, profile])
nav.run()
