from agent.stress_report_storage import (
    build_stress_report_path,
    compare_latest_stress_reports,
    compare_saved_stress_reports,
    format_latest_stress_report_changes,
    generate_latest_stress_report_summary,
    get_latest_stress_report_path,
    load_latest_stress_report,
    load_stress_report,
    load_stress_reports,
    save_stress_report,
    summarize_latest_stress_report_changes,
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

def test_get_latest_stress_report_path_returns_latest_report_path(tmp_path):
    save_stress_report(
        {"success_rate": 0.5},
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {"success_rate": 0.9},
        str(tmp_path / "stress-report-002.json"),
    )
    save_stress_report(
        {"ignored": True},
        str(tmp_path / "notes.json"),
    )

    result = get_latest_stress_report_path(str(tmp_path))

    assert result == os_path(str(tmp_path), "stress-report-002.json")


def test_get_latest_stress_report_path_returns_none_without_reports(tmp_path):
    save_stress_report(
        {"ignored": True},
        str(tmp_path / "notes.json"),
    )

    assert get_latest_stress_report_path(str(tmp_path)) is None
    assert get_latest_stress_report_path(str(tmp_path / "missing")) is None


def test_load_latest_stress_report_returns_latest_report(tmp_path):
    old_report = {
        "success_rate": 0.5,
    }
    latest_report = {
        "success_rate": 0.9,
    }

    save_stress_report(
        old_report,
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        latest_report,
        str(tmp_path / "stress-report-002.json"),
    )

    result = load_latest_stress_report(str(tmp_path))

    assert result == latest_report


def test_load_latest_stress_report_returns_none_without_reports(tmp_path):
    save_stress_report(
        {"ignored": True},
        str(tmp_path / "notes.json"),
    )

    assert load_latest_stress_report(str(tmp_path)) is None
    assert load_latest_stress_report(str(tmp_path / "missing")) is None




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

def test_compare_latest_stress_reports_returns_latest_report_deltas(tmp_path):
    save_stress_report(
        {
            "success_rate": 0.5,
            "failure_rate": 0.5,
        },
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
        },
        str(tmp_path / "stress-report-002.json"),
    )

    result = compare_latest_stress_reports(str(tmp_path))

    assert result == {
        "success_rate_delta": 0.3,
        "failure_rate_delta": -0.3,
    }


def test_compare_latest_stress_reports_returns_empty_dict_without_two_reports(tmp_path):
    assert compare_latest_stress_reports(str(tmp_path)) == {}

    save_stress_report(
        {
            "success_rate": 0.5,
        },
        str(tmp_path / "stress-report-001.json"),
    )

    assert compare_latest_stress_reports(str(tmp_path)) == {}

def test_summarize_latest_stress_report_changes_returns_deltas(tmp_path):
    save_stress_report(
        {
            "success_rate": 0.5,
            "failure_rate": 0.5,
        },
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
        },
        str(tmp_path / "stress-report-002.json"),
    )

    result = summarize_latest_stress_report_changes(str(tmp_path))

    assert result == {
        "has_changes": True,
        "deltas": {
            "success_rate_delta": 0.3,
            "failure_rate_delta": -0.3,
        },
    }


def test_summarize_latest_stress_report_changes_handles_missing_comparison(tmp_path):
    assert summarize_latest_stress_report_changes(str(tmp_path)) == {
        "has_changes": False,
        "deltas": {},
    }






def test_format_latest_stress_report_changes_returns_text():
    summary = {
        "has_changes": True,
        "deltas": {
            "success_rate_delta": 0.3,
            "failure_rate_delta": -0.3,
        },
    }

    result = format_latest_stress_report_changes(summary)

    assert result == (
        "Changes detected: yes\n"
        "Failure rate delta: -0.3000\n"
        "Success rate delta: +0.3000"
    )


def test_format_latest_stress_report_changes_handles_empty_summary():
    summary = {
        "has_changes": False,
        "deltas": {},
    }

    result = format_latest_stress_report_changes(summary)

    assert result == "Changes detected: no"

def test_generate_latest_stress_report_summary_returns_text(tmp_path):
    save_stress_report(
        {
            "success_rate": 0.5,
            "failure_rate": 0.5,
        },
        str(tmp_path / "stress-report-001.json"),
    )
    save_stress_report(
        {
            "success_rate": 0.8,
            "failure_rate": 0.2,
        },
        str(tmp_path / "stress-report-002.json"),
    )

    result = generate_latest_stress_report_summary(str(tmp_path))

    assert result == (
        "Changes detected: yes\n"
        "Failure rate delta: -0.3000\n"
        "Success rate delta: +0.3000"
    )


def test_generate_latest_stress_report_summary_handles_missing_reports(tmp_path):
    result = generate_latest_stress_report_summary(str(tmp_path))

    assert result == "Changes detected: no"

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