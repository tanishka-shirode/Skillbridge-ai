import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "skillbridge_data.json"


def load_data():
    """Load saved dashboard data."""
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data):
    """Save dashboard data locally."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_profile(profile):
    data = load_data()
    data["profile"] = profile
    save_data(data)


def save_skill_analysis(analysis):
    data = load_data()
    data["skill_analysis"] = analysis
    save_data(data)


def save_workflow(workflow):
    data = load_data()
    data["workflow"] = workflow
    save_data(data)


def save_completed_tasks(completed_tasks):
    data = load_data()
    data["completed_tasks"] = completed_tasks
    save_data(data)