"""Helpers for comparing reliability reports across runs."""

from agent.stress_report_storage import load_stress_reports


TREND_METRICS = [
    "success_rate",
    "degraded_rate",
    "failure_rate",
    "debate_rate",
    "reliability_score",
]


def compare_reliability_reports(
    previous_report: dict,
    current_report: dict,
) -> dict:
    """Return metric deltas between previous and current reliability reports."""
    deltas = {}

    for metric in TREND_METRICS:
        if metric not in previous_report or metric not in current_report:
            continue

        previous_value = previous_report[metric]
        current_value = current_report[metric]

        if not isinstance(previous_value, (int, float)):
            continue

        if not isinstance(current_value, (int, float)):
            continue

        deltas[f"{metric}_delta"] = round(current_value - previous_value, 4)

    return deltas


def build_reliability_history(reports: list[dict]) -> list[dict]:
    """Return reliability trend history for consecutive reports."""
    history = []

    for index in range(1, len(reports)):
        previous_report = reports[index - 1]
        current_report = reports[index]

        history.append(
            {
                "index": index,
                "deltas": compare_reliability_reports(
                    previous_report,
                    current_report,
                ),
            }
        )

    return history


def build_reliability_history_from_directory(directory: str) -> list[dict]:
    """Load saved stress reports and return reliability trend history."""
    reports = load_stress_reports(directory)
    return build_reliability_history(reports)

def summarize_reliability_history(history: list[dict]) -> dict:
    """Return counts of reliability directions across history entries."""
    summary = {
        "total_comparisons": len(history),
        "improving_count": 0,
        "declining_count": 0,
        "unchanged_count": 0,
        "unknown_count": 0,
    }

    for entry in history:
        trend = summarize_reliability_trend(entry.get("deltas", {}))
        direction = trend["direction"]

        if direction == "improving":
            summary["improving_count"] += 1
        elif direction == "declining":
            summary["declining_count"] += 1
        elif direction == "unchanged":
            summary["unchanged_count"] += 1
        else:
            summary["unknown_count"] += 1

    return summary


def generate_reliability_history_report(directory: str) -> dict:
    """Build a reliability history report from saved reports."""
    history = build_reliability_history_from_directory(directory)

    return {
        "history": history,
        "summary": summarize_reliability_history(history),
    }


def summarize_reliability_trend(deltas: dict) -> dict:
    """Return a simple trend summary from reliability metric deltas."""
    reliability_score_delta = deltas.get("reliability_score_delta")

    if reliability_score_delta is None:
        direction = "unknown"
    elif reliability_score_delta > 0:
        direction = "improving"
    elif reliability_score_delta < 0:
        direction = "declining"
    else:
        direction = "unchanged"

    return {
        "direction": direction,
        "deltas": deltas,
    }

def format_reliability_history_report(report: dict) -> str:
    """Return a human-readable reliability history report."""
    summary = report.get("summary", {})

    lines = [
        "Reliability History Report",
        "",
        f"Total comparisons: {summary.get('total_comparisons', 0)}",
        f"Improving: {summary.get('improving_count', 0)}",
        f"Declining: {summary.get('declining_count', 0)}",
        f"Unchanged: {summary.get('unchanged_count', 0)}",
        f"Unknown: {summary.get('unknown_count', 0)}",
    ]

    return "\n".join(lines)



def format_reliability_trend_summary(summary: dict) -> str:
    """Return a human-readable reliability trend summary."""
    deltas = summary.get("deltas", {})

    lines = [
        f"Reliability trend: {summary['direction']}",
    ]

    if "reliability_score_delta" in deltas:
        lines.append(
            "Reliability score delta: "
            f"{deltas['reliability_score_delta']:+.3f}"
        )

    for metric in [
        "success_rate_delta",
        "degraded_rate_delta",
        "failure_rate_delta",
        "debate_rate_delta",
    ]:
        if metric in deltas:
            label = metric.replace("_", " ").replace(" delta", " delta")
            lines.append(f"{label.capitalize()}: {deltas[metric] * 100:+.1f}%")

    return "\n".join(lines)