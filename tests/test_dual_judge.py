from unittest.mock import patch

from agent.dual_judge import run_dual_judgment


def _judgment(score, needs_debate, winner):
    return {
        "agreement_score": score,
        "needs_debate": needs_debate,
        "agreements": [],
        "differences": [],
        "more_complete_response": winner,
        "final_answer": "final",
    }


@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_no_debate_when_judges_agree(
    mock_gemini_judge,
    mock_deepseek,
):
    mock_gemini_judge.return_value = _judgment(90, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 90,
      "needs_debate": false,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """

    result = run_dual_judgment("question", "gemini", "deepseek")

    assert result["final_needs_debate"] is False


@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_debates_when_either_judge_requests_it(
    mock_gemini_judge,
    mock_deepseek,
):
    mock_gemini_judge.return_value = _judgment(90, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 60,
      "needs_debate": true,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """

    result = run_dual_judgment("question", "gemini", "deepseek")

    assert result["final_needs_debate"] is True


@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_debates_when_winners_disagree(
    mock_gemini_judge,
    mock_deepseek,
):
    mock_gemini_judge.return_value = _judgment(90, False, "gemini")
    mock_deepseek.return_value = """
    {
      "agreement_score": 90,
      "needs_debate": false,
      "agreements": [],
      "differences": [],
      "more_complete_response": "deepseek",
      "final_answer": "final"
    }
    """

    result = run_dual_judgment("question", "gemini", "deepseek")

    assert result["final_needs_debate"] is True


@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_debates_when_scores_differ_significantly(
    mock_gemini_judge,
    mock_deepseek,
):
    mock_gemini_judge.return_value = _judgment(95, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 60,
      "needs_debate": false,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """

    result = run_dual_judgment("question", "gemini", "deepseek")

    assert result["final_needs_debate"] is True