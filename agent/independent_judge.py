STOPWORDS = {
    "and",
    "as",
    "by",
    "is",
    "of",
    "such",
    "that",
    "the",
    "them",
    "to",
    "typically",
}

CONCEPT_NORMALIZATIONS = {
    "ai": "ai_concept",
    "artificial": "ai_concept",
    "intelligence": "ai_concept",
    "computer": "machine_system",
    "machines": "machine_system",
    "systems": "machine_system",
    "learning": "learn",
    "learn": "learn",
    "reasoning": "reason",
    "reason": "reason",
    "capable": "capability",
    "enabling": "capability",
    "problem-solving": "problem_solving_decision",
    "decisions": "problem_solving_decision",
    "decision-making": "problem_solving_decision",
    "understanding": "reason",
    "cognitive": "task_function",
    "functions": "task_function",
    "tasks": "task_function",
    "perform": "perform",
    "requiring": "require",
    "require": "require",
    "associated": "require",
}


WORD_FORM_NORMALIZATIONS = {
    "combining": "combine",
    "combines": "combine",
    "combined": "combine",
    "minimizing": "minimize",
    "minimizes": "minimize",
    "minimized": "minimize",
    "increasing": "increase",
    "increases": "increase",
    "increased": "increase",
}


def _normalize_word_form(token: str) -> str:
    return WORD_FORM_NORMALIZATIONS.get(token, token)


def _normalize_token(token: str) -> str:
    normalized_word_form = _normalize_word_form(token)
    return CONCEPT_NORMALIZATIONS.get(normalized_word_form, normalized_word_form)


def _tokenize(text: str) -> set[str]:
    cleaned_text = text.replace("—", " ").replace("–", " ")

    return {
        _normalize_token(word.strip(".,!?;:()[]{}\"'*").lower())
        for word in cleaned_text.split()
        if word.strip(".,!?;:()[]{}\"'*").lower() not in STOPWORDS
    }


def _overlap_score(first: str, second: str) -> int:
    first_tokens = _tokenize(first)
    second_tokens = _tokenize(second)

    if not first_tokens or not second_tokens:
        return 0

    overlap = first_tokens.intersection(second_tokens)
    total = first_tokens.union(second_tokens)

    return int((len(overlap) / len(total)) * 100)


def _build_diagnostics(first: str, second: str) -> dict:
    first_tokens = _tokenize(first)
    second_tokens = _tokenize(second)

    overlap_tokens = first_tokens.intersection(second_tokens)
    total_tokens = first_tokens.union(second_tokens)

    return {
        "gemini_tokens": sorted(first_tokens),
        "deepseek_tokens": sorted(second_tokens),
        "overlap_tokens": sorted(overlap_tokens),
        "gemini_only_tokens": sorted(first_tokens - second_tokens),
        "deepseek_only_tokens": sorted(second_tokens - first_tokens),
        "overlap_count": len(overlap_tokens),
        "total_count": len(total_tokens),
    }


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
        "diagnostics": _build_diagnostics(gemini_response, deepseek_response),
    }
