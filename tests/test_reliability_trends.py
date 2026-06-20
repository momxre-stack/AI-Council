from agent.reliability_trends import (
    compare_reliability_reports,
    format_reliability_trend_summary,
    summarize_reliability_trend,
)


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


def test_summarize_reliability_trend_marks_improving():
    deltas = {
        "reliability_score_delta": 0.05,
    }

    result = summarize_reliability_trend(deltas)

    assert result == {
        "direction": "improving",
        "deltas": deltas,
    }


def test_summarize_reliability_trend_marks_declining():
    deltas = {
        "reliability_score_delta": -0.05,
    }

    result = summarize_reliability_trend(deltas)

    assert result == {
        "direction": "declining",
        "deltas": deltas,
    }


def test_summarize_reliability_trend_marks_unchanged():
    deltas = {
        "reliability_score_delta": 0,
    }

    result = summarize_reliability_trend(deltas)

    assert result == {
        "direction": "unchanged",
        "deltas": deltas,
    }


def test_summarize_reliability_trend_marks_unknown_without_reliability_score():
    deltas = {
        "success_rate_delta": 0.1,
    }

    result = summarize_reliability_trend(deltas)

    assert result == {
        "direction": "unknown",
        "deltas": deltas,
    }


def test_format_reliability_trend_summary_returns_human_readable_text():
    summary = {
        "direction": "improving",
        "deltas": {
            "reliability_score_delta": 0.05,
            "success_rate_delta": 0.10,
            "failure_rate_delta": -0.05,
        },
    }

    result = format_reliability_trend_summary(summary)

    assert result == (
        "Reliability trend: improving\n"
        "Reliability score delta: +0.050\n"
        "Success rate delta: +10.0%\n"
        "Failure rate delta: -5.0%"
    )


def test_format_reliability_trend_summary_handles_missing_deltas():
    summary = {
        "direction": "unknown",
    }

    result = format_reliability_trend_summary(summary)

    assert result == "Reliability trend: unknown"