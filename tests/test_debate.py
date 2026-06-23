from unittest.mock import patch

import pytest

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


@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_malformed_json(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "Gemini says "quoted text"",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer"
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_missing_required_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "Gemini strength",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details"
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_non_string_required_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": [],
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": null,
      "consensus_answer": 123
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )


@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_empty_required_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "",
      "deepseek_strengths": "   ",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer"
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_unexpected_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "Gemini strength",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer",
      "debug_notes": "Internal notes"
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

def test_run_debate_rejects_empty_question():
    with pytest.raises(ValueError):
        run_debate(
            question="   ",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

def test_run_debate_rejects_empty_gemini_response():
    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="   ",
            deepseek_response="deepseek answer",
        )

def test_run_debate_rejects_empty_deepseek_response():
    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="   ",
        )

def test_run_debate_rejects_identical_model_responses():
    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="same answer",
            deepseek_response="same answer",
        )

@patch("agent.debate.ask_gemini")
def test_run_debate_rejects_too_short_required_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "ok",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer"
    }
    """

    with pytest.raises(ValueError):
        run_debate(
            question="question",
            gemini_response="gemini answer",
            deepseek_response="deepseek answer",
        )

@patch("agent.debate.ask_gemini")
def test_run_debate_trims_inputs_before_prompt(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "Gemini strength",
      "deepseek_strengths": "DeepSeek strength",
      "criticisms": "Both missed details",
      "consensus_answer": "Final answer"
    }
    """

    run_debate(
        question="  question  ",
        gemini_response="\n gemini answer \n",
        deepseek_response="  deepseek answer  ",
    )

    prompt = mock_gemini.call_args[0][0]

    assert "Question:\nquestion\n" in prompt
    assert "Gemini said:\ngemini answer\n" in prompt
    assert "DeepSeek said:\ndeepseek answer\n" in prompt

@patch("agent.debate.ask_gemini")
def test_run_debate_trims_output_fields(mock_gemini):
    mock_gemini.return_value = """
    {
      "gemini_strengths": "  Gemini strength  ",
      "deepseek_strengths": " DeepSeek strength ",
      "criticisms": " Both missed details ",
      "consensus_answer": " Final answer "
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