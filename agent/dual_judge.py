from agent.providers.gemini import ask_gemini
from agent.providers.deepseek import ask_deepseek
from agent.judge_v2 import judge_responses_v2


SIGNIFICANT_SCORE_GAP = 30


def _judge_with_provider(
    question: str,
    gemini_response: str,
    deepseek_response: str,
    provider_name: str,
) -> dict:
    if provider_name == "gemini":
        return judge_responses_v2(
            question=question,
            gemini_response=gemini_response,
            deepseek_response=deepseek_response,
        )

    if provider_name == "deepseek":
        # DeepSeek judge will be implemented in a later integration step.
        # For now keep the same structured output contract.
        return judge_responses_v2(
            question=question,
            gemini_response=gemini_response,
            deepseek_response=deepseek_response,
        )

    raise ValueError(f"Unknown provider: {provider_name}")


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


def run_dual_judgment(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:
    gemini_judgment = _judge_with_provider(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
        provider_name="gemini",
    )

    deepseek_judgment = _judge_with_provider(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
        provider_name="deepseek",
    )

    final_needs_debate = (
        gemini_judgment.get("needs_debate", False)
        or deepseek_judgment.get("needs_debate", False)
        or _winner_disagreement(
            gemini_judgment,
            deepseek_judgment,
        )
        or _score_disagreement(
            gemini_judgment,
            deepseek_judgment,
        )
    )

    return {
        "gemini_judge": gemini_judgment,
        "deepseek_judge": deepseek_judgment,
        "final_needs_debate": final_needs_debate,
    }