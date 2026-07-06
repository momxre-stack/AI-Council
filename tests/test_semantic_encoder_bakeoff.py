SEMANTIC_ENCODER_EVALUATION_CASES = [
    {
        "category": "aligned_paraphrase",
        "text_a": "Normalization reduces data redundancy.",
        "text_b": "Normalization minimizes duplicate data.",
        "expected_relationship": "aligned",
    },
    {
        "category": "negation_conflict",
        "text_a": "Normalization reduces data redundancy.",
        "text_b": "Normalization does not reduce data redundancy.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "opposite_action",
        "text_a": "The process increases system performance.",
        "text_b": "The process decreases system performance.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "unrelated",
        "text_a": "Normalization reduces redundancy.",
        "text_b": "The moon orbits the Earth.",
        "expected_relationship": "unrelated",
    },
    {
        "category": "modal_conflict",
        "text_a": "Python can be used for web development.",
        "text_b": "Python cannot be used for web development.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "absolute_conflict",
        "text_a": "The cache always stores the result.",
        "text_b": "The cache never stores the result.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "temporal_conflict",
        "text_a": "Validation happens before execution.",
        "text_b": "Validation happens after execution.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "requirement_conflict",
        "text_a": "Authentication is required.",
        "text_b": "Authentication is optional.",
        "expected_relationship": "conflicting",
    },
    {
        "category": "related_but_different",
        "text_a": "Normalization reduces redundancy.",
        "text_b": "Denormalization improves read performance.",
        "expected_relationship": "partial",
    },
    {
        "category": "subset",
        "text_a": "Python is a programming language.",
        "text_b": (
            "Python is a programming language used for web development, "
            "automation, data analysis, and scripting."
        ),
        "expected_relationship": "partial",
    },
]


def test_semantic_encoder_evaluation_cases_are_labeled():
    assert len(SEMANTIC_ENCODER_EVALUATION_CASES) == 10

    for case in SEMANTIC_ENCODER_EVALUATION_CASES:
        assert case["category"]
        assert case["text_a"]
        assert case["text_b"]
        assert case["expected_relationship"] in {
            "aligned",
            "conflicting",
            "partial",
            "unrelated",
        }
