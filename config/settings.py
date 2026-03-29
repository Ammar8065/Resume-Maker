import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODELS = {
    "MiniMax M2.5": "minimax/minimax-m2.5:free",
    "Qwen3 Next 80B A3B Instruct": "qwen/qwen3-next-80b-a3b-instruct:free",
    "NVIDIA Nemotron 3 Super": "nvidia/nemotron-3-super-120b-a12b:free",
    "OpenAI: gpt-oss-120b (free)": "openai/gpt-oss-120b:free",
}

PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "profile.json")
SAMPLE_PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_profile.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def _get_streamlit_secret(key_name):
    try:
        import streamlit as st
    except Exception:
        return None

    try:
        return st.secrets.get(key_name)
    except Exception:
        return None


def get_secret_or_env(key_name):
    return _get_streamlit_secret(key_name) or os.getenv(key_name)


def get_openrouter_api_key():
    return get_secret_or_env("OPENROUTER_API_KEY")


def get_api_key_for_model(model_name):
    if model_name == "OpenAI: gpt-oss-120b (free)":
        return get_secret_or_env("GPT_OSS_120B_API_KEY")
    return get_openrouter_api_key()


def get_api_key_error_message(model_name):
    if model_name == "OpenAI: gpt-oss-120b (free)":
        return (
            "gpt-oss-120b API key not found. Add GPT_OSS_120B_API_KEY "
            "to Streamlit secrets or your local environment."
        )
    return (
        "OpenRouter API key not found. Add OPENROUTER_API_KEY "
        "to Streamlit secrets or your local environment."
    )
