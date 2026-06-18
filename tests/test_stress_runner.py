from agent.stress_runner import run_stress_test, summarize_stress_results


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


def test_runs_stress_test_with_injected_council_runner():
    calls = []

    def fake_council_runner(question: str) -> dict:
        calls.append(question)
        return {
            "question": question,
            "status": "ok",
            "debate": None,
        }

    summary = run_stress_test(
        question="test question",
        request_count=3,
        council_runner=fake_council_runner,
    )

    assert calls == ["test question", "test question", "test question"]
    assert summary["report"]["total_count"] == 3
    assert summary["report"]["success_count"] == 3
    assert summary["report"]["failure_count"] == 0


def test_runs_stress_test_records_runner_failures():
    def failing_council_runner(question: str) -> dict:
        raise RuntimeError(f"failed question: {question}")

    summary = run_stress_test(
        question="unstable question",
        request_count=2,
        council_runner=failing_council_runner,
    )

    assert summary["results"] == [
        {
            "question": "unstable question",
            "status": "failed",
            "error": "failed question: unstable question",
            "debate": None,
        },
        {
            "question": "unstable question",
            "status": "failed",
            "error": "failed question: unstable question",
            "debate": None,
        },
    ]
    assert summary["report"]["total_count"] == 2
    assert summary["report"]["success_count"] == 0
    assert summary["report"]["degraded_count"] == 0
    assert summary["report"]["failure_count"] == 2
    assert summary["report"]["debate_count"] == 0
    assert summary["summary"] == (
        "Total requests: 2\n"
        "Success rate: 0.0%\n"
        "Degraded rate: 0.0%\n"
        "Failure rate: 100.0%\n"
        "Debate rate: 0.0%"
    )