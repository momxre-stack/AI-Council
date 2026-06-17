from unittest.mock import patch

from agent.council import ask_council


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_council_without_debate(
    mock_judge,
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = "DeepSeek answer"

    mock_judge.return_value = {
        "gemini_judge": {},
        "deepseek_judge": {},
        "final_needs_debate": False,
    }

    result = ask_council("test")

    assert result["question"] == "test"
    assert result["debate"] is None
    assert result["judgment"]["final_needs_debate"] is False


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_debate")
@patch("agent.council.run_dual_judgment")
def test_council_with_debate(
    mock_judge,
    mock_debate,
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = "DeepSeek answer"

    mock_judge.return_value = {
        "gemini_judge": {},
        "deepseek_judge": {},
        "final_needs_debate": True,
    }

    mock_debate.return_value = {
        "debate": "debate result",
    }

    result = ask_council("test")

    assert result["debate"] is not None

    mock_debate.assert_called_once()