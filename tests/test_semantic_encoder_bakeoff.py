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
]


def test_semantic_encoder_evaluation_cases_are_labeled():
    assert len(SEMANTIC_ENCODER_EVALUATION_CASES) == 4

    for case in SEMANTIC_ENCODER_EVALUATION_CASES:
        assert case["category"]
        assert case["text_a"]
        assert case["text_b"]
        assert case["expected_relationship"] in {
            "aligned",
            "conflicting",
            "unrelated",
        }
