from agent.independent_judge import independent_judge_responses
from tests.test_independent_judge_benchmark import BENCHMARK_CASES


def _coverage_score(source: str, target: str) -> int:
    source_tokens = {
        word.strip(".,!?;:()[]{}\"'*").lower()
        for word in source.split()
    }
    target_tokens = {
        word.strip(".,!?;:()[]{}\"'*").lower()
        for word in target.split()
    }

    if not source_tokens:
        return 0

    covered_tokens = source_tokens.intersection(target_tokens)

    return int((len(covered_tokens) / len(source_tokens)) * 100)


def _extract_claims(response: str) -> list[str]:
    return [
        sentence.strip().lower()
        for sentence in response.split(".")
        if sentence.strip()
    ]


def _build_claim_pairs(
    gemini_claims: list[str],
    deepseek_claims: list[str],
) -> list[dict]:
    pairs = []

    for gemini_index, gemini_claim in enumerate(gemini_claims, start=1):
        for deepseek_index, deepseek_claim in enumerate(deepseek_claims, start=1):
            pairs.append(
                {
                    "gemini_claim_index": gemini_index,
                    "deepseek_claim_index": deepseek_index,
                    "gemini_claim": gemini_claim,
                    "deepseek_claim": deepseek_claim,
                }
            )

    return pairs


def _build_multi_response_judge_prompt(
    question: str,
    responses: list[dict],
) -> str:
    response_blocks = "\n\n".join(
        f"{response['id']}:\n{response['text']}"
        for response in responses
    )

    return (
        "You are an independent judge evaluating anonymous AI responses.\n"
        "Do not infer provider identity.\n"
        "Evaluate whether the responses share the same core answer, whether "
        "there are material contradictions, and whether any response is an outlier.\n"
        "Return JSON only.\n\n"
        f"Question:\n{question}\n\n"
        f"Responses:\n{response_blocks}"
    )


def _run_baseline_cases() -> list[dict]:
    results = []

    for index, case in enumerate(BENCHMARK_CASES, start=1):
        result = independent_judge_responses(
            question=case["question"],
            gemini_response=case["gemini_response"],
            deepseek_response=case["deepseek_response"],
        )

        results.append(
            {
                "case": index,
                "agreement_score": result["agreement_score"],
                "needs_debate": result["needs_debate"],
            }
        )

    return results


def test_bakeoff_harness_records_current_baseline_results():
    results = _run_baseline_cases()

    assert results == [
        {
            "case": 1,
            "agreement_score": 29,
            "needs_debate": True,
        },
        {
            "case": 2,
            "agreement_score": 27,
            "needs_debate": True,
        },
        {
            "case": 3,
            "agreement_score": 32,
            "needs_debate": True,
        },
    ]


def test_bakeoff_includes_subset_answer_control_case():
    full_result = independent_judge_responses(
        question="What is Python?",
        gemini_response=(
            "Python is a programming language used for web development, "
            "automation, data analysis, and scripting."
        ),
        deepseek_response="Python is a programming language.",
    )

    reversed_result = independent_judge_responses(
        question="What is Python?",
        gemini_response="Python is a programming language.",
        deepseek_response=(
            "Python is a programming language used for web development, "
            "automation, data analysis, and scripting."
        ),
    )

    assert full_result["agreement_score"] == reversed_result["agreement_score"]
    assert full_result["more_complete_response"] == "gemini"
    assert reversed_result["more_complete_response"] == "deepseek"


def test_bidirectional_coverage_detects_subset_asymmetry():
    full_response = (
        "Python is a programming language used for web development, "
        "automation, data analysis, and scripting."
    )
    short_response = "Python is a programming language."

    short_to_full = _coverage_score(short_response, full_response)
    full_to_short = _coverage_score(full_response, short_response)

    assert short_to_full > full_to_short


def test_bakeoff_includes_negation_disagreement_control_case():
    result = independent_judge_responses(
        question="What does normalization do?",
        gemini_response="Normalization reduces data redundancy.",
        deepseek_response="Normalization does not reduce data redundancy.",
    )

    assert result["needs_debate"] is True
    assert "negation_mismatch" not in result["diagnostics"]


def test_claim_extractor_splits_response_into_claims():
    claims = _extract_claims(
        "Normalization reduces redundancy. Denormalization improves read performance."
    )

    assert claims == [
        "normalization reduces redundancy",
        "denormalization improves read performance",
    ]


def test_claim_pair_builder_creates_all_cross_pairs():
    gemini_claims = [
        "normalization reduces redundancy",
        "denormalization improves read performance",
    ]
    deepseek_claims = [
        "normalization minimizes duplicate data",
        "denormalization reduces joins",
        "denormalization improves read performance",
    ]

    pairs = _build_claim_pairs(gemini_claims, deepseek_claims)

    assert pairs == [
        {
            "gemini_claim_index": 1,
            "deepseek_claim_index": 1,
            "gemini_claim": "normalization reduces redundancy",
            "deepseek_claim": "normalization minimizes duplicate data",
        },
        {
            "gemini_claim_index": 1,
            "deepseek_claim_index": 2,
            "gemini_claim": "normalization reduces redundancy",
            "deepseek_claim": "denormalization reduces joins",
        },
        {
            "gemini_claim_index": 1,
            "deepseek_claim_index": 3,
            "gemini_claim": "normalization reduces redundancy",
            "deepseek_claim": "denormalization improves read performance",
        },
        {
            "gemini_claim_index": 2,
            "deepseek_claim_index": 1,
            "gemini_claim": "denormalization improves read performance",
            "deepseek_claim": "normalization minimizes duplicate data",
        },
        {
            "gemini_claim_index": 2,
            "deepseek_claim_index": 2,
            "gemini_claim": "denormalization improves read performance",
            "deepseek_claim": "denormalization reduces joins",
        },
        {
            "gemini_claim_index": 2,
            "deepseek_claim_index": 3,
            "gemini_claim": "denormalization improves read performance",
            "deepseek_claim": "denormalization improves read performance",
        },
    ]


def test_multi_response_judge_prompt_uses_anonymous_response_ids():
    prompt = _build_multi_response_judge_prompt(
        question="What is AI?",
        responses=[
            {"id": "R1", "text": "AI lets machines perform human-like tasks."},
            {"id": "R2", "text": "Artificial intelligence enables systems to learn and reason."},
        ],
    )

    assert "What is AI?" in prompt
    assert "R1" in prompt
    assert "R2" in prompt
    assert "Gemini" not in prompt
    assert "DeepSeek" not in prompt
    assert "OpenAI" not in prompt
    assert "JSON" in prompt
