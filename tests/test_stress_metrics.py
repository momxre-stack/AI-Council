from agent.stress_metrics import (
    build_reliability_summary,
    build_stress_report,
    calculate_rates,
    count_statuses,
    format_stress_report,
)


def test_counts_stress_result_statuses():
    results = [
        {"status": "ok", "debate": None},
        {"status": "ok", "debate": {"consensus_answer": "final"}},
        {"status": "degraded", "debate": None},
        {"status": "failed", "debate": None},
    ]

    metrics = count_statuses(results)

    assert metrics == {
        "success_count": 2,
        "degraded_count": 1,
        "failure_count": 1,
        "debate_count": 1,
    }

def test_count_statuses_treats_missing_status_as_failure():
    results = [
        {"debate": None},
    ]

    metrics = count_statuses(results)

    assert metrics == {
        "success_count": 0,
        "degraded_count": 0,
        "failure_count": 1,
        "debate_count": 0,
    }


def test_counts_twenty_simulated_requests():
    results = []

    for _ in range(15):
        results.append({"status": "ok", "debate": None})

    for _ in range(3):
        results.append({"status": "degraded", "debate": None})

    results.append(
        {"status": "ok", "debate": {"consensus_answer": "final"}}
    )

    results.append({"status": "failed", "debate": None})

    metrics = count_statuses(results)

    assert len(results) == 20

    assert metrics == {
        "success_count": 16,
        "degraded_count": 3,
        "failure_count": 1,
        "debate_count": 1,
    }


def test_counts_fifty_simulated_requests():
    results = []

    for _ in range(40):
        results.append({"status": "ok", "debate": None})

    for _ in range(7):
        results.append({"status": "degraded", "debate": None})

    results.append(
        {"status": "ok", "debate": {"consensus_answer": "final"}}
    )

    for _ in range(2):
        results.append({"status": "failed", "debate": None})

    metrics = count_statuses(results)

    assert len(results) == 50

    assert metrics == {
        "success_count": 41,
        "degraded_count": 7,
        "failure_count": 2,
        "debate_count": 1,
    }


def test_calculates_stress_rates():
    metrics = {
        "success_count": 16,
        "degraded_count": 3,
        "failure_count": 1,
        "debate_count": 1,
    }

    rates = calculate_rates(metrics, total_count=20)

    assert rates == {
        "success_rate": 0.8,
        "degraded_rate": 0.15,
        "failure_rate": 0.05,
        "debate_rate": 0.05,
    }


def test_calculates_debate_usage_rate():
    metrics = {
        "success_count": 16,
        "degraded_count": 3,
        "failure_count": 1,
        "debate_count": 4,
    }

    rates = calculate_rates(metrics, total_count=20)

    assert rates["debate_rate"] == 0.2


def test_calculates_zero_rates_for_empty_results():
    metrics = {
        "success_count": 0,
        "degraded_count": 0,
        "failure_count": 0,
        "debate_count": 0,
    }

    rates = calculate_rates(metrics, total_count=0)

    assert rates == {
        "success_rate": 0,
        "degraded_rate": 0,
        "failure_rate": 0,
        "debate_rate": 0,
    }


def test_builds_stress_report():
    results = [
        {"status": "ok", "debate": None},
        {"status": "ok", "debate": {"consensus_answer": "final"}},
        {"status": "degraded", "debate": None},
        {"status": "failed", "debate": None},
    ]

    report = build_stress_report(results)

    assert report == {
        "total_count": 4,
        "success_count": 2,
        "degraded_count": 1,
        "failure_count": 1,
        "debate_count": 1,
        "success_rate": 0.5,
        "degraded_rate": 0.25,
        "failure_rate": 0.25,
        "debate_rate": 0.25,
    }


def test_formats_stress_report():
    report = {
        "total_count": 50,
        "success_rate": 0.82,
        "degraded_rate": 0.14,
        "failure_rate": 0.04,
        "debate_rate": 0.02,
    }

    formatted = format_stress_report(report)

    assert formatted == (
        "Total requests: 50\n"
        "Success rate: 82.0%\n"
        "Degraded rate: 14.0%\n"
        "Failure rate: 4.0%\n"
        "Debate rate: 2.0%"
    )


def test_formats_stress_report_with_timing_metrics():
    report = {
        "total_count": 50,
        "success_rate": 0.82,
        "degraded_rate": 0.14,
        "failure_rate": 0.04,
        "debate_rate": 0.02,
        "average_duration_seconds": 1.23456,
        "min_duration_seconds": 0.5,
        "max_duration_seconds": 2.75,
    }

    formatted = format_stress_report(report)

    assert formatted == (
        "Total requests: 50\n"
        "Success rate: 82.0%\n"
        "Degraded rate: 14.0%\n"
        "Failure rate: 4.0%\n"
        "Debate rate: 2.0%\n"
        "Average duration: 1.235s\n"
        "Min duration: 0.500s\n"
        "Max duration: 2.750s"
    )

def test_formats_stress_report_with_reliability_metrics():
    report = {
        "total_count": 50,
        "success_rate": 0.82,
        "degraded_rate": 0.14,
        "failure_rate": 0.04,
        "debate_rate": 0.02,
        "reliability_score": 0.89,
        "reliability_status": "good",
    }

    formatted = format_stress_report(report)

    assert formatted == (
        "Reliability status: good\n"
        "Reliability score: 0.890\n"
        "\n"
        "Total requests: 50\n"
        "Success rate: 82.0%\n"
        "Degraded rate: 14.0%\n"
        "Failure rate: 4.0%\n"
        "Debate rate: 2.0%"
    )


def test_counts_one_hundred_simulated_requests():
    results = []

    for _ in range(82):
        results.append({"status": "ok", "debate": None})

    for _ in range(12):
        results.append({"status": "degraded", "debate": None})

    for _ in range(4):
        results.append({"status": "failed", "debate": None})

    for _ in range(2):
        results.append(
            {"status": "ok", "debate": {"consensus_answer": "final"}}
        )

    report = build_stress_report(results)

    assert report["total_count"] == 100
    assert report["success_count"] == 84
    assert report["degraded_count"] == 12
    assert report["failure_count"] == 4
    assert report["debate_count"] == 2
    assert report["success_rate"] == 0.84
    assert report["degraded_rate"] == 0.12
    assert report["failure_rate"] == 0.04
    assert report["debate_rate"] == 0.02

def test_builds_excellent_reliability_summary():
    summary = build_reliability_summary(
        {
            "success_rate": 0.98,
            "degraded_rate": 0.0,
        }
    )

    assert summary == {
        "reliability_score": 0.98,
        "status": "excellent",
    }


def test_builds_good_reliability_summary():
    summary = build_reliability_summary(
        {
            "success_rate": 0.85,
            "degraded_rate": 0.0,
        }
    )

    assert summary == {
        "reliability_score": 0.85,
        "status": "good",
    }


def test_builds_fair_reliability_summary():
    summary = build_reliability_summary(
        {
            "success_rate": 0.50,
            "degraded_rate": 0.20,
        }
    )

    assert summary == {
        "reliability_score": 0.60,
        "status": "fair",
    }


def test_builds_poor_reliability_summary():
    summary = build_reliability_summary(
        {
            "success_rate": 0.20,
            "degraded_rate": 0.20,
        }
    )

    assert summary == {
        "reliability_score": 0.30,
        "status": "poor",
    }

def test_format_stress_report_defaults_missing_reliability_status():
    report = {
        "total_count": 1,
        "success_rate": 1.0,
        "degraded_rate": 0.0,
        "failure_rate": 0.0,
        "debate_rate": 0.0,
        "reliability_score": 1.0,
    }

    formatted = format_stress_report(report)

    assert formatted == (
        "Reliability status: unknown\n"
        "Reliability score: 1.000\n"
        "\n"
        "Total requests: 1\n"
        "Success rate: 100.0%\n"
        "Degraded rate: 0.0%\n"
        "Failure rate: 0.0%\n"
        "Debate rate: 0.0%"
    )