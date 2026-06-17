def _tokenize(text: str) -> set[str]:
    return {
        word.strip(".,!?;:()[]{}\"'").lower()
        for word in text.split()
        if word.strip(".,!?;:()[]{}\"'")
    }


def _overlap_score(first: str, second: str) -> int:
    first_tokens = _tokenize(first)
    second_tokens = _tokenize(second)

    if not first_tokens or not second_tokens:
        return 0

    overlap = first_tokens.intersection(second_tokens)
    total = first_tokens.union(second_tokens)

    return int((len(overlap) / len(total)) * 100)


def _more_complete_response(
    gemini_response: str,
    deepseek_response: str,
) -> str:
    gemini_length = len(_tokenize(gemini_response))
    deepseek_length = len(_tokenize(deepseek_response))

    if abs(gemini_length - deepseek_length) <= 5:
        return "tie"

    if gemini_length > deepseek_length:
        return "gemini"

    return "deepseek"


def independent_judge_responses(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:
    agreement_score = _overlap_score(gemini_response, deepseek_response)
    more_complete = _more_complete_response(
        gemini_response,
        deepseek_response,
    )

    needs_debate = agreement_score < 50

    return {
        "agreement_score": agreement_score,
        "needs_debate": needs_debate,
        "agreements": [],
        "differences": [],
        "more_complete_response": more_complete,
        "final_answer": "",
        "judge_type": "independent_rule_based",
    }