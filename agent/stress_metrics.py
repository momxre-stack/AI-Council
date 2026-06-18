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