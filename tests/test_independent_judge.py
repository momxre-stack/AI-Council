from agent.independent_judge import independent_judge_responses


def test_independent_judge_detects_high_agreement():
    result = independent_judge_responses(
        question="What is the capital of France?",
        gemini_response="The capital of France is Paris.",
        deepseek_response="Paris is the capital of France.",
    )

    assert result["agreement_score"] > 0
    assert result["judge_type"] == "independent_rule_based"


def test_independent_judge_detects_low_agreement():
    result = independent_judge_responses(
        question="Explain nuclear energy.",
        gemini_response="Nuclear energy uses fission reactions.",
        deepseek_response="Bananas are rich in potassium.",
    )

    assert result["needs_debate"] is True


def test_independent_judge_detects_more_complete_response():
    result = independent_judge_responses(
        question="Explain Python.",
        gemini_response=(
            "Python is a programming language used for "
            "web development, automation, data science, "
            "machine learning, and scripting."
        ),
        deepseek_response="Python is a programming language.",
    )

    assert result["more_complete_response"] == "gemini"


def test_independent_judge_recognizes_real_ai_semantic_alignment():
    result = independent_judge_responses(
        question="What is AI in one sentence?",
        gemini_response=(
            "Artificial Intelligence (AI) is the development of computer systems "
            "capable of performing tasks that typically require human intelligence, "
            "such as learning, reasoning, and problem-solving."
        ),
        deepseek_response=(
            "AI is the simulation of human intelligence by machines, "
            "enabling them to learn, reason, and make decisions."
        ),
    )

    assert result["agreement_score"] >= 50
    assert result["needs_debate"] is False

def test_independent_judge_keeps_unrelated_answers_low_agreement():
    result = independent_judge_responses(
        question="What is AI in one sentence?",
        gemini_response=(
            "Artificial Intelligence is the development of computer systems "
            "capable of learning and reasoning."
        ),
        deepseek_response=(
            "Photosynthesis is the process plants use to convert sunlight "
            "into chemical energy."
        ),
    )

    assert result["agreement_score"] < 50
    assert result["needs_debate"] is True

def test_independent_judge_recognizes_live_ai_semantic_alignment():
    result = independent_judge_responses(
        question="What is AI in one sentence?",
        gemini_response=(
            "Artificial Intelligence (AI) is the ability of machines to perform "
            "cognitive functions typically associated with human intelligence, "
            "such as learning, understanding, problem-solving, and decision-making."
        ),
        deepseek_response=(
            "AI is a field of computer science focused on creating systems that "
            "can perform tasks typically requiring human intelligence, such as "
            "learning, reasoning, and problem-solving."
        ),
    )

    assert result["agreement_score"] >= 50
    assert result["needs_debate"] is False


def test_independent_judge_exposes_diagnostic_evidence():
    result = independent_judge_responses(
        question="What is AI in one sentence?",
        gemini_response=(
            "Artificial Intelligence is the development of computer systems "
            "capable of learning and reasoning."
        ),
        deepseek_response=(
            "AI is the ability of machines to learn and reason."
        ),
    )

    assert "diagnostics" in result

    diagnostics = result["diagnostics"]

    assert diagnostics["gemini_tokens"]
    assert diagnostics["deepseek_tokens"]
    assert diagnostics["overlap_tokens"]
    assert diagnostics["gemini_only_tokens"]
    assert diagnostics["deepseek_only_tokens"]
    assert diagnostics["overlap_count"] == len(diagnostics["overlap_tokens"])
    assert diagnostics["total_count"] >= diagnostics["overlap_count"]


def test_independent_judge_tokenization_ignores_markdown_emphasis():
    plain_result = independent_judge_responses(
        question="Compare two responses.",
        gemini_response="Process and thread share memory.",
        deepseek_response="Process and thread share memory.",
    )

    markdown_result = independent_judge_responses(
        question="Compare two responses.",
        gemini_response="**Process** and *thread* share **memory**.",
        deepseek_response="Process and thread share memory.",
    )

    assert markdown_result["agreement_score"] == plain_result["agreement_score"]


def test_independent_judge_tokenization_splits_em_dash_words():
    separated_result = independent_judge_responses(
        question="Compare two responses.",
        gemini_response="Redundancy often improves read performance.",
        deepseek_response="Redundancy often improves read performance.",
    )

    em_dash_result = independent_judge_responses(
        question="Compare two responses.",
        gemini_response="Redundancy—often improves read performance.",
        deepseek_response="Redundancy often improves read performance.",
    )

    assert em_dash_result["agreement_score"] == separated_result["agreement_score"]
