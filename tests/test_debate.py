from unittest.mock import patch

from agent.debate import run_debate


@patch("agent.debate.ask_gemini")
def test_run_debate_returns_structured_result(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "Gemini strength",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer"
    }
    """

    result = run_debate(
        question="question",
        gemini_response="gemini answer",
        deepseek_response="deepseek answer",
    )

    assert result == {
        "gemini_strengths": "Gemini strength",
        "deepseek_strengths": "DeepSeek strength",
        "criticisms": "Both missed details",
        "consensus_answer": "Final answer",
    }

    mock_gemini.assert_called_once()