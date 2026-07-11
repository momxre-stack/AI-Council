import pytest
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
        "gemini_judge": {"agreement_score": 90},
        "deepseek_judge": {"agreement_score": 80},
        "independent_judge": {"agreement_score": 40},
        "final_needs_debate": False,
    }

    result = ask_council("test")

    assert result["question"] == "test"
    assert result["status"] == "ok"
    assert result["degraded_reason"] is None
    assert result["debate"] is None
    assert result["semantic_validation"]["independent_score"] == 40
    assert result["semantic_validation"]["llm_average_score"] == 85
    assert result["semantic_validation"]["agreement_gap"] == 50
    assert result["semantic_validation"]["is_semantic_candidate"] is True
    assert result["judgment"]["final_needs_debate"] is False
    assert result["assessment"] == {
        "confidence": "low",
        "reason": "low_agreement",
        "signals": {
            "agreement_rate": 0,
            "debate_used": False,
            "reliability_status": "healthy",
        },
    }

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
    assert result["degraded_reason"] is None
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
    assert result["degraded_reason"] == "provider_failure"
    assert result["responses"]["gemini"] is None
    assert result["responses"]["deepseek"] == "DeepSeek answer"
    assert result["provider_errors"]["gemini"] == "Gemini failed"
    assert result["judgment"] is None
    assert result["debate"] is None
    assert result["assessment"] is None


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
    assert result["degraded_reason"] == "judge_failure"
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
    assert result["degraded_reason"] == "debate_failure"
    assert result["judgment"] is not None
    assert result["debate"] is None
    assert result["debate_error"] == "Debate failed"


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_marks_provider_quota_errors(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.side_effect = RuntimeError("429 RESOURCE_EXHAUSTED")
    mock_deepseek.return_value = "DeepSeek answer"

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["provider_errors"]["gemini"] == "429 RESOURCE_EXHAUSTED"
    assert result["quota_errors"]["gemini"] is True
    assert result["quota_errors"]["deepseek"] is False


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_raises_when_both_providers_fail(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.side_effect = RuntimeError("429 RESOURCE_EXHAUSTED")
    mock_deepseek.side_effect = RuntimeError("429 RESOURCE_EXHAUSTED")

    with pytest.raises(RuntimeError) as error:
        ask_council("test")

    assert str(error.value) == (
        "Both providers failed: "
        "gemini=429 RESOURCE_EXHAUSTED; "
        "deepseek=429 RESOURCE_EXHAUSTED"
    )


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_gemini_returns_empty_response(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "   "
    mock_deepseek.return_value = "DeepSeek answer"

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["gemini"] is None
    assert result["responses"]["deepseek"] == "DeepSeek answer"
    assert result["provider_errors"]["gemini"] == "Provider returned empty response"
    assert result["judgment"] is None
    assert result["debate"] is None


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_deepseek_returns_empty_response(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = ""

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["gemini"] == "Gemini answer"
    assert result["responses"]["deepseek"] is None
    assert result["provider_errors"]["deepseek"] == "Provider returned empty response"
    assert result["judgment"] is None
    assert result["debate"] is None

@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_gemini_returns_none(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = None
    mock_deepseek.return_value = "DeepSeek answer"

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["gemini"] is None
    assert result["provider_errors"]["gemini"] == "Provider returned invalid response"


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_degraded_when_deepseek_returns_dict(
    mock_deepseek,
    mock_gemini,
):
    mock_gemini.return_value = "Gemini answer"
    mock_deepseek.return_value = {"answer": "test"}

    result = ask_council("test")

    assert result["status"] == "degraded"
    assert result["responses"]["deepseek"] is None
    assert result["provider_errors"]["deepseek"] == "Provider returned invalid response"

@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_council_assessment_uses_judgment_agreement_rate(
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
        "agreement_rate": 0.9,
    }

    result = ask_council("test")

    assert result["assessment"]["confidence"] == "high"
    assert result["assessment"]["signals"]["agreement_rate"] == 0.9

@patch("agent.council.PROVIDERS")
def test_ask_gemini_uses_provider_registry(mock_providers):
    mock_providers.__getitem__.return_value.return_value = "Gemini answer"

    from agent.council import ask_gemini

    result = ask_gemini("test prompt")

    assert result == "Gemini answer"
    mock_providers.__getitem__.assert_called_once_with("gemini")
    mock_providers.__getitem__.return_value.assert_called_once_with(
        "test prompt"
    )


@patch("agent.council.PROVIDERS")
def test_ask_deepseek_uses_provider_registry(mock_providers):
    mock_providers.__getitem__.return_value.return_value = "DeepSeek answer"

    from agent.council import ask_deepseek

    result = ask_deepseek("test prompt")

    assert result == "DeepSeek answer"
    mock_providers.__getitem__.assert_called_once_with("deepseek")
    mock_providers.__getitem__.return_value.assert_called_once_with(
        "test prompt"
    )

@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
@patch("agent.council.run_dual_judgment")
def test_council_response_includes_only_gemini_and_deepseek(
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

    assert set(result["responses"]) == {"gemini", "deepseek"}
    assert set(result["provider_errors"]) == {"gemini", "deepseek"}
    assert set(result["quota_errors"]) == {"gemini", "deepseek"}


@patch("agent.council.ask_gemini")
@patch("agent.council.ask_deepseek")
def test_council_redacts_api_key_from_provider_error(
    mock_deepseek,
    mock_gemini,
):
    exposed_key = "secret-gemini-api-key"
    mock_gemini.side_effect = RuntimeError(
        "503 Service Unavailable for "
        "https://generativelanguage.googleapis.com/"
        f"generateContent?key={exposed_key}"
    )
    mock_deepseek.return_value = "DeepSeek answer"

    result = ask_council("test")

    gemini_error = result["provider_errors"]["gemini"]

    assert result["status"] == "degraded"
    assert result["degraded_reason"] == "provider_failure"
    assert exposed_key not in gemini_error
    assert "?key=[REDACTED]" in gemini_error
