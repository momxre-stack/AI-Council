from agent.reliability_trends import (
    build_reliability_assessment,
    build_reliability_confidence,
    build_reliability_history,
    build_reliability_history_from_directory,
    compare_reliability_reports,
    format_reliability_history_report,
    format_reliability_trend_summary,
    generate_reliability_history_report,
    summarize_reliability_history,
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

def test_build_reliability_history_returns_consecutive_report_deltas():
    reports = [
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
            "reliability_score": 0.75,
        },
        {
            "success_rate": 0.9,
            "failure_rate": 0.1,
            "reliability_score": 0.8,
        },
        {
            "success_rate": 0.85,
            "failure_rate": 0.15,
            "reliability_score": 0.78,
        },
    ]

    result = build_reliability_history(reports)

    assert result == [
        {
            "index": 1,
            "deltas": {
                "success_rate_delta": 0.1,
                "failure_rate_delta": -0.1,
                "reliability_score_delta": 0.05,
            },
        },
        {
            "index": 2,
            "deltas": {
                "success_rate_delta": -0.05,
                "failure_rate_delta": 0.05,
                "reliability_score_delta": -0.02,
            },
        },
    ]


def test_build_reliability_history_returns_empty_list_for_fewer_than_two_reports():
    assert build_reliability_history([]) == []
    assert build_reliability_history([{"success_rate": 0.8}]) == []


def test_build_reliability_history_from_directory_loads_saved_reports(tmp_path):
    from agent.stress_report_storage import save_stress_report

    save_stress_report(
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
            "reliability_score": 0.75,
        },
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {
            "success_rate": 0.9,
            "failure_rate": 0.1,
            "reliability_score": 0.8,
        },
        str(tmp_path / "stress-report-002.json"),
    )

    result = build_reliability_history_from_directory(str(tmp_path))

    assert result == [
        {
            "index": 1,
            "deltas": {
                "success_rate_delta": 0.1,
                "failure_rate_delta": -0.1,
                "reliability_score_delta": 0.05,
            },
        },
    ]

def test_generate_reliability_history_report_builds_history_and_summary(tmp_path):
    from agent.stress_report_storage import save_stress_report

    save_stress_report(
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
            "reliability_score": 0.75,
        },
        str(tmp_path / "stress-report-001.json"),
    )

    save_stress_report(
        {
            "success_rate": 0.9,
            "failure_rate": 0.1,
            "reliability_score": 0.8,
        },
        str(tmp_path / "stress-report-002.json"),
    )

    result = generate_reliability_history_report(str(tmp_path))

    assert result == {
        "history": [
            {
                "index": 1,
                "deltas": {
                    "success_rate_delta": 0.1,
                    "failure_rate_delta": -0.1,
                    "reliability_score_delta": 0.05,
                },
            },
        ],
        "summary": {
            "total_comparisons": 1,
            "improving_count": 1,
            "declining_count": 0,
            "unchanged_count": 0,
            "unknown_count": 0,
        },
    }

def test_summarize_reliability_history_counts_trend_directions():
    history = [
        {
            "index": 1,
            "deltas": {
                "reliability_score_delta": 0.1,
            },
        },
        {
            "index": 2,
            "deltas": {
                "reliability_score_delta": -0.1,
            },
        },
        {
            "index": 3,
            "deltas": {
                "reliability_score_delta": 0,
            },
        },
        {
            "index": 4,
            "deltas": {
                "success_rate_delta": 0.1,
            },
        },
    ]

    result = summarize_reliability_history(history)

    assert result == {
        "total_comparisons": 4,
        "improving_count": 1,
        "declining_count": 1,
        "unchanged_count": 1,
        "unknown_count": 1,
    }



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

def test_format_reliability_history_report_returns_human_readable_text():
    report = {
        "summary": {
            "total_comparisons": 4,
            "improving_count": 2,
            "declining_count": 1,
            "unchanged_count": 1,
            "unknown_count": 0,
        },
    }

    result = format_reliability_history_report(report)

    assert result == (
        "Reliability History Report\n"
        "\n"
        "Total comparisons: 4\n"
        "Improving: 2\n"
        "Declining: 1\n"
        "Unchanged: 1\n"
        "Unknown: 0"
    )


def test_format_reliability_history_report_handles_empty_summary():
    result = format_reliability_history_report({})

    assert result == (
        "Reliability History Report\n"
        "\n"
        "Total comparisons: 0\n"
        "Improving: 0\n"
        "Declining: 0\n"
        "Unchanged: 0\n"
        "Unknown: 0"
    )



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

def test_format_reliability_trend_summary_defaults_missing_direction_to_unknown():
    result = format_reliability_trend_summary({})

    assert result == "Reliability trend: unknown"

def test_format_reliability_trend_summary_handles_none_deltas():
    summary = {
        "direction": "unknown",
        "deltas": None,
    }

    result = format_reliability_trend_summary(summary)

    assert result == "Reliability trend: unknown"

def test_build_reliability_confidence_returns_high():
    result = build_reliability_confidence(
        agreement_rate=0.9,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "high",
    }


def test_build_reliability_confidence_returns_medium():
    result = build_reliability_confidence(
        agreement_rate=0.7,
        debate_used=True,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "medium",
    }


def test_build_reliability_confidence_returns_low():
    result = build_reliability_confidence(
        agreement_rate=0.5,
        debate_used=True,
        reliability_status="degraded",
    )

    assert result == {
        "confidence": "low",
    }

def test_build_reliability_assessment_returns_confidence_and_signals():
    result = build_reliability_assessment(
        agreement_rate=0.9,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "high",
        "reason": "high_agreement",
        "signals": {
            "agreement_rate": 0.9,
            "debate_used": False,
            "reliability_status": "healthy",
        },
    }


def test_build_reliability_assessment_reuses_confidence_logic():
    result = build_reliability_assessment(
        agreement_rate=0.5,
        debate_used=True,
        reliability_status="degraded",
    )

    assert result == {
        "confidence": "low",
        "reason": "unhealthy_reliability",
        "signals": {
            "agreement_rate": 0.5,
            "debate_used": True,
            "reliability_status": "degraded",
        },
    }

def test_build_reliability_assessment_marks_debate_required_reason():
    result = build_reliability_assessment(
        agreement_rate=0.9,
        debate_used=True,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "medium",
        "reason": "debate_required",
        "signals": {
            "agreement_rate": 0.9,
            "debate_used": True,
            "reliability_status": "healthy",
        },
    }

def test_build_reliability_confidence_boundary_at_point_six():
    result = build_reliability_confidence(
        agreement_rate=0.6,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "medium",
    }


def test_build_reliability_confidence_boundary_at_point_eight():
    result = build_reliability_confidence(
        agreement_rate=0.8,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "high",
    }

def test_build_reliability_confidence_below_point_eight_is_medium():
    result = build_reliability_confidence(
        agreement_rate=0.79,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "medium",
    }

def test_build_reliability_confidence_below_point_six_is_low():
    result = build_reliability_confidence(
        agreement_rate=0.59,
        debate_used=False,
        reliability_status="healthy",
    )

    assert result == {
        "confidence": "low",
    }
