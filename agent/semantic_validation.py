def build_validation_record(council_result: dict) -> dict:
    judgment = council_result.get("judgment") or {}
    independent_judge = judgment.get("independent_judge") or {}
    gemini_judge = judgment.get("gemini_judge") or {}
    deepseek_judge = judgment.get("deepseek_judge") or {}
    responses = council_result.get("responses") or {}

    independent_score = independent_judge.get("agreement_score") or 0
    gemini_score = gemini_judge.get("agreement_score") or 0
    deepseek_score = deepseek_judge.get("agreement_score") or 0

    max_provider_agreement = max(gemini_score, deepseek_score)
    agreement_gap = max_provider_agreement - independent_score

    return {
        "question": council_result.get("question"),
        "gemini_response": responses.get("gemini"),
        "deepseek_response": responses.get("deepseek"),
        "independent_score": independent_score,
        "gemini_score": gemini_score,
        "deepseek_score": deepseek_score,
        "max_provider_agreement": max_provider_agreement,
        "agreement_gap": agreement_gap,
        "debate_used": judgment.get("final_needs_debate"),
        "status": council_result.get("status"),
        "assessment": council_result.get("assessment"),
    }
