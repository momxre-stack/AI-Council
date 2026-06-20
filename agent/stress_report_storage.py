"""Helpers for saving and loading stress report summaries."""

import json
import os


def build_stress_report_path(directory: str, run_id: str) -> str:
    """Return a deterministic JSON path for a stress report run."""
    filename = f"stress-report-{run_id}.json"
    return os.path.join(directory, filename)


def save_stress_report(summary: dict, path: str) -> None:
    """Save a stress report summary as JSON."""
    directory = os.path.dirname(path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, sort_keys=True)


def load_stress_report(path: str) -> dict:
    """Load a stress report summary from JSON."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def load_stress_reports(directory: str) -> list[dict]:
    """Load all stress report JSON files from a directory."""
    if not os.path.isdir(directory):
        return []

    reports = []

    for filename in sorted(os.listdir(directory)):
        if not filename.startswith("stress-report-"):
            continue

        if not filename.endswith(".json"):
            continue

        path = os.path.join(directory, filename)
        reports.append(load_stress_report(path))

    return reports

def compare_saved_stress_reports(previous_report: dict, current_report: dict) -> dict:
    """Compare numeric metrics from two loaded stress reports."""
    deltas = {}

    for key, previous_value in previous_report.items():
        if key not in current_report:
            continue

        current_value = current_report[key]

        if not isinstance(previous_value, (int, float)):
            continue

        if not isinstance(current_value, (int, float)):
            continue

        deltas[f"{key}_delta"] = round(current_value - previous_value, 4)

    return deltas