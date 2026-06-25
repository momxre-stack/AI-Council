from agent.stress_cli import run_stress_cli


def test_run_stress_cli_returns_exported_real_stress_summary():
    def fake_runner(request_count):
        assert request_count == 1
        return {
            "reliability": {
                "status": "strong",
                "reliability_score": 1.0,
            },
            "summary": "Stress report text",
        }

    output = run_stress_cli(runner=fake_runner)

    assert output == (
        "Reliability status: strong\n"
        "Reliability score: 1.000\n\n"
        "Stress report text"
    )