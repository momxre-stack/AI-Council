from agent.stress_report_storage import (
    build_stress_report_path,
    compare_saved_stress_reports,
    load_stress_report,
    load_stress_reports,
    save_stress_report,
)


def test_save_and_load_stress_report(tmp_path):
    report = {
        "success_rate": 1.0,
        "failure_rate": 0.0,
        "reliability_score": 1.0,
    }

    report_file = tmp_path / "report.json"

    save_stress_report(report, str(report_file))

    loaded_report = load_stress_report(str(report_file))

    assert loaded_report == report


def test_save_stress_report_creates_parent_directory(tmp_path):
    report = {
        "success_rate": 1.0,
    }

    report_file = tmp_path / "reports" / "stress" / "report.json"

    save_stress_report(report, str(report_file))

    assert report_file.exists()
    assert load_stress_report(str(report_file)) == report


def test_build_stress_report_path_returns_deterministic_json_path():
    result = build_stress_report_path("reports", "nightly-001")

    assert result == os_path("reports", "stress-report-nightly-001.json")


def test_load_stress_reports_returns_reports_from_directory(tmp_path):
    report_one = {
        "success_rate": 1.0,
    }
    report_two = {
        "success_rate": 0.5,
    }

    save_stress_report(
        report_two,
        str(tmp_path / "stress-report-002.json"),
    )
    save_stress_report(
        report_one,
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {"ignored": True},
        str(tmp_path / "notes.json"),
    )

    result = load_stress_reports(str(tmp_path))

    assert result == [
        report_one,
        report_two,
    ]


def test_load_stress_reports_returns_empty_list_for_missing_directory(tmp_path):
    result = load_stress_reports(str(tmp_path / "missing"))

    assert result == []


def test_compare_saved_stress_reports_returns_numeric_deltas():
    previous_report = {
        "total_count": 10,
        "success_rate": 0.8,
        "failure_rate": 0.2,
        "reliability_score": 0.75,
    }
    current_report = {
        "total_count": 12,
        "success_rate": 0.9,
        "failure_rate": 0.1,
        "reliability_score": 0.81234,
    }

    result = compare_saved_stress_reports(previous_report, current_report)

    assert result == {
        "total_count_delta": 2,
        "success_rate_delta": 0.1,
        "failure_rate_delta": -0.1,
        "reliability_score_delta": 0.0623,
    }


def test_compare_saved_stress_reports_ignores_missing_and_non_numeric_values():
    previous_report = {
        "success_rate": 0.8,
        "failure_rate": 0.2,
        "status": "ok",
        "previous_only": 1.0,
    }
    current_report = {
        "success_rate": 0.9,
        "failure_rate": "not numeric",
        "status": "ok",
        "current_only": 1.0,
    }

    result = compare_saved_stress_reports(previous_report, current_report)

    assert result == {
        "success_rate_delta": 0.1,
    }


def os_path(*parts):
    import os

    return os.path.join(*parts)