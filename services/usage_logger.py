import os
import csv
from datetime import datetime

def log_usage(jd_title, skills):
    """Append a usage record to the CSV log."""
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "usage_log.csv")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "jd_title", "skills"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            jd_title,
            ", ".join(skills) if isinstance(skills, (list, set)) else skills
        ])
