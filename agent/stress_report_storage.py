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