from unittest.mock import Mock, patch

import httpx
import pytest
from google.genai.errors import APIError, ServerError, UnknownApiResponseError

from agent.providers.gemini import MAX_RETRIES, REQUEST_TIMEOUT_SECONDS, ask_gemini


def _success_response_data(text="Gemini answer"):
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": text}
                    ]
                }
            }
        ]
    }


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_server_errors_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    server_error = ServerError(
        500,
        {"error": {"message": "temporary provider failure"}},
    )
    mock_post.side_effect = server_error

    with pytest.raises(ServerError) as error:
        ask_gemini("test prompt")

    assert error.value is server_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_recovers_after_temporary_server_error(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    server_error = ServerError(
        500,
        {"error": {"message": "temporary provider failure"}},
    )
    mock_post.side_effect = [
        server_error,
        _success_response_data("Recovered answer"),
    ]

    result = ask_gemini("test prompt")

    assert result == "Recovered answer"
    assert mock_post.call_count == 2
    assert mock_sleep.call_count == 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_api_errors_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    api_error = APIError(
        500,
        {"error": {"message": "temporary provider failure"}},
    )
    mock_post.side_effect = api_error

    with pytest.raises(APIError) as error:
        ask_gemini("test prompt")

    assert error.value is api_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_unknown_api_response_errors_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    unknown_response_error = UnknownApiResponseError(
        "unknown API response"
    )
    mock_post.side_effect = unknown_response_error

    with pytest.raises(UnknownApiResponseError) as error:
        ask_gemini("test prompt")

    assert error.value is unknown_response_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_recovers_after_unknown_api_response_error(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    unknown_response_error = UnknownApiResponseError(
        "unknown API response"
    )
    mock_post.side_effect = [
        unknown_response_error,
        _success_response_data("Recovered answer"),
    ]

    result = ask_gemini("test prompt")

    assert result == "Recovered answer"
    assert mock_post.call_count == 2
    assert mock_sleep.call_count == 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_timeout_errors_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    timeout_error = TimeoutError("_ssl.c:989: The handshake operation timed out")
    mock_post.side_effect = timeout_error

    with pytest.raises(TimeoutError) as error:
        ask_gemini("test prompt")

    assert error.value is timeout_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_httpx_connect_timeout_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    timeout_error = httpx.ConnectTimeout("timed out")
    mock_post.side_effect = timeout_error

    with pytest.raises(httpx.ConnectTimeout) as error:
        ask_gemini("test prompt")

    assert error.value is timeout_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.time.sleep")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_gemini_retries_http_status_errors_until_exhausted(
    mock_getenv,
    mock_post,
    mock_sleep,
):
    mock_getenv.return_value = "test-key"

    request = httpx.Request("POST", "https://example.com")
    response = httpx.Response(500, request=request)
    status_error = httpx.HTTPStatusError(
        "server error",
        request=request,
        response=response,
    )
    mock_post.side_effect = status_error

    with pytest.raises(httpx.HTTPStatusError) as error:
        ask_gemini("test prompt")

    assert error.value is status_error
    assert mock_post.call_count == MAX_RETRIES
    assert mock_sleep.call_count == MAX_RETRIES - 1


@patch("agent.providers.gemini.os.getenv")
def test_gemini_requires_api_key(mock_getenv):
    mock_getenv.return_value = None

    with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
        ask_gemini("test prompt")


def test_parse_generate_content_response_returns_first_candidate_text():
    from agent.providers.gemini import _parse_generate_content_response

    assert (
        _parse_generate_content_response(
            _success_response_data("Gemini REST answer")
        )
        == "Gemini REST answer"
    )


@patch("agent.providers.gemini.httpx.post")
def test_post_generate_content_sends_rest_request(mock_post):
    from agent.providers.gemini import _post_generate_content

    mock_response = Mock()
    mock_response.json.return_value = {"candidates": []}
    mock_post.return_value = mock_response

    result = _post_generate_content("test-key", "Hello")

    assert result == {"candidates": []}
    mock_response.raise_for_status.assert_called_once()
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


@patch("agent.providers.gemini._parse_generate_content_response")
@patch("agent.providers.gemini._post_generate_content")
@patch("agent.providers.gemini.os.getenv")
def test_ask_gemini_uses_rest_helpers(
    mock_getenv,
    mock_post,
    mock_parse,
):
    mock_getenv.return_value = "test-key"

    mock_post.return_value = {"candidates": []}
    mock_parse.return_value = "Gemini answer"

    result = ask_gemini("Hello")

    assert result == "Gemini answer"
    mock_post.assert_called_once_with("test-key", "Hello")
    mock_parse.assert_called_once_with({"candidates": []})
