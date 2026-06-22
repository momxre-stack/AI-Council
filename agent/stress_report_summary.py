"""Helpers for formatting stress report summaries."""


def format_latest_stress_report_changes(summary: dict) -> str:
    """Return a human-readable latest stress report summary."""
    deltas = summary.get("deltas") or {}

    lines = [
        f"Changes detected: {'yes' if summary.get('has_changes', False) else 'no'}",
    ]

    for metric in sorted(deltas):
        value = deltas[metric]
        label = metric.replace("_", " ").replace(" delta", " delta")
        lines.append(f"{label.capitalize()}: {value:+.4f}")

    return "\n".join(lines)


def generate_latest_stress_report_summary(summary: dict) -> str:
    """Generate a human-readable latest stress report summary."""
    return format_latest_stress_report_changes(summary)