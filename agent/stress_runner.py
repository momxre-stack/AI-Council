from time import perf_counter

from agent.council import ask_council
from agent.stress_metrics import (
    build_reliability_summary,
    build_stress_report,
    format_stress_report,
)

DEFAULT_STRESS_QUESTIONS = [
    "Explain AI Council in one sentence.",
    "Compare reliability and speed in software systems.",
    "List three risks of malformed JSON outputs.",
]


def _build_timing_report(results: list[dict]) -> dict:
    durations = [
        result["duration_seconds"]
        for result in results
        if "duration_seconds" in result
    ]

    if not durations:
        return {
            "average_duration_seconds": 0,
            "min_duration_seconds": 0,
            "max_duration_seconds": 0,
        }

    return {
        "average_duration_seconds": sum(durations) / len(durations),
        "min_duration_seconds": min(durations),
        "max_duration_seconds": max(durations),
    }


def summarize_stress_results(results: list[dict]) -> dict:
    report = {
        **build_stress_report(results),
        **_build_timing_report(results),
    }

    reliability = build_reliability_summary(report)

    return {
        "results": results,
        "report": report,
        "reliability": reliability,
        "summary": format_stress_report(report),
    }


def export_stress_summary(summary: dict) -> str:
    reliability = summary["reliability"]

    return (
        f"Reliability status: {reliability['status']}\n"
        f"Reliability score: "
        f"{reliability['reliability_score']:.3f}\n\n"
        f"{summary['summary']}"
    )


def _run_stress_request(question: str, council_runner, timer=perf_counter) -> dict:
    start_time = timer()

    try:
        result = council_runner(question)
    except Exception as error:
        result = {
            "question": question,
            "status": "failed",
            "error": str(error),
            "debate": None,
        }

    end_time = timer()
    return {
        **result,
        "duration_seconds": end_time - start_time,
    }


def run_stress_test(
    question: str,
    request_count: int,
    council_runner=ask_council,
    timer=perf_counter,
) -> dict:
    if request_count <= 0:
        raise ValueError("request_count must be positive")

    results = [
        _run_stress_request(question, council_runner, timer)
        for _ in range(request_count)
    ]

    return summarize_stress_results(results)


def run_stress_questions(
    questions: list[str],
    council_runner=ask_council,
    timer=perf_counter,
) -> dict:
    results = [
        _run_stress_request(question, council_runner, timer)
        for question in questions
    ]

    return summarize_stress_results(results)


def run_default_stress_test(
    questions: list[str] | None = None,
    council_runner=ask_council,
    timer=perf_counter,
) -> dict:
    return run_stress_questions(
        questions=questions or DEFAULT_STRESS_QUESTIONS,
        council_runner=council_runner,
        timer=timer,
    )

def run_real_stress_test(
    request_count: int,
) -> dict:
    questions = DEFAULT_STRESS_QUESTIONS * request_count

    return run_stress_questions(
        questions=questions,
    )