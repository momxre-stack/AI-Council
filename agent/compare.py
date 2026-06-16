def compare_responses(gemini_response: str, deepseek_response: str) -> dict:
    return {
        "agreements": [
            "Both responses were generated successfully."
        ],
        "differences": [
            {
                "gemini": gemini_response,
                "deepseek": deepseek_response,
            }
        ],
    }