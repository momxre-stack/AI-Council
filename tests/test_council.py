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
    assert result["status"] == "ok"
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

    assert result["status"] == "ok"
    assert result["debate"] is not None

    mock_debate.assert_called_once()


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_gemini_fails(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.side_effect = RuntimeError("Gemini failed")
    mock_deepseek.return_value = "DeepSeek answer"

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["gemini"] is None
    assert result["responses"]["deepseek"] == "DeepSeek answer"
    assert result["provider_errors"]["gemini"] == "Gemini failed"
    assert result["judgment"] is None
    assert result["debate"] is None


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_deepseek_fails(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.side_effect = RuntimeError("DeepSeek failed")

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["gemini"] == "Gemini answer"
    assert result["responses"]["deepseek"] is None
    assert result["provider_errors"]["deepseek"] == "DeepSeek failed"
    assert result["judgment"] is None
    assert result["debate"] is None


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_council_degraded_when_judge_fails(
    mock_judge,
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = "DeepSeek answer"
    mock_judge.side_effect = RuntimeError("Judge failed")

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["judgment"] is None
    assert result["judgment_error"] == "Judge failed"
    assert result["debate"] is None


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_council_degraded_when_judge_returns_malformed_json(
    mock_judge,
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = "DeepSeek answer"
    mock_judge.side_effect = ValueError(
        "Judge did not return JSON: malformed judge output"
    )

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["judgment"] is None
    assert (
        result["judgment_error"]
        == "Judge did not return JSON: malformed judge output"
    )
    assert result["debate"] is None


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_debate")
@patch("agent.council.run_dual_judgment")
def test_council_degraded_when_debate_fails(
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

    mock_debate.side_effect = RuntimeError("Debate failed")

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["judgment"] is not None
    assert result["debate"] is None
    assert result["debate_error"] == "Debate failed"
