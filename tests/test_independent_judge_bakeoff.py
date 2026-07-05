from agent.independent_judge import independent_judge_responses
from tests.test_independent_judge_benchmark import BENCHMARK_CASES


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
