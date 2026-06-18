from agent.quota_utils import is_quota_error


def test_detects_resource_exhausted_error():
    assert is_quota_error(
        Exception("429 RESOURCE_EXHAUSTED")
    )


def test_detects_resource_exhausted_without_code():
    assert is_quota_error(
        Exception("RESOURCE_EXHAUSTED")
    )


def test_detects_rate_limit_error():
    assert is_quota_error(
        Exception("Rate limit exceeded")
    )


def test_non_quota_error_returns_false():
    assert not is_quota_error(
        Exception("Connection failed")
    )