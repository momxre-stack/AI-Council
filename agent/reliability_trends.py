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