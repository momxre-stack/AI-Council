from unittest.mock import Mock, patch

from agent.providers.openai_provider import REQUEST_TIMEOUT_SECONDS, ask_openai


@patch("agent.providers.openai_provider.OpenAI")
@patch("agent.providers.openai_provider.os.getenv")
def test_openai_client_uses_request_timeout(
    mock_getenv,
    mock_openai,
):
    mock_getenv.return_value = "test-key"

    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content="OpenAI answer"))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    result = ask_openai("test prompt")

    assert result == "OpenAI answer"
    mock_openai.assert_called_once_with(
        api_key="test-key",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

