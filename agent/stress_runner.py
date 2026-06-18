from agent.council import ask_council
from agent.stress_metrics import build_stress_report, format_stress_report


def summarize_stress_results(results: list[dict]) -> dict:
    report = build_stress_report(results)

    return {
        "results": results,
        "report": report,
        "summary": format_stress_report(report),
    }


def run_stress_test(
    question: str,
    request_count: int,
    council_runner=ask_council,
) -> dict:
    results = []

    for _ in range(request_count):
        try:
            results.append(council_runner(question))
        except Exception as error:
            results.append(
                {
                    "question": question,
                    "status": "failed",
                    "error": str(error),
                    "debate": None,
                }
            )

    return summarize_stress_results(results)