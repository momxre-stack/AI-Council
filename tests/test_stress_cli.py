from agent.stress_cli import parse_request_count, run_stress_cli, run_stress_cli_from_args


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


def test_run_stress_cli_passes_request_count_to_runner():
    captured_request_counts = []

    def fake_runner(request_count):
        captured_request_counts.append(request_count)
        return {
            "reliability": {
                "status": "strong",
                "reliability_score": 1.0,
            },
            "summary": "Stress report text",
        }

    run_stress_cli(request_count=3, runner=fake_runner)

    assert captured_request_counts == [3]


def test_parse_request_count_uses_default_when_no_arguments():
    assert parse_request_count([]) == 1


def test_parse_request_count_uses_first_argument():
    assert parse_request_count(["3"]) == 3


def test_parse_request_count_rejects_non_numeric_argument():
    try:
        parse_request_count(["abc"])
    except ValueError as error:
        assert str(error) == "request_count must be a positive integer"
    else:
        raise AssertionError("Expected ValueError")


def test_parse_request_count_rejects_non_positive_argument():
    try:
        parse_request_count(["0"])
    except ValueError as error:
        assert str(error) == "request_count must be a positive integer"
    else:
        raise AssertionError("Expected ValueError")


def test_run_stress_cli_from_args_uses_request_count_argument():
    captured_request_counts = []

    def fake_runner(request_count):
        captured_request_counts.append(request_count)
        return {
            "reliability": {
                "status": "strong",
                "reliability_score": 1.0,
            },
            "summary": "Stress report text",
        }

    output = run_stress_cli_from_args(["3"], runner=fake_runner)

    assert captured_request_counts == [3]
    assert output == (
        "Reliability status: strong\n"
        "Reliability score: 1.000\n\n"
        "Stress report text"
    )