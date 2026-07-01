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

def summarize_validation_records(records: list[dict]) -> dict:
    if not records:
        return {
            "records_count": 0,
            "average_independent_score": 0,
            "average_provider_score": 0,
            "average_agreement_gap": 0,
        }

    records_count = len(records)
    total_independent_score = sum(
        record.get("independent_score") or 0
        for record in records
    )
    total_provider_score = sum(
        record.get("max_provider_agreement") or 0
        for record in records
    )
    total_agreement_gap = sum(
        record.get("agreement_gap") or 0
        for record in records
    )

    return {
        "records_count": records_count,
        "average_independent_score": total_independent_score / records_count,
        "average_provider_score": total_provider_score / records_count,
        "average_agreement_gap": total_agreement_gap / records_count,
    }
