from agent.stress_report_storage import (
    load_stress_report,
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