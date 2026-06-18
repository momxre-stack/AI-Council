def is_quota_error(error: Exception) -> bool:
    message = str(error).lower()

    quota_markers = [
        "429",
        "resource_exhausted",
        "rate limit",
        "rate_limit",
        "quota",
    ]

    return any(marker in message for marker in quota_markers)