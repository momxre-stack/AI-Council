from agent.stress_metrics import build_stress_report, format_stress_report


def summarize_stress_results(results: list[dict]) -> dict:
    report = build_stress_report(results)

    return {
        "results": results,
        "report": report,
        "summary": format_stress_report(report),
    }