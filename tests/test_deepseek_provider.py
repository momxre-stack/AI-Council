from unittest.mock import Mock, patch

import httpx
import pytest
from openai import APIConnectionError, APIError, RateLimitError

from agent.providers.deepseek import MAX_RETRIES, ask_deepseek


@patch("agent.providers.deepseek.time.sleep")
@patch("agent.providers.deepseek.OpenAI")
@patch("agent.providers.deepseek.os.getenv")
def test_deepseek_retries_api_errors_until_exhausted(
    mock_getenv,
    mock_openai,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    api_error = APIError(
        "temporary provider failure",
        request=Mock(),
        body=None,
    )

    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = api_error
    mock_openai.return_value = mock_client

    with pytest.raises(APIError) as error:
        ask_deepseek("test prompt")

    assert error.value is api_error
    assert mock_client.chat.completions.create.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

@patch("agent.providers.deepseek.time.sleep")
@patch("agent.providers.deepseek.OpenAI")
@patch("agent.providers.deepseek.os.getenv")
def test_deepseek_recovers_after_temporary_api_error(
    mock_getenv,
    mock_openai,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    api_error = APIError(
        "temporary provider failure",
        request=Mock(),
        body=None,
    )

    success_response = Mock()
    success_response.choices = [
        Mock(message=Mock(content="Recovered answer"))
    ]

    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = [
        api_error,
        success_response,
    ]

    mock_openai.return_value = mock_client

    result = ask_deepseek("test prompt")

    assert result == "Recovered answer"
    assert mock_client.chat.completions.create.call_count == 2
    assert mock_sleep.call_count == 1


@patch("agent.providers.deepseek.time.sleep")
@patch("agent.providers.deepseek.OpenAI")
@patch("agent.providers.deepseek.os.getenv")
def test_deepseek_retries_rate_limit_errors_until_exhausted(
    mock_getenv,
    mock_openai,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    rate_limit_error = RateLimitError(
        "rate limit exceeded",
        response=httpx.Response(429, request=httpx.Request("POST", "https://api.deepseek.com")),
        body=None,
    )

    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = rate_limit_error
    mock_openai.return_value = mock_client

    with pytest.raises(RateLimitError) as error:
        ask_deepseek("test prompt")

    assert error.value is rate_limit_error
    assert mock_client.chat.completions.create.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

@patch("agent.providers.deepseek.time.sleep")
@patch("agent.providers.deepseek.OpenAI")
@patch("agent.providers.deepseek.os.getenv")
def test_deepseek_retries_connection_errors_until_exhausted(
    mock_getenv,
    mock_openai,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    connection_error = APIConnectionError(
        message="connection failed",
        request=httpx.Request("POST", "https://api.deepseek.com"),
    )

    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = connection_error
    mock_openai.return_value = mock_client

    with pytest.raises(APIConnectionError) as error:
        ask_deepseek("test prompt")

    assert error.value is connection_error
    assert mock_client.chat.completions.create.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1