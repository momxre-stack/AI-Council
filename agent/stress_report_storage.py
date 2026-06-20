"""Helpers for saving and loading stress report summaries."""

import json


def save_stress_report(summary: dict, path: str) -> None:
    """Save a stress report summary as JSON."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, sort_keys=True)


def load_stress_report(path: str) -> dict:
    """Load a stress report summary from JSON."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)