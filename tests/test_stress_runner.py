from agent.stress_runner import (
    run_stress_questions,
    run_stress_test,
    summarize_stress_results,
)


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
        "average_duration_seconds": 0,
        "min_duration_seconds": 0,
        "max_duration_seconds": 0,
    }


def test_runs_stress_test_with_injected_council_runner():
    times = iter([1.0, 1.5, 2.0, 2.5, 3.0, 3.5])

    def fake_timer():
        return next(times)

    def fake_council_runner(question: str) -> dict:
        return {
            "question": question,
            "status": "ok",
            "debate": None,
        }

    summary = run_stress_test(
        question="test question",
        request_count=3,
        council_runner=fake_council_runner,
        timer=fake_timer,
    )

    assert summary["report"]["total_count"] == 3
    assert summary["report"]["success_count"] == 3
    assert summary["report"]["failure_count"] == 0
    assert summary["report"]["average_duration_seconds"] == 0.5
    assert summary["report"]["min_duration_seconds"] == 0.5
    assert summary["report"]["max_duration_seconds"] == 0.5


def test_runs_stress_test_counts_degraded_results():
    times = iter([1.0, 1.25, 2.0, 2.75])

    def fake_timer():
        return next(times)

    def degraded_council_runner(question: str) -> dict:
        return {
            "question": question,
            "status": "degraded",
            "debate": None,
        }

    summary = run_stress_test(
        question="partial outage",
        request_count=2,
        council_runner=degraded_council_runner,
        timer=fake_timer,
    )

    assert summary["report"]["total_count"] == 2
    assert summary["report"]["success_count"] == 0
    assert summary["report"]["degraded_count"] == 2
    assert summary["report"]["failure_count"] == 0
    assert summary["report"]["debate_count"] == 0
    assert summary["report"]["average_duration_seconds"] == 0.5
    assert summary["report"]["min_duration_seconds"] == 0.25
    assert summary["report"]["max_duration_seconds"] == 0.75


def test_runs_stress_test_records_runner_failures():
    times = iter([1.0, 1.5, 2.0, 2.5])

    def fake_timer():
        return next(times)

    def failing_council_runner(question: str) -> dict:
        raise RuntimeError(f"failed question: {question}")

    summary = run_stress_test(
        question="unstable question",
        request_count=2,
        council_runner=failing_council_runner,
        timer=fake_timer,
    )

    assert summary["results"] == [
        {
            "question": "unstable question",
            "status": "failed",
            "error": "failed question: unstable question",
            "debate": None,
            "duration_seconds": 0.5,
        },
        {
            "question": "unstable question",
            "status": "failed",
            "error": "failed question: unstable question",
            "debate": None,
            "duration_seconds": 0.5,
        },
    ]
    assert summary["report"]["failure_count"] == 2


def test_runs_stress_questions_with_multiple_questions():
    times = iter([1.0, 1.5, 2.0, 2.5])

    def fake_timer():
        return next(times)

    def fake_council_runner(question: str) -> dict:
        return {
            "question": question,
            "status": "ok",
            "debate": None,
        }

    summary = run_stress_questions(
        questions=["question one", "question two"],
        council_runner=fake_council_runner,
        timer=fake_timer,
    )

    assert summary["report"]["total_count"] == 2
    assert summary["report"]["success_count"] == 2
    assert summary["report"]["failure_count"] == 0


def test_runs_stress_questions_counts_debate_results():
    times = iter([1.0, 1.5, 2.0, 2.5])

    def fake_timer():
        return next(times)

    def debate_council_runner(question: str) -> dict:
        return {
            "question": question,
            "status": "ok",
            "debate": {"consensus_answer": f"final answer for {question}"},
        }

    summary = run_stress_questions(
        questions=["debate one", "debate two"],
        council_runner=debate_council_runner,
        timer=fake_timer,
    )

    assert summary["report"]["total_count"] == 2
    assert summary["report"]["success_count"] == 2
    assert summary["report"]["degraded_count"] == 0
    assert summary["report"]["failure_count"] == 0
    assert summary["report"]["debate_count"] == 2
    assert summary["report"]["debate_rate"] == 1.0