from agent.reliability_trends import compare_reliability_reports


def test_compare_reliability_reports_returns_metric_deltas():
    previous_report = {
        "success_rate": 0.80,
        "degraded_rate": 0.10,
        "failure_rate": 0.10,
        "debate_rate": 0.25,
        "reliability_score": 0.85,
    }
    current_report = {
        "success_rate": 0.90,
        "degraded_rate": 0.05,
        "failure_rate": 0.05,
        "debate_rate": 0.30,
        "reliability_score": 0.925,
    }

    result = compare_reliability_reports(previous_report, current_report)

    assert result == {
        "success_rate_delta": 0.1,
        "degraded_rate_delta": -0.05,
        "failure_rate_delta": -0.05,
        "debate_rate_delta": 0.05,
        "reliability_score_delta": 0.075,
    }


def test_compare_reliability_reports_ignores_missing_metrics():
    previous_report = {
        "success_rate": 0.80,
        "failure_rate": 0.10,
    }
    current_report = {
        "success_rate": 0.90,
    }

    result = compare_reliability_reports(previous_report, current_report)

    assert result == {
        "success_rate_delta": 0.1,
    }


def test_compare_reliability_reports_ignores_non_numeric_metrics():
    previous_report = {
        "success_rate": 0.80,
        "reliability_score": "good",
    }
    current_report = {
        "success_rate": 0.90,
        "reliability_score": "excellent",
    }

    result = compare_reliability_reports(previous_report, current_report)

    assert result == {
        "success_rate_delta": 0.1,
    }


def test_compare_reliability_reports_returns_empty_dict_without_comparable_metrics():
    previous_report = {
        "status": "good",
    }
    current_report = {
        "status": "excellent",
    }

    result = compare_reliability_reports(previous_report, current_report)

    assert result == {}