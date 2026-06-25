from agent.stress_runner import export_stress_summary, run_real_stress_test


def run_stress_cli(runner=run_real_stress_test) -> str:
    summary = runner(request_count=1)

    return export_stress_summary(summary)