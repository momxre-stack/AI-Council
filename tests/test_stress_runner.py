from agent.stress_runner import (
    export_stress_summary,
    run_default_stress_test,
    run_real_stress_test,
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
        "debate_success_count": 1,
        "debate_failure_count": 0,
        "debate_vote_count": 0,
        "judge_agreement_count": 0,
        "judge_disagreement_count": 0,
        "judge_useful_count": 0,
        "success_rate": 0.5,
        "degraded_rate": 0.25,
        "failure_rate": 0.25,
        "debate_rate": 0.25,
        "debate_effectiveness_rate": 1.0,
        "judge_agreement_rate": 0,
        "judge_disagreement_rate": 0,
        "category_count": 0,
        "average_duration_seconds": 0,
        "min_duration_seconds": 0,
        "max_duration_seconds": 0,
    }

    assert summary["reliability"] == {
        "reliability_score": 0.625,
        "status": "fair",
    }


def test_runs_stress_test_with_injected_council_runner():
    times = iter([
        1.0, 1.5,
        2.0, 2.5,
        3.0, 3.5,
        4.0, 4.5,
        5.0, 5.5,
    ])

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

def test_run_stress_test_rejects_non_positive_request_count():
    try:
        run_stress_test(
            question="test question",
            request_count=0,
        )
    except ValueError as error:
        assert str(error) == "request_count must be positive"
    else:
        raise AssertionError("Expected ValueError")


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

def test_run_stress_questions_preserves_question_categories():
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
        questions=[
            {
                "category": "reliability",
                "question": "Compare reliability and speed.",
            },
            {
                "category": "json",
                "question": "List JSON output risks.",
            },
        ],
        council_runner=fake_council_runner,
        timer=fake_timer,
    )

    assert summary["results"][0]["question"] == "Compare reliability and speed."
    assert summary["results"][0]["category"] == "reliability"
    assert summary["results"][1]["question"] == "List JSON output risks."
    assert summary["results"][1]["category"] == "json"


def test_run_stress_questions_rejects_empty_questions():
    try:
        run_stress_questions([])
    except ValueError as error:
        assert str(error) == "questions must not be empty"
    else:
        raise AssertionError("Expected ValueError")


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

def test_exports_stress_summary_text():
    summary = {
        "reliability": {
            "reliability_score": 0.625,
            "status": "fair",
        },
        "summary": (
            "Total requests: 2\n"
            "Success rate: 100.0%\n"
            "Degraded rate: 0.0%\n"
            "Failure rate: 0.0%\n"
            "Debate rate: 0.0%"
        )
    }

    exported = export_stress_summary(summary)

    assert exported == (
        "Reliability status: fair\n"
        "Reliability score: 0.625\n\n"
        "Total requests: 2\n"
        "Success rate: 100.0%\n"
        "Degraded rate: 0.0%\n"
        "Failure rate: 0.0%\n"
        "Debate rate: 0.0%"
    )

def test_runs_default_stress_test_with_default_questions():
    times = iter([
        1.0, 1.5,
        2.0, 2.5,
        3.0, 3.5,
        4.0, 4.5,
        5.0, 5.5,
    ])
    calls = []

    def fake_timer():
        return next(times)

    def fake_council_runner(question: str) -> dict:
        calls.append(question)
        return {
            "question": question,
            "status": "ok",
            "debate": None,
        }

    summary = run_default_stress_test(
        council_runner=fake_council_runner,
        timer=fake_timer,
    )

    assert calls == [
        "Explain AI Council in one sentence.",
        "Compare reliability and speed in software systems.",
        "List three risks of malformed JSON outputs.",
        "Explain when an AI judge should trigger debate.",
        "Identify the strongest and weakest answer in a comparison.",
    ]
    assert summary["report"]["total_count"] == 5
    assert summary["report"]["category_count"] == 5
    assert summary["report"]["success_count"] == 5
    assert summary["report"]["failure_count"] == 0

def test_runs_default_stress_test_with_custom_questions():
    times = iter([1.0, 1.5, 2.0, 2.5])
    calls = []

    def fake_timer():
        return next(times)

    def fake_council_runner(question: str) -> dict:
        calls.append(question)
        return {
            "question": question,
            "status": "ok",
            "debate": None,
        }

    summary = run_default_stress_test(
        questions=["custom one", "custom two"],
        council_runner=fake_council_runner,
        timer=fake_timer,
    )

    assert calls == ["custom one", "custom two"]
    assert summary["report"]["total_count"] == 2
    assert summary["report"]["success_count"] == 2
    assert summary["report"]["failure_count"] == 0

def test_real_stress_test_uses_default_questions(monkeypatch):
    captured_questions = []

    def fake_run_stress_questions(questions):
        captured_questions.extend(questions)
        return {
            "report": {
                "total_count": len(questions),
                "success_count": len(questions),
                "failure_count": 0,
            }
        }

    monkeypatch.setattr(
        "agent.stress_runner.run_stress_questions",
        fake_run_stress_questions,
    )

    summary = run_real_stress_test(request_count=1)

    assert captured_questions == [
        {
            "category": "general",
            "question": "Explain AI Council in one sentence.",
        },
        {
            "category": "reliability",
            "question": "Compare reliability and speed in software systems.",
        },
        {
            "category": "json",
            "question": "List three risks of malformed JSON outputs.",
        },
        {
            "category": "debate",
            "question": "Explain when an AI judge should trigger debate.",
        },
        {
            "category": "comparison",
            "question": "Identify the strongest and weakest answer in a comparison.",
        },
    ]
    assert summary["report"]["total_count"] == 5
    assert summary["report"]["success_count"] == 5
    assert summary["report"]["failure_count"] == 0

def test_run_real_stress_test_rejects_non_positive_request_count():
    try:
        run_real_stress_test(request_count=0)
    except ValueError as error:
        assert str(error) == "request_count must be positive"
    else:
        raise AssertionError("Expected ValueError")