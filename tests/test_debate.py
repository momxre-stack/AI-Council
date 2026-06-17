from unittest.mock import patch

from agent.debate import run_debate


@patch("agent.debate.ask_gemini")
def test_run_debate_returns_debate_result(mock_gemini):
    mock_gemini.return_value = "debate result"

    result = run_debate(
        question="question",
        gemini_response="gemini answer",
        deepseek_response="deepseek answer",
    )

    assert result == {
        "debate": "debate result",
    }

    mock_gemini.assert_called_once()