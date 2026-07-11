from agent.json_utils import parse_json_object
from agent.providers.deepseek import ask_deepseek
from agent.judge_v2 import judge_responses_v2
from agent.independent_judge import independent_judge_responses


SIGNIFICANT_SCORE_GAP = 30
DEBATE_VOTE_THRESHOLD = 2


def _build_judge_prompt(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> str:
    return f"""
You are the judge in a multi-model AI council.

Question:
{question}

Gemini response:
{gemini_response}

DeepSeek response:
{deepseek_response}

Return ONLY valid JSON with this exact structure:
{{
  "agreement_score": 0,
  "needs_debate": true,
  "agreements": [],
  "differences": [],
  "more_complete_response": "",
  "final_answer": ""
}}

Rules:
- agreement_score must be an integer from 0 to 100.
- needs_debate must be true if agreement_score is below 70.
- agreements must be a list of short strings.
- differences must be a list of short strings.
- more_complete_response must be "gemini", "deepseek", or "tie".
- final_answer must combine the strongest parts of both responses.
- Do not include markdown.
- Do not include explanations outside JSON.
"""


def _parse_judge_json(raw_response: str) -> dict:
    return parse_json_object(raw_response, "Judge did not return JSON")


def _judge_with_deepseek(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:
    prompt = _build_judge_prompt(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
    )

    return _parse_judge_json(ask_deepseek(prompt))


def _winner_disagreement(
    gemini_judgment: dict,
    deepseek_judgment: dict,
) -> bool:
    return (
        gemini_judgment.get("more_complete_response")
        != deepseek_judgment.get("more_complete_response")
    )


def _score_disagreement(
    gemini_judgment: dict,
    deepseek_judgment: dict,
) -> bool:
    score_a = gemini_judgment.get("agreement_score", 0)
    score_b = deepseek_judgment.get("agreement_score", 0)

    return abs(score_a - score_b) >= SIGNIFICANT_SCORE_GAP


def _debate_vote_count(
    gemini_judgment: dict,
    deepseek_judgment: dict,
    independent_judgment: dict,
) -> int:
    return sum(
        [
            bool(gemini_judgment.get("needs_debate", False)),
            bool(deepseek_judgment.get("needs_debate", False)),
            bool(independent_judgment.get("needs_debate", False)),
        ]
    )


def _provider_debate_vote_count(
    gemini_judgment: dict,
    deepseek_judgment: dict,
) -> int:
    return sum(
        [
            bool(gemini_judgment.get("needs_debate", False)),
            bool(deepseek_judgment.get("needs_debate", False)),
        ]
    )


def _independent_debate_vote(independent_judgment: dict) -> bool:
    return bool(independent_judgment.get("needs_debate", False))


def run_dual_judgment(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:
    gemini_judgment = judge_responses_v2(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
    )

    deepseek_judgment = _judge_with_deepseek(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
    )

    independent_judgment = independent_judge_responses(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
    )

    debate_vote_count = _debate_vote_count(
        gemini_judgment,
        deepseek_judgment,
        independent_judgment,
    )

    provider_debate_vote_count = _provider_debate_vote_count(
        gemini_judgment,
        deepseek_judgment,
    )
    independent_debate_vote = _independent_debate_vote(
        independent_judgment,
    )

    provider_only_final_needs_debate = (
        provider_debate_vote_count >= DEBATE_VOTE_THRESHOLD
        or _winner_disagreement(gemini_judgment, deepseek_judgment)
        or _score_disagreement(gemini_judgment, deepseek_judgment)
    )

    final_needs_debate = (
        debate_vote_count >= DEBATE_VOTE_THRESHOLD
        or _winner_disagreement(gemini_judgment, deepseek_judgment)
        or _score_disagreement(gemini_judgment, deepseek_judgment)
    )

    return {
        "gemini_judge": gemini_judgment,
        "deepseek_judge": deepseek_judgment,
        "independent_judge": independent_judgment,
        "debate_vote_count": debate_vote_count,
        "provider_debate_vote_count": provider_debate_vote_count,
        "independent_debate_vote": independent_debate_vote,
        "final_needs_debate": final_needs_debate,
        "provider_only_final_needs_debate": (
            provider_only_final_needs_debate
        ),
    }
