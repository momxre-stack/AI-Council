import os

import pytest


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


def _semantic_encoder_bakeoff_enabled() -> bool:
    return os.getenv("RUN_SEMANTIC_ENCODER_BAKEOFF") == "1"


def _load_sentence_transformer():
    if not _semantic_encoder_bakeoff_enabled():
        pytest.skip("Set RUN_SEMANTIC_ENCODER_BAKEOFF=1 to run encoder bake-off")

    sentence_transformers = pytest.importorskip("sentence_transformers")
    return sentence_transformers.SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )


def _measure_reference_encoder_cases() -> dict[str, float]:
    model = _load_sentence_transformer()

    texts = [
        text
        for case in SEMANTIC_ENCODER_EVALUATION_CASES
        for text in (case["text_a"], case["text_b"])
    ]
    embeddings = model.encode(texts, normalize_embeddings=True)

    scores = {}

    for index, case in enumerate(SEMANTIC_ENCODER_EVALUATION_CASES):
        first_embedding = embeddings[index * 2]
        second_embedding = embeddings[index * 2 + 1]
        scores[case["category"]] = round(
            float(first_embedding @ second_embedding) * 100,
            1,
        )

    return scores


def _has_conflict_signal(text_a: str, text_b: str) -> bool:
    first_tokens = {
        word.strip(".,!?;:()[]{}\"'*").lower()
        for word in text_a.split()
    }
    second_tokens = {
        word.strip(".,!?;:()[]{}\"'*").lower()
        for word in text_b.split()
    }

    opposite_terms = [
        ("before", "after"),
        ("increases", "decreases"),
        ("can", "cannot"),
    ]

    for first_term, second_term in opposite_terms:
        if first_term in first_tokens and second_term in second_tokens:
            return True

        if second_term in first_tokens and first_term in second_tokens:
            return True

    return False


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


def test_reference_encoder_separates_related_from_unrelated_text():
    scores = _measure_reference_encoder_cases()

    assert scores["aligned_paraphrase"] >= 80
    assert scores["unrelated"] < 20


def test_reference_encoder_does_not_detect_conflicts_by_itself():
    scores = _measure_reference_encoder_cases()

    assert scores["negation_conflict"] >= 80
    assert scores["opposite_action"] >= 80
    assert scores["temporal_conflict"] >= 80


def test_conflict_signal_detects_temporal_opposites():
    assert _has_conflict_signal(
        "Validation happens before execution.",
        "Validation happens after execution.",
    ) is True


def test_conflict_signal_does_not_flag_matching_temporal_terms():
    assert _has_conflict_signal(
        "Validation happens before execution.",
        "Checks happen before deployment.",
    ) is False


def test_conflict_signal_detects_opposite_actions():
    assert _has_conflict_signal(
        "The process increases system performance.",
        "The process decreases system performance.",
    ) is True


def test_conflict_signal_does_not_flag_matching_actions():
    assert _has_conflict_signal(
        "The process increases system performance.",
        "The optimization increases application performance.",
    ) is False


def test_conflict_signal_detects_modal_opposites():
    assert _has_conflict_signal(
        "Python can be used for web development.",
        "Python cannot be used for web development.",
    ) is True


def test_conflict_signal_does_not_flag_matching_modal_terms():
    assert _has_conflict_signal(
        "Python can be used for web development.",
        "Python can be used for automation.",
    ) is False
