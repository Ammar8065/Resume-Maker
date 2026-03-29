import json
import os
import shutil
from config.settings import PROFILE_PATH, SAMPLE_PROFILE_PATH


def get_default_profile():
    return {
        "personal_info": {
            "full_name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "portfolio": "",
        },
        "summary": "",
        "skills": {"technical": [], "tools": [], "soft": []},
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
    }


def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    if os.path.exists(SAMPLE_PROFILE_PATH):
        shutil.copy(SAMPLE_PROFILE_PATH, PROFILE_PATH)
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    profile = get_default_profile()
    save_profile(profile)
    return profile


def save_profile(profile):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)


def validate_profile(profile):
    issues = []
    info = profile.get("personal_info", {})
    if not info.get("full_name"):
        issues.append("Full name is required")
    if not info.get("email"):
        issues.append("Email is required")
    if not profile.get("summary"):
        issues.append("Professional summary is empty")
    if not profile.get("experience"):
        issues.append("No work experience added")
    skills = profile.get("skills", {})
    all_skills = skills.get("technical", []) + skills.get("tools", []) + skills.get("soft", [])
    if not all_skills:
        issues.append("No skills added")
    return issues
