from agent.semantic_validation import build_validation_record


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
