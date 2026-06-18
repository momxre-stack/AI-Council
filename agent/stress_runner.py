from agent.council import ask_council
from agent.stress_metrics import build_stress_report, format_stress_report


def summarize_stress_results(results: list[dict]) -> dict:
    report = build_stress_report(results)

    return {
        "results": results,
        "report": report,
        "summary": format_stress_report(report),
    }


def _run_stress_request(question: str, council_runner) -> dict:
    try:
        return council_runner(question)
    except Exception as error:
        return {
            "question": question,
            "status": "failed",
            "error": str(error),
            "debate": None,
        }


def run_stress_test(
    question: str,
    request_count: int,
    council_runner=ask_council,
) -> dict:
    results = [
        _run_stress_request(question, council_runner)
        for _ in range(request_count)
    ]

    return summarize_stress_results(results)


def run_stress_questions(
    questions: list[str],
    council_runner=ask_council,
) -> dict:
    results = [
        _run_stress_request(question, council_runner)
        for question in questions
    ]

    return summarize_stress_results(results)