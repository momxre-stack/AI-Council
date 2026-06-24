def count_statuses(results: list[dict]) -> dict:
    metrics = {
        "success_count": 0,
        "degraded_count": 0,
        "failure_count": 0,
        "debate_count": 0,
        "debate_success_count": 0,
        "debate_vote_count": 0,
        "judge_agreement_count": 0,
        "judge_disagreement_count": 0,
    }

    for result in results:
        status = result.get("status")

        if status == "ok":
            metrics["success_count"] += 1
        elif status == "degraded":
            metrics["degraded_count"] += 1
        else:
            metrics["failure_count"] += 1

        if result.get("debate") is not None:
            metrics["debate_count"] += 1

            if status == "ok":
                metrics["debate_success_count"] += 1

        judgment = result.get("judgment") or {}
        metrics["debate_vote_count"] += judgment.get("debate_vote_count", 0)

        if judgment and judgment.get("final_needs_debate") is False:
            metrics["judge_agreement_count"] += 1

        if judgment and judgment.get("final_needs_debate") is True:
            metrics["judge_disagreement_count"] += 1

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
    lines = []

    if "reliability_score" in report:
        lines.extend(
            [
                f"Reliability status: {report.get('reliability_status', 'unknown')}",
                f"Reliability score: {report['reliability_score']:.3f}",
                "",
            ]
        )

    lines.extend(
        [
            f"Total requests: {report['total_count']}",
            f"Success rate: {report['success_rate'] * 100:.1f}%",
            f"Degraded rate: {report['degraded_rate'] * 100:.1f}%",
            f"Failure rate: {report['failure_rate'] * 100:.1f}%",
            f"Debate rate: {report['debate_rate'] * 100:.1f}%",
        ]
    )

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


def build_reliability_summary(report: dict) -> dict:
    reliability_score = round(
        report["success_rate"] + report["degraded_rate"] * 0.5,
        4,
    )

    if reliability_score >= 0.95:
        status = "excellent"
    elif reliability_score >= 0.80:
        status = "good"
    elif reliability_score >= 0.60:
        status = "fair"
    else:
        status = "poor"

    return {
        "reliability_score": reliability_score,
        "status": status,
    }