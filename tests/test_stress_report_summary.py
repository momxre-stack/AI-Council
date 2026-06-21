from agent.stress_report_summary import (
    format_latest_stress_report_changes,
)


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