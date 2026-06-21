"""Helpers for formatting stress report summaries."""


def format_latest_stress_report_changes(summary: dict) -> str:
    """Return a human-readable latest stress report summary."""
    lines = [
        f"Changes detected: {'yes' if summary['has_changes'] else 'no'}",
    ]

    for metric in sorted(summary["deltas"]):
        value = summary["deltas"][metric]
        label = metric.replace("_", " ").replace(" delta", " delta")
        lines.append(f"{label.capitalize()}: {value:+.4f}")

    return "\n".join(lines)