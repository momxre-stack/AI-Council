from agent.stress_runner import summarize_stress_results


def test_summarizes_stress_results():
    results = [
        {"status": "ok", "debate": None},
        {"status": "degraded", "debate": None},
        {"status": "failed", "debate": None},
        {"status": "ok", "debate": {"consensus_answer": "final"}},
    ]

    summary = summarize_stress_results(results)

    assert summary["results"] == results
    assert summary["report"] == {
        "total_count": 4,
        "success_count": 2,
        "degraded_count": 1,
        "failure_count": 1,
        "debate_count": 1,
        "success_rate": 0.5,
        "degraded_rate": 0.25,
        "failure_rate": 0.25,
        "debate_rate": 0.25,
    }
    assert summary["summary"] == (
        "Total requests: 4\n"
        "Success rate: 50.0%\n"
        "Degraded rate: 25.0%\n"
        "Failure rate: 25.0%\n"
        "Debate rate: 25.0%"
    )