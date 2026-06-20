"""Helpers for comparing reliability reports across runs."""


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