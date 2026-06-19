from time import perf_counter

from agent.council import ask_council
from agent.stress_metrics import build_stress_report, format_stress_report


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

    return {
        "results": results,
        "report": report,
        "summary": format_stress_report(report),
    }


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