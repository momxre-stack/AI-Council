def _count_statuses(results):
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


def test_counts_stress_result_statuses():
    results = [
        {"status": "ok", "debate": None},
        {"status": "ok", "debate": {"consensus_answer": "final"}},
        {"status": "degraded", "debate": None},
        {"status": "failed", "debate": None},
    ]

    metrics = _count_statuses(results)

    assert metrics == {
        "success_count": 2,
        "degraded_count": 1,
        "failure_count": 1,
        "debate_count": 1,
    }


def test_counts_twenty_simulated_requests():
    results = []

    for _ in range(15):
        results.append({"status": "ok", "debate": None})

    for _ in range(3):
        results.append({"status": "degraded", "debate": None})

    results.append(
        {"status": "ok", "debate": {"consensus_answer": "final"}}
    )

    results.append(
        {"status": "failed", "debate": None}
    )

    metrics = _count_statuses(results)

    assert len(results) == 20

    assert metrics == {
        "success_count": 16,
        "degraded_count": 3,
        "failure_count": 1,
        "debate_count": 1,
    }