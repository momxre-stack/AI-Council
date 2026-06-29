from unittest.mock import Mock, patch

import httpx
import pytest
from google.genai.errors import APIError, ServerError, UnknownApiResponseError

from agent.providers.gemini import MAX_RETRIES, REQUEST_TIMEOUT_SECONDS, ask_gemini


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_server_errors_until_exhausted(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    server_error = ServerError(
    500,
    {"error": {"message": "temporary provider failure"}},
)

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = server_error
    mock_client_class.return_value = mock_client

    with pytest.raises(ServerError) as error:
        ask_gemini("test prompt")

    assert error.value is server_error
    assert mock_client.models.generate_content.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_recovers_after_temporary_server_error(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    server_error = ServerError(
    500,
    {"error": {"message": "temporary provider failure"}},
)

    success_response = Mock()
    success_response.text = "Recovered answer"

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = [
        server_error,
        success_response,
    ]

    mock_client_class.return_value = mock_client

    result = ask_gemini("test prompt")

    assert result == "Recovered answer"
    assert mock_client.models.generate_content.call_count == 2
    assert mock_sleep.call_count == 1

@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_api_errors_until_exhausted(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    api_error = APIError(
        500,
        {"error": {"message": "temporary provider failure"}},
    )

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = api_error
    mock_client_class.return_value = mock_client

    with pytest.raises(APIError) as error:
        ask_gemini("test prompt")

    assert error.value is api_error
    assert mock_client.models.generate_content.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_unknown_api_response_errors_until_exhausted(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    unknown_response_error = UnknownApiResponseError(
        "unknown API response"
    )

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = unknown_response_error
    mock_client_class.return_value = mock_client

    with pytest.raises(UnknownApiResponseError) as error:
        ask_gemini("test prompt")

    assert error.value is unknown_response_error
    assert mock_client.models.generate_content.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_recovers_after_unknown_api_response_error(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    unknown_response_error = UnknownApiResponseError(
        "unknown API response"
    )

    success_response = Mock()
    success_response.text = "Recovered answer"

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = [
        unknown_response_error,
        success_response,
    ]

    mock_client_class.return_value = mock_client

    result = ask_gemini("test prompt")

    assert result == "Recovered answer"
    assert mock_client.models.generate_content.call_count == 2
    assert mock_sleep.call_count == 1

@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_client_uses_request_timeout(
    mock_getenv,
    mock_client_class,
):
    mock_getenv.return_value = "test-key"

    mock_client = Mock()
    mock_response = Mock()
    mock_response.text = "Gemini answer"
    mock_client.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client

    ask_gemini("test prompt")

    client_kwargs = mock_client_class.call_args.kwargs

    assert client_kwargs["api_key"] == "test-key"
    assert client_kwargs["http_options"].timeout == REQUEST_TIMEOUT_SECONDS

@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_timeout_errors_until_exhausted(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    timeout_error = TimeoutError("_ssl.c:989: The handshake operation timed out")

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = timeout_error
    mock_client_class.return_value = mock_client

    with pytest.raises(TimeoutError) as error:
        ask_gemini("test prompt")

    assert error.value is timeout_error
    assert mock_client.models.generate_content.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini.genai.Client")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_httpx_connect_timeout_until_exhausted(
    mock_getenv,
    mock_client_class,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    timeout_error = httpx.ConnectTimeout("timed out")

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = timeout_error
    mock_client_class.return_value = mock_client

    with pytest.raises(httpx.ConnectTimeout) as error:
        ask_gemini("test prompt")

    assert error.value is timeout_error
    assert mock_client.models.generate_content.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1

def test_parse_generate_content_response_returns_first_candidate_text():
    from agent.providers.gemini import _parse_generate_content_response

    response_data = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": "Gemini REST answer"}
                    ]
                }
            }
        ]
    }

    assert _parse_generate_content_response(response_data) == "Gemini REST answer"

@patch("agent.providers.gemini.httpx.post")
def test_post_generate_content_sends_rest_request(mock_post):
    from agent.providers.gemini import _post_generate_content

    mock_response = Mock()
    mock_response.json.return_value = {"candidates": []}
    mock_post.return_value = mock_response

    result = _post_generate_content("test-key", "Hello")

    assert result == {"candidates": []}
    mock_post.assert_called_once_with(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=test-key",
        json={
            "contents": [
                {
                    "parts": [
                        {"text": "Hello"}
                    ]
                }
            ]
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

