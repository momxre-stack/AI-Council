from agent.stress_metrics import count_statuses


def test_counts_stress_result_statuses():
    results = [
        {"status": "ok", "debate": None},
        {"status": "ok", "debate": {"consensus_answer": "final"}},
        {"status": "degraded", "debate": None},
        {"status": "failed", "debate": None},
    ]

    metrics = count_statuses(results)

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

    metrics = count_statuses(results)

    assert len(results) == 20

    assert metrics == {
        "success_count": 16,
        "degraded_count": 3,
        "failure_count": 1,
        "debate_count": 1,
    }


def test_counts_fifty_simulated_requests():
    results = []

    for _ in range(40):
        results.append({"status": "ok", "debate": None})

    for _ in range(7):
        results.append({"status": "degraded", "debate": None})

    results.append(
        {"status": "ok", "debate": {"consensus_answer": "final"}}
    )

    for _ in range(2):
        results.append({"status": "failed", "debate": None})

    metrics = count_statuses(results)

    assert len(results) == 50

    assert metrics == {
        "success_count": 41,
        "degraded_count": 7,
        "failure_count": 2,
        "debate_count": 1,
    }