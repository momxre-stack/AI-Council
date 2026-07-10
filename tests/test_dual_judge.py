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


@patch("agent.dual_judge.independent_judge_responses")
@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_current_policy_allows_independent_judge_as_second_vote(
    mock_gemini_judge,
    mock_deepseek,
    mock_independent_judge,
):
    mock_gemini_judge.return_value = _judgment(85, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 75,
      "needs_debate": true,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """
    mock_independent_judge.return_value = _judgment(29, True, "tie")

    result = run_dual_judgment(
        "question",
        "Gemini answer with different wording.",
        "DeepSeek answer with different wording.",
    )

    assert result["debate_vote_count"] == 2
    assert result["final_needs_debate"] is True

@patch("agent.dual_judge.independent_judge_responses")
@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_current_policy_rejects_independent_judge_as_only_vote(
    mock_gemini_judge,
    mock_deepseek,
    mock_independent_judge,
):
    mock_gemini_judge.return_value = _judgment(90, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 85,
      "needs_debate": false,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """
    mock_independent_judge.return_value = _judgment(29, True, "tie")

    result = run_dual_judgment(
        "question",
        "Gemini answer with different wording.",
        "DeepSeek answer with different wording.",
    )

    assert result["debate_vote_count"] == 1
    assert result["final_needs_debate"] is False


@patch("agent.dual_judge.independent_judge_responses")
@patch("agent.dual_judge.ask_deepseek")
@patch("agent.dual_judge.judge_responses_v2")
def test_dual_judge_exposes_provider_and_independent_vote_diagnostics(
    mock_gemini_judge,
    mock_deepseek,
    mock_independent_judge,
):
    mock_gemini_judge.return_value = _judgment(85, False, "tie")
    mock_deepseek.return_value = """
    {
      "agreement_score": 75,
      "needs_debate": true,
      "agreements": [],
      "differences": [],
      "more_complete_response": "tie",
      "final_answer": "final"
    }
    """
    mock_independent_judge.return_value = _judgment(29, True, "tie")

    result = run_dual_judgment(
        "question",
        "Gemini answer with different wording.",
        "DeepSeek answer with different wording.",
    )

    assert result["debate_vote_count"] == 2
    assert result["provider_debate_vote_count"] == 1
    assert result["independent_debate_vote"] is True
    assert result["final_needs_debate"] is True
