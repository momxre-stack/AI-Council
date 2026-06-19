def count_statuses(results: list[dict]) -> dict:
    metrics = {
        "success_count": 0,
        "degraded_count": 0,
        "failure_count": 0,
        "debate_count": 0,
    }

    for result in results:
        if result["status"] == "ok":
            metrics["success_count"] += 1
        elif result["status"] == "degraded":
            metrics["degraded_count"] += 1
        else:
            metrics["failure_count"] += 1

        if result.get("debate") is not None:
            metrics["debate_count"] += 1

    return metrics


def calculate_rates(metrics: dict, total_count: int) -> dict:
    if total_count == 0:
        return {
            "success_rate": 0,
            "degraded_rate": 0,
            "failure_rate": 0,
            "debate_rate": 0,
        }

    return {
        "success_rate": metrics["success_count"] / total_count,
        "degraded_rate": metrics["degraded_count"] / total_count,
        "failure_rate": metrics["failure_count"] / total_count,
        "debate_rate": metrics["debate_count"] / total_count,
    }


def build_stress_report(results: list[dict]) -> dict:
    metrics = count_statuses(results)
    total_count = len(results)
    rates = calculate_rates(metrics, total_count)

    return {
        "total_count": total_count,
        **metrics,
        **rates,
    }


def format_stress_report(report: dict) -> str:
    lines = [
        f"Total requests: {report['total_count']}",
        f"Success rate: {report['success_rate'] * 100:.1f}%",
        f"Degraded rate: {report['degraded_rate'] * 100:.1f}%",
        f"Failure rate: {report['failure_rate'] * 100:.1f}%",
        f"Debate rate: {report['debate_rate'] * 100:.1f}%",
    ]

    if "average_duration_seconds" in report:
        lines.extend(
            [
                (
                    "Average duration: "
                    f"{report['average_duration_seconds']:.3f}s"
                ),
                f"Min duration: {report['min_duration_seconds']:.3f}s",
                f"Max duration: {report['max_duration_seconds']:.3f}s",
            ]
        )

    return "\n".join(lines)