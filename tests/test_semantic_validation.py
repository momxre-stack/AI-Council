from agent.semantic_validation import (
    build_validation_record,
    summarize_validation_records,
    is_semantic_candidate,
)


def test_build_validation_record_from_council_result():
    result = build_validation_record(
        {
            "question": "Explain artificial intelligence.",
            "responses": {
                "gemini": "AI lets machines perform intelligent tasks.",
                "deepseek": "AI simulates human intelligence in computer systems.",
            },
            "status": "ok",
            "assessment": {"confidence": "low"},
            "judgment": {
                "gemini_judge": {"agreement_score": 90},
                "deepseek_judge": {"agreement_score": 85},
                "independent_judge": {"agreement_score": 23},
                "final_needs_debate": True,
            },
        }
    )

    assert result == {
        "question": "Explain artificial intelligence.",
        "gemini_response": "AI lets machines perform intelligent tasks.",
        "deepseek_response": "AI simulates human intelligence in computer systems.",
        "independent_score": 23,
        "gemini_score": 90,
        "deepseek_score": 85,
        "max_provider_agreement": 90,
        "agreement_gap": 67,
        "debate_used": True,
        "status": "ok",
        "assessment": {"confidence": "low"},
    }

def test_summarize_validation_records():
    summary = summarize_validation_records(
        [
            {
                "independent_score": 23,
                "max_provider_agreement": 90,
                "agreement_gap": 67,
            },
            {
                "independent_score": 40,
                "max_provider_agreement": 80,
                "agreement_gap": 40,
            },
        ]
    )

    assert summary == {
        "records_count": 2,
        "average_independent_score": 31.5,
        "average_provider_score": 85,
        "average_agreement_gap": 53.5,
    }


def test_summarize_validation_records_handles_empty_list():
    summary = summarize_validation_records([])

    assert summary == {
        "records_count": 0,
        "average_independent_score": 0,
        "average_provider_score": 0,
        "average_agreement_gap": 0,
    }

def test_is_semantic_candidate_returns_true():
    assert is_semantic_candidate(
        {
            "max_provider_agreement": 90,
            "agreement_gap": 67,
        }
    ) is True


def test_is_semantic_candidate_returns_false():
    assert is_semantic_candidate(
        {
            "max_provider_agreement": 60,
            "agreement_gap": 15,
        }
    ) is False
