import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODELS = {
    "MiniMax M2.5": "minimax/minimax-m2.5:free",
    "Qwen3 Next 80B A3B Instruct": "qwen/qwen3-next-80b-a3b-instruct:free",
    "NVIDIA Nemotron 3 Super": "nvidia/nemotron-3-super-120b-a12b:free",
}

PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "profile.json")
SAMPLE_PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_profile.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
