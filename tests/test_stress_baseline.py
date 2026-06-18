from unittest.mock import patch

from agent.council import ask_council


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_multiple_council_requests(
    mock_judge,
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = "DeepSeek answer"

    mock_judge.return_value = {
        "gemini_judge": {},
        "deepseek_judge": {},
        "independent_judge": {},
        "debate_vote_count": 0,
        "final_needs_debate": False,
    }

    for _ in range(5):
        result = ask_council("test")

        assert result["status"] == "ok"

    assert mock_judge.call_count == 5