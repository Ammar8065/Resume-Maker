
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_openrouter_api_key():
    # 1. Try Streamlit Cloud secrets
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if api_key:
        return api_key
    # 2. Try .env/local environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key
    # 3. Handle missing key gracefully
    st.error(
        "OpenRouter API key not found. Please add it to Streamlit secrets (st.secrets['OPENROUTER_API_KEY']) "
        "or set it as an environment variable locally."
    )
    st.stop()

OPENROUTER_API_KEY = get_openrouter_api_key()
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODELS = {
    "MiniMax M2.5": "minimax/minimax-m2.5:free",
    "Qwen3 Next 80B A3B Instruct": "qwen/qwen3-next-80b-a3b-instruct:free",
    "NVIDIA Nemotron 3 Super": "nvidia/nemotron-3-super-120b-a12b:free",
}

PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "profile.json")
SAMPLE_PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_profile.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
